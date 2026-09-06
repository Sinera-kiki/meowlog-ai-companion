from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app import app, _select_relevant_memories

client = TestClient(app)


def guest_headers():
    return {"X-Guest-Id": uuid4().hex}


def test_health():
    assert client.get("/health").json() == {"ok": True}


def test_memory_relevance_prefers_matching_content():
    rows = [
        {"id": 1, "content": "主人喜欢草莓蛋糕", "importance": 2},
        {"id": 2, "content": "主人明天要参加面试", "importance": 2},
    ]
    selected = _select_relevant_memories(rows, "草莓味的甜点", limit=1)
    assert selected[0]["id"] == 1


def test_adopt_interact_and_dual_slot_outfit():
    headers = guest_headers()
    assert client.get("/api/cat/status", headers=headers).json()["has_cat"] is False
    adopted = client.post(
        "/api/cat/adopt",
        headers=headers,
        json={"name": "团子", "persona_tag": "黏人甜心"},
    )
    assert adopted.status_code == 200
    assert client.post("/api/cat/interact", headers=headers, json={"action_type": "pet"}).status_code == 200
    shop = client.get("/api/shop", headers=headers).json()
    assert any(item["id"] == "daisy" and not item["owned"] for item in shop["items"])
    assert client.post("/api/shop/buy", headers=headers, json={"item_id": "daisy"}).status_code == 200
    assert client.post(
        "/api/cat/outfit", headers=headers, json={"outfit": "daisy", "slot": "accessory"}
    ).status_code == 200
    assert client.post(
        "/api/cat/outfit", headers=headers, json={"outfit": "moss_cape", "slot": "clothing"}
    ).status_code == 200
    cat = client.get("/api/cat/status", headers=headers).json()["cat"]
    assert cat["accessory"] == "daisy"
    assert cat["clothing"] == "moss_cape"


def test_daily_task_reward():
    headers = guest_headers()
    client.post("/api/cat/adopt", headers=headers, json={"name": "雪团", "persona_tag": "黏人甜心"})
    client.post("/api/cat/interact", headers=headers, json={"action_type": "feed"})
    daily = client.get("/api/daily", headers=headers).json()
    feed = next(task for task in daily["tasks"] if task["id"] == "feed")
    assert feed["progress"] == 1
    claimed = client.post("/api/daily/claim", headers=headers, json={"task_id": "feed"})
    assert claimed.status_code == 200
    assert claimed.json()["cat"]["leaf_coins"] == 38


def test_adventure_can_start():
    headers = guest_headers()
    client.post("/api/cat/adopt", headers=headers, json={"name": "乌云", "persona_tag": "神经质探险家"})
    response = client.post("/api/adventures/start", headers=headers)
    assert response.status_code == 200
    assert response.json()["adventure"]["status"] == "ongoing"
    listing = client.get("/api/adventures", headers=headers).json()
    assert listing["current"] is not None


def test_demo_chat_extracts_memory():
    headers = guest_headers()
    client.post("/api/cat/adopt", headers=headers, json={"name": "年糕", "persona_tag": "护短大佬猫"})
    response = client.post("/api/chat", headers=headers, json={"message": "我明天要参加面试，有点压力"})
    assert response.status_code == 200
    assert response.json()["memory_created"] is True
    memories = client.get("/api/memories", headers=headers).json()["memories"]
    assert len(memories) == 1
