#!/usr/bin/env python3
"""Insert the FAQ accordion ("Good to know") into each English page, just before the
closing call-to-action and footer. The Italian text sits in data-it, so build-it.py
turns it into the Italian pages, and adds Google's FAQPage data for both languages.

Edit the questions below, then run:

    python3 tools/faq.py && python3 tools/build-it.py
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# (question EN, question IT, answer EN, answer IT)
LOCATION = ('Where is Villa Maria Hotel & Spa?', "Dove si trova Villa Maria Hotel & Spa?",
    'On the hill above Francavilla al Mare, just south of Pescara in Abruzzo. Abruzzo Airport (Pescara) is a short drive away, Pescara Centrale station has easy rail connections, and the A14 Pescara Sud exit is close by.',
    "Sulla collina sopra Francavilla al Mare, appena a sud di Pescara, in Abruzzo. L'aeroporto d'Abruzzo (Pescara) è a pochi minuti d'auto, la stazione di Pescara Centrale ha comodi collegamenti e l'uscita A14 Pescara Sud è vicina.")
CHECKIN = ('What are the check-in and check-out times?', 'Quali sono gli orari di check-in e check-out?',
    'Your check-in and check-out times are in your booking confirmation. If you need an early check-in or a late check-out, ask us and we will do our best.',
    'Gli orari di check-in e check-out sono nella conferma di prenotazione. Se ti serve un check-in anticipato o un check-out posticipato, chiedicelo e faremo il possibile.')
PARKING = ('Is there parking?', "C'è il parcheggio?",
    'Yes. Private parking is free for guests and includes EV charging.',
    'Sì. Il parcheggio privato è gratuito per gli ospiti e ha la ricarica per auto elettriche.')
SPA = ('What is in the Linfa wellness & spa?', "Cosa c'è nella spa Linfa?",
    'A hydromassage pool, Turkish bath, sauna and sensory shower, plus relaxation, beauty and fitness areas. Every hotel guest has a free two-hour session; booking is required. Treatments for one or two can be added.',
    'Piscina idromassaggio, bagno turco, sauna e doccia emozionale, più aree relax, beauty e fitness. Ogni ospite ha una sessione gratuita di due ore; la prenotazione è obbligatoria. Si possono aggiungere trattamenti per uno o per due.')
DIRECT = ('Why book directly with the hotel?', 'Perché prenotare direttamente con l’hotel?',
    'You get the package exactly as designed, a real person before and during your stay, and extras that are not on booking sites, such as the €20 in-house voucher on your first direct Family Discount booking.',
    'Hai il pacchetto esattamente come progettato, una persona vera prima e durante il soggiorno ed extra che non trovi sui portali, come il voucher da 20 € alla prima prenotazione diretta con lo Sconto Famiglia.')
CANCEL = ('What is the cancellation policy?', 'Qual è la politica di cancellazione?',
    'If you book your next stay during your visit (10% off), you can cancel for free up to 6 months before arrival and change dates up to 6 weeks before. For other bookings, the terms are in your booking confirmation.',
    "Se prenoti il prossimo soggiorno durante la visita (10% di sconto), puoi cancellare gratis fino a 6 mesi prima dell'arrivo e cambiare date fino a 6 settimane prima. Per le altre prenotazioni, le condizioni sono nella conferma.")
PAYMENT = ('Do I pay when I send a booking request?', 'Pago quando invio la richiesta di prenotazione?',
    'No. You choose your dates, package and room, and we reply by email with the price and confirmation.',
    'No. Scegli date, pacchetto e camera e ti rispondiamo via email con prezzo e conferma.')

FAM_GOOD = ('Is Villa Maria good for families with children?', 'Villa Maria è adatto alle famiglie con bambini?',
    'Yes. There are two outdoor pools in a private park, a Kids Club, padel, a free shuttle to our partner beach and family dinners with Abruzzo recipes, plus the Linfa spa for parents.',
    'Sì. Ci sono due piscine all’aperto in un parco privato, un Kids Club, il padel, una navetta gratuita per la spiaggia convenzionata e cene in famiglia con ricette abruzzesi, più la spa Linfa per i genitori.')
FAM_INCL = ('What does the Family Discount include?', 'Cosa include lo Sconto Famiglia?',
    'Family rooms and suites for 2 adults and 2 teens, breakfast, spa access at the Linfa wellness centre, family activities, beach access with a free shuttle, and free parking with EV charging.',
    'Camere e suite famiglia per 2 adulti e 2 ragazzi, colazione, accesso alla spa Linfa, attività per famiglie, accesso alla spiaggia con navetta gratuita e parcheggio gratuito con ricarica per auto elettriche.')
FAM_VOUCHER = ('How does the €20 voucher work?', 'Come funziona il voucher da 20 €?',
    'It is for first-time guests booking directly with the hotel. Use it on food and drink or in the spa during your stay. It is valid for your first stay and first direct booking and expires at check-out.',
    'È per chi prenota direttamente con l’hotel per la prima volta. Usalo per food and beverage o nella spa durante il soggiorno. Vale per il primo soggiorno e la prima prenotazione diretta e scade al check-out.')

BIZ_MEET = ('Does the hotel have meeting rooms?', "L'hotel ha sale riunioni?",
    'Yes, five conference rooms, from small meeting rooms to an auditorium, with video-conferencing and fast Wi-Fi. Ask us about capacity for your group.',
    'Sì, cinque sale congressi, dalle sale riservate all’auditorium, con videoconferenza e Wi-Fi veloce. Chiedici la capienza per il tuo gruppo.')
BIZ_INVOICE = ('Can I get an invoice for my company?', 'Posso avere la fattura per la mia azienda?',
    'Yes. We bill your company directly and welcome corporate cards. If you have a company code, add it when you book.',
    'Sì. Fatturiamo direttamente alla tua azienda e accettiamo carte aziendali. Se hai un codice aziendale, inseriscilo al momento della prenotazione.')
BIZ_PKG = ('What is in the Executive Business Stay Package?', "Cosa include il Pacchetto Executive Business Stay?",
    'A Superior or Deluxe room with a writing desk, breakfast served early, high-speed Wi-Fi, spa and sauna access, padel, pool and gym, a meeting room on request, express check-out and private parking.',
    'Una camera Superior o Deluxe con scrivania, colazione servita presto, Wi-Fi ad alta velocità, spa e sauna, padel, piscina e palestra, sala riunioni su richiesta, check-out rapido e parcheggio privato.')
BIZ_PADEL = ('Can I play padel with clients or colleagues?', 'Posso giocare a padel con clienti o colleghi?',
    'Yes. Our courts are in the gardens above the Adriatic. Pair the match with the spa, an aperitivo at the bar and dinner at the chef’s table.',
    'Sì. I campi sono nei giardini sopra l’Adriatico. Abbina la partita alla spa, a un aperitivo al bar e alla cena alla tavola dello chef.')

PETS = ('Are pets allowed?', 'Sono ammessi animali?',
    'Yes, pets are welcome for a supplement. Tell us when you book so we can prepare the right room.',
    'Sì, gli animali sono benvenuti con un supplemento. Diccelo quando prenoti, così prepariamo la camera giusta.')
POOLS = ('What pools does the hotel have?', "Che piscine ha l'hotel?",
    'Two outdoor pools in the park, the Blue Pool (up to 2.5 m deep) and the Riviera Pool, plus a shallow children’s pool with water games. The outdoor pools are open in the summer season; the Linfa spa has an indoor hydromassage pool all year.',
    'Due piscine all’aperto nel parco, la Blue Pool (fino a 2,5 m di profondità) e la Riviera Pool, più una piscina bassa per bambini con giochi d’acqua. Le piscine esterne sono aperte in estate; la spa Linfa ha una piscina idromassaggio interna tutto l’anno.')
BEACH = ('Is there a beach?', "C'è una spiaggia?",
    'Yes. A free shuttle takes you to a white-sand beach in Francavilla al Mare, a few kilometres away, at a private lido with a bar and restaurant that has an agreement with the hotel.',
    'Sì. Una navetta gratuita ti porta su una spiaggia di sabbia bianca a Francavilla al Mare, a pochi chilometri, in un lido privato convenzionato con bar e ristorante.')
KIDS = ('What is there for children?', 'Cosa c’è per i bambini?',
    'A play room with games, books, colouring and puzzles, a shallow pool with water games, the park, padel and the beach by shuttle. Nearby, families love the Guardiagrele adventure park and the zoo in Lanciano.',
    'Una sala giochi con giochi, libri, colori e puzzle, una piscina bassa con giochi d’acqua, il parco, il padel e la spiaggia con la navetta. Nei dintorni le famiglie amano il parco avventura di Guardiagrele e lo zoo di Lanciano.')
NEARBY = ('What can we do nearby?', 'Cosa possiamo fare nei dintorni?',
    'Walk in the Pineta Dannunziana nature reserve in Pescara, cycle along the coast towards the Costa dei Trabocchi, go snorkelling or diving, horse riding or hiking in the hills, or visit Chieti and Pescara.',
    'Passeggiare nella riserva Pineta Dannunziana a Pescara, pedalare lungo la costa verso la Costa dei Trabocchi, fare snorkeling o immersioni, equitazione o escursioni in collina, o visitare Chieti e Pescara.')
ROOMS_Q = ('Which room is right for me?', 'Quale camera fa per me?',
    'The Superior Room, with a garden or partial sea view and a desk, suits short stays of 1 to 2 nights. The Deluxe Room and the Suites have more space and Adriatic views, for 3 nights or more.',
    'La Camera Superior, con vista giardino o parziale vista mare e scrivania, è ideale per 1–2 notti. Le Camere Deluxe e le Suite hanno più spazio e vista Adriatico, per 3 notti o più.')
REST_Q = ('Is breakfast included?', 'La colazione è inclusa?',
    'Breakfast is included in our packages and served as a local buffet. Executive guests can have it early, before the first call.',
    'La colazione è inclusa nei pacchetti ed è servita a buffet con prodotti locali. Gli ospiti Executive possono averla presto, prima della prima call.')

GENERAL = [LOCATION, CHECKIN, PARKING, SPA, POOLS, PETS, DIRECT, CANCEL]
FAQS = {
    'index.html': GENERAL,
    'rooms.html': [ROOMS_Q, CHECKIN, PETS, PARKING, CANCEL, PAYMENT],
    'spa.html': [SPA, CHECKIN, PARKING, DIRECT],
    'restaurant.html': [REST_Q, LOCATION, PARKING, DIRECT],
    'contact.html': [LOCATION, PARKING, CHECKIN, CANCEL],
    'booking.html': [PAYMENT, CANCEL, CHECKIN, PARKING, PETS],
    'activities.html': [POOLS, BEACH, SPA, KIDS, NEARBY, PETS],
    'italian-memories.html': [FAM_GOOD, KIDS, POOLS, BEACH, FAM_INCL, CHECKIN],
    'family-reset-package.html': [FAM_INCL, FAM_VOUCHER, CANCEL, FAM_GOOD, CHECKIN],
    'ciao-again.html': [CANCEL, FAM_GOOD, CHECKIN, PARKING],
    'business-travel.html': [LOCATION, BIZ_MEET, BIZ_INVOICE, BIZ_PKG, PARKING],
    'executive-business-stay.html': [BIZ_PKG, BIZ_INVOICE, BIZ_MEET, CHECKIN, CANCEL],
    'padel-experience.html': [BIZ_PADEL, BIZ_MEET, BIZ_INVOICE, PARKING],
}


def a(s):
    return html.escape(s, quote=True)


def section(items):
    rows = '\n'.join(
        f'<details class="faq-item"><summary><span data-it="{a(qi)}">{html.escape(q)}</span></summary>'
        f'<div class="faq-a" data-it="{a("<p>" + html.escape(ai) + "</p>")}"><p>{html.escape(ae)}</p></div></details>'
        for q, qi, ae, ai in items)
    return ('<section class="section faq" id="faq">\n<div class="wrap split">\n'
            '<div><p class="eb" data-it="Domande frequenti">Questions &amp; answers</p>\n'
            '<h2 class="h2" data-it="Utile da sapere &lt;i&gt;prima di partire.&lt;/i&gt;">Good to know <i>before you go.</i></h2></div>\n'
            f'<div class="faq-list">\n{rows}\n</div>\n</div>\n</section>\n')


for page, items in FAQS.items():
    path = ROOT / page
    s = path.read_text(encoding='utf-8')
    s = re.sub(r'<section class="section faq" id="faq">.*?</section>\n?', '', s, flags=re.S)
    block = section(items)
    if '<section class="cta">' in s:
        s = s.replace('<section class="cta">', block + '<section class="cta">', 1)
    else:
        s = s.replace('</main>', block + '</main>', 1)
    path.write_text(s, encoding='utf-8')
    print('faq', page, len(items))
