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
    'On the hill above Francavilla al Mare, in Abruzzo, 5 km from the centre of Pescara. Chieti, Pescara and Abruzzo International Airport are about 15 minutes away, Pescara Centrale station has easy rail connections, and the A14 Pescara Sud exit is close by.',
    "Sulla collina sopra Francavilla al Mare, in Abruzzo, a 5 km dal centro di Pescara. Chieti, Pescara e l'Aeroporto Internazionale d'Abruzzo sono a circa 15 minuti, la stazione di Pescara Centrale ha comodi collegamenti e l'uscita A14 Pescara Sud è vicina.")
CHECKIN = ('What are the check-in and check-out times?', 'Quali sono gli orari di check-in e check-out?',
    'Check-in is from 14:00 and check-out is by 11:00. An early check-in is possible for a supplement, subject to availability, and you can leave your luggage with us after check-out. For a late check-out, ask us and we will do our best.',
    'Il check-in è dalle 14:00 e il check-out entro le 11:00. Il check-in anticipato è possibile con supplemento, secondo disponibilità, e dopo il check-out puoi lasciare i bagagli in hotel. Per un check-out posticipato chiedicelo e faremo il possibile.')
PARKING = ('Is there parking?', "C'è il parcheggio?",
    'Yes. Outdoor parking is free for guests and has charging points for electric cars.',
    'Sì. Il parcheggio all’aperto è gratuito per gli ospiti e ha colonnine di ricarica per auto elettriche.')
SPA = ('What is in the Linfa wellness & spa?', "Cosa c'è nella spa Linfa?",
    'Indoor and outdoor pools with hydromassage points, a whirlpool, saunas, a Turkish bath, chromotherapy and aromatherapy showers, a herbal tea corner and a private garden. Every hotel guest has a free two-hour session; booking is required (+39 085 45 00 55 60). Massages for one or two can be added.',
    'Piscine interna ed esterna con punti idromassaggio, vasca idromassaggio, saune, bagno turco, docce di cromoterapia e aromaterapia, angolo tisane e giardino privato. Ogni ospite ha una sessione gratuita di due ore; la prenotazione è obbligatoria (+39 085 45 00 55 60). Si possono aggiungere massaggi per uno o per due.')
DIRECT = ('Why book directly with the hotel?', 'Perché prenotare direttamente con l’hotel?',
    'You get the package exactly as designed, a real person before and during your stay, and extras that are not on booking sites, such as the €50 welcome coupon (code FAMILY50) for your next direct booking.',
    'Hai il pacchetto esattamente come progettato, una persona vera prima e durante il soggiorno ed extra che non trovi sui portali, come il buono di benvenuto da 50 € (codice FAMILY50) per la tua prossima prenotazione diretta.')
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
FAM_VOUCHER = ('How does the €50 welcome coupon work?', 'Come funziona il buono di benvenuto da 50 €?',
    'Join our family list (the sign-up on the home page) and you get the code FAMILY50: €50 off your next stay when you book directly with us. Add the code in the promo field of the booking form.',
    'Iscriviti alla nostra lista famiglie (il modulo sulla home page) e ricevi il codice FAMILY50: 50 € di sconto sul prossimo soggiorno prenotando direttamente con noi. Inserisci il codice nel campo promo del modulo di prenotazione.')

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
    'Yes, pets of all sizes are welcome for a supplement. The Cottage, at the hotel entrance, has a fully fenced outdoor area for them. Tell us when you book so we can prepare the right room.',
    'Sì, gli animali di ogni taglia sono benvenuti con un supplemento. Il Cottage, all’ingresso dell’hotel, ha un’area esterna recintata per loro. Diccelo quando prenoti, così prepariamo la camera giusta.')
POOLS = ('What pools does the hotel have?', "Che piscine ha l'hotel?",
    'Two outdoor pools in the park: the Blue Pool, up to 2.5 m deep (open until 15 September), and the Riviera Pool for children, no deeper than 50 cm, with a twelve-jet fountain and a water umbrella (open until 30 September). The Linfa spa has indoor and outdoor pools with hydromassage all year.',
    'Due piscine all’aperto nel parco: la Blue Pool, profonda fino a 2,5 m (aperta fino al 15 settembre), e la Riviera Pool per i bambini, profonda al massimo 50 cm, con fontana a dodici getti e ombrello d’acqua (aperta fino al 30 settembre). La spa Linfa ha piscine interna ed esterna con idromassaggio tutto l’anno.')
BEACH = ('Is there a beach?', "C'è una spiaggia?",
    'Yes. A free shuttle takes you to a white-sand beach in Francavilla al Mare, a few kilometres away, at a private lido with a bar and restaurant that has an agreement with the hotel.',
    'Sì. Una navetta gratuita ti porta su una spiaggia di sabbia bianca a Francavilla al Mare, a pochi chilometri, in un lido privato convenzionato con bar e ristorante.')
KIDS = ('What is there for children?', 'Cosa c’è per i bambini?',
    'In July and August the Kids Club has a play room with games, books and puzzles, educational workshops from Tuesday to Saturday and an outdoor play area. There is also the Riviera Pool for children, the park, padel and the beach by shuttle. Nearby, families love the Guardiagrele adventure park and the zoo in Lanciano.',
    'A luglio e agosto il Kids Club offre sala giochi con giochi, libri e puzzle, laboratori didattici dal martedì al sabato e un’area giochi all’aperto. Ci sono anche la Riviera Pool per i bambini, il parco, il padel e la spiaggia con la navetta. Nei dintorni le famiglie amano il parco avventura di Guardiagrele e lo zoo di Lanciano.')
NEARBY = ('What can we do nearby?', 'Cosa possiamo fare nei dintorni?',
    'Cycle the Bike to Coast path towards the Costa dei Trabocchi, a few minutes from the hotel, walk in the Pineta Dannunziana nature reserve in Pescara, or join a guided excursion to the Majella and Gran Sasso national parks, Chieti and Pescara.',
    'Pedalare sulla pista Bike to Coast verso la Costa dei Trabocchi, a pochi minuti dall’hotel, passeggiare nella riserva Pineta Dannunziana a Pescara o partecipare a un’escursione guidata nei parchi nazionali della Majella e del Gran Sasso, a Chieti e a Pescara.')
ROOMS_Q = ('Which room is right for me?', 'Quale camera fa per me?',
    'For a short stay on a budget, the Standard Room faces the park. The Superior Room, near the spa with a pine grove or distant sea view, suits 1 to 2 nights. Deluxe rooms and Junior Suites have terraces over the sea or the park, Family Rooms suit families, and the Mini SPA and Master SPA Suites have their own spa in the room.',
    'Per un soggiorno breve a budget contenuto, la Camera Standard guarda il parco. La Camera Superior, vicino alla spa con vista pineta o mare in lontananza, è ideale per 1–2 notti. Deluxe e Junior Suite hanno terrazze sul mare o sul parco, le Family Room sono pensate per le famiglie e le Mini SPA e Master SPA Suite hanno la spa in camera.')
REST_Q = ('Is breakfast included?', 'La colazione è inclusa?',
    'Breakfast is included in our packages and served as a buffet from 7:00 to 10:00, on the terrace in the warmer months. Lunch is 12:30–14:00 and dinner 19:30–22:00.',
    'La colazione è inclusa nei pacchetti ed è servita a buffet dalle 7:00 alle 10:00, in terrazza nei mesi più caldi. Il pranzo è dalle 12:30 alle 14:00 e la cena dalle 19:30 alle 22:00.')

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
    'beyond-the-meeting-room.html': [BIZ_PADEL, BIZ_MEET, BIZ_INVOICE, PARKING],
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
