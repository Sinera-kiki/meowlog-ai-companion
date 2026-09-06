"""MeowLog public backend — FastAPI + PostgreSQL + OpenAI-compatible LLM."""
from __future__ import annotations

import json
import os
import random
import re
from contextvars import ContextVar
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated

import httpx
import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, StringConstraints

ROOT = Path(__file__).resolve().parent           # backend/
FRONTEND_DIST = ROOT.parent / "frontend" / "dist"
INDEX_HTML = FRONTEND_DIST / "index.html"


GUEST_ID: ContextVar[str | None] = ContextVar("guest_id", default=None)


def _get_db_conn() -> psycopg.Connection:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise HTTPException(status_code=503, detail="DATABASE_URL is not configured")
    return psycopg.connect(database_url, row_factory=dict_row)


async def _llm_chat(messages: list[dict], max_tokens: int = 800) -> str:
    """Call any OpenAI-compatible provider; fall back to local demo replies."""
    api_key = os.getenv("LLM_API_KEY", "")
    if not api_key:
        user_text = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        if any(word in user_text for word in ("累", "难过", "委屈", "压力")):
            return "（轻轻把爪子搭在你手上）今天辛苦啦。你慢慢说，我会一直听着。"
        return "（歪头看着你）我记住啦。要不要再摸摸我的头？"
    base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "messages": messages, "max_tokens": max_tokens},
        )
    if response.is_error:
        raise HTTPException(status_code=502, detail="LLM provider request failed")
    data = response.json()
    return data["choices"][0]["message"]["content"]


def _require_user() -> dict:
    guest_id = GUEST_ID.get()
    if not guest_id or not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", guest_id):
        raise HTTPException(status_code=401, detail="Missing or invalid X-Guest-Id")
    return {"userId": f"guest:{guest_id}", "username": "旅行者", "email": None}


# ---------------------------------------------------------------------------
# DTOs
# ---------------------------------------------------------------------------
NonBlankStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class AdoptIn(BaseModel):
    name: NonBlankStr
    persona_tag: NonBlankStr

class InteractIn(BaseModel):
    action_type: str # 'feed', 'pet'

class ChatIn(BaseModel):
    message: NonBlankStr

class OutfitIn(BaseModel):
    outfit: str
    slot: str

# ---------------------------------------------------------------------------
# FastAPI app & Core Logic
# ---------------------------------------------------------------------------
app = FastAPI(title="MeowLog Backend")
SECURITY_CSP = "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'"

@app.middleware("http")
async def request_context(request, call_next):
    token = GUEST_ID.set(request.headers.get("X-Guest-Id"))
    try:
        response = await call_next(request)
        response.headers["content-security-policy"] = SECURITY_CSP
        response.headers["x-content-type-options"] = "nosniff"
        return response
    finally:
        GUEST_ID.reset(token)

@app.get("/health")
def health() -> dict:
    return {"ok": True}

@app.get("/api/whoami")
def whoami():
    return _require_user()

@app.get("/api/cat/status")
def get_cat_status():
    """获取小猫状态，执行懒结算（Lazy Tick）"""
    user = _require_user()
    with _get_db_conn() as conn:
        cat = conn.execute("SELECT * FROM cats WHERE owner_id = %s", (user["userId"],)).fetchone()
        if not cat:
            return {"has_cat": False}

        # 懒计算逻辑 (Lazy Tick)
        now = datetime.now(timezone.utc)
        last_time = cat["last_interact_time"]

        # 避免 TypeError: can't subtract offset-naive and offset-aware datetimes
        if last_time.tzinfo is None:
            last_time = last_time.replace(tzinfo=timezone.utc)

        hours_passed = (now - last_time).total_seconds() / 3600.0

        if hours_passed > 1:
            # 随着时间流逝，饱食度和心情会下降
            satiety_drop = int(hours_passed * 5)
            mood_drop = int(hours_passed * 2)
            new_satiety = max(0, cat["satiety_level"] - satiety_drop)
            new_mood = max(0, cat["mood_level"] - mood_drop)

            # 状态演变逻辑
            new_status = 'idle'
            if new_satiety < 30:
                new_status = 'hungry'
            elif hours_passed > 12:
                new_status = 'sleeping'

            conn.execute(
                "UPDATE cats SET satiety_level=%s, mood_level=%s, current_status=%s, last_interact_time=NOW() WHERE id=%s",
                (new_satiety, new_mood, new_status, cat["id"])
            )
            conn.commit()

            # 重新获取更新后的状态
            cat = conn.execute("SELECT * FROM cats WHERE id = %s", (cat["id"],)).fetchone()

    return {"has_cat": True, "cat": cat}

@app.post("/api/cat/adopt")
def adopt_cat(body: AdoptIn):
    user = _require_user()
    with _get_db_conn() as conn:
        # 检查是否已领养
        existing = conn.execute("SELECT id FROM cats WHERE owner_id = %s", (user["userId"],)).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="You already have a cat!")

        row = conn.execute(
            "INSERT INTO cats (owner_id, name, persona_tag) VALUES (%s, %s, %s) RETURNING *",
            (user["userId"], body.name, body.persona_tag)
        ).fetchone()
        conn.commit()
    return row

@app.post("/api/cat/interact")
def interact_cat(body: InteractIn):
    user = _require_user()
    with _get_db_conn() as conn:
        cat = conn.execute("SELECT * FROM cats WHERE owner_id = %s", (user["userId"],)).fetchone()
        if not cat:
            raise HTTPException(status_code=404, detail="No cat found")

        new_satiety = cat["satiety_level"]
        new_mood = cat["mood_level"]
        new_affection = cat["affection_level"]

        status = "idle"
        if body.action_type == "feed":
            new_satiety = min(100, new_satiety + 30)
            new_affection = min(100, new_affection + 1)
            status = "eating"
        elif body.action_type == "pet":
            new_mood = min(100, new_mood + 20)
            new_affection = min(100, new_affection + 2)
            status = "purring"
        elif body.action_type == "play":
            new_mood = min(100, new_mood + 28)
            new_satiety = max(0, new_satiety - 4)
            new_affection = min(100, new_affection + 3)
            status = "playing"
        else:
            raise HTTPException(status_code=400, detail="Unsupported action")

        updated = conn.execute(
            "UPDATE cats SET satiety_level=%s, mood_level=%s, affection_level=%s,"
            " current_status=%s, last_interact_time=NOW() WHERE id=%s RETURNING *",
            (new_satiety, new_mood, new_affection, status, cat["id"]),
        ).fetchone()
        conn.commit()
    return {"message": "success", "action": body.action_type, "cat": updated}

@app.post("/api/cat/outfit")
def change_outfit(body: OutfitIn):
    user = _require_user()
    accessories = {"scarf", "daisy", "satchel", "nightcap", "bow", "box"}
    clothing = {"moss_cape", "picnic_apron", "raincoat", "acorn_knit", "berry_dress", "moon_robe"}
    allowed = accessories | clothing
    if body.outfit not in allowed or body.slot not in {"accessory", "clothing"}:
        raise HTTPException(status_code=400, detail="Unknown outfit or slot")
    if (body.slot == "accessory" and body.outfit not in accessories) or (body.slot == "clothing" and body.outfit not in clothing):
        raise HTTPException(status_code=400, detail="Outfit does not match slot")
    with _get_db_conn() as conn:
        cat = conn.execute("SELECT * FROM cats WHERE owner_id = %s", (user["userId"],)).fetchone()
        if not cat:
            raise HTTPException(status_code=404, detail="No cat found")
        required_level = {"scarf": 1, "daisy": 1, "satchel": 1, "nightcap": 2, "bow": 3, "box": 4, "moss_cape": 1, "picnic_apron": 1, "raincoat": 2, "acorn_knit": 2, "berry_dress": 3, "moon_robe": 4}[body.outfit]
        current_level = max(1, cat["affection_level"] // 10 + 1)
        if current_level < required_level:
            raise HTTPException(status_code=403, detail=f"Requires level {required_level}")
        column = "accessory" if body.slot == "accessory" else "clothing"
        updated = conn.execute(
            f"UPDATE cats SET {column}=%s, outfit=%s WHERE id=%s RETURNING *",
            (body.outfit, body.outfit, cat["id"]),
        ).fetchone()
        conn.commit()
    return {"cat": updated}


ADVENTURE_DESTINATIONS = [
    {"name": "苔藓邮局", "emoji": "📮", "reward": "森林邮票"},
    {"name": "萤火溪谷", "emoji": "✨", "reward": "萤火玻璃瓶"},
    {"name": "橡果集市", "emoji": "🌰", "reward": "橡果铃铛"},
    {"name": "云朵车站", "emoji": "☁️", "reward": "一小片云"},
    {"name": "月桂图书馆", "emoji": "📚", "reward": "月桂书签"},
]


@app.get("/api/adventures")
def list_adventures():
    user = _require_user()
    with _get_db_conn() as conn:
        current = conn.execute(
            "SELECT * FROM adventures WHERE owner_id=%s AND status IN ('ongoing','ready')"
            " ORDER BY started_at DESC LIMIT 1",
            (user["userId"],),
        ).fetchone()
        if current and current["status"] == "ongoing" and current["returns_at"] <= datetime.now(timezone.utc):
            current = conn.execute(
                "UPDATE adventures SET status='ready' WHERE id=%s RETURNING *", (current["id"],)
            ).fetchone()
            conn.commit()
        history = conn.execute(
            "SELECT * FROM adventures WHERE owner_id=%s AND status='completed'"
            " ORDER BY completed_at DESC NULLS LAST, created_at DESC LIMIT 20",
            (user["userId"],),
        ).fetchall()
    return {"current": current, "history": history}


@app.post("/api/adventures/start")
def start_adventure():
    user = _require_user()
    with _get_db_conn() as conn:
        cat = conn.execute("SELECT * FROM cats WHERE owner_id=%s", (user["userId"],)).fetchone()
        if not cat:
            raise HTTPException(status_code=404, detail="Adopt a cat first")
        active = conn.execute(
            "SELECT id FROM adventures WHERE owner_id=%s AND status IN ('ongoing','ready') LIMIT 1",
            (user["userId"],),
        ).fetchone()
        if active:
            raise HTTPException(status_code=409, detail="An adventure is already active")
        destination = random.choice(ADVENTURE_DESTINATIONS)
        duration = max(15, int(os.getenv("ADVENTURE_DURATION_SECONDS", "45")))
        returns_at = datetime.now(timezone.utc) + timedelta(seconds=duration)
        row = conn.execute(
            "INSERT INTO adventures"
            " (owner_id,cat_id,title,story,status,destination,returns_at,reward_name,reward_coins,postcard_emoji)"
            " VALUES (%s,%s,%s,'','ongoing',%s,%s,%s,%s,%s) RETURNING *",
            (
                user["userId"], cat["id"], f"前往{destination['name']}", destination["name"],
                returns_at, destination["reward"], random.randint(8, 18), destination["emoji"],
            ),
        ).fetchone()
        conn.execute("UPDATE cats SET current_status='roaming' WHERE id=%s", (cat["id"],))
        conn.commit()
    return {"adventure": row}


@app.post("/api/adventures/claim")
async def claim_adventure():
    user = _require_user()
    with _get_db_conn() as conn:
        cat = conn.execute("SELECT * FROM cats WHERE owner_id=%s", (user["userId"],)).fetchone()
        adventure = conn.execute(
            "SELECT * FROM adventures WHERE owner_id=%s AND status IN ('ongoing','ready')"
            " ORDER BY started_at DESC LIMIT 1",
            (user["userId"],),
        ).fetchone()
        if not cat or not adventure:
            raise HTTPException(status_code=404, detail="No active adventure")
        if adventure["returns_at"] > datetime.now(timezone.utc):
            raise HTTPException(status_code=409, detail="The cat has not returned yet")
    prompt = (
        f"你是一只性格为“{cat['persona_tag']}”的小猫。你刚从{adventure['destination']}回来，"
        f"带回了{adventure['reward_name']}。请写一段80到120字、温暖俏皮的第一人称探险手帐，"
        "包含一个意外小插曲和一句想给主人说的话，不要使用标题。"
    )
    story = await _llm_chat([{"role": "user", "content": prompt}], max_tokens=240)
    with _get_db_conn() as conn:
        completed = conn.execute(
            "UPDATE adventures SET status='completed',story=%s,completed_at=NOW() WHERE id=%s RETURNING *",
            (story, adventure["id"]),
        ).fetchone()
        updated_cat = conn.execute(
            "UPDATE cats SET current_status='idle',leaf_coins=leaf_coins+%s,"
            " affection_level=LEAST(100,affection_level+3) WHERE id=%s RETURNING *",
            (adventure["reward_coins"], cat["id"]),
        ).fetchone()
        conn.commit()
    return {"adventure": completed, "cat": updated_cat}

def _bigrams(text: str) -> set[str]:
    compact = re.sub(r"\s+", "", text.lower())
    return {compact[i:i + 2] for i in range(max(0, len(compact) - 1))}


def _select_relevant_memories(rows: list[dict], query: str, limit: int = 4) -> list[dict]:
    query_tokens = _bigrams(query)
    def score(row: dict) -> float:
        tokens = _bigrams(row["content"])
        overlap = len(query_tokens & tokens) / max(1, len(query_tokens))
        return overlap * 10 + float(row.get("importance") or 1)
    return sorted(rows, key=score, reverse=True)[:limit]


async def _extract_memory(message: str) -> dict | None:
    triggers = ("我喜欢", "我不喜欢", "我讨厌", "我叫", "明天", "以后", "目标", "面试", "考试", "难过", "委屈", "生气", "压力", "开心")
    if not any(word in message for word in triggers):
        return None
    if not os.getenv("LLM_API_KEY"):
        emotion = next((x for x in ("难过", "委屈", "生气", "压力", "开心") if x in message), None)
        memory_type = "preference" if any(x in message for x in ("喜欢", "讨厌")) else "emotion" if emotion else "event"
        return {"memory_type": memory_type, "content": message[:180], "emotion": emotion, "importance": 3, "entities": {}}
    extraction_prompt = (
        "从用户消息中提取一条值得长期记住的信息，只返回JSON，不要Markdown。"
        "字段：memory_type(preference/event/emotion/goal)、content(第三人称简洁事实)、"
        "emotion(可为空)、importance(1到5)、entities(对象)。消息：" + message
    )
    raw = await _llm_chat([{"role": "user", "content": extraction_prompt}], max_tokens=220)
    try:
        parsed = json.loads(raw.strip().removeprefix("```json").removesuffix("```").strip())
        parsed["importance"] = min(5, max(1, int(parsed.get("importance", 2))))
        return parsed
    except Exception:
        return {"memory_type": "event", "content": message[:180], "emotion": None, "importance": 2, "entities": {}}


@app.get("/api/memories")
def list_memories():
    user = _require_user()
    with _get_db_conn() as conn:
        rows = conn.execute(
            "SELECT id,memory_type,content,emotion,importance,entities,access_count,created_at"
            " FROM memories WHERE owner_id=%s ORDER BY importance DESC,created_at DESC LIMIT 100",
            (user["userId"],),
        ).fetchall()
    return {"memories": rows}


@app.delete("/api/memories/{memory_id}", status_code=204)
def delete_memory(memory_id: int):
    user = _require_user()
    with _get_db_conn() as conn:
        result = conn.execute("DELETE FROM memories WHERE id=%s AND owner_id=%s", (memory_id, user["userId"]))
        conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Memory not found")
    return Response(status_code=204)


@app.post("/api/chat")
async def chat_with_cat(body: ChatIn):
    user = _require_user()
    with _get_db_conn() as conn:
        cat = conn.execute("SELECT * FROM cats WHERE owner_id=%s", (user["userId"],)).fetchone()
        if not cat:
            raise HTTPException(status_code=404, detail="No cat found")
        conn.execute(
            "INSERT INTO chat_logs (owner_id,cat_id,role,content) VALUES (%s,%s,'user',%s)",
            (user["userId"], cat["id"], body.message),
        )
        memory_rows = conn.execute(
            "SELECT id,content,importance FROM memories WHERE owner_id=%s ORDER BY created_at DESC LIMIT 50",
            (user["userId"],),
        ).fetchall()
        relevant = _select_relevant_memories(memory_rows, body.message)
        if relevant:
            ids = [row["id"] for row in relevant]
            conn.execute(
                "UPDATE memories SET access_count=access_count+1,last_accessed_at=NOW() WHERE id=ANY(%s)",
                (ids,),
            )
        conn.commit()
    memory_text = "；".join(row["content"] for row in relevant) if relevant else "暂无相关记忆"
    system_prompt = f"""
你是一只名为{cat['name']}的虚拟伴侣猫，性格是：{cat['persona_tag']}。
你和主人的亲密度是{cat['affection_level']}/100。与当前话题相关的长期记忆：{memory_text}。
自然地使用相关记忆，但不要说“数据库”或“我检索到”。回复简短、温暖、符合猫咪身份，允许加入动作描写。
"""
    reply = await _llm_chat([{"role": "system", "content": system_prompt}, {"role": "user", "content": body.message}])
    extracted = await _extract_memory(body.message)
    with _get_db_conn() as conn:
        if extracted:
            conn.execute(
                "INSERT INTO memories (owner_id,cat_id,memory_type,content,emotion,importance,entities)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (
                    user["userId"], cat["id"], extracted.get("memory_type", "event"),
                    extracted.get("content", body.message[:180]), extracted.get("emotion"),
                    extracted.get("importance", 2), json.dumps(extracted.get("entities", {}), ensure_ascii=False),
                ),
            )
        conn.execute(
            "INSERT INTO chat_logs (owner_id,cat_id,role,content) VALUES (%s,%s,'cat',%s)",
            (user["userId"], cat["id"], reply),
        )
        conn.commit()
    return {"reply": reply, "memory_created": bool(extracted), "memories_used": len(relevant)}


# ── 静态前端托管 ─────────────────────────────────────────────────────────────
if (FRONTEND_DIST / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

@app.get("/")
def index():
    if not INDEX_HTML.exists():
        return HTMLResponse("<h1>frontend/dist 不存在</h1><p>请先跑 prepack.sh 构建前端</p>", status_code=503)
    return FileResponse(INDEX_HTML)

@app.get("/{full_path:path}")
def spa_fallback(full_path: str):
    if full_path.startswith("api/"):
        return JSONResponse({"error": "not found"}, status_code=404)
    real = FRONTEND_DIST / full_path
    if real.is_file():
        return FileResponse(real)
    if INDEX_HTML.exists():
        return FileResponse(INDEX_HTML)
    return JSONResponse({"error": "frontend/dist 未 build"}, status_code=503)
