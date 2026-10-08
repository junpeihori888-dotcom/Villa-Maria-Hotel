#!/usr/bin/env python3
"""Build the marketing emails in /emails from the campaign PDFs.

Two lists, three emails each, in English and Italian:
  family:   1 Italian Memories (welcome, with the coupon) · 2 Family Discount · 3 Ciao Again
  business: 1 Business travel (welcome) · 2 Executive Business Stay · 3 The Padel Experience

The HTML is email-safe: tables, inline styles, 600px wide, no scripts.
Run:  python3 tools/emails.py
"""
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'emails')

# Before sending, set the live address of the site (ending in /) so images and links
# are absolute, e.g. 'https://www.example.com/'. Empty = relative links for the preview.
SITE_URL = ''
# Merge tags of your email tool. Brevo: '{{ contact.FIRSTNAME }}', Mailchimp: '*|FNAME|*'.
FIRST_NAME = '{{first_name}}'
UNSUBSCRIBE = '{{unsubscribe_url}}'
# Same values as NEWSLETTER in assets/js/site.js.
FAMILY_GIFT = '€50'
FAMILY_CODE = 'FAMILY50'

SAND, SAND2, WHITE, INK, MUTED, LINE = '#F4F1EA', '#EAE5DA', '#FFFFFF', '#2B2F33', '#596066', '#DAD4C8'
SLATE, SKY, SKY_SOFT, OLIVE = '#44555F', '#8BB2C9', '#C5DAE6', '#5D6B43'
SERIF = "'Cormorant Garamond',Georgia,'Times New Roman',serif"
SANS = "Manrope,'Helvetica Neue',Helvetica,Arial,sans-serif"

LANG = 'en'


def L(x):
    """Pick the language from an (en, it) pair; plain strings are the same in both."""
    if isinstance(x, tuple):
        return x[0] if LANG == 'en' else x[1]
    return x


def link(page, campaign, hash_=''):
    base = SITE_URL if SITE_URL else '../../'
    path = ('it/' if LANG == 'it' else '') + page
    sep = '&' if '?' in path else '?'
    return f'{base}{path}{sep}utm_source=newsletter&utm_medium=email&utm_campaign={campaign}{hash_}'


def img(name):
    return (SITE_URL if SITE_URL else '../../') + 'assets/img/' + name


def rich(x):
    """Text with *italic* parts, as in the designs ('Italian Memories *begin here.*')."""
    s = html.escape(L(x), quote=False)
    parts = s.split('*')
    return ''.join(f'<i style="font-style:italic;color:inherit">{p}</i>' if i % 2 else p for i, p in enumerate(parts))


def name_line(x):
    return rich(x).replace('{name}', FIRST_NAME)


# ---------- building blocks ----------

def eyebrow(x, color=OLIVE, center=False):
    return (f'<p style="margin:0 0 10px;font:700 11px/1.4 {SANS};letter-spacing:.2em;text-transform:uppercase;'
            f'color:{color};{"text-align:center;" if center else ""}">{rich(x)}</p>')


def h(x, size=30, color=INK, center=False):
    return (f'<h2 class="h" style="margin:0;font:400 {size}px/1.15 {SERIF};color:{color};'
            f'{"text-align:center;" if center else ""}">{rich(x)}</h2>')


def p(x, color=MUTED, center=False, size=15, top=10):
    return (f'<p style="margin:{top}px 0 0;font:400 {size}px/1.6 {SANS};color:{color};'
            f'{"text-align:center;" if center else ""}">{name_line(x)}</p>')


def button(label, href, kind='dark'):
    bg, fg, bd = {'dark': (SLATE, WHITE, SLATE), 'sky': (SKY, INK, SKY), 'light': (WHITE, INK, WHITE),
                  'ghost': (WHITE, INK, SLATE), 'ghost-dark': ('transparent', WHITE, WHITE)}[kind]
    return (f'<td style="padding:6px"><table role="presentation" cellpadding="0" cellspacing="0"><tr>'
            f'<td style="background:{bg};border:1px solid {bd}">'
            f'<a href="{href}" style="display:inline-block;padding:14px 22px;font:700 12px/1 {SANS};letter-spacing:.16em;'
            f'text-transform:uppercase;color:{fg};text-decoration:none">{html.escape(L(label))}</a></td></tr></table></td>')


def buttons(items, center=True):
    cells = ''.join(button(*b) for b in items)
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:20px {"auto" if center else "0"} 0">'
            f'<tr>{cells}</tr></table>')


def section(inner, bg=SAND, pad='40px 40px'):
    return (f'<tr><td class="px" style="background:{bg};padding:{pad}">{inner}</td></tr>')


def grid(items, color=INK, sub=MUTED, line=LINE, cols=2):
    """Items of (title, text) in two columns with a hairline on top, like the PDFs."""
    rows = ''
    w = 100 // cols
    for i in range(0, len(items), cols):
        cells = ''
        for t, s in items[i:i + cols]:
            cells += (f'<td class="col" width="{w}%" valign="top" style="padding:14px 12px 10px 0;border-top:1px solid {line}">'
                      f'<p style="margin:0;font:600 15px/1.35 {SANS};color:{color}">{rich(t)}</p>'
                      f'<p style="margin:4px 0 0;font:400 13px/1.5 {SANS};color:{sub}">{rich(s)}</p></td>')
        cells += '<td></td>' * (cols - len(items[i:i + cols]))
        rows += f'<tr>{cells}</tr>'
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:22px">{rows}</table>'


def photos(items, cols=3):
    """Items of (image, eyebrow, title). Stacks on phones."""
    rows = ''
    w = 100 // cols
    for i in range(0, len(items), cols):
        cells = ''
        for im, eb, t in items[i:i + cols]:
            cells += (f'<td class="col" width="{w}%" valign="top" style="padding:0 6px 18px">'
                      f'<img src="{img(im)}" width="100%" alt="{html.escape(L(t).replace("*", ""))}" '
                      f'style="display:block;width:100%;height:auto;border:0">'
                      + (f'<p style="margin:10px 0 0;font:700 10px/1.4 {SANS};letter-spacing:.18em;text-transform:uppercase;color:{OLIVE}">{rich(eb)}</p>' if eb else '')
                      + f'<p style="margin:4px 0 0;font:400 20px/1.2 {SERIF};color:{INK}">{rich(t)}</p></td>')
        rows += f'<tr>{cells}</tr>'
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:22px -6px 0">{rows}</table>'


REVIEWS = [
    (('“A place of peace and serenity. Thank you, Villa Maria, we’ll be back!”', '“Un luogo di pace e serenità. Grazie, Villa Maria, torneremo!”'),
     ('Google · July 2026 · translated', 'Google · luglio 2026')),
    (('“Everything excellent: friendly staff, a restorative spa, a wonderful restaurant.”', '“Tutto eccellente: personale cordiale, una spa rigenerante, un ristorante meraviglioso.”'),
     ('Google · 2026 · translated', 'Google · 2026')),
    (('“Courteous staff, a beautiful spa with superb treatments, and an excellent breakfast.”', '“Personale cortese, una bellissima spa con trattamenti superbi e un’ottima colazione.”'),
     ('Google · 2026 · translated', 'Google · 2026')),
]


def reviews(title):
    cells = ''.join(
        f'<td class="col" width="33%" valign="top" style="padding:14px 10px 0 0;border-top:1px solid {INK}">'
        f'<p style="margin:0;font:italic 400 18px/1.35 {SERIF};color:{INK}">{rich(q)}</p>'
        f'<p style="margin:10px 0 0;font:400 11px/1.4 {SANS};color:{MUTED}"><span style="color:{OLIVE}">★★★★★</span> {rich(c)}</p></td>'
        for q, c in REVIEWS)
    return section(eyebrow(title) + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:8px"><tr>{cells}</tr></table>', WHITE)


def header(right):
    return (f'<tr><td class="px" style="background:{SAND};padding:22px 40px">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
            f'<td style="font:400 24px/1 {SERIF};letter-spacing:.08em;color:{SLATE}">VILLA MARIA'
            f'<div style="font:600 9px/1.6 {SANS};letter-spacing:.2em;color:{MUTED};margin-top:4px">HOTEL &amp; SPA · ABRUZZO</div></td>'
            f'<td align="right" style="font:600 10px/1.4 {SANS};letter-spacing:.2em;text-transform:uppercase;color:{MUTED}">{rich(right)}</td>'
            f'</tr></table></td></tr>')


def hero(image, alt):
    return (f'<tr><td><img src="{img(image)}" width="600" alt="{html.escape(L(alt))}" '
            f'style="display:block;width:100%;max-width:600px;height:auto;border:0"></td></tr>')


def intro(eb, title, lead, btns, note=''):
    inner = (eyebrow(eb, MUTED, True) + h(title, 36, INK, True) + p(lead, MUTED, True, 15, 14) + buttons(btns)
             + (p(note, MUTED, True, 12, 16) if note else ''))
    return section(inner, SAND, '36px 40px 40px')


def cta(title, lead, btns, bg=INK):
    return section(h(title, 30, WHITE, True) + p(lead, '#D9DCDD', True) + buttons(btns), bg, '44px 40px')


def footer():
    return (f'<tr><td class="px" style="background:{SAND};padding:28px 40px 36px">'
            f'<p style="margin:0;font:italic 400 17px/1.4 {SERIF};color:{INK}">{rich(("Exceptional stays for a more meaningful tomorrow.", "Soggiorni eccezionali per un domani più significativo."))}</p>'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:8px"><tr>'
            f'<td style="font:400 11px/1.6 {SANS};color:{MUTED}">Villa Maria Hotel &amp; Spa · Contrada Pretaro, 66023 Francavilla al Mare (CH), Abruzzo · {L(("Italy", "Italia"))}<br>'
            f'{L(("You receive this email because you signed up on our website.", "Ricevi questa email perché ti sei iscritto sul nostro sito."))}</td>'
            f'<td align="right" valign="top" style="font:400 11px/1.6 {SANS}"><a href="{UNSUBSCRIBE}" style="color:{SLATE}">{L(("Unsubscribe", "Annulla l’iscrizione"))}</a></td>'
            f'</tr></table></td></tr>')


def page(subject, preheader, rows):
    return f'''<!DOCTYPE html>
<html lang="{LANG}" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>{html.escape(L(subject))}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;1,400&amp;family=Manrope:wght@400;600;700&amp;display=swap" rel="stylesheet">
<style>
  body{{margin:0;padding:0;background:{SAND2}}}
  a{{color:{SLATE}}}
  @media (max-width:620px){{
    .px{{padding-left:20px!important;padding-right:20px!important}}
    .col{{display:block!important;width:100%!important;box-sizing:border-box}}
    .h{{font-size:28px!important}}
  }}
</style>
</head>
<body style="margin:0;padding:0;background:{SAND2}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">{html.escape(L(preheader))}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{SAND2}">
<tr><td align="center" style="padding:24px 8px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:{SAND}">
{"".join(rows)}
</table>
</td></tr>
</table>
</body>
</html>
'''


# ---------- the six emails ----------

def family_1():
    c = 'family-1-italian-memories'
    rows = [
        header(('Francavilla al Mare', 'Francavilla al Mare')),
        hero('pool-fountain.jpg', ('The pool and fountain in the hotel park', 'La piscina con la fontana nel parco dell’hotel')),
        intro(('Family hotel & spa in Abruzzo', 'Hotel & spa per famiglie in Abruzzo'),
              ('Italian Memories *begin here.*', 'I ricordi italiani *iniziano qui.*'),
              ('Hi {name}, a four-star seaside hotel & spa in Francavilla al Mare, made for rest and time together.',
               'Ciao {name}, un hotel & spa quattro stelle sul mare a Francavilla al Mare, pensato per il relax e per il tempo trascorso insieme.'),
              [(('Discover Italian Memories →', 'Scopri i ricordi italiani →'), link('italian-memories.html', c), 'dark'),
               (('Chat with us', 'Scrivici in chat'), link('contact.html', c, '#help'), 'ghost')],
              ('★★★★★ Loved by families · Verified reviews on Google, Booking.com & TripAdvisor',
               '★★★★★ Amato dalle famiglie · Recensioni verificate su Google, Booking.com e TripAdvisor')),
    ]
    if FAMILY_GIFT:
        rows.append(section(
            eyebrow(('Your welcome gift', 'Il tuo regalo di benvenuto'), OLIVE, True) +
            f'<p style="margin:0;text-align:center;font:400 64px/1 {SERIF};color:{OLIVE}">{FAMILY_GIFT}</p>' +
            p((f'Thank you for joining our family list. Here is {FAMILY_GIFT} off your next stay: add the code when you book.',
               f'Grazie per esserti iscritto alla lista famiglie. Ecco {FAMILY_GIFT} di sconto sul prossimo soggiorno: inserisci il codice quando prenoti.'), MUTED, True) +
            f'<p style="margin:16px auto 0;max-width:260px;border:1px dashed {OLIVE};background:{SAND};padding:14px;text-align:center;font:700 22px/1 {SANS};letter-spacing:.24em;color:{OLIVE}">{FAMILY_CODE}</p>' +
            buttons([(('Book with my coupon →', 'Prenota con il buono →'), link(f'booking.html?code={FAMILY_CODE}', c, '#family-discount'), 'sky')]),
            WHITE))
    rows += [
        section(eyebrow(('Why families come to us', 'Perché le famiglie scelgono noi')) +
                h(('Quality time has become *a luxury.*', 'Il tempo di qualità è diventato *un lusso.*')) +
                grid([(('Calendars that never align', 'Agende che non coincidono mai'), ('Work, school and sport pull you apart.', 'Lavoro, scuola e sport vi tengono lontani.')),
                      (('Screens at every table', 'Schermi a ogni tavola'), ('Together, but somewhere else.', 'Insieme, ma altrove.')),
                      (('Conversations that stay short', 'Conversazioni che restano brevi'), ('Check-ins replace real talks.', 'I messaggi di controllo sostituiscono le vere chiacchierate.')),
                      (('Holidays that feel like work', 'Vacanze che sembrano un lavoro'), ('Hours of planning, still the worry.', 'Ore di organizzazione, e la preoccupazione resta.'))])),
        section(eyebrow(('The Villa Maria difference', 'La differenza Villa Maria'), SKY_SOFT) +
                h(('More than a holiday. *A chance to reconnect.*', 'Più di una vacanza. *L’occasione di ritrovarsi.*'), 30, WHITE) +
                p(('We take care of the details, so you can take care of each other.', 'Pensiamo noi ai dettagli, così potete prendervi cura gli uni degli altri.'), '#D9DCDD') +
                grid([(('Effortless planning', 'Organizzazione senza pensieri'), ('Tell us who’s coming.', 'Dicci chi viene.')),
                      (('Made for families', 'Pensato per le famiglie'), ('Moments to share.', 'Momenti da condividere.')),
                      (('Real rest for parents', 'Vero riposo per i genitori'), ('Two pools in a private park.', 'Due piscine in un parco privato.')),
                      (('Freedom for teens', 'Libertà per i ragazzi'), ('Padel, pools, beach shuttle.', 'Padel, piscine, navetta per la spiaggia.')),
                      (('Long family dinners', 'Lunghe cene in famiglia'), ('Hotel restaurant, Abruzzo recipes.', 'Ristorante dell’hotel, ricette abruzzesi.')),
                      (('Linfa wellness & spa', 'Benessere e spa Linfa'), ('Rituals for one or two.', 'Rituali per uno o per due.'))],
                     WHITE, '#C9CED1', 'rgba(255,255,255,.25)'), SLATE),
        section(eyebrow(('Create memories together', 'Crea ricordi insieme')) +
                h(('The moments your family *will talk about for years.*', 'I momenti di cui la tua famiglia *parlerà per anni.*')) +
                photos([('people/moment-pool.jpg', ('Pool & park days', 'Giornate tra piscina e parco'), ('The day no one checked the time', 'Il giorno in cui nessuno guardò l’ora')),
                        ('restaurant-dinner.jpg', ('Hotel restaurant', 'Ristorante dell’hotel'), ('Dinners that last until the stars', 'Cene che durano fino alle stelle')),
                        ('wellness.jpg', ('Spa moments', 'Momenti in spa'), ('An afternoon to exhale', 'Un pomeriggio per respirare'))]), WHITE),
        section(eyebrow(('Something for every generation', 'Qualcosa per ogni generazione'), SLATE, True) +
                h(('Everyone gets *the holiday they hoped for.*', 'Ognuno ha *la vacanza che sperava.*'), 28, INK, True) +
                grid([(('For parents', 'Per i genitori'), ('Long mornings, spa afternoons.', 'Mattine lente, pomeriggi in spa.')),
                      (('For teenagers', 'Per i ragazzi'), ('Pools, padel, beach days.', 'Piscine, padel, giornate in spiaggia.')),
                      (('Together', 'Insieme'), ('Evenings sharing it all.', 'Serate in cui si condivide tutto.'))], INK, '#3D4A52', 'rgba(43,47,51,.25)', 3), SKY),
        reviews(('In their own words', 'Con le loro parole')),
        cta(('Your next family memory *starts here.*', 'Il prossimo ricordo della tua famiglia *inizia qui.*'),
            ('Discover why families return to our seaside hotel in Abruzzo.', 'Scopri perché le famiglie tornano nel nostro hotel sul mare in Abruzzo.'),
            [(('Explore family experiences →', 'Scopri le esperienze per famiglie →'), link('italian-memories.html', c), 'light'),
             (('Chat with us', 'Scrivici in chat'), link('contact.html', c, '#help'), 'ghost-dark')]),
        footer()]
    return c, (('Italian Memories begin here', 'I ricordi italiani iniziano qui') if not FAMILY_GIFT else
               (f'Your {FAMILY_GIFT} welcome gift, and Italian Memories', f'Il tuo regalo di benvenuto da {FAMILY_GIFT}, e i ricordi italiani')), \
        ('A four-star seaside hotel & spa, made for rest and time together.', 'Un hotel & spa quattro stelle sul mare, pensato per stare insieme.'), rows


def family_2():
    c = 'family-2-family-discount'
    rows = [
        header(('Family Discount', 'Sconto Famiglia')),
        hero('suite-terrace.jpg', ('Suite terrace with hot tub and sea view', 'Terrazza della suite con vasca idromassaggio e vista mare')),
        intro(('Family Discount · 4-star hotel & spa', 'Sconto Famiglia · Hotel & spa 4 stelle'),
              ('Create unforgettable *Italian family memories.*', 'Crea ricordi di famiglia *indimenticabili in Italia.*'),
              ('Hi {name}, time together by the sea, with our exclusive Family Discount package.',
               'Ciao {name}, tempo insieme in riva al mare con il nostro esclusivo pacchetto Sconto Famiglia.'),
              [(('Book now →', 'Prenota ora →'), link('booking.html', c, '#family-discount'), 'dark'),
               (('Check availability', 'Verifica la disponibilità'), link('booking.html', c, '#family-discount'), 'ghost')],
              ('★★★★★ Loved by families · Verified reviews on Google, Booking.com & TripAdvisor',
               '★★★★★ Amato dalle famiglie · Recensioni verificate su Google, Booking.com e TripAdvisor')),
        section(eyebrow(('Exclusive offer', 'Offerta esclusiva'), SKY_SOFT, True) +
                h(('Your *family rate*', 'La tariffa *per la tua famiglia*'), 34, WHITE, True) +
                p(('Room, breakfast and spa included, for families who book direct.', 'Camera, colazione e spa inclusi, per le famiglie che prenotano direttamente.'), '#D9DCDD', True) +
                eyebrow(('Limited availability', 'Disponibilità limitata'), SKY_SOFT, True).replace('margin:0 0 10px', 'margin:16px 0 0'), SLATE),
        section(eyebrow(('What’s included', 'Cosa è incluso')) +
                h(('Your family package, *at a glance.*', 'Il tuo pacchetto famiglia, *in breve.*')) +
                grid([(('Family rooms & suites', 'Camere e suite famiglia'), ('For 2 adults and 2 teens', 'Per 2 adulti e 2 ragazzi')),
                      (('Breakfast included', 'Colazione inclusa'), ('Local buffet', 'Buffet locale')),
                      (('Spa included', 'Spa inclusa'), ('Linfa wellness centre', 'Centro benessere Linfa')),
                      (('Family activities', 'Attività per famiglie'), ('Kids Club, pools, padel', 'Kids Club, piscine, padel')),
                      (('Beach access', 'Accesso alla spiaggia'), ('Free shuttle to partner beach', 'Navetta gratuita per la spiaggia convenzionata')),
                      (('Hotel restaurant', 'Ristorante dell’hotel'), ('Abruzzo recipes', 'Ricette abruzzesi')),
                      (('Family benefits', 'Vantaggi per le famiglie'), ('Extras for direct bookings', 'Extra per le prenotazioni dirette')),
                      (('Free parking', 'Parcheggio gratuito'), ('With EV charging', 'Con ricarica per auto elettriche'))])),
        section(eyebrow(('Why book direct', 'Perché prenotare direttamente'), OLIVE, True) +
                h(('Book with us, *and it pays.*', 'Prenota con noi, *e conviene.*'), 30, INK, True) +
                f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:22px"><tr>' +
                ''.join(f'<td class="col" width="50%" valign="top" style="padding:0 6px 12px"><div style="border:1px solid {LINE};background:{SAND};padding:22px">'
                        f'<p style="margin:0;font:700 10px/1.4 {SANS};letter-spacing:.18em;text-transform:uppercase;color:{OLIVE}">{rich(e)}</p>'
                        f'<p style="margin:8px 0 0;font:400 52px/1 {SERIF};color:{SLATE}">{big}</p>'
                        f'<p style="margin:4px 0 0;font:600 14px/1.4 {SANS};color:{INK}">{rich(sub)}</p>'
                        f'<p style="margin:8px 0 0;font:400 13px/1.5 {SANS};color:{MUTED}">{rich(txt)}</p></div></td>'
                        for e, big, sub, txt in [
                            (('First direct booking', 'Prima prenotazione diretta'), '€20', ('in-house voucher', 'voucher da spendere in hotel'),
                             ('For food and drink or the spa, for first-time guests booking directly. Valid for your first stay; it expires at check-out.',
                              'Per food and beverage o la spa, per chi prenota direttamente per la prima volta. Valido per il primo soggiorno; scade al check-out.')),
                            (('Your next stay', 'Il tuo prossimo soggiorno'), '10%', ('off the room rate', 'sulla tariffa della camera'),
                             ('Book your next stay at the hotel during your visit. Free cancellation up to 6 months before arrival; dates can change up to 6 weeks before.',
                              'Prenota il prossimo soggiorno in hotel durante la visita. Cancellazione gratuita fino a 6 mesi prima; date modificabili fino a 6 settimane prima.'))]) +
                '</tr></table>', WHITE),
        section(eyebrow(('The perfect family day', 'La giornata perfetta in famiglia')) +
                h(('One day, *three moments.*', 'Un giorno, *tre momenti.*')) +
                photos([('breakfast.jpg', ('Morning', 'Mattina'), ('Breakfast, then the water', 'Colazione, poi l’acqua')),
                        ('pool-park.jpg', ('Afternoon · Kids Club', 'Pomeriggio · Kids Club'), ('Everyone at their own pace', 'Ognuno con i suoi tempi')),
                        ('restaurant-dinner.jpg', ('Evening', 'Sera'), ('Dinner that lasts', 'Una cena che dura'))])),
        reviews(('Families trust us', 'Le famiglie si fidano di noi')),
        cta(('Your family’s next memory *starts here.*', 'Il prossimo ricordo della tua famiglia *inizia qui.*'),
            ('Book direct and enjoy the Family Discount on Italy’s Adriatic coast.', 'Prenota direttamente e goditi lo Sconto Famiglia sulla costa adriatica italiana.'),
            [(('Book now →', 'Prenota ora →'), link('booking.html', c, '#family-discount'), 'light'),
             (('See the package', 'Vedi il pacchetto'), link('family-reset-package.html', c), 'ghost-dark')]),
        footer()]
    return c, ('Your family rate: room, breakfast and spa included', 'La tariffa per la tua famiglia: camera, colazione e spa inclusi'), \
        ('The Family Discount, for families who book direct.', 'Lo Sconto Famiglia, per chi prenota direttamente.'), rows


def family_3():
    c = 'family-3-ciao-again'
    def polaroids(items):
        rows = ''
        for i in range(0, len(items), 2):
            rows += '<tr>' + ''.join(
                f'<td class="col" width="50%" valign="top" style="padding:0 8px 16px"><div style="background:{WHITE};padding:10px 10px 14px;box-shadow:0 6px 18px rgba(0,0,0,.12)">'
                f'<img src="{img(im)}" width="100%" alt="" style="display:block;width:100%;height:auto;border:0">'
                f'<p style="margin:10px 0 0;font:400 19px/1.2 {SERIF};color:{INK}">{rich(t)}</p>'
                f'<p style="margin:4px 0 0;font:700 10px/1.4 {SANS};letter-spacing:.18em;text-transform:uppercase;color:{MUTED}">{rich(eb)}</p></div></td>'
                for im, t, eb in items[i:i + 2]) + '</tr>'
        return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:22px">{rows}</table>'
    rows = [
        header(('For our returning guests', 'Per i nostri ospiti abituali')),
        hero('pool-park.jpg', ('The Blue Pool in the hotel park', 'La Blue Pool nel parco dell’hotel')),
        intro(('A note for our returning guests', 'Un pensiero per i nostri ospiti abituali'),
              ('Ciao again. *Your Italian story continues.*', 'Ciao di nuovo. *La tua storia italiana continua.*'),
              ('Hi {name}, some holidays end. The best stories continue.', 'Ciao {name}, alcune vacanze finiscono. Le storie più belle continuano.'),
              [(('Continue your story →', 'Continua la tua storia →'), link('booking.html', c, '#returning'), 'dark'),
               (('Relive your memories', 'Rivivi i tuoi ricordi'), link('ciao-again.html', c), 'ghost')]),
        section(eyebrow(('A look back', 'Uno sguardo indietro'), MUTED, True) +
                h(('Do you remember *these moments?*', 'Ti ricordi *questi momenti?*'), 30, INK, True) +
                p(('The long dinner where nobody reached for a phone. Take a moment and go back.',
                   'La lunga cena in cui nessuno ha preso in mano il telefono. Fermati un attimo e torna indietro.'), MUTED, True) +
                polaroids([('restaurant-dinner.jpg', ('The dinner that ran late', 'La cena che è andata per le lunghe'), ('Family table', 'Tavolo di famiglia')),
                           ('breakfast.jpg', ('Mornings with nowhere to be', 'Mattine senza nessun impegno'), ('Slow breakfasts', 'Colazioni lente')),
                           ('wellness.jpg', ('The hour you finally exhaled', 'L’ora in cui hai finalmente respirato'), ('Linfa spa', 'Spa Linfa')),
                           ('pool-fountain.jpg', ('Splashes and laughter', 'Schizzi e risate'), ('Summer days', 'Giornate d’estate'))])),
        section(eyebrow(('Memories that last', 'Ricordi che durano'), SKY_SOFT) +
                h(('The best souvenirs *are the moments we share.*', 'I souvenir più belli *sono i momenti che condividiamo.*'), 30, WHITE) +
                grid([(('Family connection', 'Legami di famiglia'), ('Really talking, at last.', 'Parlarsi davvero, finalmente.')),
                      (('Quality time', 'Tempo di qualità'), ('Hours that were only yours.', 'Ore che erano solo vostre.')),
                      (('Shared experiences', 'Esperienze condivise'), ('Remembered by all of you.', 'Ricordate da tutti voi.')),
                      (('Personal stories', 'Storie personali'), ('Jokes only your family gets.', 'Battute che capisce solo la vostra famiglia.'))],
                     WHITE, '#C9CED1', 'rgba(255,255,255,.25)'), SLATE),
        section(eyebrow(('What’s new at Villa Maria', 'Novità a Villa Maria')) +
                h(('There’s more *waiting for you.*', 'C’è ancora di più *ad aspettarti.*')) +
                photos([('spa-whirlpool.jpg', ('Wellness', 'Benessere'), ('A new ritual to try', 'Un nuovo rituale da provare')),
                        ('restaurant-hall.jpg', ('Flavours', 'Sapori'), ('La Bottega di Villa Maria', 'La Bottega di Villa Maria')),
                        ('gardens.jpg', ('Seasons', 'Stagioni'), ('Every season feels new here', 'Qui ogni stagione ha qualcosa di nuovo'))]) +
                buttons([(('Discover what’s new →', 'Scopri le novità →'), link('activities.html', c), 'ghost')], False), WHITE),
        section(eyebrow(('Share your story', 'Condividi la tua storia'), SLATE, True) +
                h(('Your experience *inspires others.*', 'La tua esperienza *ispira gli altri.*'), 28, INK, True) +
                p(('A few lines or one photo help another family choose. Tag us with #CiaoAgain.',
                   'Poche righe o una foto aiutano un’altra famiglia a scegliere. Taggaci con #CiaoAgain.'), '#3D4A52', True) +
                buttons([(('Share your experience', 'Condividi la tua esperienza'), link('ciao-again.html', c, '#review'), 'dark'),
                         (('Inspire a family', 'Ispira una famiglia'), link('italian-memories.html', c), 'light')]), SKY),
        section(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
                f'<td class="col" width="42%" valign="top" style="padding:0 18px 12px 0"><img src="{img("people/family-welcome-back.jpg")}" width="100%" alt="" style="display:block;width:100%;height:auto;border:0"></td>'
                f'<td class="col" valign="top">' +
                eyebrow(('Join the Villa Maria family', 'Entra nella famiglia Villa Maria'), SKY_SOFT) +
                h(('Stay connected *to the place you love.*', 'Resta in contatto *con il luogo che ami.*'), 26, WHITE) +
                grid([(('Loyalty programme', 'Programma fedeltà'), ('A thank-you for returning families.', 'Un grazie alle famiglie che tornano.')),
                      (('Exclusive moments', 'Momenti esclusivi'), ('Kept for returning guests.', 'Riservati agli ospiti abituali.'))],
                     WHITE, '#C9CED1', 'rgba(255,255,255,.25)', 1) +
                buttons([(('Join our family community →', 'Unisciti alla nostra community →'), link('ciao-again.html', c, '#join'), 'sky')], False) +
                '</td></tr></table>', INK),
        reviews(('Guest stories', 'Storie dei nostri ospiti')),
        cta(('The next chapter *is waiting.*', 'Il prossimo capitolo *ti aspetta.*'),
            ('Plan your next family stay at Villa Maria.', 'Pianifica il tuo prossimo soggiorno in famiglia a Villa Maria.'),
            [(('Explore your next chapter →', 'Scopri il tuo prossimo capitolo →'), link('booking.html', c, '#returning'), 'sky'),
             (('Stay connected', 'Resta in contatto'), link('ciao-again.html', c), 'ghost-dark')], SLATE),
        footer()]
    return c, ('Ciao again. Your Italian story continues.', 'Ciao di nuovo. La tua storia italiana continua.'), \
        ('Some holidays end. The best stories continue.', 'Alcune vacanze finiscono. Le storie più belle continuano.'), rows


def business_1():
    c = 'business-1-business-travel'
    rows = [
        header(('Francavilla al Mare', 'Francavilla al Mare')),
        hero('people/business-meeting.jpg', ('A business meeting at Villa Maria', 'Una riunione di lavoro a Villa Maria')),
        intro(('Business travel · Francavilla al Mare · Pescara', 'Viaggi di lavoro · Francavilla al Mare · Pescara'),
              ('Take the pressure out of *business travel.*', 'Viaggiare per lavoro, *senza pressione.*'),
              ('Hi {name}, a four-star hotel & spa above the Adriatic, minutes from Pescara, where meetings, recovery and a proper dinner are already arranged, so your only job is the one you came for.',
               'Ciao {name}, un hotel & spa quattro stelle sull’Adriatico, a pochi minuti da Pescara, dove riunioni, relax e una buona cena sono già organizzati, così pensi solo al lavoro per cui sei venuto.'),
              [(('Discover the Executive Experience →', 'Scopri l’Executive Experience →'), link('business-travel.html', c), 'dark')]),
        section(grid([(('Pescara Airport', 'Aeroporto di Pescara'), ('A short drive away', 'A pochi minuti d’auto')),
                      ('Pescara Centrale', ('Easy rail connections', 'Comodi collegamenti ferroviari')),
                      (('A14 motorway', 'Autostrada A14'), ('Near the Pescara Sud exit', 'Vicino all’uscita Pescara Sud')),
                      (('Sea view', 'Vista mare'), ('Quiet, outside the city', 'Tranquillo, fuori città'))],
                     WHITE, '#C9CED1', 'rgba(255,255,255,.25)', 4).replace('margin-top:22px', 'margin-top:0'), SLATE, '24px 40px'),
        section(h(('A destination that *moves business forward.*', 'Una destinazione che *fa avanzare il business.*'), 30, INK, True) +
                photos([('auditorium.jpg', ('Work', 'Lavoro'), ('Private rooms to an auditorium', 'Dalle sale riservate all’auditorium')),
                        ('restaurant-hall.jpg', ('Connect', 'Relazioni'), ('Dinners that close the deal', 'Cene di lavoro che chiudono l’accordo')),
                        ('spa-whirlpool.jpg', ('Recharge', 'Benessere'), ('Spa, sauna and massage', 'Spa, sauna e massaggi'))]) +
                grid([(('Early breakfast', 'Colazione anticipata'), ('Before your first call', 'Prima della prima call')),
                      (('Express check-out', 'Check-out rapido'), ('Your flight stays on time', 'Il volo resta in orario')),
                      (('A real desk', 'Una vera scrivania'), ('Power by the bed', 'Prese vicino al letto')),
                      (('Private parking', 'Parcheggio privato'), ('On site', 'In hotel'))], cols=4), WHITE),
        section(eyebrow(('For business guests', 'Per chi viaggia per lavoro'), OLIVE, True) +
                h(('Executive Business *Stay Package*', 'Pacchetto Executive *Business Stay*'), 30, INK, True) +
                p(('Planning regular trips to Abruzzo? Ask us about the Executive Business Stay Package and the company rates we offer to business travellers.',
                   'Viaggi spesso in Abruzzo? Chiedici dell’Executive Business Stay Package e delle tariffe aziendali che riserviamo a chi viaggia per lavoro.'), MUTED, True) +
                buttons([(('Ask about company rates', 'Chiedi delle tariffe aziendali'), link('business-travel.html', c, '#message'), 'ghost')])),
        cta(('Your next trip to Abruzzo *can feel lighter.*', 'La tua prossima trasferta in Abruzzo *può essere più leggera.*'),
            ('Ask us anything, from meeting-room capacity to the quietest room in the house.', 'Chiedici qualsiasi cosa, dalla capienza delle sale alla camera più silenziosa.'),
            [(('Discover the Executive Experience →', 'Scopri l’Executive Experience →'), link('executive-business-stay.html', c), 'sky')], SLATE),
        footer()]
    return c, ('Take the pressure out of business travel', 'Viaggiare per lavoro, senza pressione'), \
        ('Meetings, recovery and dinner in one four-star address by the sea.', 'Riunioni, relax e cena in un solo indirizzo quattro stelle sul mare.'), rows


def business_2():
    c = 'business-2-executive-business-stay'
    rows = [
        header(('Executive Business Stay', 'Executive Business Stay')),
        hero('dining.jpg', ('The restaurant above the garden', 'Il ristorante sul giardino')),
        intro(('Executive Business Stay Package', 'Pacchetto Executive Business Stay'),
              ('Your business stay, *already arranged.*', 'Il tuo soggiorno di lavoro, *già organizzato.*'),
              ('Hi {name}, one package, one address above the Adriatic: a quiet room to work in, breakfast before your first call, the spa after your last, and a team that handles the rest.',
               'Ciao {name}, un pacchetto, un indirizzo sull’Adriatico: una camera silenziosa per lavorare, la colazione prima della prima call, la spa dopo l’ultima, e un team che pensa al resto.'),
              [(('Book now →', 'Prenota ora →'), link('booking.html', c, '#executive'), 'dark')],
              ('Secure booking direct with Villa Maria · Company invoicing available', 'Prenotazione diretta e sicura con Villa Maria · Fatturazione aziendale disponibile')),
        section(eyebrow(('What’s included', 'Cosa è incluso'), OLIVE, True) +
                h(('Everything a working trip needs, *in one package.*', 'Tutto ciò che serve a una trasferta, *in un solo pacchetto.*'), 28, INK, True) +
                grid([(('Superior or Deluxe room', 'Camera Superior o Deluxe'), ('Quiet, with a writing desk', 'Silenziosa, con scrivania')),
                      (('Daily breakfast', 'Colazione inclusa'), ('Served early, before your first call', 'Servita presto, prima della prima call')),
                      (('High-speed Wi-Fi', 'Wi-Fi ad alta velocità'), ('Ready for video calls', 'Pronto per le videochiamate')),
                      (('Spa & sauna access', 'Accesso a spa e sauna'), ('Recover after the last meeting', 'Per rigenerarti dopo l’ultima riunione')),
                      (('Padel, pool & gym', 'Padel, piscina e palestra'), ('Train without leaving the hotel', 'Allenati senza uscire dall’hotel')),
                      (('Meeting room on request', 'Sala riunioni su richiesta'), ('Private, with video-conferencing', 'Riservata, con videoconferenza')),
                      (('Express check-out', 'Check-out rapido'), ('Your morning flight stays on time', 'Il volo del mattino resta in orario')),
                      (('Private parking', 'Parcheggio privato'), ('Close to the A14 Pescara Sud exit', 'Vicino all’uscita A14 Pescara Sud'))]) +
                photos([('breakfast.jpg', ('Early breakfast', 'Colazione anticipata'), ''),
                        ('meeting-hall.jpg', ('Meeting room', 'Sala riunioni'), ''),
                        ('spa-whirlpool.jpg', ('Spa & sauna', 'Spa e sauna'), '')]), WHITE),
        section(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
                f'<td class="col" width="42%" valign="top" style="padding:0 20px 12px 0"><img src="{img("reception.jpg")}" width="100%" alt="" style="display:block;width:100%;height:auto;border:0"></td>'
                f'<td class="col" valign="top">' + eyebrow(('Why book direct', 'Perché prenotare direttamente'), SLATE) +
                h(('Booked with us, *handled by us.*', 'Prenotato con noi, *seguito da noi.*'), 26) +
                grid([(('A direct line to our team', 'Un contatto diretto con il nostro team'), ('Room preferences arranged before you arrive', 'Preferenze di camera pronte prima del tuo arrivo')),
                      (('Company invoicing', 'Fatturazione aziendale'), ('Billing to your company, corporate cards welcome', 'Fattura alla tua azienda, carte aziendali accettate')),
                      (('Corporate & group stays', 'Soggiorni aziendali e di gruppo'), ('Have a company code? Add it when you book.', 'Hai un codice aziendale? Inseriscilo al momento della prenotazione.'))],
                     INK, '#3D4A52', 'rgba(43,47,51,.25)', 1) + '</td></tr></table>', SKY),
        section(eyebrow(('Choose your room', 'Scegli la tua camera'), MUTED, True) +
                h(('One package, *two ways to stay.*', 'Un pacchetto, *due modi di soggiornare.*'), 30, INK, True) +
                '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:22px"><tr>' +
                ''.join(f'<td class="col" width="50%" valign="top" style="padding:0 6px 12px"><div style="background:{WHITE};border:1px solid {LINE}">'
                        f'<img src="{img(im)}" width="100%" alt="" style="display:block;width:100%;height:auto;border:0"><div style="padding:18px 18px 22px;text-align:center">'
                        f'<p style="margin:0;font:700 10px/1.4 {SANS};letter-spacing:.18em;text-transform:uppercase;color:{MUTED}">{rich(eb)}</p>'
                        f'<p style="margin:6px 0 0;font:400 24px/1.2 {SERIF};color:{INK}">{rich(t)}</p>'
                        f'<p style="margin:6px 0 0;font:400 13px/1.5 {SANS};color:{MUTED}">{rich(s)}</p>'
                        + buttons([(('Book now', 'Prenota ora'), link('booking.html', c, hs), 'dark')]) + '</div></div></td>'
                        for im, eb, t, s, hs in [
                            ('superior-room.jpg', ('For the short trip', 'Per il viaggio breve'), ('Superior Room', 'Camera Superior'),
                             ('Garden or partial sea view, writing desk. Ideal for 1 to 2 nights.', 'Vista giardino o parziale vista mare, scrivania. Ideale per 1–2 notti.'), '#superior'),
                            ('deluxe-room.jpg', ('For the longer stay', 'Per il soggiorno più lungo'), ('Deluxe Room & Suites', 'Camere Deluxe e Suite'),
                             ('More space, Adriatic views, desk and lounge area. For 3+ nights.', 'Più spazio, vista Adriatico, scrivania e zona lounge. Per 3+ notti.'), '#deluxe')]) +
                '</tr></table>'),
        cta(('Your next trip to Abruzzo, *booked in a minute.*', 'La tua prossima trasferta in Abruzzo, *prenotata in un minuto.*'),
            ('Executive Business Stay Package · Villa Maria Hotel & Spa, Francavilla al Mare', 'Pacchetto Executive Business Stay · Villa Maria Hotel & Spa, Francavilla al Mare'),
            [(('Book now →', 'Prenota ora →'), link('booking.html', c, '#executive'), 'light'),
             (('Questions first? Chat with us', 'Prima qualche domanda? Chatta con noi'), link('contact.html', c, '#help'), 'ghost-dark')], SLATE),
        footer()]
    return c, ('Your business stay, already arranged', 'Il tuo soggiorno di lavoro, già organizzato'), \
        ('Room, breakfast, spa and meeting space in one package.', 'Camera, colazione, spa e sale meeting in un solo pacchetto.'), rows


def business_3():
    c = 'business-3-padel-experience'
    rows = [
        header(('For our returning guests', 'Per i nostri ospiti abituali')),
        hero('garden-gazebo.jpg', ('The gardens of Villa Maria', 'I giardini di Villa Maria')),
        intro(('The Padel Experience · Villa Maria', 'La Padel Experience · Villa Maria'),
              ('Some of the best business relationships continue *beyond the meeting room.*', 'Alcune delle migliori relazioni di lavoro continuano *oltre la sala riunioni.*'),
              ('Welcome back, {name}. You already know the quiet rooms, the spa and the table by the garden. Next time, bring a racket, and the client, the colleague or the team you want to know better.',
               'Bentornato, {name}. Conosci già le camere silenziose, la spa e il tavolo sul giardino. La prossima volta porta una racchetta, e il cliente, il collega o il team che vuoi conoscere meglio.'),
              [(('Explore the Padel Experience →', 'Scopri la Padel Experience →'), link('padel-experience.html', c), 'dark'),
               (('Refer a colleague', 'Consiglia un collega'), link('padel-experience.html', c, '#refer'), 'ghost')]),
        section(eyebrow(('Why padel, why here', 'Perché il padel, perché qui'), MUTED, True) +
                h(('Four players, one court, *no agenda.*', 'Quattro giocatori, un campo, *nessuna agenda.*'), 30, INK, True) +
                p(('Padel is played in doubles, easy to learn and impossible to play in silence, which is exactly why it works.',
                   'Il padel si gioca in doppio, si impara in fretta ed è impossibile giocarlo in silenzio, ed è proprio per questo che funziona.'), MUTED, True) +
                grid([(('01 · Networking', '01 · Networking'), ('A match says more than a pitch deck. Invite a client, close the day as partners.', 'Una partita dice più di una presentazione. Invita un cliente, chiudete la giornata da partner.')),
                      (('02 · Wellness', '02 · Benessere'), ('An hour of movement between meetings, then sauna and massage to recover.', 'Un’ora di movimento tra una riunione e l’altra, poi sauna e massaggio per recuperare.')),
                      (('03 · Social', '03 · Socialità'), ('Doubles by design. Meet other guests, play with your team, laugh a little.', 'Si gioca in doppio. Conosci altri ospiti, gioca con il tuo team, sorridi un po’.')),
                      (('04 · A reason to return', '04 · Un motivo per tornare'), ('Courts in the gardens above the Adriatic, a rematch is always waiting.', 'Campi nei giardini sopra l’Adriatico, la rivincita ti aspetta sempre.'))]), WHITE),
        section(eyebrow(('The Villa Maria padel ritual', 'Il rituale padel di Villa Maria'), MUTED, True) +
                h(('Play. Recover. Toast. *Dine.*', 'Gioca. Recupera. Brinda. *Cena.*'), 30, INK, True) +
                p(('The match is only the beginning. The rest of the evening is already waiting.', 'La partita è solo l’inizio. Il resto della serata ti sta già aspettando.'), MUTED, True) +
                photos([('people/business-padel.jpg', '18:00', ('The match', 'La partita')),
                        ('spa-whirlpool.jpg', '19:15', ('Recovery', 'Recupero')),
                        ('bar.jpg', '20:15', ('The toast', 'Il brindisi')),
                        ('chef-dinner.jpg', '21:00', ('The dinner', 'La cena'))], 2)),
        section(eyebrow(('Welcome back, every time', 'Bentornato, ogni volta'), SLATE, True) +
                h(('Your preferred business destination *awaits.*', 'La tua destinazione business preferita *ti aspetta.*'), 28, INK, True) +
                grid([(('Your room, the way you like it', 'La tua camera, come piace a te'), ('Share your preferences once and we’ll keep them for your next stay.', 'Indicaci le tue preferenze una volta e le terremo pronte per il prossimo soggiorno.')),
                      (('Regular trips, made simple', 'Trasferte ricorrenti, più semplici'), ('Coming back every month? Talk to us about recurring stays.', 'Torni ogni mese? Parliamo di soggiorni ricorrenti.')),
                      (('Next time, with the family', 'La prossima volta, con la famiglia'), ('Pools, gardens and a kids’ club: the same hotel at a weekend pace.', 'Piscine, giardini e un kids’ club: lo stesso hotel, al ritmo del weekend.')),
                      (('Stay in the loop', 'Resta aggiornato'), ('Padel evenings, chef’s dinners and spa news, straight to your inbox.', 'Serate di padel, cene dello chef e novità della spa, direttamente via email.'))],
                     INK, '#3D4A52', 'rgba(43,47,51,.25)'), SKY),
        section(eyebrow(('Refer a colleague', 'Consiglia un collega'), SKY_SOFT, True) +
                h(('Good places are *meant to be shared.*', 'I bei posti sono fatti *per essere condivisi.*'), 30, WHITE, True) +
                p(('Know someone who travels to Abruzzo for work, and would play a better game here? Introduce them to Villa Maria. We’ll take care of them the way we take care of you.',
                   'Conosci qualcuno che viaggia in Abruzzo per lavoro, e che qui giocherebbe meglio? Presentagli Villa Maria. Ci prenderemo cura di lui come ci prendiamo cura di te.'), '#D9DCDD', True) +
                grid([(('1', '1'), ('Share your personal link', 'Condividi il tuo link personale')),
                      (('2', '2'), ('Your colleague stays', 'Il tuo collega soggiorna')),
                      (('3', '3'), ('We welcome them like you', 'Lo accogliamo come te'))], WHITE, '#C9CED1', 'rgba(255,255,255,.25)', 3) +
                buttons([(('Refer a colleague →', 'Consiglia un collega →'), link('padel-experience.html', c, '#refer'), 'light')]) +
                p(('Enjoyed your stay? <a href="' + link('padel-experience.html', c, '#review') + '" style="color:#FFFFFF">Share your review</a>',
                   'Ti è piaciuto il soggiorno? <a href="' + link('padel-experience.html', c, '#review') + '" style="color:#FFFFFF">Lascia una recensione</a>'), '#D9DCDD', True, 13, 16)
                .replace('&lt;', '<').replace('&gt;', '>'), SLATE),
        section(h(('Your court is ready. *So is your room.*', 'Il tuo campo è pronto. *Anche la tua camera.*'), 30, INK, True) +
                buttons([(('Book the Padel Experience →', 'Prenota la Padel Experience →'), link('booking.html', c, '#padel'), 'dark')])),
        footer()]
    return c, ('The best business relationships continue beyond the meeting room', 'Le migliori relazioni di lavoro continuano oltre la sala riunioni'), \
        ('Next time, bring a racket.', 'La prossima volta, porta una racchetta.'), rows


EMAILS = [('family', 1, family_1), ('family', 2, family_2), ('family', 3, family_3),
          ('business', 1, business_1), ('business', 2, business_2), ('business', 3, business_3)]
WHEN = {1: ('Right after sign-up', 'Subito dopo l’iscrizione'), 2: ('7 days later', '7 giorni dopo'),
        3: ('After check-out, to returning guests', 'Dopo il check-out, agli ospiti che tornano')}


def main():
    global LANG
    index = []
    for LANG in ('en', 'it'):
        os.makedirs(os.path.join(OUT, LANG), exist_ok=True)
        for lst, n, fn in EMAILS:
            slug, subject, pre, rows = fn()
            with open(os.path.join(OUT, LANG, slug + '.html'), 'w') as f:
                f.write(page(subject, pre, rows))
            index.append((LANG, lst, n, slug, L(subject), L(pre), L(WHEN[n])))
    with open(os.path.join(OUT, 'index.html'), 'w') as f:
        import json
        f.write(PREVIEW.replace('__DATA__', json.dumps([dict(zip(('lang', 'list', 'step', 'file', 'subject', 'preheader', 'send'), r)) for r in index], ensure_ascii=False))
                .replace('__MERGE__', json.dumps(FIRST_NAME)))
    print('built', len(index), 'emails')


PREVIEW = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Villa Maria emails</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;1,400&family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root{--sand:#F4F1EA;--sand-2:#EAE5DA;--ink:#2B2F33;--muted:#596066;--line:#DAD4C8;--slate:#44555F;--olive:#5D6B43}
  *{box-sizing:border-box}
  body{margin:0;background:var(--sand-2);color:var(--ink);font:400 15px/1.5 Manrope,Arial,sans-serif}
  header{padding:20px 16px;background:var(--sand);border-bottom:1px solid var(--line)}
  header .in,main{max-width:1180px;margin:0 auto}
  h1{font:400 32px/1.1 'Cormorant Garamond',Georgia,serif;margin:0}
  header p{margin:6px 0 0;color:var(--muted);font-size:14px}
  main{display:grid;grid-template-columns:340px 1fr;gap:24px;padding:24px 16px}
  .seg{display:flex;gap:4px;padding:4px;border:1px solid var(--line);border-radius:999px;background:#fff;width:max-content;margin-bottom:14px}
  .seg button{appearance:none;border:0;background:none;border-radius:999px;padding:7px 14px;font:700 11px Manrope,Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);cursor:pointer}
  .seg button[aria-pressed=true]{background:var(--slate);color:#fff}
  h2{font:700 11px Manrope,Arial,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--olive);margin:18px 0 8px}
  .list button{display:block;width:100%;text-align:left;appearance:none;border:1px solid var(--line);background:#fff;padding:12px 14px;margin-bottom:8px;cursor:pointer;font:inherit;color:inherit}
  .list button[aria-current=true]{border-color:var(--slate);box-shadow:inset 3px 0 0 var(--slate)}
  .list b{display:block;font-weight:600}
  .list span{display:block;font-size:12px;color:var(--muted)}
  .meta{background:#fff;border:1px solid var(--line);padding:12px 16px;font-size:13px}
  .meta b{display:inline-block;min-width:76px;color:var(--muted);font-weight:600}
  .meta a{color:var(--slate)}
  iframe{display:block;width:100%;height:80vh;border:1px solid var(--line);background:#fff;margin-top:12px}
  @media (max-width:860px){main{grid-template-columns:1fr}iframe{height:70vh}}
</style>
</head>
<body>
<header><div class="in"><h1>Email marketing</h1>
<p>Two lists from the sign-up pop-up: families and business guests. Three emails each, in English and Italian. Sample names are filled in here; the files use your email tool’s merge tag.</p></div></header>
<main>
<div>
  <div class="seg" id="lang"><button type="button" data-v="en" aria-pressed="true">English</button><button type="button" data-v="it" aria-pressed="false">Italiano</button></div>
  <div class="list" id="list"></div>
</div>
<div>
  <div class="meta" id="meta"></div>
  <iframe id="view" title="Email preview"></iframe>
</div>
</main>
<script>
var DATA = __DATA__, MERGE = __MERGE__, lang = 'en', cur = null;
var NAMES = { family: 'Sarah', business: 'Alessandro' };
var LISTS = { family: ['Family list', 'Lista famiglie'], business: ['Business list', 'Lista business'] };
function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
function render() {
  var out = '';
  ['family', 'business'].forEach(function (l) {
    out += '<h2>' + LISTS[l][lang === 'en' ? 0 : 1] + '</h2>';
    DATA.filter(function (d) { return d.lang === lang && d.list === l; }).forEach(function (d) {
      out += '<button type="button" data-f="' + d.file + '"' + (cur && cur.file === d.file ? ' aria-current="true"' : '') + '><b>' + d.step + '. ' + esc(d.subject) + '</b><span>' + esc(d.send) + '</span></button>';
    });
  });
  document.getElementById('list').innerHTML = out;
}
function show(file) {
  cur = DATA.filter(function (d) { return d.lang === lang && d.file === file; })[0];
  render();
  var path = lang + '/' + file + '.html';
  document.getElementById('meta').innerHTML = '<div><b>Subject</b> ' + esc(cur.subject) + '</div><div><b>Preview</b> ' + esc(cur.preheader) + '</div><div><b>Send</b> ' + esc(cur.send) + '</div><div><b>File</b> <a href="' + path + '" target="_blank" rel="noopener">emails/' + path + '</a></div>';
  fetch(path).then(function (r) { return r.text(); }).then(function (h) {
    h = h.split(MERGE).join(NAMES[cur.list]).replace('<head>', '<head><base href="' + new URL(lang + '/', location.href).href + '" target="_blank">');
    document.getElementById('view').srcdoc = h;
  }).catch(function () { document.getElementById('view').src = path; });
}
document.getElementById('list').addEventListener('click', function (e) { var b = e.target.closest('[data-f]'); if (b) show(b.getAttribute('data-f')); });
document.getElementById('lang').addEventListener('click', function (e) {
  var b = e.target.closest('[data-v]'); if (!b) return;
  lang = b.getAttribute('data-v');
  this.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
  show(cur ? cur.file : DATA[0].file);
});
show(DATA[0].file);
</script>
</body>
</html>
"""


if __name__ == '__main__':
    main()
