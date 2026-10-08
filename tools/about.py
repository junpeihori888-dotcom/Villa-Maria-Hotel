#!/usr/bin/env python3
"""Insert the longer "About" descriptions (expandable topics) and the photo galleries
into the hotel pages listed in the menu under "The hotel". English is the page text;
Italian sits in data-it so build-it.py can produce the Italian pages.

Edit the text or photos below, then run:

    python3 tools/about.py && python3 tools/build-it.py
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def a(s):
    return html.escape(s, quote=True)


# Each page: eyebrow, heading, intro, [(topic, paragraphs)], gallery [(file, caption)]
# Every text is (English, Italian). Only facts from the campaign emails and designs.
PAGES = {
 'index.html': {
  'eb': ('About Villa Maria', 'Su Villa Maria'),
  'h2': ('A four-star hotel &amp; spa <i>above the Adriatic.</i>', 'Un hotel &amp; spa quattro stelle <i>sopra l’Adriatico.</i>'),
  'intro': ('Villa Maria Hotel &amp; Spa sits in a private park on the hill above Francavilla al Mare, just south of Pescara in Abruzzo. Families come for time together; business guests come for quiet rooms, meeting spaces and a proper dinner at the end of the day.',
            'Villa Maria Hotel &amp; Spa si trova in un parco privato sulla collina sopra Francavilla al Mare, appena a sud di Pescara, in Abruzzo. Le famiglie vengono per stare insieme; chi viaggia per lavoro per le camere silenziose, le sale meeting e una buona cena a fine giornata.'),
  'topics': [
   (('The hotel and its park', 'L’hotel e il parco'), [
     ('Two outdoor pools sit in a private park with pine and olive trees, a fountain, loungers and a gazebo, and the sea is in view from the terraces. The hotel is outside the city, so evenings are quiet.',
      'Due piscine all’aperto si trovano in un parco privato tra pini e ulivi, con fontana, lettini e gazebo, e il mare è visibile dalle terrazze. L’hotel è fuori città, per serate tranquille.')]),
   (('For families', 'Per le famiglie'), [
     ('Parents get real rest and children get freedom: pools, a Kids Club, padel, a free shuttle to our partner beach, and long family dinners with Abruzzo recipes. The Family Discount puts room, breakfast and spa in one booking.',
      'I genitori riposano davvero e i ragazzi hanno libertà: piscine, Kids Club, padel, navetta gratuita per la spiaggia convenzionata e lunghe cene in famiglia con ricette abruzzesi. Lo Sconto Famiglia riunisce camera, colazione e spa in una prenotazione.')]),
   (('For business travel', 'Per i viaggi di lavoro'), [
     ('Meeting spaces go from private rooms to an auditorium, with video-conferencing and fast Wi-Fi. Breakfast starts early, check-out is express, and the spa, gym and padel courts are there after the last meeting. Pescara Airport, Pescara Centrale station and the A14 are all close.',
      'Le sale vanno dalle sale riservate all’auditorium, con videoconferenza e Wi-Fi veloce. La colazione inizia presto, il check-out è rapido e spa, palestra e campi da padel ti aspettano dopo l’ultima riunione. Aeroporto di Pescara, stazione di Pescara Centrale e A14 sono vicini.')]),
   (('Wellness, food and service', 'Benessere, cucina e servizio'), [
     ('The Linfa wellness &amp; spa has pools, a sauna, relaxation areas and treatments for one or two. The restaurant cooks Abruzzo recipes with local products, and the team is warm and attentive, before you arrive and during your stay.',
      'La spa Linfa ha piscine, sauna, aree relax e trattamenti per uno o per due. Il ristorante cucina ricette abruzzesi con prodotti locali e il team è caloroso e attento, prima dell’arrivo e durante il soggiorno.')]),
  ],
  'gallery': [
   ('villa-adriatic.jpg', ('Villa Maria above the Adriatic', 'Villa Maria sopra l’Adriatico')),
   ('pool-park.jpg', ('The outdoor pool in the private park', 'La piscina all’aperto nel parco privato')),
   ('pool-fountain.jpg', ('Fountain and pool area', 'Fontana e area piscina')),
   ('garden-gazebo.jpg', ('The gazebo in the garden', 'Il gazebo in giardino')),
   ('suite-terrace.jpg', ('Suite terrace with sea view', 'Terrazza della suite con vista mare')),
   ('reception.jpg', ('Reception', 'Reception')),
   ('restaurant-hall.jpg', ('The restaurant', 'Il ristorante')),
   ('spa-whirlpool.jpg', ('Linfa spa', 'Spa Linfa')),
   ('meeting-hall.jpg', ('Meeting room', 'Sala riunioni')),
  ],
 },
 'rooms.html': {
  'eb': ('About our rooms', 'Le nostre camere'),
  'h2': ('Quiet rooms, <i>made for rest and work.</i>', 'Camere silenziose, <i>per riposare e lavorare.</i>'),
  'intro': ('Every room is a quiet place to sleep well, with a writing desk, power by the bed and high-speed Wi-Fi. Choose the Superior Room for a short trip, or the Deluxe Room and Suites for more space and the Adriatic in view.',
            'Ogni camera è un posto tranquillo per dormire bene, con scrivania, prese vicino al letto e Wi-Fi ad alta velocità. Scegli la Camera Superior per un viaggio breve, o le Camere Deluxe e le Suite per più spazio e l’Adriatico davanti.'),
  'topics': [
   (('Superior Room', 'Camera Superior'), [
     ('A garden or partial sea view and a writing desk. Ideal for one or two nights, and the standard room of the Executive Business Stay Package.',
      'Vista giardino o parziale vista mare e scrivania. Ideale per una o due notti, ed è la camera standard del Pacchetto Executive Business Stay.')]),
   (('Deluxe Room', 'Camera Deluxe'), [
     ('More space, Adriatic views, a desk and a lounge area. Our choice for stays of three nights or more.',
      'Più spazio, vista Adriatico, scrivania e zona lounge. La nostra scelta per soggiorni di tre notti o più.')]),
   (('Suites with a terrace', 'Suite con terrazza'), [
     ('The suites add a private terrace with loungers, a hot tub and a view of the sea: the room our guests remember long after they leave.',
      'Le suite aggiungono una terrazza privata con lettini, vasca idromassaggio e vista sul mare: la camera che i nostri ospiti ricordano a lungo.')]),
   (('Family rooms', 'Camere per famiglie'), [
     ('With the Family Discount, family rooms and suites sleep 2 adults and 2 teens, with breakfast and spa included. Tell us who is coming when you book and we will suggest the best room.',
      'Con lo Sconto Famiglia, camere e suite famiglia ospitano 2 adulti e 2 ragazzi, con colazione e spa incluse. Dicci chi viene quando prenoti e ti suggeriamo la camera migliore.')]),
   (('For business travellers', 'Per chi viaggia per lavoro'), [
     ('Quiet rooms away from the city, a real desk, fast Wi-Fi for video calls, early breakfast and express check-out. Share your room preferences once and we keep them for your next stay.',
      'Camere silenziose lontane dalla città, una vera scrivania, Wi-Fi veloce per le videochiamate, colazione presto e check-out rapido. Indicaci le tue preferenze una volta e le terremo per il prossimo soggiorno.')]),
  ],
  'gallery': [
   ('superior-room.jpg', ('Superior Room', 'Camera Superior')),
   ('deluxe-room.jpg', ('Deluxe Room', 'Camera Deluxe')),
   ('suite-terrace.jpg', ('Suite terrace with hot tub', 'Terrazza della suite con vasca idromassaggio')),
   ('suite-seaview.jpg', ('Sea view from a suite', 'Vista mare da una suite')),
   ('concierge.jpg', ('Concierge desk', 'Concierge')),
  ],
 },
 'spa.html': {
  'eb': ('About the Linfa spa', 'La spa Linfa'),
  'h2': ('Water, warmth <i>and quiet.</i>', 'Acqua, calore <i>e silenzio.</i>'),
  'intro': ('The Linfa wellness &amp; spa is where the day slows down: pools, a sauna, relaxation, beauty and fitness areas, and treatments for one or two. Parents unwind while the kids are at the Kids Club; business guests recover after the last meeting.',
            'La spa Linfa è il luogo dove la giornata rallenta: piscine, sauna, aree relax, beauty e fitness, e trattamenti per uno o per due. I genitori si rilassano mentre i bambini sono al Kids Club; chi viaggia per lavoro si rigenera dopo l’ultima riunione.'),
  'topics': [
   (('Pools and water', 'Piscine e acqua'), [
     ('An indoor pool and a whirlpool look out through tall windows over the park and towards the sea, so the view comes with you into the water.',
      'Una piscina interna e una vasca idromassaggio guardano, attraverso grandi vetrate, il parco e il mare, così la vista entra con te in acqua.')]),
   (('Sauna and relaxation', 'Sauna e relax'), [
     ('A wooden sauna for heat, then the relaxation area for quiet. Many guests pair it with a massage at the end of the day.',
      'Una sauna in legno per il calore, poi l’area relax per il silenzio. Molti ospiti la abbinano a un massaggio a fine giornata.')]),
   (('Treatments for one or two', 'Trattamenti per uno o per due'), [
     ('Massages and treatments can be booked for one person or as a couple. Ask our team for the current list, prices and free times.',
      'Massaggi e trattamenti si possono prenotare per una persona o in coppia. Chiedi al nostro team l’elenco aggiornato, i prezzi e gli orari liberi.')]),
   (('Spa in your package', 'La spa nel tuo pacchetto'), [
     ('Spa access is included in the Family Discount and in the Executive Business Stay Package. The Padel Experience ends the match with sauna, spa and a massage.',
      'L’accesso alla spa è incluso nello Sconto Famiglia e nel Pacchetto Executive Business Stay. La Padel Experience chiude la partita con sauna, spa e massaggio.')]),
   (('Opening hours', 'Orari di apertura'), [
     ('Opening hours can change with the season. Send us a message or ask at reception and we will tell you the times for your stay.',
      'Gli orari possono cambiare con la stagione. Scrivici un messaggio o chiedi in reception e ti diremo gli orari per il tuo soggiorno.')]),
  ],
  'gallery': [
   ('spa.jpg', ('Indoor pool', 'Piscina interna')),
   ('spa-whirlpool.jpg', ('Whirlpool with a view of the park', 'Idromassaggio con vista sul parco')),
   ('sauna.jpg', ('Sauna', 'Sauna')),
   ('wellness.jpg', ('Indoor pool with a sea view', 'Piscina interna con vista mare')),
   ('walk.jpg', ('Terrace with a plunge pool and sea view', 'Terrazza con piscinetta e vista mare')),
  ],
 },
 'restaurant.html': {
  'eb': ('About the restaurant', 'Il ristorante'),
  'h2': ('Abruzzo <i>at every meal.</i>', 'L’Abruzzo <i>a ogni pasto.</i>'),
  'intro': ('From the breakfast buffet to dinner at the chef’s table, our kitchen cooks Abruzzo recipes with local products. Families stay at the table until the stars come out; business guests have a working lunch over the garden and dinners that close the deal.',
            'Dalla colazione a buffet alla cena alla tavola dello chef, la nostra cucina prepara ricette abruzzesi con prodotti locali. Le famiglie restano a tavola fino alle stelle; chi viaggia per lavoro ha pranzi operativi sul giardino e cene che chiudono l’accordo.'),
  'topics': [
   (('Breakfast', 'Colazione'), [
     ('A local buffet with fresh fruit, cakes and savoury dishes, included in our packages. Business guests can have it early, before the first call.',
      'Un buffet locale con frutta fresca, dolci e piatti salati, incluso nei pacchetti. Chi viaggia per lavoro può farla presto, prima della prima call.')]),
   (('Lunch and dinner', 'Pranzo e cena'), [
     ('Abruzzo recipes and shared plates in a dining room that opens onto the park. Long family dinners and quiet business dinners both have their place.',
      'Ricette abruzzesi e piatti da condividere in una sala che si apre sul parco. Lunghe cene in famiglia e cene di lavoro tranquille hanno entrambe il loro posto.')]),
   (('The chef’s table', 'La tavola dello chef'), [
     ('For a special evening, or the dinner after a padel match, the chef’s table is where conversations last and deals are made.',
      'Per una serata speciale, o la cena dopo una partita di padel, la tavola dello chef è dove le conversazioni durano e nascono gli accordi.')]),
   (('Bar and aperitivo', 'Bar e aperitivo'), [
     ('An aperitivo at the bar before dinner: the toast after the match, the end of a long day, or the start of a family evening.',
      'Un aperitivo al bar prima di cena: il brindisi dopo la partita, la fine di una lunga giornata o l’inizio di una serata in famiglia.')]),
   (('La Bottega di Villa Maria', 'La Bottega di Villa Maria'), [
     ('Our corner of local products and Abruzzo flavours, to taste during your stay and take a little of the region home.',
      'Il nostro angolo di prodotti locali e sapori abruzzesi, da gustare durante il soggiorno e da portare un po’ a casa.')]),
   (('Allergies and reservations', 'Allergie e prenotazioni'), [
     ('Tell us about allergies or diets when you book, or send us a message. For opening times and table reservations, ask our team.',
      'Segnalaci allergie o diete quando prenoti, o scrivici un messaggio. Per orari e prenotazione del tavolo, chiedi al nostro team.')]),
  ],
  'gallery': [
   ('restaurant-hall.jpg', ('The dining room', 'La sala')),
   ('restaurant-dinner.jpg', ('Dinner with a view', 'Cena con vista')),
   ('breakfast.jpg', ('Breakfast buffet', 'Colazione a buffet')),
   ('chef-dinner.jpg', ('The chef’s dishes', 'I piatti dello chef')),
   ('bar.jpg', ('The bar', 'Il bar')),
  ],
 },
 'contact.html': {
  'eb': ('Plan your arrival', 'Pianifica l’arrivo'),
  'h2': ('Easy to reach, <i>quiet when you arrive.</i>', 'Facile da raggiungere, <i>tranquillo all’arrivo.</i>'),
  'intro': ('Villa Maria is on the hill above Francavilla al Mare, minutes from Pescara: close to the airport, the main station and the A14 motorway, yet outside the city and its traffic.',
            'Villa Maria è sulla collina sopra Francavilla al Mare, a pochi minuti da Pescara: vicina all’aeroporto, alla stazione centrale e all’autostrada A14, ma fuori dalla città e dal traffico.'),
  'topics': [
   (('By plane', 'In aereo'), [
     ('Abruzzo Airport (Pescara) is a short drive away. Ask us about a transfer when you book.',
      'L’aeroporto d’Abruzzo (Pescara) è a pochi minuti d’auto. Chiedici un transfer quando prenoti.')]),
   (('By train', 'In treno'), [
     ('Pescara Centrale station has easy rail connections across Italy. From the station, take a taxi or ask us about a transfer.',
      'La stazione di Pescara Centrale ha comodi collegamenti con tutta Italia. Dalla stazione prendi un taxi o chiedici un transfer.')]),
   (('By car', 'In auto'), [
     ('Leave the A14 motorway at the Pescara Sud – Francavilla exit and follow the signs for Francavilla al Mare. Free private parking with EV charging is waiting at the hotel.',
      'Esci dall’A14 a Pescara Sud – Francavilla e segui le indicazioni per Francavilla al Mare. In hotel ti aspetta il parcheggio privato gratuito con ricarica per auto elettriche.')]),
   (('The beach', 'La spiaggia'), [
     ('Family Discount guests have a free shuttle to our partner beach on the Adriatic.',
      'Con lo Sconto Famiglia la navetta per la spiaggia convenzionata sull’Adriatico è gratuita.')]),
   (('Arrival and check-in', 'Arrivo e check-in'), [
     ('Your check-in and check-out times are in your booking confirmation. Tell us your expected arrival time when you book, and ask if you need an early check-in or a late check-out.',
      'Gli orari di check-in e check-out sono nella conferma di prenotazione. Indicaci l’orario di arrivo quando prenoti e chiedici se ti serve un check-in anticipato o un check-out posticipato.')]),
  ],
  'gallery': [
   ('gardens.jpg', ('The gardens', 'I giardini')),
   ('villa-adriatic.jpg', ('The hotel and the sea', 'L’hotel e il mare')),
   ('reception.jpg', ('Reception', 'Reception')),
   ('garden-gazebo.jpg', ('The gazebo', 'Il gazebo')),
   ('walk.jpg', ('Terrace with a sea view', 'Terrazza con vista mare')),
  ],
 },
}


def about_section(p):
    topics = '\n'.join(
        f'<details class="about-item"><summary><span data-it="{a(t[1])}">{t[0]}</span></summary>'
        + ''.join(f'<p data-it="{a(it)}">{en}</p>' for en, it in paras) + '</details>'
        for t, paras in p['topics'])
    return ('<section class="section about" id="about">\n<div class="wrap split">\n'
            f'<div><p class="eb" data-it="{a(p["eb"][1])}">{p["eb"][0]}</p>\n'
            f'<h2 class="h2" data-it="{a(p["h2"][1])}">{p["h2"][0]}</h2></div>\n'
            f'<div><p class="about-intro" data-it="{a(p["intro"][1])}">{p["intro"][0]}</p>\n'
            f'<div class="about-list">\n{topics}\n</div></div>\n</div>\n</section>\n')


def gallery_section(p):
    items = '\n'.join(
        f'<figure><a class="g-item" href="assets/img/{f}" data-caption="{a(cap[0])}" data-it-caption="{a(cap[1])}">'
        f'<img src="assets/img/{f}" alt="{a(cap[0])}" data-it-alt="{a(cap[1])}" loading="lazy"></a>'
        f'<figcaption data-it="{a(cap[1])}">{cap[0]}</figcaption></figure>'
        for f, cap in p['gallery'])
    return ('<section class="section white gallery-sec" id="gallery">\n<div class="wrap">\n'
            '<div class="head"><div><p class="eb" data-it="Galleria">Gallery</p>\n'
            '<h2 class="h2" data-it="Guarda <i>prima di arrivare.</i>">See it <i>before you arrive.</i></h2></div></div>\n'
            f'<div class="gallery">\n{items}\n</div>\n</div>\n</section>\n')


for page, p in PAGES.items():
    path = ROOT / page
    s = path.read_text(encoding='utf-8')
    s = re.sub(r'<section class="section about" id="about">.*?</section>\n?', '', s, flags=re.S)
    s = re.sub(r'<section class="section white gallery-sec" id="gallery">.*?</section>\n?', '', s, flags=re.S)
    block = about_section(p) + gallery_section(p)
    anchor = '<section class="section faq" id="faq">'
    assert anchor in s, page
    s = s.replace(anchor, block + anchor, 1)
    path.write_text(s, encoding='utf-8')
    print('about+gallery', page, len(p['topics']), 'topics,', len(p['gallery']), 'photos')
