"""Idempotent PostgreSQL schema initialization for MeowLog."""
import os
import psycopg

SCHEMA = """
-- 1. 小猫主档表（记录性格、数值、懒计算时间戳）
CREATE TABLE IF NOT EXISTS cats (
    id SERIAL PRIMARY KEY,
    owner_id TEXT NOT NULL UNIQUE,  -- 每个用户暂定领养一只专属猫
    name TEXT NOT NULL,
    persona_tag TEXT NOT NULL,      -- 傲娇/黏人/哲学家/探险家/吃货/护短
    affection_level INT DEFAULT 0,  -- 好感度亲密度
    satiety_level INT DEFAULT 100,  -- 饱食度
    mood_level INT DEFAULT 100,     -- 心情值
    current_status TEXT DEFAULT 'idle', -- 当前状态 (idle, sleeping, roaming)
    outfit TEXT DEFAULT 'scarf',        -- 旧版兼容字段
    accessory TEXT DEFAULT 'scarf',     -- 配饰槽
    clothing TEXT DEFAULT 'none',       -- 服装槽
    leaf_coins INT DEFAULT 30,           -- 探险与任务奖励叶子币
    owned_items TEXT[] DEFAULT ARRAY['scarf','daisy','moss_cape','picnic_apron']::TEXT[],
    last_checkin_date DATE,
    checkin_streak INT DEFAULT 0,
    daily_date DATE DEFAULT CURRENT_DATE,
    daily_progress JSONB DEFAULT '{"feed":0,"pet":0,"play":0,"chat":0,"claimed":[]}'::jsonb,
    last_interact_time TIMESTAMPTZ DEFAULT NOW(), -- 上次互动时间（用于离线懒计算）
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 核心亮点：长效记忆表（AI 萃取后的结构化记忆）
CREATE TABLE IF NOT EXISTS memories (
    id SERIAL PRIMARY KEY,
    owner_id TEXT NOT NULL,
    cat_id INT REFERENCES cats(id) ON DELETE CASCADE,
    memory_type TEXT NOT NULL,      -- preference / event / emotion / goal
    content TEXT NOT NULL,
    emotion TEXT,
    importance INT DEFAULT 2,
    entities JSONB DEFAULT '{}'::jsonb,
    last_accessed_at TIMESTAMPTZ,
    access_count INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_memories_owner ON memories(owner_id);

-- 3. 日常聊天上下文表
CREATE TABLE IF NOT EXISTS chat_logs (
    id SERIAL PRIMARY KEY,
    owner_id TEXT NOT NULL,
    cat_id INT REFERENCES cats(id) ON DELETE CASCADE,
    role TEXT NOT NULL,             -- 'user' 还是 'cat'
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_chat_logs_owner ON chat_logs(owner_id);

-- 4. 探险手帐与 AIGC 明信片收集表
CREATE TABLE IF NOT EXISTS adventures (
    id SERIAL PRIMARY KEY,
    owner_id TEXT NOT NULL,
    cat_id INT REFERENCES cats(id) ON DELETE CASCADE,
    title TEXT NOT NULL,            -- 探险标题
    story TEXT NOT NULL,            -- AIGC 生成的探险日记
    image_data BYTEA,               -- 后续可存 AIGC 明信片
    status TEXT DEFAULT 'completed',
    destination TEXT,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    returns_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    reward_name TEXT,
    reward_coins INT DEFAULT 0,
    postcard_emoji TEXT DEFAULT '🌿',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_adventures_owner ON adventures(owner_id);

-- 兼容已部署的早期版本
ALTER TABLE cats ADD COLUMN IF NOT EXISTS outfit TEXT DEFAULT 'scarf';
ALTER TABLE cats ADD COLUMN IF NOT EXISTS accessory TEXT DEFAULT 'scarf';
ALTER TABLE cats ADD COLUMN IF NOT EXISTS clothing TEXT DEFAULT 'none';
ALTER TABLE cats ADD COLUMN IF NOT EXISTS leaf_coins INT DEFAULT 30;
ALTER TABLE cats ADD COLUMN IF NOT EXISTS owned_items TEXT[] DEFAULT ARRAY['scarf','daisy','moss_cape','picnic_apron']::TEXT[];
ALTER TABLE cats ADD COLUMN IF NOT EXISTS last_checkin_date DATE;
ALTER TABLE cats ADD COLUMN IF NOT EXISTS checkin_streak INT DEFAULT 0;
ALTER TABLE cats ADD COLUMN IF NOT EXISTS daily_date DATE DEFAULT CURRENT_DATE;
ALTER TABLE cats ADD COLUMN IF NOT EXISTS daily_progress JSONB DEFAULT '{"feed":0,"pet":0,"play":0,"chat":0,"claimed":[]}'::jsonb;
UPDATE cats SET leaf_coins=30 WHERE leaf_coins=0;
UPDATE cats SET owned_items = ARRAY(
  SELECT DISTINCT unnest(owned_items || ARRAY['scarf','daisy','moss_cape','picnic_apron',COALESCE(accessory,'scarf'),COALESCE(NULLIF(clothing,'none'),'moss_cape')])
) WHERE owned_items IS NOT NULL;
ALTER TABLE memories ADD COLUMN IF NOT EXISTS emotion TEXT;
ALTER TABLE memories ADD COLUMN IF NOT EXISTS importance INT DEFAULT 2;
ALTER TABLE memories ADD COLUMN IF NOT EXISTS entities JSONB DEFAULT '{}'::jsonb;
ALTER TABLE memories ADD COLUMN IF NOT EXISTS last_accessed_at TIMESTAMPTZ;
ALTER TABLE memories ADD COLUMN IF NOT EXISTS access_count INT DEFAULT 0;
ALTER TABLE adventures ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'completed';
ALTER TABLE adventures ADD COLUMN IF NOT EXISTS destination TEXT;
ALTER TABLE adventures ADD COLUMN IF NOT EXISTS started_at TIMESTAMPTZ DEFAULT NOW();
ALTER TABLE adventures ADD COLUMN IF NOT EXISTS returns_at TIMESTAMPTZ;
ALTER TABLE adventures ADD COLUMN IF NOT EXISTS completed_at TIMESTAMPTZ;
ALTER TABLE adventures ADD COLUMN IF NOT EXISTS reward_name TEXT;
ALTER TABLE adventures ADD COLUMN IF NOT EXISTS reward_coins INT DEFAULT 0;
ALTER TABLE adventures ADD COLUMN IF NOT EXISTS postcard_emoji TEXT DEFAULT '🌿';
-- 将旧版单槽位穿搭迁移到对应的新槽位
UPDATE cats SET accessory = outfit
WHERE outfit IN ('scarf','daisy','satchel','nightcap','bow','box')
  AND (accessory IS NULL OR accessory = 'scarf');
UPDATE cats SET clothing = outfit
WHERE outfit IN ('moss_cape','picnic_apron','raincoat','acorn_knit','berry_dress','moon_robe')
  AND (clothing IS NULL OR clothing = 'none');
"""

def main() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required")
    with psycopg.connect(database_url) as conn:
        conn.execute(SCHEMA)
        conn.commit()
    print("[init_db] done (MeowLog tables created)")

if __name__ == "__main__":
    main()
