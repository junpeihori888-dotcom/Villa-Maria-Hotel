#!/usr/bin/env python3
"""Build the static Italian site in it/ from the English pages.

The English pages are the source. Every element with data-it="..." gets that Italian
HTML baked in, so Google and visitors receive real Italian pages without waiting for
JavaScript. Run after editing any page:

    python3 tools/build-it.py
"""
import json
import pathlib
import re

from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'it'
# Final address of your own site, e.g. 'https://www.villamaria-example.com'. Used for the
# hreflang links that tell Google the EN and IT pages belong together (Google needs full
# URLs). Leave empty until the domain is known: the links are then left out.
SITE_URL = ''

IT_META = {
    'index.html': ('Villa Maria Hotel & Spa · Francavilla al Mare, Abruzzo',
                   'Hotel e spa 4 stelle sul mare a Francavilla al Mare, in Abruzzo. Soggiorni per famiglie e per il business, spa Linfa, due piscine in un parco privato.'),
    'italian-memories.html': ('Italian Memories · Villa Maria Hotel & Spa',
                              'I ricordi italiani iniziano qui: hotel & spa quattro stelle sul mare a Francavilla al Mare, pensato per il relax e il tempo insieme.'),
    'family-reset-package.html': ('Sconto Famiglia · Villa Maria Hotel & Spa',
                                  'Sconto Famiglia a Villa Maria Hotel & Spa: camera, colazione e spa inclusi prenotando direttamente, più un voucher da 20 € e il 10% sul prossimo soggiorno.'),
    'ciao-again.html': ('Ciao Again · Villa Maria Hotel & Spa',
                        'Ciao di nuovo: per le famiglie che tornano a Villa Maria Hotel & Spa. La tua storia italiana continua.'),
    'business-travel.html': ('Viaggiare per lavoro, senza pressione · Villa Maria Hotel & Spa',
                             'Riunioni, recupero e cena in un unico indirizzo 4 stelle sul mare, vicino all\'aeroporto di Pescara e all\'A14.'),
    'executive-business-stay.html': ('Pacchetto Executive Business Stay · Villa Maria Hotel & Spa',
                                     'Pacchetto Executive Business Stay: camera silenziosa, colazione presto, Wi-Fi veloce, spa e sala riunioni in un unico pacchetto sull\'Adriatico.'),
    'padel-experience.html': ('La Padel Experience · Villa Maria Hotel & Spa',
                              'La Padel Experience a Villa Maria Hotel & Spa: porta una racchetta e il cliente, il collega o il team che vuoi conoscere meglio.'),
    'rooms.html': ('Camere e Suite · Villa Maria Hotel & Spa',
                   'Camere Superior, Deluxe e suite a Villa Maria Hotel & Spa, molte con vista sull\'Adriatico.'),
    'spa.html': ('Linfa Wellness & Spa · Villa Maria Hotel & Spa',
                 'Spa Linfa a Villa Maria Hotel & Spa: piscina interna, sauna e area relax a Francavilla al Mare.'),
    'restaurant.html': ('Ristorante · Villa Maria Hotel & Spa',
                        'Il ristorante di Villa Maria Hotel & Spa: ricette abruzzesi, colazione e cene con vista.'),
    'contact.html': ('Come arrivare e contatti · Villa Maria Hotel & Spa',
                     'Come raggiungere Villa Maria Hotel & Spa a Francavilla al Mare: indirizzo, mappa e indicazioni in aereo, treno o auto.'),
    'booking.html': ('Prenota il tuo soggiorno · Villa Maria Hotel & Spa',
                     'Prenota il tuo soggiorno a Villa Maria Hotel & Spa a Francavilla al Mare: scegli date, pacchetto e camera e invia la richiesta.'),
    'privacy.html': ('Privacy e cookie · Villa Maria Hotel & Spa',
                     'Informativa privacy e cookie del sito di Villa Maria Hotel & Spa.'),
}


def url(lang, page):
    path = '' if page == 'index.html' else page
    return f"{SITE_URL}/{'it/' if lang == 'it' else ''}{path}"


def set_alternates(soup, page):
    head = soup.head
    for link in head.find_all('link', rel='alternate'):
        link.decompose()
    if not SITE_URL:
        return
    for lang, code in (('en', 'en'), ('it', 'it'), ('en', 'x-default')):
        tag = soup.new_tag('link', rel='alternate', hreflang=code, href=url(lang, page))
        head.append(tag)
        head.append('\n')


def set_faq_schema(soup):
    """Google FAQPage data built from the visible FAQ accordion, so they always match."""
    old = soup.find('script', id='faq-schema')
    if old:
        old.decompose()
    items = soup.select('details.faq-item')
    if not items:
        return
    data = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': d.summary.get_text(' ', strip=True),
         'acceptedAnswer': {'@type': 'Answer', 'text': d.select_one('.faq-a').get_text(' ', strip=True)}}
        for d in items]}
    tag = soup.new_tag('script', type='application/ld+json', id='faq-schema')
    tag.string = json.dumps(data, ensure_ascii=False)
    soup.head.append(tag)


def build(page):
    src = ROOT / page
    en = BeautifulSoup(src.read_text(encoding='utf-8'), 'html.parser')
    set_alternates(en, page)
    set_faq_schema(en)
    # Removing old alternate links leaves their line breaks behind; collapse them.
    src.write_text(re.sub(r'\n\s*\n+', '\n', str(en)), encoding='utf-8')

    soup = BeautifulSoup(src.read_text(encoding='utf-8'), 'html.parser')
    soup.html['lang'] = 'it'
    title, desc = IT_META[page]
    soup.title.string = title
    soup.find('meta', attrs={'name': 'description'})['content'] = desc

    for el in soup.select('[data-it]'):
        el.clear()
        for node in list(BeautifulSoup(el['data-it'], 'html.parser').contents):
            el.append(node)
        del el['data-it']
    for el in soup.select('[data-it-placeholder]'):
        el['placeholder'] = el['data-it-placeholder']
        del el['data-it-placeholder']
    for el in soup.select('[data-it-alt]'):
        el['alt'] = el['data-it-alt']
        del el['data-it-alt']

    set_faq_schema(soup)
    html = str(soup)
    html = re.sub(r'(\s(?:src|href|poster))="assets/', r'\1="../assets/', html)
    (OUT / page).write_text(html, encoding='utf-8')
    print('it/' + page)


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for page in IT_META:
        build(page)
