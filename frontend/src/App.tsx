import React, { useEffect, useMemo, useRef, useState } from 'react';
import './index.css';
import './forest-upgrade.css';
import './closet-tabs-upgrade.css';
import './tailoring-fix.css';
import './adventure.css';
import './memory.css';
import './gameplay.css';

type Role = 'user' | 'cat';
type Action = 'feed' | 'pet' | 'play' | null;
type Page = 'home' | 'journal' | 'wardrobe' | 'shop';
type ClosetTab = 'accessory' | 'clothing' | 'favorite';

interface Cat {
  id: number;
  name: string;
  persona_tag: string;
  satiety_level: number;
  mood_level: number;
  affection_level: number;
  current_status: string;
  outfit?: string;
  accessory?: string;
  clothing?: string;
  leaf_coins?: number;
  owned_items?: string[];
}

interface Adventure {
  id: number;
  title: string;
  story: string;
  status: 'ongoing' | 'ready' | 'completed';
  destination: string;
  returns_at: string;
  reward_name: string;
  reward_coins: number;
  postcard_emoji: string;
  completed_at?: string;
}

interface DailyTask {
  id: 'feed' | 'pet' | 'play' | 'chat';
  title: string;
  target: number;
  progress: number;
  reward: number;
  icon: string;
  claimed: boolean;
}

interface ShopItem {
  id: string;
  name: string;
  category: 'accessory' | 'clothing';
  price: number;
  level: number;
  icon: string;
  owned: boolean;
}

interface MemoryItem {
  id: number;
  memory_type: string;
  content: string;
  emotion?: string;
  importance: number;
  access_count: number;
  created_at: string;
}

interface Message { role: Role; content: string }
interface Particle { id: number; x: number; y: number; glyph: string }

const PERSONALITIES = [
  ['傲娇猫猫', '嘴硬心软，偷偷把喜欢藏进尾巴里'],
  ['黏人甜心', '喜欢贴贴，你一回来就跑来迎接'],
  ['哲学发呆猫', '爱看云和月亮，偶尔说点猫生哲理'],
  ['神经质探险家', '好奇心旺盛，总能带回奇怪故事'],
  ['吃货摆烂猫', '把吃饭睡觉当作猫生头等大事'],
  ['护短大佬猫', '平时高冷，有人欺负你立刻炸毛'],
];

const STATUS_COPY: Record<string, string> = {
  idle: '正在窗边晒太阳', sleeping: '缩成一团做甜甜的梦', hungry: '肚子咕咕叫了',
  eating: '认真享用小鱼干', purring: '舒服得呼噜呼噜', playing: '追着毛线球满屋跑',
};

const CLOSET_ITEMS = [
  {id:'scarf',name:'赤豆围巾',icon:'⌁',level:1,rarity:'稀有',category:'accessory'},
  {id:'daisy',name:'林间雏菊',icon:'✿',level:1,rarity:'清新',category:'accessory'},
  {id:'satchel',name:'探险挎包',icon:'▱',level:1,rarity:'故事',category:'accessory'},
  {id:'nightcap',name:'云朵睡帽',icon:'☁',level:2,rarity:'梦境',category:'accessory'},
  {id:'bow',name:'海盐领结',icon:'⋈',level:3,rarity:'典雅',category:'accessory'},
  {id:'box',name:'神秘纸箱',icon:'□',level:4,rarity:'珍藏',category:'accessory'},
  {id:'moss_cape',name:'苔藓小斗篷',icon:'♠',level:1,rarity:'森语',category:'clothing'},
  {id:'picnic_apron',name:'野餐格围裙',icon:'▦',level:1,rarity:'田园',category:'clothing'},
  {id:'raincoat',name:'青柠雨衣',icon:'♧',level:2,rarity:'雨日',category:'clothing'},
  {id:'acorn_knit',name:'橡果针织衫',icon:'♨',level:2,rarity:'温暖',category:'clothing'},
  {id:'berry_dress',name:'莓果小礼服',icon:'♛',level:3,rarity:'华丽',category:'clothing'},
  {id:'moon_robe',name:'月光睡袍',icon:'☾',level:4,rarity:'珍藏',category:'clothing'},
] as const;
const OUTFIT_NAMES = Object.fromEntries(CLOSET_ITEMS.map(item => [item.id, item.name])) as Record<string,string>;

function getGuestId() {
  const key = 'meowlog-guest-id';
  let id = localStorage.getItem(key);
  if (!id) {
    id = globalThis.crypto?.randomUUID?.().replaceAll('-', '') || `guest_${Date.now()}_${Math.random().toString(36).slice(2)}`;
    localStorage.setItem(key, id);
  }
  return id;
}

function apiFetch(path: string, init: RequestInit = {}) {
  const headers = new Headers(init.headers);
  headers.set('X-Guest-Id', getGuestId());
  return fetch(path, { ...init, headers });
}

function Meter({ icon, label, value, color }: { icon: string; label: string; value: number; color: string }) {
  return <div className="meter">
    <div className="meter-line"><span>{icon} {label}</span><strong>{value}</strong></div>
    <div className="meter-track"><i style={{ width: `${value}%`, background: color }} /></div>
  </div>;
}

function CatIllustration({ action, accessory = 'scarf', clothing = 'none', onPet }: { action: Action; accessory?: string; clothing?: string; onPet: (e: React.MouseEvent) => void }) {
  return <button aria-label="摸摸小猫" className={`cat-illustration ${action ? `is-${action}` : ''} outfit-${accessory} outfit-${clothing}`} onClick={onPet}>
    <span className="cat-shadow" />
    <span className="cat-tail" />
    <span className="cat-body"><span className="cat-belly" /></span>
    <span className="cat-paw paw-left" /><span className="cat-paw paw-right" />
    <span className="silver-mark mark-body" />
    <span className="cat-head">
      <span className="cat-ear ear-left"><i /></span><span className="cat-ear ear-right"><i /></span>
      <span className="cat-face">
        <i className="eye eye-left" /><i className="eye eye-right" />
        <i className="cat-nose" /><i className="cat-mouth" />
        <i className="whisker w1" /><i className="whisker w2" /><i className="whisker w3" />
        <i className="whisker w4" /><i className="whisker w5" /><i className="whisker w6" />
        <i className="silver-mark mark-head" />
      </span>
    </span>
    <span className="wearable wearable-scarf"><i /></span>
    <span className="wearable wearable-daisy">✿</span>
    <span className="wearable wearable-satchel"><i /></span>
    <span className="wearable wearable-nightcap"><i /></span>
    <span className="wearable wearable-bow">⋈</span>
    <span className="wearable wearable-box">MEOW</span>
    <span className="wearable wearable-moss-cape"><i /></span>
    <span className="wearable wearable-picnic-apron"><i /></span>
    <span className="wearable wearable-raincoat"><i /></span>
    <span className="wearable wearable-acorn-knit"><i /></span>
    <span className="wearable wearable-berry-dress"><i /></span>
    <span className="wearable wearable-moon-robe"><i /></span>
  </button>;
}

export default function App() {
  const [loading, setLoading] = useState(true);
  const [cat, setCat] = useState<Cat | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [action, setAction] = useState<Action>(null);
  const [particles, setParticles] = useState<Particle[]>([]);
  const [page, setPage] = useState<Page>('home');
  const [chatOpen, setChatOpen] = useState(false);
  const [thinking, setThinking] = useState(false);
  const [closetTab, setClosetTab] = useState<ClosetTab>('accessory');
  const [favorites, setFavorites] = useState<string[]>(() => {
    try { return JSON.parse(localStorage.getItem('meowlog-favorites') || '["daisy","moss_cape"]'); }
    catch { return ['daisy','moss_cape']; }
  });
  const [currentAdventure, setCurrentAdventure] = useState<Adventure | null>(null);
  const [adventureHistory, setAdventureHistory] = useState<Adventure[]>([]);
  const [adventureBusy, setAdventureBusy] = useState(false);
  const [clock, setClock] = useState(Date.now());
  const [memoryOpen, setMemoryOpen] = useState(false);
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [dailyOpen, setDailyOpen] = useState(false);
  const [dailyTasks, setDailyTasks] = useState<DailyTask[]>([]);
  const [shopItems, setShopItems] = useState<ShopItem[]>([]);
  const [shopBusy, setShopBusy] = useState<string | null>(null);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    apiFetch('/api/cat/status').then(r => r.json()).then(data => {
      if (data.has_cat) { setCat(data.cat); loadDaily(); }
    }).finally(() => setLoading(false));
  }, []);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, thinking]);
  useEffect(() => {
    const timer = window.setInterval(() => setClock(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, []);
  useEffect(() => {
    if (page === 'journal') loadAdventures();
    if (page === 'shop') loadShop();
  }, [page]);

  const greeting = useMemo(() => {
    if (!cat) return '';
    if (cat.satiety_level < 30) return '我闻到小鱼干的味道了……是给我的吗？';
    if (cat.current_status === 'sleeping') return '唔……你回来啦？让我再眯五分钟。';
    return '你回来啦！我刚刚在窗边发现了一朵猫猫形状的云。';
  }, [cat]);

  function sensoryFeedback(kind: 'feed' | 'pet' | 'play' | 'reward') {
    try {
      navigator.vibrate?.(kind === 'reward' ? [35, 30, 55] : kind === 'play' ? [25, 20, 25] : 30);
      const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
      const ctx = new AudioContextClass();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = kind === 'reward' ? 'sine' : 'triangle';
      osc.frequency.value = kind === 'feed' ? 520 : kind === 'pet' ? 360 : kind === 'play' ? 620 : 760;
      gain.gain.setValueAtTime(.045, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + .18);
      osc.connect(gain); gain.connect(ctx.destination); osc.start(); osc.stop(ctx.currentTime + .18);
    } catch { /* browsers may disable haptics/audio */ }
  }

  function burst(x: number, y: number, glyphs: string[]) {
    const now = Date.now();
    const next = Array.from({ length: 8 }, (_, i) => ({ id: now + i, x: x + (Math.random() - .5) * 90, y: y + (Math.random() - .5) * 25, glyph: glyphs[i % glyphs.length] }));
    setParticles(p => [...p, ...next]);
    setTimeout(() => setParticles(p => p.filter(item => !next.some(n => n.id === item.id))), 1400);
  }

  async function interact(next: Exclude<Action, null>, e: React.MouseEvent) {
    if (action) return;
    setAction(next);
    sensoryFeedback(next);
    burst(e.clientX, e.clientY, next === 'feed' ? ['🐟', '✨'] : next === 'play' ? ['🧶', '⭐'] : ['♡', '✦']);
    const optimistic = cat && { ...cat,
      satiety_level: next === 'feed' ? Math.min(100, cat.satiety_level + 30) : next === 'play' ? Math.max(0, cat.satiety_level - 4) : cat.satiety_level,
      mood_level: next === 'pet' ? Math.min(100, cat.mood_level + 20) : next === 'play' ? Math.min(100, cat.mood_level + 28) : cat.mood_level,
      affection_level: Math.min(100, cat.affection_level + (next === 'play' ? 3 : next === 'pet' ? 2 : 1)),
      current_status: next === 'feed' ? 'eating' : next === 'pet' ? 'purring' : 'playing'
    };
    if (optimistic) setCat(optimistic);
    try {
      const res = await apiFetch('/api/cat/interact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ action_type: next }) });
      const data = await res.json();
      if (data.cat) setCat(data.cat);
      loadDaily();
    } finally { setTimeout(() => setAction(null), 1050); }
  }

  async function adopt(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    const payload = { name: form.get('name'), persona_tag: form.get('persona') };
    const res = await apiFetch('/api/cat/adopt', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    const data = await res.json();
    setCat(data); setMessages([{ role: 'cat', content: `喵呜，我是${data.name}。从今天开始，这里就是我们的家啦。` }]);
  }

  function toggleFavorite(id: string) {
    setFavorites(current => {
      const next = current.includes(id) ? current.filter(x => x !== id) : [...current, id];
      localStorage.setItem('meowlog-favorites', JSON.stringify(next));
      return next;
    });
  }

  async function changeOutfit(outfit: string, requiredLevel: number, slot: 'accessory' | 'clothing') {
    const level = Math.max(1, Math.floor((cat?.affection_level || 0) / 10) + 1);
    if (!cat || level < requiredLevel) return;
    const previous = cat;
    setCat({ ...cat, [slot]: outfit });
    try {
      const res = await apiFetch('/api/cat/outfit', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ outfit, slot }) });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || '换装失败');
      if (data.cat) setCat(data.cat);
    } catch { setCat(previous); }
  }

  async function loadDaily() {
    const res = await apiFetch('/api/daily');
    if (!res.ok) return;
    const data = await res.json();
    setDailyTasks(data.tasks || []);
    setCat(current => current ? { ...current, leaf_coins: data.leaf_coins } : current);
  }

  async function claimTask(taskId: string) {
    const res = await apiFetch('/api/daily/claim', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ task_id: taskId }) });
    if (!res.ok) return;
    const data = await res.json();
    sensoryFeedback('reward');
    setCat(data.cat);
    await loadDaily();
  }

  async function loadShop() {
    const res = await apiFetch('/api/shop');
    if (!res.ok) return;
    const data = await res.json();
    setShopItems(data.items || []);
    setCat(current => current ? { ...current, leaf_coins: data.leaf_coins } : current);
  }

  async function buyItem(item: ShopItem) {
    if (shopBusy || item.owned) return;
    setShopBusy(item.id);
    try {
      const res = await apiFetch('/api/shop/buy', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ item_id: item.id }) });
      if (!res.ok) return;
      const data = await res.json();
      sensoryFeedback('reward');
      setCat(data.cat);
      setShopItems(items => items.map(entry => entry.id === item.id ? { ...entry, owned: true } : entry));
    } finally { setShopBusy(null); }
  }

  async function loadAdventures() {
    const res = await apiFetch('/api/adventures');
    if (!res.ok) return;
    const data = await res.json();
    setCurrentAdventure(data.current || null);
    setAdventureHistory(data.history || []);
  }

  async function startAdventure() {
    if (adventureBusy) return;
    setAdventureBusy(true);
    try {
      const res = await apiFetch('/api/adventures/start', { method: 'POST' });
      const data = await res.json();
      if (res.ok) { setCurrentAdventure(data.adventure); setCat(c => c ? { ...c, current_status: 'roaming' } : c); }
    } finally { setAdventureBusy(false); }
  }

  async function claimAdventure() {
    if (adventureBusy) return;
    setAdventureBusy(true);
    try {
      const res = await apiFetch('/api/adventures/claim', { method: 'POST' });
      const data = await res.json();
      if (res.ok) {
        setCat(data.cat); setCurrentAdventure(null);
        setAdventureHistory(items => [data.adventure, ...items]);
      }
    } finally { setAdventureBusy(false); }
  }

  async function openMemories() {
    const res = await apiFetch('/api/memories');
    if (!res.ok) return;
    const data = await res.json();
    setMemories(data.memories || []);
    setMemoryOpen(true);
  }

  async function removeMemory(id: number) {
    const res = await apiFetch(`/api/memories/${id}`, { method: 'DELETE' });
    if (res.ok) setMemories(items => items.filter(item => item.id !== id));
  }

  async function chat(e: React.FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || thinking) return;
    setMessages(m => [...m, { role: 'user', content: text }]); setInput(''); setThinking(true);
    try {
      const res = await apiFetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: text }) });
      const data = await res.json();
      setMessages(m => [...m, { role: 'cat', content: data.reply || '刚刚走神去追光点了，你可以再说一次吗？' }]);
      loadDaily();
    } catch { setMessages(m => [...m, { role: 'cat', content: '网络像毛线团一样缠住了，等我挠开它再聊。' }]); }
    finally { setThinking(false); }
  }

  if (loading) return <div className="loading"><span className="loading-cat">🐾</span><p>正在推开小屋的门…</p></div>;

  if (!cat) return <main className="adoption-page">
    <section className="adoption-card">
      <div className="box-cat"><span>♡</span></div>
      <small>MEOWLOG · 初次相遇</small><h1>给彼此一个家</h1><p>它会拥有自己的生活，也会慢慢记住关于你的每一件小事。</p>
      <form onSubmit={adopt}>
        <label>它的名字<input name="name" maxLength={12} placeholder="例如：晚晚、团子、乌云" required /></label>
        <label>它是什么样的小猫<select name="persona">{PERSONALITIES.map(([name, desc]) => <option key={name} value={`${name}（${desc}）`}>{name} · {desc}</option>)}</select></label>
        <button>打开纸箱，带它回家 <b>→</b></button>
      </form>
    </section>
  </main>;

  const adventureRemaining = currentAdventure ? Math.max(0, new Date(currentAdventure.returns_at).getTime() - clock) : 0;
  const adventureReady = Boolean(currentAdventure && (currentAdventure.status === 'ready' || adventureRemaining === 0));

  return <main className="game-shell">
    {particles.map(p => <span className="particle" key={p.id} style={{ left: p.x, top: p.y }}>{p.glyph}</span>)}
    <header className="game-header">
      <div><small>MEOWLOG · {new Date().toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' })}</small><h1>{cat.name}的小屋</h1></div>
      <button className="level-chip">♡ Lv.{Math.max(1, Math.floor(cat.affection_level / 10) + 1)}</button>
    </header>

    {page === 'home' && <>
      <section className="room-card">
        <div className="sun-glow" /><div className="window"><i /><b /><span className="cloud c1" /><span className="cloud c2" /></div>
        <div className="wall-picture"><i>✿</i></div><div className="hanging-plant"><i /><b /></div>
        <div className="shelf"><span>▥</span><span>▤</span><span>◒</span></div>
        <div className="rug" /><div className="floor-lines" />
        <div className="cat-bed"><i /></div><div className="food-bowl">MEOW</div><div className="toy-mouse">●<i /></div>
        <div className="speech">{action === 'feed' ? '啊呜！今天的小鱼干格外香。' : action === 'pet' ? '呼噜呼噜……再摸一下也不是不可以。' : action === 'play' ? '抓到你啦，毛线球！' : greeting}</div>
        {action === 'feed' && <div className="flying-fish">🐟</div>}
        {action === 'pet' && <div className="petting-hand">☝</div>}
        {action === 'play' && <div className="rolling-yarn">●</div>}
        <CatIllustration action={action} accessory={cat.accessory || 'scarf'} clothing={cat.clothing || 'none'} onPet={e => interact('pet', e)} />
        <div className="status-caption"><span className="live-dot" />{STATUS_COPY[cat.current_status] || '正在小屋里自由活动'}</div>
      </section>

      <section className="stat-card">
        <Meter icon="◒" label="饱食" value={cat.satiety_level} color="#db9a70" />
        <Meter icon="✦" label="心情" value={cat.mood_level} color="#e8b85b" />
        <Meter icon="♡" label="亲密" value={cat.affection_level} color="#d98886" />
      </section>

      <section className="actions">
        <button onClick={e => interact('feed', e)}><i className="action-icon fish-icon">◇</i><span>喂小鱼干<small>饱食 +30</small></span></button>
        <button onClick={e => interact('pet', e)}><i className="action-icon hand-icon">♧</i><span>摸摸头<small>亲密 +2</small></span></button>
        <button onClick={e => interact('play', e)}><i className="action-icon yarn-icon">●</i><span>玩毛线球<small>心情 +28</small></span></button>
      </section>

      <button className="talk-card" onClick={() => setChatOpen(true)}><span className="mini-avatar"><i>•ᴗ•</i></span><span><b>想和你说说话</b><small>它会记住你的开心和烦恼</small></span><em>→</em></button>
      <button className="daily-card" onClick={() => { loadDaily(); setDailyOpen(true); }}><span>✓</span><div><b>今日陪伴任务</b><small>{dailyTasks.filter(task=>task.claimed).length}/{dailyTasks.length || 4} 已领取 · 完成任务赚叶子币</small></div><em>{cat.leaf_coins || 0} 🍃</em></button>
    </>}

    {page === 'journal' && <section className="book-page adventure-page">
      <small>ADVENTURE JOURNAL · 叶子币 {cat.leaf_coins || 0}</small>
      <h2>{cat.name}的探险手帐</h2>
      <p className="book-intro">它会独自出发，也会带着故事和礼物回来。</p>

      {currentAdventure ? <div className={`adventure-mission ${adventureReady ? 'ready' : ''}`}>
        <div className="mission-scene"><span>{currentAdventure.postcard_emoji}</span><i>🐾</i><b>⌂</b></div>
        <div className="mission-copy"><small>{adventureReady ? '已抵达家门口' : '正在探险中'}</small><h3>{currentAdventure.destination}</h3>
          {!adventureReady && <p>预计还有 <strong>{String(Math.floor(adventureRemaining / 60000)).padStart(2,'0')}:{String(Math.floor(adventureRemaining / 1000) % 60).padStart(2,'0')}</strong> 回家</p>}
          {adventureReady && <p>它抱着一个鼓鼓的小包，正等你来拆礼物。</p>}
        </div>
        <button disabled={!adventureReady || adventureBusy} onClick={claimAdventure}>{adventureBusy ? '正在整理手帐…' : adventureReady ? '迎接回家' : '耐心等等'}</button>
      </div> : <div className="adventure-start">
        <div className="map-dots"><i>⌂</i><span>· · · · ·</span><b>?</b></div>
        <h3>今天会遇见什么？</h3><p>目的地、故事和礼物都会由猫咪自己决定。</p>
        <button disabled={adventureBusy} onClick={startAdventure}>{adventureBusy ? '正在收拾背包…' : '准备小背包，出发'}</button>
      </div>}

      <div className="journal-heading"><b>过往手帐</b><span>{adventureHistory.length} 篇</span></div>
      {adventureHistory.length === 0 && <div className="empty-journal">第一张明信片还在路上。</div>}
      {adventureHistory.map((item, index) => <article className="postcard" key={item.id} style={{transform:`rotate(${index%2 ? 1 : -1}deg)`}}>
        <div className="postcard-art generated"><span>{item.postcard_emoji}</span><i>{item.destination?.slice(0,1)}</i><b>🐾</b></div>
        <small>{item.completed_at ? new Date(item.completed_at).toLocaleDateString('zh-CN') : '刚刚'} · {item.destination}</small>
        <h3>{item.title}</h3><p>{item.story}</p><em>获得：{item.reward_name} · 叶子币 +{item.reward_coins}</em>
      </article>)}
    </section>}

    {page === 'wardrobe' && <section className="book-page wardrobe-page">
      <small>FOREST CLOSET · 今日搭配</small>
      <h2>{cat.name}的森系衣橱</h2>
      <p className="book-intro">选择分类、收藏单品，再点击卡片试穿。</p>
      <div className="closet-stage">
        <div className="closet-vines">❧　❧　❧</div>
        <div className="closet-cat"><CatIllustration action={null} accessory={cat.accessory || 'scarf'} clothing={cat.clothing || 'none'} onPet={() => {}} /></div>
        <div className="look-label"><span>今日穿搭</span><b>{OUTFIT_NAMES[cat.clothing || 'none'] || '基础毛色'} · {OUTFIT_NAMES[cat.accessory || 'scarf']}</b></div>
      </div>
      <div className="closet-tabs">
        <button className={closetTab==='accessory'?'active':''} onClick={()=>setClosetTab('accessory')}>配饰</button>
        <button className={closetTab==='clothing'?'active':''} onClick={()=>setClosetTab('clothing')}>衣服</button>
        <button className={closetTab==='favorite'?'active':''} onClick={()=>setClosetTab('favorite')}>收藏 <span>{favorites.length}</span></button>
      </div>
      <div className="items-grid">
        {CLOSET_ITEMS.filter(item => closetTab === 'favorite' ? favorites.includes(item.id) : item.category === closetTab).map(item=>{
          const level=Math.max(1,Math.floor(cat.affection_level/10)+1);
          const owned=(cat.owned_items || ['scarf','moss_cape']).includes(item.id);
          const locked=level<item.level || !owned;
          const selected = item.category === 'accessory' ? cat.accessory === item.id : cat.clothing === item.id;
          return <div className={`closet-item-wrap ${selected?'selected':''}`} key={item.id}>
            <button className="favorite-btn" aria-label={favorites.includes(item.id)?'取消收藏':'收藏'} onClick={()=>toggleFavorite(item.id)}>{favorites.includes(item.id)?'♥':'♡'}</button>
            <button className="outfit-btn" disabled={locked} onClick={()=>changeOutfit(item.id,item.level,item.category)}>
              <i>{item.icon}</i><span>{item.name}</span><em>{item.rarity}</em>
              {locked&&<b>{!owned?'未拥有':`Lv.${item.level}`}</b>}{selected&&<strong>✓</strong>}
            </button>
          </div>
        })}
        {closetTab==='favorite' && favorites.length===0 && <div className="empty-favorites"><i>♡</i><b>还没有收藏</b><span>去“配饰”或“衣服”点亮爱心吧</span></div>}
      </div>
    </section>}

    {page === 'shop' && <section className="book-page shop-page">
      <small>FOREST BAZAAR · 叶子币商店</small><h2>松果婆婆的杂货铺</h2><p className="book-intro">完成陪伴任务和探险，换一件送给小猫的礼物。</p>
      <div className="wallet-card"><span>🍃</span><div><small>我的叶子币</small><b>{cat.leaf_coins || 0}</b></div><em>每天都有新故事</em></div>
      <div className="shop-grid">{shopItems.map(item=>{const level=Math.max(1,Math.floor(cat.affection_level/10)+1);const canBuy=level>=item.level&&(cat.leaf_coins||0)>=item.price;return <article key={item.id} className={item.owned?'owned':''}><div className="shop-art"><i>{item.icon}</i><span>{item.category==='accessory'?'配饰':'服装'}</span></div><h3>{item.name}</h3><small>亲密 Lv.{item.level} 解锁</small><button disabled={item.owned||!canBuy||shopBusy===item.id} onClick={()=>buyItem(item)}>{item.owned?'已拥有':shopBusy===item.id?'打包中…':`${item.price} 🍃`}</button></article>})}</div>
    </section>}

    <nav className="bottom-nav">
      <button className={page==='home'?'active':''} onClick={()=>setPage('home')}><i>⌂</i><span>小屋</span></button>
      <button className={page==='journal'?'active':''} onClick={()=>setPage('journal')}><i>▤</i><span>手帐</span></button>
      <button className={page==='wardrobe'?'active':''} onClick={()=>setPage('wardrobe')}><i>♢</i><span>衣橱</span></button>
      <button className={page==='shop'?'active':''} onClick={()=>setPage('shop')}><i>♧</i><span>商店</span></button>
    </nav>

    {dailyOpen && <div className="daily-overlay" onClick={()=>setDailyOpen(false)}><section onClick={e=>e.stopPropagation()}><header><div><small>DAILY WITH ME</small><h3>今日陪伴任务</h3></div><button onClick={()=>setDailyOpen(false)}>×</button></header><div className="daily-list">{dailyTasks.map(task=>{const done=task.progress>=task.target;return <article key={task.id} className={task.claimed?'claimed':''}><i>{task.icon}</i><div><b>{task.title}</b><span>{task.progress}/{task.target}</span><em><u style={{width:`${Math.min(100,task.progress/task.target*100)}%`}} /></em></div><button disabled={!done||task.claimed} onClick={()=>claimTask(task.id)}>{task.claimed?'已领取':done?`领取 ${task.reward} 🍃`:'进行中'}</button></article>})}</div><footer>每天陪伴一点点，关系就会慢慢长大。</footer></section></div>}

    {chatOpen && <div className="chat-overlay"><section className="chat-panel">
      <header><button onClick={()=>setChatOpen(false)}>⌄</button><div className="chat-cat-face">•ᴗ•</div><div><b>{cat.name}</b><small><i />正在听你说</small></div><button className="memory-button" onClick={openMemories}>回忆</button></header>
      <div className="chat-list"><div className="day-pill">今天</div>{messages.length===0&&<div className="bubble cat">{greeting}</div>}{messages.map((m,i)=><div key={i} className={`bubble ${m.role}`}>{m.content}</div>)}{thinking&&<div className="bubble cat typing"><i/><i/><i/></div>}<div ref={endRef}/></div>
      <form onSubmit={chat} className="composer"><button type="button">＋</button><input value={input} onChange={e=>setInput(e.target.value)} placeholder="今天发生了什么？"/><button className="send">↑</button></form>
    </section>{memoryOpen && <section className="memory-shelf">
      <header><div><small>LONG-TERM MEMORY</small><h3>{cat.name}记住的事</h3></div><button onClick={()=>setMemoryOpen(false)}>×</button></header>
      <p className="memory-note">这些记忆会帮助它更懂你。你可以随时删除不想保留的内容。</p>
      <div className="memory-list">{memories.length===0&&<div className="empty-memory">还没有长期记忆，试着告诉它你的喜好或最近的重要事情。</div>}{memories.map(item=><article key={item.id}><i>{item.memory_type==='preference'?'♡':item.memory_type==='emotion'?'☁':item.memory_type==='goal'?'✦':'▤'}</i><div><small>{item.memory_type} · 重要度 {item.importance}</small><p>{item.content}</p></div><button onClick={()=>removeMemory(item.id)}>删除</button></article>)}</div>
    </section>}</div>}
  </main>;
}
