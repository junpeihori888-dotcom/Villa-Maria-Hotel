#!/usr/bin/env python3
"""Insert the longer descriptions (an intro plus topics that open on click) and, where
listed, a photo gallery into each page. English is the page text; Italian sits in
data-it so build-it.py can produce the Italian pages.

Sources: the hotel's campaign emails (PDFs), the official site's pages on pools & beach,
kids, rooms, Linfa spa and meetings (as indexed by search engines), and booking-site
listings. Topics marked  # illustrative  are example copy written for this concept site:
check them with the hotel before publishing for real.

Edit, then run:

    python3 tools/about.py && python3 tools/build-it.py
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def a(s):
    return html.escape(s, quote=True)


def T(en, it):
    return (en, it)


PAGES = {
 # ------------------------------------------------------------------ Home
 'index.html': {
  'eb': T('About Villa Maria', 'Su Villa Maria'),
  'h2': T('A four-star hotel &amp; spa <i>above the Adriatic.</i>', 'Un hotel &amp; spa quattro stelle <i>sopra l’Adriatico.</i>'),
  'intro': T('Villa Maria Hotel &amp; Spa is a four-star hotel on the hills of Francavilla al Mare, 5 km from the centre of Pescara. It sits in a 6-hectare park of pines and olive trees with a view over the Adriatic coast, about 15 minutes from Chieti, Pescara and Abruzzo International Airport. Two outdoor pools, the Linfa spa, a padel court and an outdoor gym are inside the park, and a free shuttle takes you to a white-sand beach.',
             'Villa Maria Hotel &amp; Spa è un hotel quattro stelle sulle colline di Francavilla al Mare, a 5 km dal centro di Pescara. Si trova in un parco di 6 ettari tra pini e ulivi, con vista sulla costa adriatica, a circa 15 minuti da Chieti, Pescara e dall’Aeroporto Internazionale d’Abruzzo. Nel parco ci sono due piscine all’aperto, la spa Linfa, un campo da padel e una palestra all’aperto, e una navetta gratuita ti porta su una spiaggia di sabbia bianca.'),
  'topics': [
   (T('The hotel and its park', 'L’hotel e il parco'), [
     T('A 6-hectare park to walk or jog in, among pines and olive groves, with the Adriatic coast in view from the hill. Inside it are the two outdoor pools, the new padel court between the pools and an outdoor fitness area with Technogym equipment.',
       'Un parco di 6 ettari dove passeggiare o correre, tra pini e ulivi, con la costa adriatica in vista dalla collina. Al suo interno ci sono le due piscine all’aperto, il nuovo campo da padel tra le piscine e un’area fitness all’aperto con attrezzature Technogym.')]),
   (T('Rooms and suites', 'Camere e suite'), [
     T('Standard, Superior and Deluxe rooms, Junior Suites, Family Rooms, the Mini SPA Suite and the Master SPA Suite, plus the Cottage for guests travelling with a pet. Every room has free Wi-Fi, air conditioning, satellite TV, a safe, a hairdryer, a wellness kit and spa access.',
       'Camere Standard, Superior e Deluxe, Junior Suite, Family Room, Mini SPA Suite e Master SPA Suite, più il Cottage per chi viaggia con un animale. Ogni camera ha Wi-Fi gratuito, aria condizionata, TV satellitare, cassaforte, asciugacapelli, kit benessere e accesso alla spa.')]),
   (T('For families', 'Per le famiglie'), [
     T('In July and August the Kids Club has a play room with games, books and puzzles, educational workshops from Tuesday to Saturday and an outdoor play area. The Riviera Pool is made for children: no deeper than 50 cm, with a twelve-jet fountain and a water umbrella. Family Rooms give everyone privacy and comfort.',
       'A luglio e agosto il Kids Club offre una sala giochi con giochi, libri e puzzle, laboratori didattici dal martedì al sabato e un’area giochi all’aperto. La Riviera Pool è pensata per i bambini: profonda al massimo 50 cm, con fontana a dodici getti e ombrello d’acqua. Le Family Room danno a tutti privacy e comfort.')]),
   (T('For business travel', 'Per i viaggi di lavoro'), [
     T('Five conference rooms, from small meetings to plenary sessions, with video-conferencing and fast Wi-Fi, 15 minutes from Abruzzo Airport, Chieti and Pescara. The day can end in the spa, in the outdoor gym or on the padel court.',
       'Cinque sale congressi, dalle riunioni ristrette alle plenarie, con videoconferenza e Wi-Fi veloce, a 15 minuti da Aeroporto d’Abruzzo, Chieti e Pescara. La giornata può finire in spa, nella palestra all’aperto o sul campo da padel.')]),
   (T('Wellness and food', 'Benessere e cucina'), [
     T('The Linfa wellness centre has indoor and outdoor pools with hydromassage points, saunas, a Turkish bath, emotional showers, a herbal tea corner and a private garden, with a free two-hour session for hotel guests. Breakfast is served from 7:00 to 10:00, lunch from 12:30 to 14:00 and dinner from 19:30 to 22:00.',
       'Il centro benessere Linfa ha piscine interna ed esterna con punti idromassaggio, saune, bagno turco, docce emozionali, angolo tisane e giardino privato, con una sessione gratuita di due ore per gli ospiti. La colazione è servita dalle 7:00 alle 10:00, il pranzo dalle 12:30 alle 14:00 e la cena dalle 19:30 alle 22:00.')]),
   (T('Pets welcome', 'Animali benvenuti'), [
     T('Pets of all sizes are welcome. The Cottage, at the hotel entrance with its own door, has a fully fenced outdoor area just for them. A supplement applies: tell us when you book.',
       'Gli animali di ogni taglia sono benvenuti. Il Cottage, all’ingresso dell’hotel con entrata indipendente, ha un’area esterna completamente recintata solo per loro. È previsto un supplemento: diccelo quando prenoti.')]),
  ],
  'gallery': [
   ('villa-adriatic.jpg', T('Villa Maria above the Adriatic', 'Villa Maria sopra l’Adriatico')),
   ('pool-park.jpg', T('The Blue Pool in the park', 'La Blue Pool nel parco')),
   ('pool-fountain.jpg', T('Fountain and pool area', 'Fontana e area piscina')),
   ('garden-gazebo.jpg', T('The gazebo in the garden', 'Il gazebo in giardino')),
   ('suite-terrace.jpg', T('Suite terrace with sea view', 'Terrazza della suite con vista mare')),
   ('reception.jpg', T('Reception', 'Reception')),
   ('restaurant-hall.jpg', T('The restaurant', 'Il ristorante')),
   ('spa-whirlpool.jpg', T('Linfa spa', 'Spa Linfa')),
   ('meeting-hall.jpg', T('Meeting room', 'Sala riunioni')),
  ],
 },
 # ------------------------------------------------------------------ Rooms
 'rooms.html': {
  'eb': T('About our rooms', 'Le nostre camere'),
  'h2': T('Every kind of stay, <i>park or sea.</i>', 'Ogni tipo di soggiorno, <i>parco o mare.</i>'),
  'intro': T('Villa Maria has rooms for every kind of stay, from a Standard room for a short visit to the Master SPA Suite with its own sauna. Rooms face the park or the Adriatic, and most are in the central building with direct access to the Linfa spa from your floor.',
             'Villa Maria ha camere per ogni tipo di soggiorno, dalla Standard per una visita breve alla Master SPA Suite con la sua sauna. Le camere guardano il parco o l’Adriatico e la maggior parte è nel corpo centrale, con accesso diretto alla spa Linfa dal piano.'),
  'topics': [
   (T('Standard rooms', 'Camere Standard'), [
     T('A simple, functional room with a park view, in a quiet part of the hotel reached along the corridor past the winter garden. It is not directly connected to the spa: you reach it through reception. Ideal for a short stay on a budget.',
       'Una camera sobria e funzionale con vista sul parco, in una zona tranquilla dell’hotel raggiungibile dal corridoio oltre il giardino d’inverno. Non è collegata direttamente alla spa: si accede dalla reception. Ideale per un soggiorno breve a budget contenuto.')]),
   (T('Superior rooms', 'Camere Superior'), [
     T('In the main building near the spa, with direct access from your floor and a view of the pine trees in the park or of the sea in the distance.',
       'Nel corpo centrale vicino alla spa, con accesso diretto dal piano e vista sui pini del parco o sul mare in lontananza.')]),
   (T('Deluxe rooms', 'Camere Deluxe'), [
     T('In the central building with direct spa access. Most have a terrace looking at the sea or the pine forest, and each comes with a double bed or two single beds.',
       'Nel corpo centrale con accesso diretto alla spa. La maggior parte ha una terrazza sul mare o sulla pineta, e ognuna è disponibile con letto matrimoniale o due letti singoli.')]),
   (T('Junior Suites', 'Junior Suite'), [
     T('In the central building, with a sleeping area and a separate sitting area, a terrace over the sea or the park, and direct access to the spa by lift.',
       'Nel corpo centrale, con zona notte e zona soggiorno separate, terrazza sul mare o sul parco e accesso diretto alla spa in ascensore.')]),
   (T('Family Rooms', 'Family Room'), [
     T('The ideal solution for families who want total privacy and maximum comfort. Tell us who is coming and we will suggest the right layout.',
       'La soluzione ideale per le famiglie che vogliono privacy totale e il massimo comfort. Dicci chi viene e ti suggeriamo la sistemazione giusta.')]),
   (T('Mini SPA and Master SPA Suites', 'Mini SPA e Master SPA Suite'), [
     T('The Mini SPA Suite has a hydromassage tub for two inside the room and a sea-view terrace with a solarium. The Master SPA Suite has two rooms, a sauna for two and a large corner terrace with a solarium and a heated mini jacuzzi, facing east and fully private.',
       'La Mini SPA Suite ha una vasca idromassaggio di coppia in camera e una terrazza vista mare con solarium. La Master SPA Suite ha due ambienti, una sauna di coppia e una grande terrazza ad angolo con solarium e mini jacuzzi riscaldata, esposta a est e riservata.')]),
   (T('The Cottage, for guests with pets', 'Il Cottage, per chi viaggia con animali'), [
     T('A small annex at the hotel entrance with its own entrance, about 39 m², with a fully fenced outdoor area for pets of all sizes. Inside: air conditioning, a coffee machine, a kitchenette with microwave, LCD TV, Wi-Fi, an iron and board and a park view. Laundry service on request.',
       'Una piccola dépendance all’ingresso dell’hotel con entrata indipendente, di circa 39 m², con un’area esterna completamente recintata per animali di ogni taglia. All’interno: aria condizionata, macchina del caffè, angolo cottura con microonde, TV LCD, Wi-Fi, ferro e asse da stiro e vista sul parco. Servizio lavanderia su richiesta.')]),
   (T('In every room', 'In tutte le camere'), [
     T('Free Wi-Fi, air conditioning, satellite TV, a safe, a hairdryer, a wellness kit and spa access. The minibar is charged.',
       'Wi-Fi gratuito, aria condizionata, TV satellitare, cassaforte, asciugacapelli, kit benessere e accesso alla spa. Il minibar è a pagamento.')]),
  ],
  'gallery': [],  # no gallery: the room cards above already show the photos
 },
 # ------------------------------------------------------------------ Spa
 'spa.html': {
  'eb': T('About the Linfa spa', 'La spa Linfa'),
  'h2': T('Your own space <i>to unwind.</i>', 'Il tuo spazio <i>per rilassarti.</i>'),
  'intro': T('Linfa is the hotel’s wellness centre. Its relaxation area has indoor and outdoor pools with several hydromassage points, a whirlpool, saunas, a Turkish bath, chromotherapy and aromatherapy showers with water jets and a waterfall, a herbal tea corner and a private garden. Every hotel guest gets a free two-hour session; booking is required.',
             'Linfa è il centro benessere dell’hotel. L’area relax ha piscine interna ed esterna con diversi punti idromassaggio, vasca idromassaggio, saune, bagno turco, docce di cromoterapia e aromaterapia con getti d’acqua e cascata, angolo tisane e giardino privato. Ogni ospite dell’hotel ha una sessione gratuita di due ore; la prenotazione è obbligatoria.'),
  'topics': [
   (T('The relaxation area', 'L’area relax'), [
     T('A visit lasts two hours and includes the indoor and outdoor pools with hydromassage points, the whirlpool, the saunas, the Turkish bath, the emotional showers, the herbal tea corner and the private garden.',
       'L’ingresso dura due ore e comprende le piscine interna ed esterna con punti idromassaggio, la vasca idromassaggio, le saune, il bagno turco, le docce emozionali, l’angolo tisane e il giardino privato.')]),
   (T('Your free two-hour session', 'La tua sessione gratuita di due ore'), [
     T('Every hotel guest can enjoy two hours in the relaxation area at no extra cost. Book your time at reception, call the spa on +39 085 45 00 55 60 or write to benessere@hvillamaria.it, especially in high season.',
       'Ogni ospite dell’hotel può godere di due ore nell’area relax senza costi aggiuntivi. Prenota l’orario in reception, chiama la spa al +39 085 45 00 55 60 o scrivi a benessere@hvillamaria.it, soprattutto in alta stagione.')]),
   (T('Opening hours', 'Orari di apertura'), [
     T('Monday to Thursday 10:00–21:00, Friday 10:00–23:30, Saturday 9:00–23:30, Sunday 9:00–21:00. Hours can change with the season, so check with the spa before you go.',
       'Dal lunedì al giovedì 10:00–21:00, venerdì 10:00–23:30, sabato 9:00–23:30, domenica 9:00–21:00. Gli orari possono cambiare con la stagione: verifica con la spa prima di andare.')]),
   (T('Massages and treatments', 'Massaggi e trattamenti'), [
     T('Massages and beauty treatments for one or for two. Couple massages take place at the same time in two separate cabins. Wellness paths combine the spa with a massage, such as a volcanic hot-stone back massage.',
       'Massaggi e trattamenti beauty per uno o per due. I massaggi di coppia si svolgono in contemporanea in due cabine separate. I percorsi benessere abbinano la spa a un massaggio, come il massaggio alla schiena con pietre vulcaniche calde.')]),
   (T('Private SPA for two', 'SPA privata per due'), [
     T('A private spa in the Master SPA Suite: a sauna for two, a heated mini jacuzzi on the terrace and a solarium over the sea. Some packages add a couple massage and an aperitif on the sea-view terrace.',
       'Una spa privata nella Master SPA Suite: sauna di coppia, mini jacuzzi riscaldata in terrazza e solarium sul mare. Alcuni pacchetti aggiungono un massaggio di coppia e un aperitivo sulla terrazza vista mare.')]),
   (T('Fitness', 'Fitness'), [
     T('An outdoor fitness area with Technogym equipment among the trees of the park, with a view of the sea, and the padel court between the two pools.',
       'Un’area fitness all’aperto con attrezzature Technogym tra gli alberi del parco, con vista mare, e il campo da padel tra le due piscine.')]),
   (T('Spa in your package', 'La spa nel tuo pacchetto'), [
     T('Spa access is included in the Family Discount and in the Executive Business Stay Package. Beyond the Meeting Room ends the match with sauna, spa and a massage.',
       'L’accesso alla spa è incluso nello Sconto Famiglia e nel Pacchetto Executive Business Stay. Beyond the Meeting Room chiude la partita con sauna, spa e massaggio.')]),
  ],
  'gallery': [
   ('spa.jpg', T('Indoor pool', 'Piscina interna')),
   ('spa-whirlpool.jpg', T('Hydromassage pool with a view of the park', 'Piscina idromassaggio con vista sul parco')),
   ('sauna.jpg', T('Sauna', 'Sauna')),
   ('wellness.jpg', T('Indoor pool with a sea view', 'Piscina interna con vista mare')),
   ('walk.jpg', T('Terrace with a plunge pool and sea view', 'Terrazza con piscinetta e vista mare')),
  ],
 },
 # ------------------------------------------------------------------ Restaurant
 'restaurant.html': {
  'eb': T('About the restaurant', 'Il ristorante'),
  'h2': T('Abruzzo <i>at every meal.</i>', 'L’Abruzzo <i>a ogni pasto.</i>'),
  'intro': T('The restaurant looks out over the hotel’s centuries-old park, with a sea-view terrace for summer evenings and events. The kitchen cooks Italian dishes and Abruzzo specialities with local products, from breakfast to dinner.',
             'Il ristorante guarda il parco secolare dell’hotel, con una terrazza vista mare per le serate d’estate e gli eventi. La cucina propone piatti italiani e specialità abruzzesi con prodotti locali, dalla colazione alla cena.'),
  'topics': [
   (T('Opening times', 'Orari'), [
     T('Breakfast 7:00–10:00 on the ground floor, and on the terrace in the warmer months. Lunch 12:30–14:00, dinner 19:30–22:00. The bar is open from 10:00 to 23:00. Times can change with the season.',
       'Colazione 7:00–10:00 al piano terra, e in terrazza nei mesi più caldi. Pranzo 12:30–14:00, cena 19:30–22:00. Il bar è aperto dalle 10:00 alle 23:00. Gli orari possono cambiare con la stagione.')]),
   (T('Breakfast', 'Colazione'), [
     T('A buffet with fresh fruit, cakes, pastries and savoury dishes, included in our packages. Business guests can have it early, before the first call.',
       'Un buffet con frutta fresca, torte, dolci e piatti salati, incluso nei pacchetti. Chi viaggia per lavoro può farla presto, prima della prima call.')]),
   (T('Lunch and dinner', 'Pranzo e cena'), [
     T('À la carte Italian cuisine and Abruzzo specialities, served in the dining room or on the terrace. Long family dinners and quiet business dinners both have their place.',
       'Cucina italiana à la carte e specialità abruzzesi, servite in sala o in terrazza. Lunghe cene in famiglia e cene di lavoro tranquille hanno entrambe il loro posto.')]),
   (T('The chef’s table', 'La tavola dello chef'), [
     T('For a special evening, or the dinner after a padel match, the chef’s table is where conversations last and deals are made.',
       'Per una serata speciale, o la cena dopo una partita di padel, la tavola dello chef è dove le conversazioni durano e nascono gli accordi.')]),
   (T('The terrace and events', 'La terrazza e gli eventi'), [
     T('The sea-view terrace hosts aperitifs, celebrations and events. Ask us about a private dinner or a party for your group.',
       'La terrazza vista mare ospita aperitivi, feste ed eventi. Chiedici una cena privata o una festa per il tuo gruppo.')]),
   (T('The beach and the trabocchi', 'La spiaggia e i trabocchi'), [
     T('Our partner lido on the beach has its own bar and restaurant for lunches on the sand and summer evenings. Further south, along the Costa dei Trabocchi, the old fishing platforms over the sea serve fish dishes such as brodetto: ask us to book a table.',
       'Il lido convenzionato in spiaggia ha il suo bar e ristorante per pranzi sulla sabbia e serate d’estate. Più a sud, lungo la Costa dei Trabocchi, le antiche macchine da pesca sul mare servono piatti di pesce come il brodetto: chiedici di prenotare un tavolo.')]),
   (T('La Bottega di Villa Maria', 'La Bottega di Villa Maria'), [
     T('Our corner of local products and Abruzzo flavours, to taste during your stay and take a little of the region home.',
       'Il nostro angolo di prodotti locali e sapori abruzzesi, da gustare durante il soggiorno e da portare un po’ a casa.')]),
   (T('Allergies and reservations', 'Allergie e prenotazioni'), [
     T('Tell us about allergies or diets when you book, or send us a message. To reserve a table, call +39 085 45 00 51.',
       'Segnalaci allergie o diete quando prenoti, o scrivici un messaggio. Per prenotare un tavolo chiama il +39 085 45 00 51.')]),
  ],
  'gallery': [
   ('restaurant-hall.jpg', T('The dining room', 'La sala')),
   ('restaurant-dinner.jpg', T('Dinner with a view', 'Cena con vista')),
   ('breakfast.jpg', T('Breakfast buffet', 'Colazione a buffet')),
   ('chef-dinner.jpg', T('The chef’s dishes', 'I piatti dello chef')),
   ('bar.jpg', T('The bar', 'Il bar')),
  ],
 },
 # ------------------------------------------------------------------ Getting here
 'contact.html': {
  'eb': T('Plan your arrival', 'Pianifica l’arrivo'),
  'h2': T('Easy to reach, <i>quiet when you arrive.</i>', 'Facile da raggiungere, <i>tranquillo all’arrivo.</i>'),
  'intro': T('Villa Maria is in Contrada Pretaro, on the hill above Francavilla al Mare: 5 km from the centre of Pescara and about 15 minutes from Chieti, Pescara and Abruzzo International Airport, yet outside the city and its traffic.',
             'Villa Maria è in Contrada Pretaro, sulla collina sopra Francavilla al Mare: a 5 km dal centro di Pescara e a circa 15 minuti da Chieti, Pescara e dall’Aeroporto Internazionale d’Abruzzo, ma fuori dalla città e dal traffico.'),
  'topics': [
   (T('By plane', 'In aereo'), [
     T('Abruzzo International Airport (Pescara) is about 15 minutes away by car. Ask us about a transfer when you book.',
       'L’Aeroporto Internazionale d’Abruzzo (Pescara) è a circa 15 minuti d’auto. Chiedici un transfer quando prenoti.')]),
   (T('By train', 'In treno'), [
     T('Pescara Centrale station has easy rail connections along the Adriatic line and to Rome. From the station, take a taxi or ask us about a transfer.',
       'La stazione di Pescara Centrale ha comodi collegamenti sulla linea adriatica e verso Roma. Dalla stazione prendi un taxi o chiedici un transfer.')]),
   (T('By car', 'In auto'), [
     T('Leave the A14 at the Pescara Sud – Francavilla exit and follow the signs for Francavilla al Mare and Contrada Pretaro. Free outdoor parking with charging points for electric cars is waiting at the hotel.',
       'Esci dall’A14 a Pescara Sud – Francavilla e segui le indicazioni per Francavilla al Mare e Contrada Pretaro. In hotel ti aspetta il parcheggio gratuito all’aperto con colonnine di ricarica per auto elettriche.')]),
   (T('The beach shuttle', 'La navetta per la spiaggia'), [
     T('A free shuttle takes you to our partner lido on a white-sand beach in Francavilla al Mare, with a bar and restaurant on the sand.',
       'Una navetta gratuita ti porta al lido convenzionato su una spiaggia di sabbia bianca a Francavilla al Mare, con bar e ristorante sulla sabbia.')]),
   (T('Who to contact', 'Chi contattare'), [
     T('Reception: +39 085 45 00 51, info@hvillamaria.it. Reservations: reservation@hvillamaria.it. Meetings and events: +39 085 45 00 55 07, congressi@hvillamaria.it. Linfa spa: +39 085 45 00 55 60, benessere@hvillamaria.it.',
       'Reception: +39 085 45 00 51, info@hvillamaria.it. Prenotazioni: reservation@hvillamaria.it. Meeting ed eventi: +39 085 45 00 55 07, congressi@hvillamaria.it. Spa Linfa: +39 085 45 00 55 60, benessere@hvillamaria.it.')]),
   (T('Arrival and check-in', 'Arrivo e check-in'), [
     T('Your check-in and check-out times are in your booking confirmation. Tell us your expected arrival time when you book, and ask if you need an early check-in or a late check-out.',
       'Gli orari di check-in e check-out sono nella conferma di prenotazione. Indicaci l’orario di arrivo quando prenoti e chiedici se ti serve un check-in anticipato o un check-out posticipato.')]),
  ],
  'gallery': [
   ('gardens.jpg', T('The gardens', 'I giardini')),
   ('villa-adriatic.jpg', T('The hotel and the sea', 'L’hotel e il mare')),
   ('reception.jpg', T('Reception', 'Reception')),
   ('garden-gazebo.jpg', T('The gazebo', 'Il gazebo')),
   ('walk.jpg', T('Terrace with a sea view', 'Terrazza con vista mare')),
  ],
 },
 # ------------------------------------------------------------------ Activities (new page)
 'activities.html': {
  'eb': T('Things to do', 'Cosa fare'),
  'h2': T('Water, wellness <i>and the open air.</i>', 'Acqua, benessere <i>e aria aperta.</i>'),
  'intro': T('Days at Villa Maria can be as busy or as slow as you like: two pools in a 6-hectare park, the beach by shuttle, the Linfa spa, padel and an outdoor gym, a Kids Club in summer, and the hills, coast and towns of Abruzzo all within easy reach.',
             'Le giornate a Villa Maria possono essere piene o lente quanto vuoi: due piscine in un parco di 6 ettari, la spiaggia con la navetta, la spa Linfa, il padel e una palestra all’aperto, un Kids Club d’estate e colline, costa e borghi d’Abruzzo a portata di mano.'),
  'topics': [
   (T('Swimming pools', 'Piscine'), [
     T('Two outdoor pools in the park, among pines and olive trees. The Blue Pool, up to 2.5 metres deep, is for a real swim and is open until 15 September. The Riviera Pool is made for children: no deeper than 50 cm, with a twelve-jet fountain, a water umbrella and hydromassage points, open until 30 September.',
       'Due piscine all’aperto nel parco, tra pini e ulivi. La Blue Pool, profonda fino a 2,5 metri, è per nuotare davvero ed è aperta fino al 15 settembre. La Riviera Pool è pensata per i bambini: profonda al massimo 50 cm, con fontana a dodici getti, ombrello d’acqua e punti idromassaggio, aperta fino al 30 settembre.')]),
   (T('The beach', 'La spiaggia'), [
     T('A free shuttle takes you to a white-sand beach in Francavilla al Mare, at a private lido with a special agreement with the hotel. The lido has a bar and a restaurant for lunches on the beach, aperitifs and evening events.',
       'Una navetta gratuita ti porta su una spiaggia di sabbia bianca a Francavilla al Mare, in un lido privato convenzionato con l’hotel. Il lido ha bar e ristorante per pranzi in spiaggia, aperitivi ed eventi serali.')]),
   (T('Kids Club', 'Kids Club'), [
     T('In July and August: a play room with games, books and puzzles, the Riviera Pool, educational workshops from Tuesday to Saturday and an outdoor play area.',
       'A luglio e agosto: sala giochi con giochi, libri e puzzle, la Riviera Pool, laboratori didattici dal martedì al sabato e un’area giochi all’aperto.')]),
   (T('Linfa wellness &amp; spa', 'Benessere e spa Linfa'), [
     T('Indoor and outdoor pools with hydromassage points, saunas, a Turkish bath and emotional showers. Hotel guests enjoy a free two-hour spa session; booking is required.',
       'Piscine interna ed esterna con punti idromassaggio, saune, bagno turco e docce emozionali. Gli ospiti dell’hotel hanno una sessione spa gratuita di due ore; la prenotazione è obbligatoria.')]),
   (T('Padel', 'Padel'), [
     T('The new padel court is in the park, between the two pools. Book a slot for a family match or bring a client: Beyond the Meeting Room pairs the game with the spa, an aperitivo and dinner.',
       'Il nuovo campo da padel è nel parco, tra le due piscine. Prenota un orario per una partita in famiglia o porta un cliente: Beyond the Meeting Room abbina la partita a spa, aperitivo e cena.')]),
   (T('Outdoor gym and the park', 'Palestra all’aperto e parco'), [
     T('An outdoor fitness area with Technogym equipment among the trees, with a view of the sea, and 6 hectares of park to walk or jog in.',
       'Un’area fitness all’aperto con attrezzature Technogym tra gli alberi, con vista mare, e 6 ettari di parco dove passeggiare o correre.')]),
   (T('Cycling the coast', 'In bici lungo la costa'), [
     T('The Bike to Coast cycle and pedestrian path runs along the Abruzzo coast towards the Costa dei Trabocchi, a few minutes from the hotel.',
       'La pista ciclopedonale Bike to Coast corre lungo la costa abruzzese verso la Costa dei Trabocchi, a pochi minuti dall’hotel.')]),
   (T('Abruzzo Experience', 'Abruzzo Experience'), [
     T('Guided excursions with transfers, also in English and German: the Majella and Gran Sasso national parks, the trabocchi coast, Chieti and Pescara. Ask us what is running during your stay.',
       'Escursioni guidate con transfer, anche in inglese e tedesco: i parchi nazionali della Majella e del Gran Sasso, la costa dei trabocchi, Chieti e Pescara. Chiedici cosa è in programma durante il tuo soggiorno.')]),
   (T('Days out with children', 'Gite con i bambini'), [
     T('Two favourites with families: the Guardiagrele adventure park, with tree-top trails in the woods at the foot of the Majella, and the zoo in Lanciano.',
       'Due preferiti dalle famiglie: il parco avventura di Guardiagrele, con percorsi tra gli alberi ai piedi della Majella, e lo zoo di Lanciano.')]),
  ],
  'gallery': [
   ('pool-park.jpg', T('The Blue Pool', 'La Blue Pool')),
   ('pool-fountain.jpg', T('Fountain and pool area', 'Fontana e area piscina')),
   ('people/moment-pool.jpg', T('Pool days with the family', 'Giornate in piscina in famiglia')),
   ('spa-whirlpool.jpg', T('Linfa spa', 'Spa Linfa')),
   ('sauna.jpg', T('Sauna', 'Sauna')),
   ('people/business-padel.jpg', T('Padel in the garden', 'Padel in giardino')),
   ('garden-gazebo.jpg', T('The gazebo in the park', 'Il gazebo nel parco')),
   ('gardens.jpg', T('Shade in the gardens', 'Ombra nei giardini')),
   ('walk.jpg', T('Terrace with a sea view', 'Terrazza con vista mare')),
  ],
 },
 # ------------------------------------------------------------------ Italian Memories
 'italian-memories.html': {
  'eb': T('About Italian Memories', 'Italian Memories'),
  'h2': T('A family holiday <i>that feels easy.</i>', 'Una vacanza in famiglia <i>senza fatica.</i>'),
  'intro': T('Italian Memories is our promise to families: we take care of the details so you can take care of each other. Here is what a stay looks like, from the first swim to the last dinner.',
             'Italian Memories è la nostra promessa alle famiglie: pensiamo noi ai dettagli, così potete prendervi cura gli uni degli altri. Ecco com’è un soggiorno, dal primo tuffo all’ultima cena.'),
  'topics': [
   (T('Pools for every age', 'Piscine per ogni età'), [
     T('The Blue Pool and the Riviera Pool sit in the private park. The Riviera Pool is made for children, no deeper than 50 cm, with water games; teenagers get the Blue Pool to swim and play.',
       'La Blue Pool e la Riviera Pool sono nel parco privato. La Riviera Pool è pensata per i bambini, profonda al massimo 50 cm, con giochi d’acqua; i ragazzi hanno la Blue Pool per nuotare e giocare.')]),
   (T('The beach, without the hassle', 'La spiaggia, senza pensieri'), [
     T('A free shuttle runs to our partner lido on a white-sand beach in Francavilla al Mare, with a bar and restaurant for lunch on the sand.',
       'Una navetta gratuita porta al lido convenzionato su una spiaggia di sabbia bianca a Francavilla al Mare, con bar e ristorante per pranzare sulla sabbia.')]),
   (T('Play room and Kids Club', 'Sala giochi e Kids Club'), [
     T('Games, books, colouring and puzzles in the play room, and the whole park to explore. Parents can slip away to the spa while children play.',
       'Giochi, libri, colori e puzzle nella sala giochi, e tutto il parco da esplorare. I genitori possono concedersi la spa mentre i bambini giocano.')]),
   (T('Time for parents', 'Tempo per i genitori'), [
     T('Every hotel guest has a free two-hour session in the Linfa spa: hydromassage pool, Turkish bath, sauna and sensory shower. Treatments for one or two can be added.',
       'Ogni ospite ha una sessione gratuita di due ore nella spa Linfa: piscina idromassaggio, bagno turco, sauna e doccia emozionale. Si possono aggiungere trattamenti per uno o per due.')]),
   (T('Days out together', 'Gite insieme'), [
     T('The Guardiagrele adventure park, the zoo in Lanciano, the pinewood of the Pineta Dannunziana and bike rides along the coast: easy trips that become family stories.',
       'Il parco avventura di Guardiagrele, lo zoo di Lanciano, la pineta della Pineta Dannunziana e le pedalate lungo la costa: gite facili che diventano storie di famiglia.')]),
   (T('Long family dinners', 'Lunghe cene in famiglia'), [  # illustrative
     T('Shared plates of Abruzzo recipes on the terrace over the pool, while the children run on the lawn and nobody checks the time.',
       'Piatti abruzzesi da condividere sulla terrazza sopra la piscina, mentre i bambini corrono sul prato e nessuno guarda l’ora.')]),
  ],
 },
 # ------------------------------------------------------------------ Ciao Again
 'ciao-again.html': {
  'eb': T('For returning families', 'Per le famiglie che tornano'),
  'h2': T('Welcome back, <i>it’s good to see you.</i>', 'Bentornati, <i>che piacere rivedervi.</i>'),
  'intro': T('You already know the park, the pools and the table by the garden. Here is what is waiting for you this time, and how we make coming back even easier.',
             'Conoscete già il parco, le piscine e il tavolo sul giardino. Ecco cosa vi aspetta questa volta, e come rendiamo il ritorno ancora più facile.'),
  'topics': [
   (T('Your room, remembered', 'La tua camera, ricordata'), [
     T('Tell us what you liked last time, the view, the floor, the room type, and we will do our best to give it to you again.',
       'Dicci cosa ti è piaciuto l’ultima volta, la vista, il piano, il tipo di camera, e faremo il possibile per ridartelo.')]),
   (T('What’s new in the spa', 'Le novità della spa'), [
     T('Linfa is organised into relaxation, beauty and fitness areas, with the hydromassage pool, Turkish bath, sauna and sensory shower. Your free two-hour session is waiting; just book your time.',
       'Linfa è organizzata in aree relax, beauty e fitness, con piscina idromassaggio, bagno turco, sauna e doccia emozionale. La tua sessione gratuita di due ore ti aspetta: basta prenotare l’orario.')]),
   (T('La Bottega di Villa Maria', 'La Bottega di Villa Maria'), [
     T('Local products and Abruzzo flavours to taste during your stay and take home: a little of the region for your kitchen.',
       'Prodotti locali e sapori abruzzesi da gustare durante il soggiorno e da portare a casa: un po’ di regione per la tua cucina.')]),
   (T('New things to try', 'Novità da provare'), [
     T('Padel in the garden for a family match, the beach shuttle to the white-sand lido, and days out to the Guardiagrele adventure park or along the Costa dei Trabocchi.',
       'Il padel in giardino per una partita in famiglia, la navetta per il lido di sabbia bianca e gite al parco avventura di Guardiagrele o lungo la Costa dei Trabocchi.')]),
   (T('10% off when you book again', '10% quando prenoti di nuovo'), [
     T('Book your next stay at the hotel during your visit and get 10% off the room rate, with free cancellation up to 6 months before arrival.',
       'Prenota il prossimo soggiorno in hotel durante la visita e hai il 10% sulla camera, con cancellazione gratuita fino a 6 mesi prima dell’arrivo.')]),
   (T('Loyalty thank-yous', 'Ringraziamenti fedeltà'), [  # illustrative
     T('Returning families receive small thank-yous from us, a welcome treat in the room, news of new seasons first, and moments kept just for our regular guests. Join the community to hear about them.',
       'Le famiglie che tornano ricevono da noi piccoli ringraziamenti, un pensiero di benvenuto in camera, le novità di stagione in anteprima e momenti riservati agli ospiti abituali. Iscriviti alla community per saperne di più.')]),
  ],
 },
 # ------------------------------------------------------------------ Business travel
 'business-travel.html': {
  'eb': T('About business stays', 'Soggiorni di lavoro'),
  'h2': T('Work, meet and recover <i>in one place.</i>', 'Lavora, incontra e recupera <i>in un unico posto.</i>'),
  'intro': T('Villa Maria is a congress hotel as well as a spa hotel: five conference rooms, quiet rooms with a real desk, a restaurant for business dinners and the Linfa spa for the end of the day, all minutes from Pescara.',
             'Villa Maria è un hotel congressuale oltre che un hotel con spa: cinque sale congressi, camere silenziose con una vera scrivania, un ristorante per le cene di lavoro e la spa Linfa per fine giornata, a pochi minuti da Pescara.'),
  'topics': [
   (T('Five conference rooms', 'Cinque sale congressi'), [
     T('From board meetings to plenary sessions, the hotel has five conference rooms, with video-conferencing and fast Wi-Fi. Send us your group size and format and we will propose the right room.',
       'Dal consiglio di amministrazione alla sessione plenaria, l’hotel ha cinque sale congressi, con videoconferenza e Wi-Fi veloce. Inviaci numero di partecipanti e formato e ti proponiamo la sala giusta.')]),
   (T('Events and incentives', 'Eventi e incentive'), [  # illustrative
     T('Product launches, training days and company retreats: we can combine meeting rooms with coffee breaks, lunches on the terrace, padel tournaments and team dinners. Ask for a tailored proposal.',
       'Lanci di prodotto, giornate di formazione e ritiri aziendali: possiamo abbinare sale riunioni, coffee break, pranzi in terrazza, tornei di padel e cene di gruppo. Chiedi una proposta su misura.')]),
   (T('Getting here fast', 'Arrivare in fretta'), [
     T('Abruzzo Airport (Pescara) is a short drive away, Pescara Centrale station has rail links along the Adriatic and to Rome, and the A14 Pescara Sud exit is close. Free private parking on site.',
       'L’aeroporto d’Abruzzo (Pescara) è a pochi minuti d’auto, la stazione di Pescara Centrale è collegata lungo l’Adriatico e verso Roma, e l’uscita A14 Pescara Sud è vicina. Parcheggio privato gratuito in hotel.')]),
   (T('Rooms that work', 'Camere per lavorare'), [
     T('Quiet rooms facing the park or the sea, with a writing desk, power by the bed and high-speed Wi-Fi for video calls. Early breakfast and express check-out keep you on time.',
       'Camere silenziose con vista parco o mare, scrivania, prese vicino al letto e Wi-Fi veloce per le videochiamate. Colazione presto e check-out rapido ti tengono nei tempi.')]),
   (T('After the last meeting', 'Dopo l’ultima riunione'), [
     T('A free two-hour session in the Linfa spa (hydromassage pool, Turkish bath, sauna), a game on the padel court in the garden, and dinner on the terrace.',
       'Una sessione gratuita di due ore nella spa Linfa (piscina idromassaggio, bagno turco, sauna), una partita sul campo da padel in giardino e la cena in terrazza.')]),
  ],
 },
 # ------------------------------------------------------------------ Executive
 'executive-business-stay.html': {
  'eb': T('About the package', 'Il pacchetto'),
  'h2': T('What your stay <i>looks like.</i>', 'Com’è il tuo <i>soggiorno.</i>'),
  'intro': T('The Executive Business Stay Package is built around a working day: a quiet room, breakfast before the first call, a meeting room when you need one and the spa when you are done.',
             'Il Pacchetto Executive Business Stay è pensato intorno a una giornata di lavoro: una camera silenziosa, la colazione prima della prima call, una sala riunioni quando serve e la spa quando hai finito.'),
  'topics': [
   (T('Your room', 'La tua camera'), [
     T('A Superior Room (pine grove or distant sea view) for one or two nights, or a Deluxe Room or Suite with Adriatic views and a lounge area for three nights or more. Every room has a writing desk and fast Wi-Fi.',
       'Una Camera Superior (vista pineta o mare in lontananza) per una o due notti, o una Deluxe o Suite con vista Adriatico e zona lounge per tre notti o più. Ogni camera ha scrivania e Wi-Fi veloce.')]),
   (T('Meeting room on request', 'Sala riunioni su richiesta'), [
     T('Need to meet a client or your team? Book one of our five conference rooms for a few hours, with video-conferencing.',
       'Devi incontrare un cliente o il tuo team? Prenota per qualche ora una delle nostre cinque sale congressi, con videoconferenza.')]),
   (T('Spa, sauna and fitness', 'Spa, sauna e fitness'), [
     T('Your free two-hour Linfa session includes the hydromassage pool, Turkish bath, sauna and sensory shower. The fitness area and the padel court are there if you prefer to move.',
       'La sessione gratuita di due ore a Linfa include piscina idromassaggio, bagno turco, sauna e doccia emozionale. Area fitness e campo da padel ti aspettano se preferisci muoverti.')]),
   (T('Invoicing and company rates', 'Fatturazione e tariffe aziendali'), [
     T('We invoice your company directly and welcome corporate cards. Companies and meeting delegations can ask for corporate and group rates; if you have a company code, add it when you book.',
       'Fatturiamo direttamente alla tua azienda e accettiamo carte aziendali. Aziende e delegazioni possono chiedere tariffe aziendali e di gruppo; se hai un codice aziendale, inseriscilo quando prenoti.')]),
   (T('A typical day', 'Una giornata tipo'), [  # illustrative
     T('Breakfast at 6:30, a video call from your room, a client meeting at 10:00, lunch on the terrace, a padel match and a massage at 18:30, dinner at the chef’s table at 21:00.',
       'Colazione alle 6:30, una videochiamata dalla camera, riunione con il cliente alle 10:00, pranzo in terrazza, padel e massaggio alle 18:30, cena alla tavola dello chef alle 21:00.')]),
  ],
 },
 # ------------------------------------------------------------------ Padel
 'beyond-the-meeting-room.html': {
  'eb': T('About Beyond the Meeting Room', 'Beyond the Meeting Room'),
  'h2': T('The court, the spa <i>and the table.</i>', 'Il campo, la spa <i>e la tavola.</i>'),
  'intro': T('Padel is played in doubles, easy to learn and impossible to play in silence. Our court is in the garden above the Adriatic, and the evening continues in the spa, at the bar and at the chef’s table.',
             'Il padel si gioca in doppio, si impara in fretta ed è impossibile giocarlo in silenzio. Il nostro campo è in giardino sopra l’Adriatico, e la serata continua in spa, al bar e alla tavola dello chef.'),
  'topics': [
   (T('The court', 'Il campo'), [
     T('A padel court in the hotel garden, surrounded by greenery. Book your slot at reception or add it to your booking request.',
       'Un campo da padel nel giardino dell’hotel, circondato dal verde. Prenota l’orario in reception o aggiungilo alla richiesta di prenotazione.')]),
   (T('New to padel?', 'Mai giocato a padel?'), [  # illustrative
     T('No problem: rackets and balls can be arranged, and the rules take ten minutes to learn. A short lesson can be organised on request so everyone enjoys the first match.',
       'Nessun problema: racchette e palline si possono organizzare e le regole si imparano in dieci minuti. Su richiesta si può organizzare una breve lezione perché tutti si godano la prima partita.')]),
   (T('Recovery in the Linfa spa', 'Recupero nella spa Linfa'), [
     T('After the match: hydromassage pool, Turkish bath, sauna and sensory shower, with a free two-hour session for hotel guests. Add a massage for the full ritual.',
       'Dopo la partita: piscina idromassaggio, bagno turco, sauna e doccia emozionale, con una sessione gratuita di due ore per gli ospiti. Aggiungi un massaggio per il rituale completo.')]),
   (T('Aperitivo and dinner', 'Aperitivo e cena'), [
     T('Winners pay for the aperitivo at the bar; then dinner at the chef’s table, with Abruzzo specialities and a quiet corner for business talk.',
       'Chi vince offre l’aperitivo al bar; poi cena alla tavola dello chef, con specialità abruzzesi e un angolo tranquillo per parlare di lavoro.')]),
   (T('Team days and tournaments', 'Giornate di team e tornei'), [  # illustrative
     T('Bring your team: a padel round-robin in the afternoon, a meeting room in the morning and a group dinner make a simple, memorable company day.',
       'Porta il tuo team: un torneo di padel nel pomeriggio, una sala riunioni al mattino e una cena di gruppo fanno una giornata aziendale semplice e memorabile.')]),
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
    if not p.get('gallery'):
        return ''
    items = '\n'.join(
        f'<figure><a class="g-item" href="assets/img/{f}" data-caption="{a(cap[0])}" data-it-caption="{a(cap[1])}">'
        f'<img src="assets/img/{f}" alt="{a(cap[0])}" data-it-alt="{a(cap[1])}" loading="lazy"></a>'
        f'<figcaption data-it="{a(cap[1])}">{cap[0]}</figcaption></figure>'
        for f, cap in p['gallery'])
    return ('<section class="section white gallery-sec" id="gallery">\n<div class="wrap">\n'
            '<div class="head"><div><p class="eb" data-it="Galleria">Gallery</p>\n'
            '<h2 class="h2" data-it="Guarda <i>prima di arrivare.</i>">See it <i>before you arrive.</i></h2></div></div>\n'
            f'<div class="gallery">\n{items}\n</div>\n</div>\n</section>\n')


# ---------------------------------------------------------------------------------
# Showcase carousels (replace the grid gallery on these pages): each card has its own
# photo slider with ‹ › arrows. Card = (eyebrow, title, text, [(photo, caption)]).
# ---------------------------------------------------------------------------------
P = lambda f, en, it: (f, (en, it))
CARDS = {
 'index.html': [
  (T('Accommodation', 'Sistemazione'), T('Rooms', 'Camere'),
   T('From Standard rooms to the Master SPA Suite, facing the park or the Adriatic.', 'Dalla Standard alla Master SPA Suite, con vista sul parco o sull’Adriatico.'),
   [P('rooms/deluxe-1.jpg', 'Deluxe Room', 'Camera Deluxe'), P('rooms/superior-1.jpg', 'Superior Room', 'Camera Superior'),
    P('rooms/junior-suite-1.jpg', 'Junior Suite', 'Junior Suite'),
    P('suite-terrace.jpg', 'Suite terrace with hot tub', 'Terrazza della suite con idromassaggio'), P('suite-seaview.jpg', 'Sea view from a suite', 'Vista mare da una suite')], 'rooms.html'),
  (T('Wellness', 'Benessere'), T('Linfa wellness &amp; spa', 'Benessere e spa Linfa'),
   T('Hydromassage pool, Turkish bath, sauna and sensory shower, with a free two-hour session for every guest.', 'Piscina idromassaggio, bagno turco, sauna e doccia emozionale, con due ore gratuite per ogni ospite.'),
   [P('spa-whirlpool.jpg', 'Hydromassage pool', 'Piscina idromassaggio'), P('spa.jpg', 'Indoor pool', 'Piscina interna'),
    P('sauna.jpg', 'Sauna', 'Sauna'), P('wellness.jpg', 'Indoor pool with a sea view', 'Piscina interna con vista mare')], 'spa.html'),
  (T('Dining', 'Ristorante'), T('Restaurant &amp; bar', 'Ristorante e bar'),
   T('Italian cuisine and Abruzzo specialities, on the terrace over the pool or at the chef’s table.', 'Cucina italiana e specialità abruzzesi, in terrazza sulla piscina o alla tavola dello chef.'),
   [P('restaurant-hall.jpg', 'The dining room', 'La sala'), P('restaurant-dinner.jpg', 'Dinner with a view', 'Cena con vista'),
    P('chef-dinner.jpg', 'The chef’s dishes', 'I piatti dello chef'), P('breakfast.jpg', 'Breakfast buffet', 'Colazione a buffet'), P('bar.jpg', 'The bar', 'Il bar')], 'restaurant.html'),
  (T('Outdoors', 'All’aperto'), T('Pools &amp; park', 'Piscine e parco'),
   T('The Blue Pool and the Riviera Pool, made for children, in a 6-hectare park.', 'La Blue Pool e la Riviera Pool, pensata per i bambini, in un parco di 6 ettari.'),
   [P('pool-park.jpg', 'The Blue Pool', 'La Blue Pool'), P('pool-fountain.jpg', 'Fountain and pool area', 'Fontana e area piscina'),
    P('people/moment-pool.jpg', 'Pool days with the family', 'Giornate in piscina in famiglia'), P('garden-gazebo.jpg', 'The gazebo', 'Il gazebo')], 'activities.html'),
  (T('Business', 'Business'), T('Meetings &amp; events', 'Meeting ed eventi'),
   T('Five conference rooms, from small meetings to an auditorium, with video-conferencing.', 'Cinque sale congressi, dalle riunioni ristrette all’auditorium, con videoconferenza.'),
   [P('meeting-hall.jpg', 'Meeting room', 'Sala riunioni'), P('auditorium.jpg', 'Auditorium', 'Auditorium'),
    P('meeting-room.jpg', 'Private meeting room', 'Sala riservata'), P('people/business-meeting.jpg', 'A working session', 'Una sessione di lavoro')], 'business-travel.html'),
  (T('Sport', 'Sport'), T('Padel &amp; gardens', 'Padel e giardini'),
   T('A padel court in the garden, shady lawns and terraces with a view of the sea.', 'Un campo da padel in giardino, prati all’ombra e terrazze con vista mare.'),
   [P('people/business-padel.jpg', 'Padel in the garden', 'Padel in giardino'), P('gardens.jpg', 'The gardens', 'I giardini'),
    P('walk.jpg', 'Terrace with a sea view', 'Terrazza con vista mare')], 'beyond-the-meeting-room.html'),
 ],
 'spa.html': [
  (T('Relaxation area', 'Area relax'), T('Water &amp; warmth', 'Acqua e calore'),
   T('Indoor and outdoor pools with hydromassage points, saunas and a Turkish bath.', 'Piscine interna ed esterna con punti idromassaggio, saune e bagno turco.'),
   [P('spa-whirlpool.jpg', 'Hydromassage pool', 'Piscina idromassaggio'), P('spa.jpg', 'Indoor pool', 'Piscina interna'),
    P('wellness.jpg', 'Indoor pool with a sea view', 'Piscina interna con vista mare')], ''),
  (T('Heat', 'Calore'), T('Sauna &amp; Turkish bath', 'Sauna e bagno turco'),
   T('A wooden sauna, the Turkish bath and the sensory shower: the classic Linfa circuit.', 'Sauna in legno, bagno turco e doccia emozionale: il classico percorso Linfa.'),
   [P('sauna.jpg', 'Sauna', 'Sauna'), P('spa.jpg', 'Rest between rounds', 'Riposo tra un giro e l’altro')], ''),
  (T('Beauty area', 'Area beauty'), T('Treatments for one or two', 'Trattamenti per uno o per due'),
   T('Massages and beauty treatments, alone or as a couple. Ask our team for the current list.', 'Massaggi e trattamenti beauty, da soli o in coppia. Chiedi al team l’elenco aggiornato.'),
   [P('people/moment-spa.jpg', 'Time for two', 'Tempo per due'), P('wellness.jpg', 'Quiet after a treatment', 'Silenzio dopo il trattamento')], ''),
  (T('Fitness area', 'Area fitness'), T('Move, then recover', 'Muoviti, poi recupera'),
   T('The fitness area, and the padel court in the garden for a match before the spa.', 'L’area fitness e il campo da padel in giardino per una partita prima della spa.'),
   [P('people/business-padel.jpg', 'Padel before the spa', 'Padel prima della spa'), P('gardens.jpg', 'The gardens', 'I giardini')], 'beyond-the-meeting-room.html'),
  (T('Outside', 'Fuori'), T('Terrace &amp; plunge pool', 'Terrazza e piscinetta'),
   T('Step outside for fresh air and a view of the Adriatic.', 'Esci per un po’ d’aria e la vista sull’Adriatico.'),
   [P('walk.jpg', 'Terrace with a plunge pool', 'Terrazza con piscinetta'), P('villa-adriatic.jpg', 'The hotel above the sea', 'L’hotel sopra il mare')], ''),
 ],
 'restaurant.html': [
  (T('Dining room', 'Sala'), T('The restaurant', 'Il ristorante'),
   T('À la carte Italian cuisine and Abruzzo specialities, overlooking the pool and the park.', 'Cucina italiana à la carte e specialità abruzzesi, con vista su piscina e parco.'),
   [P('restaurant-hall.jpg', 'The dining room', 'La sala'), P('dining.jpg', 'Tables by the windows', 'Tavoli alle vetrate'),
    P('restaurant-dinner.jpg', 'Dinner with a view', 'Cena con vista')], ''),
  (T('Morning', 'Mattina'), T('Breakfast', 'Colazione'),
   T('A local buffet with fruit, cakes and savoury dishes, served early for business guests.', 'Buffet locale con frutta, dolci e salato, servito presto per chi lavora.'),
   [P('breakfast.jpg', 'Breakfast buffet', 'Colazione a buffet'), P('restaurant-hall.jpg', 'Morning light', 'Luce del mattino')], ''),
  (T('Evening', 'Sera'), T('The chef’s table', 'La tavola dello chef'),
   T('Abruzzo on the plate, for special evenings and dinners that close the deal.', 'L’Abruzzo nel piatto, per serate speciali e cene che chiudono l’accordo.'),
   [P('chef-dinner.jpg', 'The chef’s dishes', 'I piatti dello chef'), P('people/moment-dinner.jpg', 'A toast at dinner', 'Un brindisi a cena')], ''),
  (T('Bar', 'Bar'), T('Aperitivo', 'Aperitivo'),
   T('A drink before dinner: the toast after the match, or the start of a family evening.', 'Un drink prima di cena: il brindisi dopo la partita o l’inizio di una serata in famiglia.'),
   [P('bar.jpg', 'The bar', 'Il bar'), P('aperitivo.jpg', 'Aperitivo', 'Aperitivo')], ''),
  (T('Outdoors', 'All’aperto'), T('Terrace &amp; garden', 'Terrazza e giardino'),
   T('Lunch in the shade and dinners with the sea breeze.', 'Pranzi all’ombra e cene con la brezza del mare.'),
   [P('garden-gazebo.jpg', 'Lunch in the garden', 'Pranzo in giardino'), P('gardens.jpg', 'Tables under the trees', 'Tavoli sotto gli alberi')], ''),
 ],
 'contact.html': [
  (T('Arrival', 'Arrivo'), T('Reception &amp; concierge', 'Reception e concierge'),
   T('A warm welcome and a team that helps before you arrive and during your stay.', 'Un’accoglienza calorosa e un team che ti aiuta prima dell’arrivo e durante il soggiorno.'),
   [P('reception.jpg', 'Reception', 'Reception'), P('concierge.jpg', 'Concierge desk', 'Concierge'),
    P('people/family-welcome-back.jpg', 'Welcome back', 'Bentornati')], ''),
  (T('The place', 'Il luogo'), T('On the hill above the sea', 'Sulla collina sopra il mare'),
   T('Contrada Pretaro, above Francavilla al Mare: minutes from Pescara, outside the traffic.', 'Contrada Pretaro, sopra Francavilla al Mare: a pochi minuti da Pescara, fuori dal traffico.'),
   [P('villa-adriatic.jpg', 'The hotel and the sea', 'L’hotel e il mare'), P('walk.jpg', 'Terrace with a sea view', 'Terrazza con vista mare')], ''),
  (T('The park', 'Il parco'), T('Gardens &amp; pools', 'Giardini e piscine'),
   T('A large private park with two pools, a fountain and shady lawns.', 'Un grande parco privato con due piscine, una fontana e prati all’ombra.'),
   [P('gardens.jpg', 'The gardens', 'I giardini'), P('garden-gazebo.jpg', 'The gazebo', 'Il gazebo'),
    P('pool-fountain.jpg', 'Fountain and pool area', 'Fontana e area piscina')], 'activities.html'),
 ],
 'activities.html': [
  (T('Water', 'Acqua'), T('Swimming pools', 'Piscine'),
   T('The Blue Pool for a real swim and the Riviera Pool for children, in summer.', 'La Blue Pool per nuotare davvero e la Riviera Pool per i bambini, in estate.'),
   [P('pool-park.jpg', 'The Blue Pool', 'La Blue Pool'), P('pool-fountain.jpg', 'Fountain and pool area', 'Fontana e area piscina'),
    P('people/moment-pool.jpg', 'Pool days with the family', 'Giornate in piscina in famiglia')], ''),
  (T('Wellness', 'Benessere'), T('Linfa spa', 'Spa Linfa'),
   T('A free two-hour session for every guest: hydromassage, Turkish bath, sauna.', 'Due ore gratuite per ogni ospite: idromassaggio, bagno turco, sauna.'),
   [P('spa-whirlpool.jpg', 'Hydromassage pool', 'Piscina idromassaggio'), P('sauna.jpg', 'Sauna', 'Sauna'),
    P('people/moment-spa.jpg', 'Time for two', 'Tempo per due')], 'spa.html'),
  (T('Sport', 'Sport'), T('Padel', 'Padel'),
   T('A court in the garden for family matches or a game with clients.', 'Un campo in giardino per partite in famiglia o con i clienti.'),
   [P('people/business-padel.jpg', 'Padel in the garden', 'Padel in giardino'), P('gardens.jpg', 'The gardens', 'I giardini')], 'beyond-the-meeting-room.html'),
  (T('Outdoors', 'All’aperto'), T('The park', 'Il parco'),
   T('Shady lawns, a gazebo and terraces with a view of the sea.', 'Prati all’ombra, un gazebo e terrazze con vista mare.'),
   [P('garden-gazebo.jpg', 'The gazebo', 'Il gazebo'), P('walk.jpg', 'Terrace with a sea view', 'Terrazza con vista mare'),
    P('gardens.jpg', 'Garden lounge', 'Salotto in giardino')], ''),
  (T('Food', 'Cucina'), T('Tastes of Abruzzo', 'Sapori d’Abruzzo'),
   T('Abruzzo specialities, an aperitivo at the bar and lunch at the beach lido.', 'Specialità abruzzesi, aperitivo al bar e pranzo al lido.'),
   [P('chef-dinner.jpg', 'The chef’s dishes', 'I piatti dello chef'), P('bar.jpg', 'The bar', 'Il bar'),
    P('restaurant-dinner.jpg', 'Dinner with a view', 'Cena con vista')], 'restaurant.html'),
 ],
}


def showcase_section(cards):
    out = []
    for i, (eb, title, text, photos, link) in enumerate(cards):
        slides = ''.join(
            f'<a class="g-item sc-slide{" is-active" if j == 0 else ""}" href="assets/img/{f}" data-caption="{a(cap[0])}" data-it-caption="{a(cap[1])}">'
            f'<img src="assets/img/{f}" alt="{a(cap[0])}" data-it-alt="{a(cap[1])}" loading="lazy"></a>'
            for j, (f, cap) in enumerate(photos))
        ctrl = ('' if len(photos) < 2 else
                '<div class="sc-ctrl"><span class="sc-count" aria-live="polite">1 / ' + str(len(photos)) + '</span>'
                '<button type="button" class="sc-prev" aria-label="Previous photo" data-it-aria="Foto precedente">‹</button>'
                '<button type="button" class="sc-next" aria-label="Next photo" data-it-aria="Foto successiva">›</button></div>')
        more = (f'<a class="sc-more" href="{link}" data-it="Scopri di più →">Discover more →</a>' if link else '')
        out.append(
            f'<article class="sc-card"><div class="sc-media">{slides}</div>{ctrl}'
            f'<p class="eb" data-it="{a(eb[1])}">{eb[0]}</p>'
            f'<h3 class="sc-title" data-it="{a(title[1])}">{title[0]}</h3>'
            f'<p class="sc-text" data-it="{a(text[1])}">{text[0]}</p>{more}</article>')
    return ('<section class="section white showcase" id="gallery">\n<div class="wrap sc-head">\n'
            '<div><p class="eb" data-it="Galleria">Gallery</p>\n'
            '<h2 class="h2" data-it="Guarda <i>prima di arrivare.</i>">See it <i>before you arrive.</i></h2></div>\n'
            '<div class="sc-nav"><button type="button" class="sc-back" aria-label="Previous" data-it-aria="Precedente">←</button>'
            '<button type="button" class="sc-fwd" aria-label="Next" data-it-aria="Successivo">→</button></div>\n</div>\n'
            '<div class="sc-track" tabindex="0" aria-label="Photo showcase" data-it-aria="Vetrina fotografica">\n'
            + '\n'.join(out) + '\n</div>\n</section>\n')


for page, p in PAGES.items():
    path = ROOT / page
    s = path.read_text(encoding='utf-8')
    s = re.sub(r'<section class="section about" id="about">.*?</section>\n?', '', s, flags=re.S)
    s = re.sub(r'<section class="section white (?:gallery-sec|showcase)" id="gallery">.*?</section>\n?', '', s, flags=re.S)
    block = about_section(p) + (showcase_section(CARDS[page]) if page in CARDS else gallery_section(p))
    anchor = '<section class="section faq" id="faq">'
    assert anchor in s, page
    s = s.replace(anchor, block + anchor, 1)
    path.write_text(s, encoding='utf-8')
    print('about', page, len(p['topics']), 'topics,', len(p.get('gallery', [])), 'photos')
