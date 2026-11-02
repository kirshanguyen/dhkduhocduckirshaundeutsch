from pathlib import Path
import re,html,json,shutil,datetime
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'dist'
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir();shutil.copy2(ROOT/'index.html',OUT/'index.html');shutil.copytree(ROOT/'assets',OUT/'assets')
(OUT/'bai-viet').mkdir()
CATS=['Học tiếng Đức','Du học đại học Đức','Du học nghề Đức','Cuộc sống tại Đức']
def esc(v):return html.escape(str(v),quote=True)
def markdown(v):
    lines=v.splitlines();out=[];ul=False
    def inline(t):
        t=esc(t);t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
        t=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<a href="\2" rel="noopener noreferrer" target="_blank">\1</a>',t)
        return t
    for line in lines:
        t=line.strip()
        if t.startswith('- '):
            if not ul:out.append('<ul>');ul=True
            out.append('<li>'+inline(t[2:])+'</li>');continue
        if ul:out.append('</ul>');ul=False
        if not t:continue
        if t.startswith('### '):out.append('<h3>'+inline(t[4:])+'</h3>')
        elif t.startswith('## '):out.append('<h2>'+inline(t[3:])+'</h2>')
        else:out.append('<p>'+inline(t)+'</p>')
    if ul:out.append('</ul>')
    return '\n'.join(out)
def parse(path):
    text=path.read_text(encoding='utf8').lstrip('\ufeff')
    if not text.startswith('---\n'):raise ValueError(f'{path}: thiếu dấu --- đầu bài')
    _,fm,body=text.split('---',2);data={}
    for line in fm.strip().splitlines():
        if ':' in line:
            k,v=line.split(':',1);data[k.strip()]=v.strip().strip('"').strip("'")
    for key in ['title','date','category','description']:
        if not data.get(key):raise ValueError(f'{path}: thiếu {key}')
    if data['category'] not in CATS:raise ValueError(f'{path}: category không hợp lệ: {data["category"]}')
    datetime.date.fromisoformat(data['date'])
    data['slug']=path.stem;data['body']=body;return data
posts=sorted([parse(p) for p in (ROOT/'posts').glob('*.md') if not p.name.startswith('_')],key=lambda p:p['date'],reverse=True)
def header(prefix=''):
    return f'''<div class="topline">TIẾNG ĐỨC DHK · KIRSHA UND DEUTSCH</div><header><div class="wrap nav"><a class="logo" href="{prefix}index.html"><span class="mark">DHK</span><span><b>TIẾNG ĐỨC DHK</b><small>Kirsha und Deutsch</small></span></a><nav class="blog-nav"><a href="{prefix}index.html">Trang chủ</a><a href="{prefix}index.html#dich-vu">Dịch vụ</a><a href="{prefix}index.html#ve-dhk">Về DHK</a><a href="{prefix}bai-viet/index.html">Góc chia sẻ</a><a href="{prefix}index.html#lien-he">Liên hệ ↗</a></nav></div></header>'''
def page(title,body,description=''):
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(description or title)}"><meta name="theme-color" content="#163f35"><title>{esc(title)} | Tiếng Đức DHK</title><link rel="stylesheet" href="../assets/style.css"><link rel="stylesheet" href="../assets/blog.css"><style>.blog-nav{{display:flex;gap:20px;align-items:center;font-size:13px;font-weight:700;flex-wrap:wrap}}.blog-nav a:hover{{color:#287658}}@media(max-width:700px){{.blog-nav{{gap:10px;font-size:11px}}.blog-nav a:nth-child(2),.blog-nav a:nth-child(3){{display:none}}.nav{{height:auto;min-height:78px;flex-wrap:wrap;padding-top:12px;padding-bottom:12px;gap:8px}}}}</style></head><body>{header('../')}<main class="blog-page"><div class="wrap">{body}</div></main><footer><div class="wrap" style="padding-top:26px;padding-bottom:26px;font-size:13px">© Tiếng Đức DHK · Kirsha und Deutsch · <a href="../index.html#lien-he">Liên hệ</a></div></footer></body></html>'''
filters='<div class="blog-filters"><a class="blog-filter active" href="index.html">Tất cả bài viết</a>'+''.join(f'<a class="blog-filter" href="#{quote(cat)}" data-category="{esc(cat)}">{esc(cat)}</a>' for cat in CATS)+'</div>'
cards=[]
for p in posts:
    slug=quote(p['slug']);cover=p.get('image','');image=f'<img src="../{esc(cover)}" alt="" loading="lazy">' if cover and (ROOT/cover).is_file() else 'DHK · CHIA SẺ'
    cards.append(f'''<a class="blog-card" data-category="{esc(p['category'])}" href="{slug}.html"><div class="blog-card-img">{image}</div><div class="blog-card-body"><div class="blog-card-meta">{esc(p['category'])} · {esc(p['date'])}</div><h2>{esc(p['title'])}</h2><p>{esc(p['description'])}</p></div></a>''')
    article=f'''<div class="article-wrap"><a class="back-link" href="index.html">← Tất cả bài viết</a><div class="blog-eyebrow" style="margin-top:30px">{esc(p['category'])}</div><h1>{esc(p['title'])}</h1><p class="article-meta">{esc(p['date'])} · Frau Hà Anh · Tiếng Đức DHK</p>{f'<img class="article-cover" src="../{esc(cover)}" alt="Ảnh minh họa">' if cover and (ROOT/cover).is_file() else ''}<div class="article-content">{markdown(p['body'])}</div><p style="margin-top:38px"><a class="back-link" href="../index.html#lien-he">Bạn cần tư vấn? Liên hệ DHK ↗</a></p></div>'''
    (OUT/'bai-viet'/f'{p["slug"]}.html').write_text(page(p['title'],article,p['description']),encoding='utf8')
listing=f'''<div class="blog-heading"><div class="blog-eyebrow">KIRSHA UND DEUTSCH · GÓC CHIA SẺ DHK</div><h1>Những điều đáng chia sẻ.</h1><p>Kiến thức, kinh nghiệm và những câu chuyện thực tế về học tiếng Đức, du học và cuộc sống tại Đức. Một hành trình luôn có người đồng hành.</p></div>{filters}<div class="blog-grid">{''.join(cards) if cards else '<div class="empty-blog">Bài viết đầu tiên đang được chuẩn bị. Hẹn gặp bạn tại Góc chia sẻ DHK!</div>'}</div><script>document.querySelectorAll("[data-category].blog-filter").forEach(a=>a.addEventListener("click",e=>{{e.preventDefault();document.querySelectorAll(".blog-filter").forEach(x=>x.classList.remove("active"));a.classList.add("active");document.querySelectorAll(".blog-card").forEach(x=>x.hidden=x.dataset.category!==a.dataset.category)}}));document.querySelector(".blog-filter.active").addEventListener("click",()=>{{document.querySelectorAll(".blog-card").forEach(x=>x.hidden=false);document.querySelectorAll(".blog-filter").forEach(x=>x.classList.remove("active"));document.querySelector(".blog-filter").classList.add("active")}});</script>'''
(OUT/'bai-viet'/'index.html').write_text(page('Góc chia sẻ',listing,'Bài viết và kinh nghiệm thực tế về tiếng Đức, du học đại học, du học nghề và cuộc sống tại Đức.'),encoding='utf8')
print(f'Đã tạo {len(posts)} bài viết tại {OUT}')
