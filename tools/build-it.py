#!/usr/bin/env python3
"""Build the static Italian site in it/ from the English pages.

The English pages are the source. Every element with data-it="..." gets that Italian
HTML baked in, so Google and visitors receive real Italian pages without waiting for
JavaScript. Run after editing any page:

    python3 tools/build-it.py
"""
import pathlib
import re

from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'it'
# Final address of the English site, used for hreflang links (Google needs full URLs).
SITE_URL = 'https://www.hvillamaria.it'

IT_META = {
    'index.html': ('Villa Maria Hotel & Spa · Francavilla al Mare, Abruzzo',
                   'Hotel e spa 4 stelle sul mare a Francavilla al Mare, in Abruzzo. Soggiorni per famiglie e per il business, spa Linfa, due piscine in un parco privato.'),
    'italian-memories.html': ('La Dolce Family · Villa Maria Hotel & Spa',
                              'La Dolce Family: hotel e spa 4 stelle per famiglie a Francavilla al Mare, pensato per riposare e stare insieme.'),
    'family-reset-package.html': ('Family Reset: 30 € di sconto · Villa Maria Hotel & Spa',
                                  'Family Reset a Villa Maria Hotel & Spa: camera famiglia, colazione e spa in una prenotazione, con 30 € di sconto prenotando diretto.'),
    'ciao-again.html': ('Ciao Again · Villa Maria Hotel & Spa',
                        'Ciao Again: per le famiglie che tornano a Villa Maria Hotel & Spa.'),
    'business-travel.html': ('Business, senza stress · Villa Maria Hotel & Spa',
                             'Riunioni, recupero e cena in un unico indirizzo 4 stelle sul mare, vicino all\'aeroporto di Pescara e all\'A14.'),
    'executive-business-stay.html': ('Ufficio vista mare · Villa Maria Hotel & Spa',
                                     'Ufficio vista mare: camera, colazione presto, Wi-Fi veloce, spa e sala riunioni in un unico pacchetto.'),
    'padel-experience.html': ('Padel & Partner · Villa Maria Hotel & Spa',
                              'Padel & Partner: prenota un campo per te e i tuoi clienti, poi spa, aperitivo e cena a Villa Maria Hotel & Spa.'),
    'rooms.html': ('Camere e Suite · Villa Maria Hotel & Spa',
                   'Camere Superior, Deluxe e suite a Villa Maria Hotel & Spa, molte con vista sull\'Adriatico.'),
    'spa.html': ('Linfa Wellness & Spa · Villa Maria Hotel & Spa',
                 'Spa Linfa a Villa Maria Hotel & Spa: piscina interna, sauna e area relax a Francavilla al Mare.'),
    'restaurant.html': ('Ristorante · Villa Maria Hotel & Spa',
                        'Il ristorante di Villa Maria Hotel & Spa: ricette abruzzesi, colazione e cene con vista.'),
    'contact.html': ('Come arrivare e contatti · Villa Maria Hotel & Spa',
                     'Come raggiungere Villa Maria Hotel & Spa a Francavilla al Mare: indirizzo, mappa e indicazioni in aereo, treno o auto.'),
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
    for lang, code in (('en', 'en'), ('it', 'it'), ('en', 'x-default')):
        tag = soup.new_tag('link', rel='alternate', hreflang=code, href=url(lang, page))
        head.append(tag)
        head.append('\n')


def build(page):
    src = ROOT / page
    en = BeautifulSoup(src.read_text(encoding='utf-8'), 'html.parser')
    set_alternates(en, page)
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
    for el in soup.select('[data-it-alt]'):
        el['alt'] = el['data-it-alt']
        del el['data-it-alt']

    html = str(soup)
    html = re.sub(r'(\s(?:src|href|poster))="assets/', r'\1="../assets/', html)
    (OUT / page).write_text(html, encoding='utf-8')
    print('it/' + page)


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for page in IT_META:
        build(page)
