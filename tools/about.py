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
  'intro': T('Villa Maria Hotel &amp; Spa sits in a large private park in Contrada Pretaro, on the hill above Francavilla al Mare, just south of Pescara. Rooms look out over the park or the sea; two outdoor pools, the Linfa spa and a padel court are a few steps away, and a free shuttle takes you down to a white-sand beach.',
             'Villa Maria Hotel &amp; Spa si trova in un grande parco privato in Contrada Pretaro, sulla collina sopra Francavilla al Mare, appena a sud di Pescara. Le camere guardano il parco o il mare; due piscine all’aperto, la spa Linfa e il campo da padel sono a pochi passi, e una navetta gratuita ti porta su una spiaggia di sabbia bianca.'),
  'topics': [
   (T('The hotel and its park', 'L’hotel e il parco'), [
     T('The park is the heart of the hotel: pine and olive trees, a fountain, loungers in the shade and a gazebo for slow afternoons. Two pools sit inside it, the Blue Pool and the Riviera Pool, plus a shallow pool for children.',
       'Il parco è il cuore dell’hotel: pini e ulivi, una fontana, lettini all’ombra e un gazebo per pomeriggi lenti. Al suo interno ci sono due piscine, la Blue Pool e la Riviera Pool, più una piscina bassa per i bambini.')]),
   (T('Rooms and suites', 'Camere e suite'), [
     T('Six room types, from Standard and Superior rooms to Deluxe rooms, Junior Suites and the Master SPA Suite, each facing the park or the Adriatic.',
       'Sei tipologie di camere, dalle Standard e Superior alle Deluxe, alle Junior Suite e alla Master SPA Suite, tutte con vista sul parco o sull’Adriatico.')]),
   (T('For families', 'Per le famiglie'), [
     T('Children have their own play room with games, books, colouring and puzzles, a shallow pool with water games, and the beach by shuttle. Parents get the Linfa spa, long dinners and real rest. The Family Discount puts room, breakfast and spa in one booking.',
       'I bambini hanno la loro sala giochi con giochi, libri, colori e puzzle, una piscina bassa con giochi d’acqua e la spiaggia con la navetta. I genitori hanno la spa Linfa, lunghe cene e vero riposo. Lo Sconto Famiglia riunisce camera, colazione e spa in una prenotazione.')]),
   (T('For business travel', 'Per i viaggi di lavoro'), [
     T('Five conference rooms, from small meetings to plenary sessions, with video-conferencing and fast Wi-Fi. Pescara Airport, Pescara Centrale station and the A14 are close, and the day can end in the spa or on the padel court.',
       'Cinque sale congressi, dalle riunioni ristrette alle plenarie, con videoconferenza e Wi-Fi veloce. Aeroporto di Pescara, stazione di Pescara Centrale e A14 sono vicini, e la giornata può finire in spa o sul campo da padel.')]),
   (T('Wellness, food and service', 'Benessere, cucina e servizio'), [
     T('The Linfa wellness centre has a hydromassage pool, Turkish bath, sauna and sensory shower, with a free two-hour session for hotel guests. The restaurant and terrace serve Abruzzo specialities, and the team looks after you before you arrive and during your stay.',
       'Il centro benessere Linfa ha piscina idromassaggio, bagno turco, sauna e doccia emozionale, con una sessione gratuita di due ore per gli ospiti. Ristorante e terrazza propongono specialità abruzzesi, e il team si prende cura di te prima dell’arrivo e durante il soggiorno.')]),
   (T('Pets welcome', 'Animali benvenuti'), [
     T('Pets are welcome for a supplement. Tell us when you book so we can prepare the right room.',
       'Gli animali sono benvenuti con un supplemento. Diccelo quando prenoti, così prepariamo la camera giusta.')]),
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
  'h2': T('Six room types, <i>park or sea.</i>', 'Sei tipologie, <i>parco o mare.</i>'),
  'intro': T('Villa Maria has six room types, from Standard rooms to the Master SPA Suite. Every room faces the park or the Adriatic and is a quiet place to sleep well, with a writing desk, power by the bed and high-speed Wi-Fi.',
             'Villa Maria ha sei tipologie di camere, dalla Standard alla Master SPA Suite. Ogni camera guarda il parco o l’Adriatico ed è un posto tranquillo per dormire bene, con scrivania, prese vicino al letto e Wi-Fi ad alta velocità.'),
  'topics': [
   (T('Standard and Superior rooms', 'Camere Standard e Superior'), [
     T('Comfortable rooms with a garden or partial sea view and a writing desk. The Superior Room is ideal for one or two nights and is the standard room of the Executive Business Stay Package.',
       'Camere confortevoli con vista giardino o parziale vista mare e scrivania. La Camera Superior è ideale per una o due notti ed è la camera del Pacchetto Executive Business Stay.')]),
   (T('Deluxe rooms', 'Camere Deluxe'), [
     T('More space, Adriatic views, a desk and a lounge area. Our choice for stays of three nights or more.',
       'Più spazio, vista Adriatico, scrivania e zona lounge. La nostra scelta per soggiorni di tre notti o più.')]),
   (T('Junior Suites', 'Junior Suite'), [
     T('A separate sitting area and room to spread out, good for families and longer stays. Some open onto a terrace with loungers and a view of the sea.',
       'Una zona giorno separata e spazio in più, ideali per famiglie e soggiorni lunghi. Alcune si aprono su una terrazza con lettini e vista mare.')]),
   (T('Master SPA Suite', 'Master SPA Suite'), [
     T('Our most special room: a private terrace with a hot tub and a view over the Adriatic, for anniversaries, honeymoons or simply a few days just for you.',
       'La nostra camera più speciale: una terrazza privata con vasca idromassaggio e vista sull’Adriatico, per anniversari, viaggi di nozze o qualche giorno solo per te.')]),
   (T('Families and pets', 'Famiglie e animali'), [
     T('With the Family Discount, family rooms and suites sleep 2 adults and 2 teens, with breakfast and spa included. Pets are welcome for a supplement. Tell us who is coming and we will suggest the best room.',
       'Con lo Sconto Famiglia, camere e suite famiglia ospitano 2 adulti e 2 ragazzi, con colazione e spa incluse. Gli animali sono benvenuti con un supplemento. Dicci chi viene e ti suggeriamo la camera migliore.')]),
   (T('Little touches', 'Piccole attenzioni'), [  # illustrative
     T('Share your preferences once (pillow, a quiet floor, a room near the lift or away from it) and we keep them for your next stay. A late check-out can often be arranged on request.',
       'Indicaci le tue preferenze una volta (cuscino, piano tranquillo, vicino o lontano dall’ascensore) e le terremo per il prossimo soggiorno. Un check-out posticipato si può spesso organizzare su richiesta.')]),
  ],
  'gallery': [
   ('superior-room.jpg', T('Superior Room', 'Camera Superior')),
   ('deluxe-room.jpg', T('Deluxe Room', 'Camera Deluxe')),
   ('suite-terrace.jpg', T('Suite terrace with hot tub', 'Terrazza della suite con vasca idromassaggio')),
   ('suite-seaview.jpg', T('Sea view from a suite', 'Vista mare da una suite')),
   ('concierge.jpg', T('Concierge desk', 'Concierge')),
  ],
 },
 # ------------------------------------------------------------------ Spa
 'spa.html': {
  'eb': T('About the Linfa spa', 'La spa Linfa'),
  'h2': T('Your own space <i>to unwind.</i>', 'Il tuo spazio <i>per rilassarti.</i>'),
  'intro': T('Linfa is the hotel’s wellness centre, an oasis where everyone finds their own way to relax. It is organised in three areas, relaxation, beauty and fitness, and every hotel guest can enjoy a free two-hour spa session. Booking is required.',
             'Linfa è il centro benessere dell’hotel, un’oasi dove ognuno trova il suo modo di rilassarsi. È organizzato in tre aree, relax, beauty e fitness, e ogni ospite dell’hotel può godere di una sessione spa gratuita di due ore. La prenotazione è obbligatoria.'),
  'topics': [
   (T('Relaxation area', 'Area relax'), [
     T('A hydromassage pool, a Turkish bath, a sauna and a sensory shower, with tall windows over the park and towards the sea. Loungers and herbal teas make it easy to stay a little longer.',
       'Piscina idromassaggio, bagno turco, sauna e doccia emozionale, con grandi vetrate sul parco e verso il mare. Lettini e tisane rendono facile restare un po’ di più.')]),
   (T('Your free two-hour session', 'La tua sessione gratuita di due ore'), [
     T('Every hotel guest can enjoy two hours in the relaxation area at no extra cost. Book your time at reception or send us a message before you arrive, especially in high season.',
       'Ogni ospite dell’hotel può godere di due ore nell’area relax senza costi aggiuntivi. Prenota l’orario in reception o scrivici prima dell’arrivo, soprattutto in alta stagione.')]),
   (T('Beauty area and treatments', 'Area beauty e trattamenti'), [
     T('Massages and beauty treatments can be booked for one person or as a couple. Ask our team for the current list and prices, or add a treatment to your booking request.',
       'Massaggi e trattamenti beauty si possono prenotare per una persona o in coppia. Chiedi al nostro team l’elenco aggiornato e i prezzi, o aggiungi un trattamento alla richiesta di prenotazione.')]),
   (T('Fitness area', 'Area fitness'), [
     T('Keep your routine while you travel: the fitness area is part of Linfa, and the padel court in the garden is close by.',
       'Mantieni la tua routine anche in viaggio: l’area fitness fa parte di Linfa e il campo da padel in giardino è vicino.')]),
   (T('Rituals we love', 'I rituali che amiamo'), [  # illustrative
     T('A suggestion for your first visit: twenty minutes in the hydromassage pool, a round of sauna and Turkish bath, the sensory shower, then a long rest with a herbal tea while the light changes over the park.',
       'Un consiglio per la prima visita: venti minuti in idromassaggio, un giro tra sauna e bagno turco, la doccia emozionale e poi un lungo riposo con una tisana mentre la luce cambia sul parco.')]),
   (T('Spa in your package', 'La spa nel tuo pacchetto'), [
     T('Spa access is included in the Family Discount and in the Executive Business Stay Package. The Padel Experience ends the match with sauna, spa and a massage.',
       'L’accesso alla spa è incluso nello Sconto Famiglia e nel Pacchetto Executive Business Stay. La Padel Experience chiude la partita con sauna, spa e massaggio.')]),
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
  'intro': T('The restaurant and its terrace overlook the pool and the park, with the sea breeze in the evening. The kitchen cooks Italian dishes and Abruzzo specialities with local products, from the breakfast buffet to dinner at the chef’s table.',
             'Il ristorante e la sua terrazza guardano la piscina e il parco, con la brezza del mare la sera. La cucina propone piatti italiani e specialità abruzzesi con prodotti locali, dalla colazione a buffet alla cena alla tavola dello chef.'),
  'topics': [
   (T('Breakfast', 'Colazione'), [
     T('A local buffet with fresh fruit, cakes, pastries and savoury dishes, included in our packages. Business guests can have it early, before the first call.',
       'Un buffet locale con frutta fresca, torte, dolci e piatti salati, incluso nei pacchetti. Chi viaggia per lavoro può farla presto, prima della prima call.')]),
   (T('Lunch and dinner', 'Pranzo e cena'), [
     T('À la carte Italian cuisine and Abruzzo specialities, served in the dining room or on the terrace over the pool. Long family dinners and quiet business dinners both have their place.',
       'Cucina italiana à la carte e specialità abruzzesi, servite in sala o in terrazza sulla piscina. Lunghe cene in famiglia e cene di lavoro tranquille hanno entrambe il loro posto.')]),
   (T('Tastes of Abruzzo', 'I sapori dell’Abruzzo'), [  # illustrative
     T('Expect the region on the plate: pasta alla chitarra, arrosticini, fish from the Adriatic, extra-virgin olive oil from the hills and a glass of Montepulciano d’Abruzzo or Trebbiano. The menu changes with the seasons.',
       'Aspettati la regione nel piatto: spaghetti alla chitarra, arrosticini, pesce dell’Adriatico, olio extravergine delle colline e un bicchiere di Montepulciano d’Abruzzo o Trebbiano. Il menu cambia con le stagioni.')]),
   (T('The chef’s table', 'La tavola dello chef'), [
     T('For a special evening, or the dinner after a padel match, the chef’s table is where conversations last and deals are made.',
       'Per una serata speciale, o la cena dopo una partita di padel, la tavola dello chef è dove le conversazioni durano e nascono gli accordi.')]),
   (T('Bar, aperitivo and the beach', 'Bar, aperitivo e spiaggia'), [
     T('An aperitivo at the hotel bar before dinner, or lunch on the sand: the partner lido on the beach has its own bar and restaurant for beach lunches, aperitifs and summer evenings.',
       'Un aperitivo al bar dell’hotel prima di cena, o il pranzo sulla sabbia: il lido convenzionato ha il suo bar e ristorante per pranzi in spiaggia, aperitivi e serate d’estate.')]),
   (T('La Bottega di Villa Maria', 'La Bottega di Villa Maria'), [
     T('Our corner of local products and Abruzzo flavours, to taste during your stay and take a little of the region home.',
       'Il nostro angolo di prodotti locali e sapori abruzzesi, da gustare durante il soggiorno e da portare un po’ a casa.')]),
   (T('Allergies and reservations', 'Allergie e prenotazioni'), [
     T('Tell us about allergies or diets when you book, or send us a message. For opening times and table reservations, ask our team.',
       'Segnalaci allergie o diete quando prenoti, o scrivici un messaggio. Per orari e prenotazione del tavolo, chiedi al nostro team.')]),
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
  'intro': T('Villa Maria is in Contrada Pretaro, on the hill above Francavilla al Mare, minutes from Pescara: close to the airport, the main station and the A14 motorway, yet outside the city and its traffic.',
             'Villa Maria è in Contrada Pretaro, sulla collina sopra Francavilla al Mare, a pochi minuti da Pescara: vicina all’aeroporto, alla stazione centrale e all’A14, ma fuori dalla città e dal traffico.'),
  'topics': [
   (T('By plane', 'In aereo'), [
     T('Abruzzo Airport (Pescara) is a short drive away. Ask us about a transfer when you book.',
       'L’aeroporto d’Abruzzo (Pescara) è a pochi minuti d’auto. Chiedici un transfer quando prenoti.')]),
   (T('By train', 'In treno'), [
     T('Pescara Centrale station has easy rail connections along the Adriatic line and to Rome. From the station, take a taxi or ask us about a transfer.',
       'La stazione di Pescara Centrale ha comodi collegamenti sulla linea adriatica e verso Roma. Dalla stazione prendi un taxi o chiedici un transfer.')]),
   (T('By car', 'In auto'), [
     T('Leave the A14 at the Pescara Sud – Francavilla exit and follow the signs for Francavilla al Mare and Contrada Pretaro. Free private parking with EV charging is waiting at the hotel.',
       'Esci dall’A14 a Pescara Sud – Francavilla e segui le indicazioni per Francavilla al Mare e Contrada Pretaro. In hotel ti aspetta il parcheggio privato gratuito con ricarica per auto elettriche.')]),
   (T('The beach shuttle', 'La navetta per la spiaggia'), [
     T('A free shuttle takes you to our partner lido on a white-sand beach in Francavilla al Mare, a few kilometres away, with a bar and restaurant on the sand.',
       'Una navetta gratuita ti porta al lido convenzionato su una spiaggia di sabbia bianca a Francavilla al Mare, a pochi chilometri, con bar e ristorante sulla sabbia.')]),
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
  'intro': T('Days at Villa Maria can be as busy or as slow as you like: pools in the park, the beach by shuttle, the Linfa spa, padel in the garden, a play room for children, and the hills, coast and towns of Abruzzo all within easy reach.',
             'Le giornate a Villa Maria possono essere piene o lente quanto vuoi: piscine nel parco, la spiaggia con la navetta, la spa Linfa, il padel in giardino, una sala giochi per i bambini e colline, costa e borghi d’Abruzzo a portata di mano.'),
  'topics': [
   (T('Swimming pools', 'Piscine'), [
     T('Two outdoor pools in the large hotel park: the Blue Pool, up to 2.5 metres deep, and the Riviera Pool. Children have their own shallow pool, no deeper than 50 cm, with water games and hydromassage. The outdoor pools are open in the summer season; ask us for this year’s dates.',
       'Due piscine all’aperto nel grande parco dell’hotel: la Blue Pool, profonda fino a 2,5 metri, e la Riviera Pool. I bambini hanno la loro piscina bassa, profonda al massimo 50 cm, con giochi d’acqua e idromassaggio. Le piscine esterne sono aperte nella stagione estiva; chiedici le date di quest’anno.')]),
   (T('The beach', 'La spiaggia'), [
     T('A free shuttle takes you to a white-sand beach in Francavilla al Mare, a few kilometres away, at a private lido with a special agreement with the hotel. The lido has a bar and a restaurant for lunches on the beach, aperitifs and summer evenings.',
       'Una navetta gratuita ti porta su una spiaggia di sabbia bianca a Francavilla al Mare, a pochi chilometri, in un lido privato convenzionato con l’hotel. Il lido ha bar e ristorante per pranzi in spiaggia, aperitivi e serate d’estate.')]),
   (T('Kids Club and play room', 'Kids Club e sala giochi'), [
     T('Inside the hotel a play room welcomes younger guests with games, books, colouring and puzzles. In summer the park becomes their playground, between the shallow pool, the lawns and the shade of the pines.',
       'In hotel una sala giochi accoglie i più piccoli con giochi, libri, colori e puzzle. D’estate il parco diventa il loro parco giochi, tra la piscina bassa, i prati e l’ombra dei pini.')]),
   (T('Linfa wellness &amp; spa', 'Benessere e spa Linfa'), [
     T('Hydromassage pool, Turkish bath, sauna and sensory shower, plus beauty and fitness areas. Hotel guests enjoy a free two-hour spa session; booking is required.',
       'Piscina idromassaggio, bagno turco, sauna e doccia emozionale, più aree beauty e fitness. Gli ospiti dell’hotel hanno una sessione spa gratuita di due ore; la prenotazione è obbligatoria.')]),
   (T('Padel', 'Padel'), [
     T('Our padel court is in the garden. Book a slot for a family match or bring a client: The Padel Experience pairs the game with the spa, an aperitivo and dinner.',
       'Il nostro campo da padel è in giardino. Prenota un orario per una partita in famiglia o porta un cliente: la Padel Experience abbina la partita a spa, aperitivo e cena.')]),
   (T('Nature and the coast', 'Natura e costa'), [
     T('Walk among the pines of the Pineta Dannunziana nature reserve in Pescara, ride a bike along the coast towards the Costa dei Trabocchi, or go snorkelling and diving in the Adriatic. Horse riding and hiking in the hills are also close by.',
       'Passeggia tra i pini della riserva naturale Pineta Dannunziana a Pescara, pedala lungo la costa verso la Costa dei Trabocchi, o fai snorkeling e immersioni nell’Adriatico. Equitazione ed escursioni in collina sono vicine.')]),
   (T('Days out with children', 'Gite con i bambini'), [
     T('Two favourites with families: the Guardiagrele adventure park, with tree-top trails in the woods at the foot of the Majella, and the zoo in Lanciano.',
       'Due preferiti dalle famiglie: il parco avventura di Guardiagrele, con percorsi tra gli alberi ai piedi della Majella, e lo zoo di Lanciano.')]),
   (T('Towns and tastes of Abruzzo', 'Borghi e sapori d’Abruzzo'), [  # illustrative
     T('Spend a morning in Chieti’s old town, an evening by the sea in Pescara, or follow the coast south to the trabocchi, the old fishing platforms over the water where you can eat fresh fish. Ask our team for ideas for your days.',
       'Passa una mattina nel centro storico di Chieti, una sera sul mare a Pescara, o segui la costa a sud fino ai trabocchi, le antiche macchine da pesca sull’acqua dove si mangia pesce fresco. Chiedi al nostro team qualche idea per le tue giornate.')]),
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
     T('The Blue Pool and the Riviera Pool sit in the private park, with a shallow pool for children with water games. Teenagers get space to swim and play; little ones stay safely in their depth.',
       'La Blue Pool e la Riviera Pool sono nel parco privato, con una piscina bassa per i bambini con giochi d’acqua. I ragazzi hanno spazio per nuotare e giocare; i più piccoli restano al sicuro.')]),
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
 # ------------------------------------------------------------------ Family Discount
 'family-reset-package.html': {
  'eb': T('About the Family Discount', 'Lo Sconto Famiglia'),
  'h2': T('Everything in one booking, <i>explained.</i>', 'Tutto in una prenotazione, <i>spiegato.</i>'),
  'intro': T('The Family Discount brings room, breakfast and spa together for families who book directly with the hotel, plus extras you will not find on booking sites. Here are the details.',
             'Lo Sconto Famiglia riunisce camera, colazione e spa per le famiglie che prenotano direttamente con l’hotel, più extra che non trovi sui portali. Ecco i dettagli.'),
  'topics': [
   (T('Your room', 'La tua camera'), [
     T('Family rooms and suites for 2 adults and 2 teens, facing the park or the sea. Tell us the ages of your children and we will suggest the best room.',
       'Camere e suite famiglia per 2 adulti e 2 ragazzi, con vista parco o mare. Dicci l’età dei tuoi figli e ti suggeriamo la camera migliore.')]),
   (T('Breakfast and the spa', 'Colazione e spa'), [
     T('A local buffet breakfast every morning, and access to the Linfa wellness centre: hydromassage pool, Turkish bath, sauna and sensory shower. Book your spa time at reception.',
       'Colazione a buffet locale ogni mattina e accesso al centro benessere Linfa: piscina idromassaggio, bagno turco, sauna e doccia emozionale. Prenota l’orario della spa in reception.')]),
   (T('Pools, beach and play', 'Piscine, spiaggia e gioco'), [
     T('The Blue Pool, the Riviera Pool and a children’s pool with water games in the park; a free shuttle to our partner lido on a white-sand beach; a play room with games, books and puzzles; and padel in the garden.',
       'La Blue Pool, la Riviera Pool e una piscina per bambini con giochi d’acqua nel parco; navetta gratuita per il lido convenzionato su una spiaggia di sabbia bianca; una sala giochi con giochi, libri e puzzle; e il padel in giardino.')]),
   (T('The €20 voucher', 'Il voucher da 20 €'), [
     T('First-time guests who book directly with the hotel receive a €20 in-house voucher for food and drink or the spa. It is valid for your first stay and first direct booking and expires at check-out.',
       'Chi prenota direttamente con l’hotel per la prima volta riceve un voucher da 20 € per food and beverage o spa. Vale per il primo soggiorno e la prima prenotazione diretta e scade al check-out.')]),
   (T('10% off your next stay', '10% sul prossimo soggiorno'), [
     T('Book your next stay directly at the hotel during your visit and get 10% off the room rate, with free cancellation up to 6 months before arrival and date changes up to 6 weeks before.',
       'Prenota il prossimo soggiorno direttamente in hotel durante la visita e hai il 10% sulla tariffa della camera, con cancellazione gratuita fino a 6 mesi prima dell’arrivo e cambio date fino a 6 settimane prima.')]),
   (T('Parking and pets', 'Parcheggio e animali'), [
     T('Free private parking with EV charging. Pets are welcome for a supplement; let us know when you book.',
       'Parcheggio privato gratuito con ricarica per auto elettriche. Gli animali sono benvenuti con un supplemento; avvisaci quando prenoti.')]),
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
     T('A Superior Room (garden or partial sea view) for one or two nights, or a Deluxe Room or Suite with Adriatic views and a lounge area for three nights or more. Every room has a writing desk and fast Wi-Fi.',
       'Una Camera Superior (vista giardino o parziale vista mare) per una o due notti, o una Deluxe o Suite con vista Adriatico e zona lounge per tre notti o più. Ogni camera ha scrivania e Wi-Fi veloce.')]),
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
 'padel-experience.html': {
  'eb': T('About The Padel Experience', 'La Padel Experience'),
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
  (T('Accommodation', 'Camere'), T('Rooms &amp; suites', 'Camere e suite'),
   T('Six room types, from Standard rooms to the Master SPA Suite, facing the park or the Adriatic.', 'Sei tipologie, dalla Standard alla Master SPA Suite, con vista sul parco o sull’Adriatico.'),
   [P('deluxe-room.jpg', 'Deluxe Room', 'Camera Deluxe'), P('superior-room.jpg', 'Superior Room', 'Camera Superior'),
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
   T('The Blue Pool and the Riviera Pool in a private park, with a shallow pool for children.', 'La Blue Pool e la Riviera Pool in un parco privato, con una piscina bassa per i bambini.'),
   [P('pool-park.jpg', 'The Blue Pool', 'La Blue Pool'), P('pool-fountain.jpg', 'Fountain and pool area', 'Fontana e area piscina'),
    P('people/moment-pool.jpg', 'Pool days with the family', 'Giornate in piscina in famiglia'), P('garden-gazebo.jpg', 'The gazebo', 'Il gazebo')], 'activities.html'),
  (T('Business', 'Business'), T('Meetings &amp; events', 'Meeting ed eventi'),
   T('Five conference rooms, from small meetings to an auditorium, with video-conferencing.', 'Cinque sale congressi, dalle riunioni ristrette all’auditorium, con videoconferenza.'),
   [P('meeting-hall.jpg', 'Meeting room', 'Sala riunioni'), P('auditorium.jpg', 'Auditorium', 'Auditorium'),
    P('meeting-room.jpg', 'Private meeting room', 'Sala riservata'), P('people/business-meeting.jpg', 'A working session', 'Una sessione di lavoro')], 'business-travel.html'),
  (T('Sport', 'Sport'), T('Padel &amp; gardens', 'Padel e giardini'),
   T('A padel court in the garden, shady lawns and terraces with a view of the sea.', 'Un campo da padel in giardino, prati all’ombra e terrazze con vista mare.'),
   [P('people/business-padel.jpg', 'Padel in the garden', 'Padel in giardino'), P('gardens.jpg', 'The gardens', 'I giardini'),
    P('walk.jpg', 'Terrace with a sea view', 'Terrazza con vista mare')], 'padel-experience.html'),
 ],
 'rooms.html': [
  (T('For short stays', 'Per soggiorni brevi'), T('Standard &amp; Superior', 'Standard e Superior'),
   T('Garden or partial sea view and a writing desk. Ideal for one or two nights.', 'Vista giardino o parziale vista mare e scrivania. Ideali per una o due notti.'),
   [P('superior-room.jpg', 'Superior Room', 'Camera Superior'), P('villa-adriatic.jpg', 'Rooms above the park', 'Camere sopra il parco'),
    P('concierge.jpg', 'Concierge desk', 'Concierge')], 'booking.html#superior'),
  (T('More space', 'Più spazio'), T('Deluxe Room', 'Camera Deluxe'),
   T('Adriatic views, a desk and a lounge area. Our choice for three nights or more.', 'Vista Adriatico, scrivania e zona lounge. La nostra scelta per tre notti o più.'),
   [P('deluxe-room.jpg', 'Deluxe Room', 'Camera Deluxe'), P('suite-seaview.jpg', 'The view from the terrace', 'La vista dalla terrazza')], 'booking.html#deluxe'),
  (T('Suites', 'Suite'), T('Junior Suites', 'Junior Suite'),
   T('A separate sitting area and room to spread out, for families and longer stays.', 'Una zona giorno separata e spazio in più, per famiglie e soggiorni lunghi.'),
   [P('suite-seaview.jpg', 'Suite with sea view', 'Suite con vista mare'), P('deluxe-room.jpg', 'Bedroom', 'Camera da letto')], 'booking.html#suite'),
  (T('Signature suite', 'Suite esclusiva'), T('Master SPA Suite', 'Master SPA Suite'),
   T('A private terrace with a hot tub and the Adriatic in front of you.', 'Una terrazza privata con vasca idromassaggio e l’Adriatico davanti.'),
   [P('suite-terrace.jpg', 'Terrace with hot tub', 'Terrazza con idromassaggio'), P('walk.jpg', 'Terrace and plunge pool', 'Terrazza e piscinetta'),
    P('spa-whirlpool.jpg', 'Spa access included', 'Accesso alla spa incluso')], 'booking.html#suite'),
  (T('Families', 'Famiglie'), T('Family rooms', 'Camere per famiglie'),
   T('Rooms and suites for 2 adults and 2 teens, with breakfast and spa in the Family Discount.', 'Camere e suite per 2 adulti e 2 ragazzi, con colazione e spa nello Sconto Famiglia.'),
   [P('people/family-welcome-back.jpg', 'Arriving as a family', 'L’arrivo in famiglia'), P('pool-park.jpg', 'Pools a few steps away', 'Le piscine a pochi passi'),
    P('breakfast.jpg', 'Breakfast included', 'Colazione inclusa')], 'family-reset-package.html'),
 ],
 'spa.html': [
  (T('Relaxation area', 'Area relax'), T('Water &amp; warmth', 'Acqua e calore'),
   T('Hydromassage pool and indoor pool, with tall windows over the park and towards the sea.', 'Piscina idromassaggio e piscina interna, con grandi vetrate sul parco e verso il mare.'),
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
   [P('people/business-padel.jpg', 'Padel before the spa', 'Padel prima della spa'), P('gardens.jpg', 'The gardens', 'I giardini')], 'padel-experience.html'),
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
   T('The Blue Pool, the Riviera Pool and a shallow pool for children, in summer.', 'La Blue Pool, la Riviera Pool e una piscina bassa per bambini, in estate.'),
   [P('pool-park.jpg', 'The Blue Pool', 'La Blue Pool'), P('pool-fountain.jpg', 'Fountain and pool area', 'Fontana e area piscina'),
    P('people/moment-pool.jpg', 'Pool days with the family', 'Giornate in piscina in famiglia')], ''),
  (T('Wellness', 'Benessere'), T('Linfa spa', 'Spa Linfa'),
   T('A free two-hour session for every guest: hydromassage, Turkish bath, sauna.', 'Due ore gratuite per ogni ospite: idromassaggio, bagno turco, sauna.'),
   [P('spa-whirlpool.jpg', 'Hydromassage pool', 'Piscina idromassaggio'), P('sauna.jpg', 'Sauna', 'Sauna'),
    P('people/moment-spa.jpg', 'Time for two', 'Tempo per due')], 'spa.html'),
  (T('Sport', 'Sport'), T('Padel', 'Padel'),
   T('A court in the garden for family matches or a game with clients.', 'Un campo in giardino per partite in famiglia o con i clienti.'),
   [P('people/business-padel.jpg', 'Padel in the garden', 'Padel in giardino'), P('gardens.jpg', 'The gardens', 'I giardini')], 'padel-experience.html'),
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
