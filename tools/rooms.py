"""Room cards with photos and simple features (facts from the hotel's room descriptions).

Writes the same six rooms to two places:
  booking.html  step 3, as selectable cards (radio buttons)
  rooms.html    as display cards, each with a "Book this room" button

Edit ROOMS below, run `python3 tools/rooms.py`, then `python3 tools/build-it.py`.
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def A(s):
    return html.escape(s, quote=True)


ICON = {
    'park': '<path d="M12 3l5 7h-3l4 6H6l4-6H7z"/><path d="M12 16v5"/>',
    'sea': '<path d="M3 15c2-2 4-2 6 0s4 2 6 0 4-2 6 0M3 19c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/><circle cx="16" cy="7" r="3"/>',
    'quiet': '<path d="M21 13A9 9 0 1 1 11 3a7 7 0 0 0 10 10z"/>',
    'bath': '<path d="M3 12h18v3a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5z"/><path d="M6 12V6a2 2 0 0 1 4 0"/><path d="M7 20l-1 2M17 20l1 2"/>',
    'spa': '<path d="M12 3c3 4 5 6.5 5 10a5 5 0 0 1-10 0c0-3.5 2-6 5-10z"/>',
    'lift': '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 9l3-3 3 3M9 15l3 3 3-3"/>',
    'terrace': '<path d="M3 21h18M5 21v-6h14v6M4 15l8-8 8 8"/><circle cx="18" cy="5" r="2"/>',
    'sofa': '<path d="M4 18v-6a2 2 0 0 1 4 0v2h8v-2a2 2 0 0 1 4 0v6zM6 18v2M18 18v2M7 10V7a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v3"/>',
    'kettle': '<path d="M6 20h11l1-9H5z"/><path d="M18 13h2a2 2 0 0 0 0-4h-2M9 11V7h5v4M10 4h3"/>',
    'tub2': '<path d="M3 11h18v3a6 6 0 0 1-6 6H9a6 6 0 0 1-6-6z"/><circle cx="9" cy="6" r="1.5"/><circle cx="15" cy="6" r="1.5"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M5 19l1.5-1.5M17.5 6.5L19 5"/>',
    'sauna': '<path d="M12 21c-4 0-6-3-6-6 0-4 4-6 4-11 3 2 8 6 8 11 0 3-2 6-6 6z"/><path d="M12 21c-1.5 0-2.5-1-2.5-2.5S11 16 12 14c1 2 2.5 3 2.5 4.5S13.5 21 12 21z"/>',
    'jacuzzi': '<path d="M3 13h18v2a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5z"/><path d="M8 10c0-1 1-1 1-2s-1-1-1-2M12 10c0-1 1-1 1-2s-1-1-1-2M16 10c0-1 1-1 1-2s-1-1-1-2"/>',
    'rooms2': '<rect x="3" y="5" width="18" height="14"/><path d="M12 5v14M14 12h1M9 12h1"/>',
    'kit': '<rect x="4" y="7" width="16" height="13" rx="1"/><path d="M9 7V5h6v2M12 11v5M9.5 13.5h5"/>',
    'family': '<circle cx="7.5" cy="6" r="2.2"/><circle cx="16.5" cy="6" r="2.2"/><circle cx="12" cy="12.5" r="1.7"/><path d="M4 20v-5.5a3.5 3.5 0 0 1 7 0M13 14.5a3.5 3.5 0 0 1 7 0V20M9.5 20v-2.5a2.5 2.5 0 0 1 5 0V20"/>',
    'kids': '<circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c3 3 3 13 0 16M12 4c-3 3-3 13 0 16"/>',
    'paw': '<circle cx="6.5" cy="10" r="1.7"/><circle cx="10" cy="6" r="1.7"/><circle cx="14" cy="6" r="1.7"/><circle cx="17.5" cy="10" r="1.7"/><path d="M7.5 17.5c0-3 2-5.5 4.5-5.5s4.5 2.5 4.5 5.5c0 1.6-1.2 2.5-2.6 2.5-.9 0-1.4-.5-1.9-.5s-1 .5-1.9.5c-1.4 0-2.6-.9-2.6-2.5z"/>',
    'door': '<path d="M6 21V4h12v17M3 21h18"/><circle cx="15" cy="12.5" r=".8"/>',
}

# value, name EN/IT, text EN/IT, photos, features [(icon, EN, IT)]
ROOMS = [
    ('standard', 'Standard Room', 'Camera Standard',
     'Calm, practical rooms facing the park, in a quiet part of the hotel past the winter garden. The spa is reached through reception. Good for a short stay on a budget.',
     'Camere sobrie e funzionali con vista sul parco, in una zona tranquilla dell’hotel oltre il giardino d’inverno. Alla spa si accede dalla reception. Ideali per un soggiorno breve a budget contenuto.',
     [('rooms/standard-1.jpg', 'Reading corner with a view of the park', 'Angolo lettura con vista sul parco'),
      ('rooms/standard-2.jpg', 'Bathroom with walk-in shower and wellness kit', 'Bagno con doccia walk-in e kit benessere')],
     [('park', 'Park view', 'Vista parco'), ('quiet', 'Quiet area', 'Zona tranquilla'),
      ('bath', 'Shower or bath', 'Doccia o vasca'), ('kit', 'Spa access & wellness kit', 'Accesso spa e kit benessere')]),
    ('superior', 'Superior Room', 'Camera Superior',
     'In the main building next to the spa, with a view over the pine grove or the sea in the distance.',
     'Nel corpo centrale vicino alla spa, con vista sulla pineta o sul mare in lontananza.',
     [('rooms/superior-1.jpg', 'Desk and balcony over the pines, the sea in the distance', 'Scrivania e balcone sui pini, il mare in lontananza'),
      ('rooms/superior-2.jpg', 'Bathrobe, slippers and wellness kit, ready for the spa', 'Accappatoio, ciabattine e kit benessere, pronti per la spa')],
     [('park', 'Pine grove or distant sea view', 'Vista pineta o mare in lontananza'), ('lift', 'Direct spa access from your floor', 'Accesso diretto alla spa dal piano'),
      ('bath', 'Shower or bath', 'Doccia o vasca'), ('kit', 'Wellness kit', 'Kit benessere')]),
    ('deluxe', 'Deluxe Room', 'Camera Deluxe',
     'A room with its own terrace, looking out to the sea or the pine forest.',
     'Una camera con la propria terrazza, affacciata sul mare o sulla pineta.',
     [('rooms/deluxe-1.jpg', 'The room opens onto a private sea-view terrace', 'La camera si apre su una terrazza privata vista mare'),
      ('deluxe-room.jpg', 'Double bed, with the terrace beyond the glass doors', 'Letto matrimoniale, con la terrazza oltre le vetrate')],
     [('terrace', 'Private terrace', 'Terrazza privata'), ('sea', 'Sea or pine-forest view', 'Vista mare o pineta'),
      ('spa', 'Spa access', 'Accesso alla spa'), ('kit', 'Wellness kit', 'Kit benessere')]),
    ('suite', 'Junior Suite', 'Junior Suite',
     'A sleeping area and a separate sitting area, with a private terrace. Room for families and longer stays.',
     'Zona notte e soggiorno separati, con terrazza privata. Spazio per famiglie e soggiorni più lunghi.',
     [('rooms/junior-suite-1.jpg', 'Sitting area, with the bedroom beyond', 'Zona soggiorno, con la camera da letto oltre')],
     [('sofa', 'Separate sitting area', 'Zona soggiorno separata'), ('terrace', 'Private terrace', 'Terrazza privata'),
      ('lift', 'Direct spa access by lift', 'Accesso diretto alla spa in ascensore'), ('kettle', 'Kettle', 'Bollitore')]),
    ('family-room', 'Family Room', 'Family Room',
     'The ideal solution for families who want total privacy and maximum comfort. Tell us who is coming and we will prepare the right layout.',
     'La soluzione ideale per le famiglie che vogliono privacy totale e il massimo comfort. Dicci chi viene e prepariamo la sistemazione giusta.',
     [('rooms/family-1.jpg', 'Double bed and a sofa bed for the children, with the park outside', 'Letto matrimoniale e divano letto per i bambini, con il parco fuori'),
      ('rooms/family-2.jpg', 'The sofa bed, made up for two children', 'Il divano letto, pronto per due bambini'),
      ('rooms/family-3.jpg', 'Family bathroom with a bathtub and towels for four', 'Bagno di famiglia con vasca e asciugamani per quattro')],
     [('family', 'Space for the whole family', 'Spazio per tutta la famiglia'), ('quiet', 'Privacy and comfort', 'Privacy e comfort'),
      ('kids', 'Kids Club in July & August', 'Kids Club a luglio e agosto'), ('kit', 'Spa access & wellness kit', 'Accesso spa e kit benessere')]),
    ('mini-spa', 'Mini SPA Suite', 'Mini SPA Suite',
     'A hydromassage tub for two inside the suite, and a sea-view terrace with a solarium.',
     'Una vasca idromassaggio di coppia in camera e una terrazza vista mare con solarium.',
     [('spa-whirlpool.jpg', 'The Linfa spa, reached directly from your floor', 'La spa Linfa, raggiungibile direttamente dal piano')],
     [('tub2', 'Hydromassage tub for two', 'Vasca idromassaggio di coppia'), ('sun', 'Sea-view terrace & solarium', 'Terrazza vista mare e solarium'),
      ('lift', 'Direct spa access from your floor', 'Accesso diretto alla spa dal piano'), ('kit', 'Wellness kit', 'Kit benessere')]),
    ('master-spa', 'Master SPA Suite', 'Master SPA Suite',
     'Two rooms with a sauna for two, and a large corner terrace with a heated mini jacuzzi, facing east and fully private.',
     'Due ambienti con sauna di coppia e una grande terrazza ad angolo con mini jacuzzi riscaldata, esposta a est e riservata.',
     [('suite-terrace.jpg', 'Private terrace with a hot tub and a sea view', 'Terrazza privata con vasca idromassaggio e vista mare'),
      ('sauna.jpg', 'Sauna for two', 'Sauna di coppia')],
     [('rooms2', 'Two rooms, separate bathroom', 'Due ambienti, bagno separato'), ('sauna', 'Sauna for two', 'Sauna di coppia'),
      ('jacuzzi', 'Heated mini jacuzzi on the terrace', 'Mini jacuzzi riscaldata in terrazza'), ('sun', 'Corner terrace & solarium', 'Terrazza ad angolo e solarium')]),
    ('cottage', 'Cottage', 'Cottage',
     'A small annex at the hotel entrance with its own entrance, made for guests travelling with a pet of any size.',
     'Una piccola dépendance all’ingresso dell’hotel con entrata indipendente, pensata per chi viaggia con un animale di qualsiasi taglia.',
     [('rooms/cottage-1.jpg', 'The Cottage: its own entrance and a fenced garden for your dog', 'Il Cottage: ingresso indipendente e giardino recintato per il tuo cane')],
     [('paw', 'Fenced garden for pets of all sizes', 'Giardino recintato per animali di ogni taglia'), ('door', 'Own entrance, about 39 m²', 'Ingresso indipendente, circa 39 m²'),
      ('kettle', 'Kitchenette, microwave & coffee machine', 'Angolo cottura, microonde e macchina del caffè'), ('park', 'Park view', 'Vista parco')])
]

ALL = ('In every room: free Wi-Fi, air conditioning, satellite TV, safe, hairdryer and minibar (charged).',
       'In tutte le camere: Wi-Fi gratuito, aria condizionata, TV satellitare, cassaforte, asciugacapelli e minibar (a pagamento).')



def media(photos, icon='park'):
    """photos = [(file, caption EN, caption IT)]; the caption is the alt text and shows on the photo.
    No photos yet: an icon panel that says so, never a photo of another room."""
    if not photos:
        return (f'<span class="rc-media rc-nophoto"><svg aria-hidden="true" viewbox="0 0 24 24">{ICON[icon]}</svg>'
                '<span class="rc-cap" data-it="Foto in arrivo">Photo coming soon</span></span>')
    slides = ''.join(f'<img alt="{A(en)}" class="rc-slide{" is-active" if i == 0 else ""}" data-it-alt="{A(it)}" loading="lazy" src="assets/img/{f}"/>'
                     for i, (f, en, it) in enumerate(photos))
    cap = f'<span class="rc-cap" data-it="{A(photos[0][2])}">{html.escape(photos[0][1], quote=False)}</span>'
    nav = ('<button aria-label="Previous photo" class="rc-prev" data-it-aria="Foto precedente" type="button">‹</button>'
           '<button aria-label="Next photo" class="rc-next" data-it-aria="Foto successiva" type="button">›</button>'
           f'<span class="rc-count">1 / {len(photos)}</span>') if len(photos) > 1 else ''
    return f'<span class="rc-media">{slides}{cap}{nav}</span>'


def feats(fs):
    return '<ul class="rc-feats">' + ''.join(f'<li><svg viewbox="0 0 24 24">{ICON[i]}</svg><span data-it="{A(it)}">{html.escape(en, quote=False)}</span></li>' for i, en, it in fs) + '</ul>'


def pick_card(r, first):
    """Booking page: the whole card is a radio choice."""
    v, n_en, n_it, d_en, d_it, photos, fs = r
    chk = ' checked=""' if first else ''
    return f'''<label class="room-card"><input{chk} name="room" type="radio" value="{v}"/>
{media(photos, fs[0][0])}
<span class="rc-body">
<span class="rc-head"><b class="rc-name" data-it="{A(n_it)}">{n_en}</b><span class="rc-price" data-rate="{v}"></span></span>
<span class="rc-text" data-it="{A(d_it)}">{d_en}</span>
{feats(fs)}
<span class="rc-pick"><span class="rc-pick-off" data-it="Scegli questa camera">Select this room</span><span class="rc-pick-on" data-it="Camera scelta ✓">Selected ✓</span></span>
</span>
</label>
'''


def show_card(r):
    """Rooms page: same card, with a button to book this room."""
    v, n_en, n_it, d_en, d_it, photos, fs = r
    return f'''<article class="room-card is-display" id="room-{v}">
{media(photos, fs[0][0])}
<div class="rc-body">
<div class="rc-head"><h3 class="rc-name" data-it="{A(n_it)}">{n_en}</h3><span class="rc-price" data-rate="{v}"></span></div>
<p class="rc-text" data-it="{A(d_it)}">{d_en}</p>
{feats(fs)}
<a class="btn btn-sky rc-book" data-book="{v}" href="booking.html#{v}" data-it="Prenota questa camera →">Book this room →</a>
</div>
</article>
'''


ALL_P = f'<p class="rc-all" data-it="{A(ALL[1])}">{ALL[0]}</p>\n'


def write(name, pattern, block):
    p = ROOT / name
    s = p.read_text(encoding='utf-8')
    s2, n = re.subn(pattern, lambda m: block, s, count=1, flags=re.S)
    assert n == 1, name
    if s2 != s:
        p.write_text(s2, encoding='utf-8')
    print(name, 'updated' if s2 != s else 'unchanged')


write('booking.html', r'<div class="room-list">.*?<p class="rc-all"[^>]*>.*?</p>\n',
      '<div class="room-list">\n' + ''.join(pick_card(r, i == 1) for i, r in enumerate(ROOMS)) + '</div>\n' + ALL_P)

write('rooms.html', r'<section class="section rooms-list" id="rooms">.*?</section>\n',
      '<section class="section rooms-list" id="rooms">\n<div class="wrap">\n'
      '<p class="eb" data-it="Le camere">The rooms</p>\n'
      '<h2 class="h2" data-it="Scegli &lt;i&gt;la tua camera.&lt;/i&gt;">Choose <i>your room.</i></h2>\n'
      '<div class="room-list">\n' + ''.join(show_card(r) for r in ROOMS) + '</div>\n' + ALL_P +
      '<p class="muted" data-it="I prezzi cambiano con le date: il sistema di prenotazione mostra sempre la tariffa aggiornata.">'
      'Prices change with your dates. The booking system always shows today\'s rate.</p>\n'
      '</div>\n</section>\n')
