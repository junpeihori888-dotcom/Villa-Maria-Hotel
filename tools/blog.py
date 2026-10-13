#!/usr/bin/env python3
"""Build the blog from content/blog.html (the Word document, converted with
`pandoc Digital_Marketing.docx -t html --wrap=none -o content/blog.html`).

Each article stays in the language it was written in:
  family articles (English)   -> blog-<slug>.html      at the site root
  business articles (Italian) -> it/blog-<slug>.html   next to the Italian pages
The blog index is built in both languages: blog.html and it/blog.html.
The MENU lists the articles from PAGES.blog in assets/js/site.js; keep it in step
with POSTS below.

Run:  python3 tools/blog.py
"""
import html
import json
import pathlib
import re

from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'content' / 'blog.html'

# In the order of the document. cover/inline are photos in assets/img/.
POSTS = [
    dict(slug='italian-stop-family-abruzzo', list='family', lang='en', cover='pool-park.jpg', inline='people/moment-pool.jpg',
         teaser='Halfway through a big Italy trip, everyone needs a break. Here is the stop on the Adriatic coast that gives the whole family one.',
         cta=('The stop your family needs', 'Italian Memories begins at Villa Maria.', 'Discover Italian Memories →', 'italian-memories.html')),
    dict(slug='three-days-zero-alarm-clocks', list='family', lang='en', cover='breakfast.jpg', inline='suite-terrace.jpg',
         teaser='Padel scores, warm water and dinners nobody wants to end: a three-day rhythm for families who need a real break.',
         cta=('Your three days start here', 'Room, breakfast and spa included with the Family Discount.', 'See the Family Discount →', 'family-reset-package.html')),
    dict(slug='letter-to-the-family-planner', list='family', lang='en', cover='suite-seaview.jpg', inline='people/family-welcome-back.jpg',
         teaser='Fourteen tabs open at 11 PM? Rooms, meals, cancellation and getting here, told the way a friend would tell you.',
         cta=('Ready when you are', 'Choose your dates and we confirm by email. No payment now.', 'Check availability →', 'booking.html#family-discount')),
    dict(slug='martedi-sera-manager-pescara', list='business', lang='it', cover='dining.jpg', inline='superior-room.jpg',
         teaser='Dall’aereo alla cena di lavoro: come un hotel a dieci minuti da Pescara diventa ufficio, spogliatoio e ristorante.',
         cta=('La tua prossima trasferta, già organizzata', 'Camera silenziosa, colazione presto, spa e sala riunioni.', 'Scopri l’Executive Business Stay →', 'executive-business-stay.html')),
    dict(slug='quando-il-meeting-funziona', list='business', lang='it', cover='meeting-room.jpg', inline='auditorium.jpg',
         teaser='Sale nel verde, pernottamento nello stesso posto e una sera che trasforma il team in squadra.',
         cta=('Organizza il tuo meeting', 'Raccontaci data, numero di persone e formato: ti proponiamo la sala giusta.', 'Scrivici →', 'business-travel.html#message')),
    dict(slug='dopo-l-ultima-call', list='business', lang='it', cover='garden-gazebo.jpg', inline='people/business-padel.jpg',
         teaser='Il venerdì sera che non ti aspettavi: una partita a padel, una cena e magari la famiglia che ti raggiunge.',
         cta=('Il campo è pronto. Anche la camera.', 'Gioca, recupera, brinda, cena.', 'Scopri Beyond the Meeting Room →', 'beyond-the-meeting-room.html')),
]

UI = {
    'en': dict(blog='Blog', family='For families', business='For business', read='min read', lang_name='English',
               faq='Questions & answers', faq_h='Good to know <i>before you go.</i>', more='More from the blog',
               all='All articles →', help='Help', index_t='Stories from <i>Villa Maria.</i>',
               index_p='Ideas and stories for your holiday on the Adriatic coast of Abruzzo.',
               index_title='Blog · Villa Maria Hotel & Spa',
               index_desc='Stories from Villa Maria Hotel & Spa in Francavilla al Mare: ideas for family holidays in Abruzzo.',
               en='English', it='Italiano'),
    'it': dict(blog='Blog', family='Per le famiglie', business='Per il business', read='min di lettura', lang_name='Italiano',
               faq='Domande frequenti', faq_h='Utile da sapere <i>prima di partire.</i>', more='Altri articoli dal blog',
               all='Tutti gli articoli →', help='Aiuto', index_t='Storie da <i>Villa Maria.</i>',
               index_p='Idee e storie per i tuoi viaggi di lavoro sulla costa adriatica, a pochi minuti da Pescara.',
               index_title='Blog · Villa Maria Hotel & Spa',
               index_desc='Storie da Villa Maria Hotel & Spa a Francavilla al Mare: idee per i viaggi di lavoro vicino a Pescara.',
               en='English', it='Italiano'),
}


def head(title, desc, base, extra=''):
    return f'''<!DOCTYPE html>
<html lang="{{lang}}">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>{html.escape(title)}</title>
<meta content="{html.escape(desc)}" name="description"/>
{extra}<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&amp;family=Manrope:wght@400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="{base}assets/css/style.css" rel="stylesheet"/>
<link href="{base}assets/img/logo.png" rel="icon"/>
</head>
<body>
<main id="main">
'''


FOOT = '''</main>
<script src="{base}assets/js/site.js"></script>
</body>
</html>
'''


def parse():
    soup = BeautifulSoup(SRC.read_text(encoding='utf-8'), 'html.parser')
    posts, cur = [], None
    for el in soup.find_all(recursive=False):
        if el.name == 'h1':
            cur = dict(title=re.sub(r'^Blog \d+:\s*', '', el.get_text(' ', strip=True)), keywords='', body=[], faq=[])
            posts.append(cur)
            mode = 'body'
            continue
        if cur is None or el.name == 'h3':      # h3s in the source are empty separators
            continue
        text = el.get_text(' ', strip=True)
        if el.name == 'p' and el.find('em') and re.match(r'^Keywords?:', text):
            cur['keywords'] = re.sub(r'^Keywords?:\s*', '', text)
            continue
        if el.name == 'h4' and text.upper() == 'FAQ':
            mode = 'faq'
            continue
        if mode == 'faq' and el.name == 'p' and el.strong:
            q = el.strong.get_text(' ', strip=True)
            el.strong.extract()
            a = el.decode_contents().strip()
            a = re.sub(r'^(<br\s*/?>\s*)+', '', a).strip()
            cur['faq'].append((q, a))
            continue
        if mode == 'faq':                       # anything after the FAQ is not part of the article
            continue
        if el.name == 'h4':
            cur['body'].append(f'<h2 class="h3">{html.escape(text)}</h2>')
            continue
        if el.name == 'p' and not text:
            continue
        for br in el.find_all('br'):
            br.replace_with(' ')
        cur['body'].append(str(el))
    assert len(posts) == len(POSTS), f'{len(posts)} articles in the document, {len(POSTS)} in POSTS'
    for p, meta in zip(posts, POSTS):
        p.update(meta)
        words = len(BeautifulSoup(''.join(p['body']), 'html.parser').get_text(' ').split())
        p['minutes'] = max(1, round(words / 220))
    return posts


def href(post, from_lang):
    """Link to an article from a page in from_lang's folder."""
    f = f'blog-{post["slug"]}.html'
    if post['lang'] == from_lang:
        return f
    return ('it/' if post['lang'] == 'it' else '../') + f


def card(post, from_lang, base):
    u = UI[from_lang]
    label = u['family'] if post['list'] == 'family' else u['business']
    return (f'<a class="card blog-card" href="{href(post, from_lang)}" hreflang="{post["lang"]}">'
            f'<div class="ph"><img alt="" loading="lazy" src="{base}assets/img/{post["cover"]}"/></div>'
            f'<p class="eb">{label}</p>'
            f'<div class="t" lang="{post["lang"]}">{html.escape(post["title"])}</div>'
            f'<div class="s" lang="{post["lang"]}">{html.escape(post["teaser"])}</div>'
            f'<span class="more">{post["minutes"]} {u["read"]}</span></a>')


def article(post, posts):
    lang, u = post['lang'], UI[post['lang']]
    base = '../' if lang == 'it' else ''
    label = u['family'] if post['list'] == 'family' else u['business']
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': BeautifulSoup(a, 'html.parser').get_text(' ', strip=True)}}
        for q, a in post['faq']]}
    art_ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': post['title'], 'description': post['teaser'],
              'inLanguage': lang, 'keywords': post['keywords'], 'image': f'{base}assets/img/{post["cover"]}',
              'publisher': {'@type': 'Hotel', 'name': 'Villa Maria Hotel & Spa'}}
    extra = (f'<meta content="{html.escape(post["keywords"])}" name="keywords"/>\n'
             f'<script type="application/ld+json">{json.dumps(art_ld, ensure_ascii=False)}</script>\n'
             + (f'<script id="faq-schema" type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>\n' if post['faq'] else ''))
    body = list(post['body'])
    # one photo in the middle of the story
    h2s = [i for i, b in enumerate(body) if b.startswith('<h2')]
    if len(h2s) >= 2:
        body.insert(h2s[1], f'<figure class="post-fig"><img alt="" loading="lazy" src="{base}assets/img/{post["inline"]}"/></figure>')
    faq = ''
    if post['faq']:
        faq = ('<section class="section faq" id="faq">\n<div class="wrap split">\n'
               f'<div><p class="eb">{u["faq"]}</p>\n<h2 class="h2">{u["faq_h"]}</h2></div>\n<div class="faq-list">\n'
               + ''.join(f'<details class="faq-item"><summary><span>{html.escape(q)}</span></summary><div class="faq-a"><p>{a}</p></div></details>\n'
                         for q, a in post['faq'])
               + '</div>\n</div>\n</section>\n')
    ct, cp, cb, cl = post['cta']
    others = [p for p in posts if p['list'] == post['list'] and p is not post]
    out = head(f'{post["title"]} · Villa Maria Hotel & Spa', post['teaser'], base, extra).replace('{lang}', lang)
    out += f'''<article>
<header class="post-head">
<div class="wrap">
<p class="eb"><a href="blog.html">{u["blog"]}</a> · {label}</p>
<h1 class="h2 post-title">{html.escape(post["title"])}</h1>
<p class="post-teaser">{html.escape(post["teaser"])}</p>
<p class="post-meta">{post["minutes"]} {u["read"]} · {u["lang_name"]}</p>
</div>
<div class="wrap"><figure class="post-cover"><img alt="" src="{base}assets/img/{post["cover"]}"/></figure></div>
</header>
<div class="section tight">
<div class="wrap"><div class="prose post-body">
{chr(10).join(body)}
</div></div>
</div>
</article>
{faq}<section class="cta">
<div class="wrap">
<div><h2 class="h2">{html.escape(ct)}</h2>
<p>{html.escape(cp)}</p></div>
<div class="btns"><a class="btn btn-sky" href="{cl}">{html.escape(cb)}</a><button class="btn btn-ghost" data-help="" type="button">{u["help"]}</button></div>
</div>
</section>
<section class="section white">
<div class="wrap">
<div class="head"><div><p class="eb">{u["more"]}</p></div><a class="more-link" href="blog.html">{u["all"]}</a></div>
<div class="cards" style="--cols:2">
{chr(10).join(card(p, lang, base) for p in others)}
</div>
</div>
</section>
''' + FOOT.format(base=base)
    return out


def index(posts, lang):
    u = UI[lang]
    base = '../' if lang == 'it' else ''
    out = head(u['index_title'], u['index_desc'], base).replace('{lang}', lang)
    out += f'''<section class="post-head blog-head">
<div class="wrap">
<p class="eb">{u["blog"]}</p>
<h1 class="h2 post-title">{u["index_t"]}</h1>
<p class="post-teaser">{u["index_p"]}</p>
</div>
</section>
'''
    for lst in ('family', 'business'):
        group = [p for p in posts if p['list'] == lst and p['lang'] == lang]   # only articles in this language
        if not group:
            continue
        out += f'''<section class="section{' white' if lst == 'business' else ''} tight" id="{lst}">
<div class="wrap">
<div class="head"><div><p class="eb">{u[lst]}</p></div></div>
<div class="cards" style="--cols:3">
{chr(10).join(card(p, lang, base) for p in group)}
</div>
</div>
</section>
'''
    return out + FOOT.format(base=base)


def main():
    posts = parse()
    for p in posts:
        path = ROOT / ('it' if p['lang'] == 'it' else '') / f'blog-{p["slug"]}.html'
        path.write_text(article(p, posts), encoding='utf-8')
        print('wrote', path.relative_to(ROOT), f'({len(p["faq"])} FAQ, {p["minutes"]} min)')
    (ROOT / 'blog.html').write_text(index(posts, 'en'), encoding='utf-8')
    (ROOT / 'it' / 'blog.html').write_text(index(posts, 'it'), encoding='utf-8')
    print('wrote blog.html, it/blog.html')
    # for the MENU in assets/js/site.js
    print(json.dumps([[f'blog-{p["slug"]}.html', p['title'], p['lang'], p['list']] for p in posts], ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
