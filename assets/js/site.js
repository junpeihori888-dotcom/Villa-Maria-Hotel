/* Villa Maria Hotel & Spa — shared header, MENU overlay, footer, Help (contact) panel,
   phone booking bar and EN/IT switch. */
(function () {
  'use strict';

  /* ======================================================================
     HOTEL SETTINGS — the only place to edit hotel facts.
     Leave a field empty ('') and the site hides it instead of showing a guess.
     ====================================================================== */
  var HOTEL = {
    name: 'Villa Maria Hotel & Spa',
    legalName: '',            // company name as registered, e.g. 'Villa Maria S.r.l.'
    vat: '',                  // P.IVA, e.g. '01234567890'
    cin: '',                  // Codice Identificativo Nazionale, e.g. 'IT069035A1XXXXXXXX'
    phone: '',                // e.g. '+39 085 000 0000'
    whatsapp: '',             // digits only with country code, e.g. '39333000000'
    email: '',                // e.g. 'info@yourhotel.it'
    conciergeHours: { en: '', it: '' },   // e.g. { en: 'Concierge desk: 7:00–23:00, every day', it: 'Concierge: 7:00–23:00, tutti i giorni' }
    checkIn: '',              // e.g. '14:00'
    checkOut: '',             // e.g. '11:00'
    // Shown next to the message button. Keep it true to how fast the team really answers.
    replyTime: { en: 'We typically reply within 30 minutes', it: 'Di solito rispondiamo entro 30 minuti' },
    // Address as shown on booking sites. Confirm before going live.
    address: 'Contrada Pretaro, Via San Paolo, 66023 Francavilla al Mare (CH), Italy',
    mapsUrl: 'https://www.google.com/maps/search/?api=1&query=Villa+Maria+Hotel+%26+Spa+Francavilla+al+Mare',
    reviews: {
      rating: '',             // e.g. '4.6' — shown only together with count
      count: '',              // e.g. '1,240'
      source: 'Google'        // where the rating comes from
    }
  };

  /* Where our own forms (booking requests, reviews, messages, sign-ups) are sent.
     Any service that accepts a JSON POST works: your own server, Formspree, Basin,
     a Google Apps Script web app… Leave empty and forms run in demo mode
     (the guest sees a clear "not sent" note). */
  var FORMS_ENDPOINT = '';

  /* Reviews are only for guests who have stayed. This server receives
     {reference, email} and answers {verified: true|false, name?} after checking
     that the booking exists and its check-out date has passed. Leave empty and the
     review form runs in demo mode (it says so and nothing is checked). */
  var REVIEW_VERIFY_ENDPOINT = '';

  /* AI chat in Help. Your own server receives {messages: [{role, content}], lang, facts}
     and answers {reply}. It should call an AI model with the facts as its only source.
     Leave empty: inside the claude.ai preview the chat uses Claude itself; elsewhere it
     gives instant answers from the FAQ and says so. */
  var CHAT_ENDPOINT = '';

  var OFFERS = {
    familyDiscount: {
      fromPrice: '',          // e.g. '€189' (per night, room for the family)
      validFrom: '',          // e.g. '1 June 2027'
      validTo: '',            // e.g. '30 September 2027'
      minNights: ''           // e.g. '3'
    }
  };

  /* ---------- Language and paths ---------- */
  var lang = document.documentElement.lang === 'it' ? 'it' : 'en';
  var BASE = lang === 'it' ? '../' : '';     // Italian pages live in /it/
  var page = location.pathname.split('/').pop() || 'index.html';
  if (!/\.html$/.test(page)) page = 'index.html';
  function t(en, it) { return lang === 'it' ? it : en; }

  // [href, EN name, IT name]
  var PAGES = {
    families: [
      ['italian-memories.html', 'Italian Memories', 'Italian Memories'],
      ['family-reset-package.html', 'Family Discount', 'Sconto Famiglia'],
      ['ciao-again.html', 'Ciao Again', 'Ciao Again']
    ],
    business: [
      ['business-travel.html', 'Take the pressure out of business travel', 'Viaggiare per lavoro, senza pressione'],
      ['executive-business-stay.html', 'Executive Business Stay Package', 'Pacchetto Executive Business Stay'],
      ['padel-experience.html', 'The Padel Experience', 'La Padel Experience']
    ],
    hotel: [
      ['index.html', 'Home', 'Home', 'villa-adriatic.jpg'],
      ['rooms.html', 'Rooms & Suites', 'Camere e Suite', 'deluxe-room.jpg'],
      ['spa.html', 'Linfa Wellness & Spa', 'Linfa Wellness & Spa', 'spa.jpg'],
      ['restaurant.html', 'Restaurant', 'Ristorante', 'restaurant-hall.jpg'],
      ['contact.html', 'Getting here & contact', 'Come arrivare e contatti', 'gardens.jpg']
    ]
  };

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }
  function links(list, withPhotos) {
    return list.map(function (p) {
      var cur = p[0] === page ? ' aria-current="page"' : '';
      var img = withPhotos && p[3] ? '<img src="' + BASE + 'assets/img/' + p[3] + '" alt="" loading="lazy">' : '';
      return '<li><a href="' + p[0] + '"' + cur + (img ? ' class="with-photo"' : '') + '>' + img + '<span>' + esc(t(p[1], p[2])) + '</span></a></li>';
    }).join('');
  }
  function telHref(n) { return 'tel:' + n.replace(/[^\d+]/g, ''); }

  /* Contact lines used by the footer, Help panel and contact page (empty fields are skipped). */
  function contactList() {
    var out = [];
    if (HOTEL.phone) out.push('<li><span class="k">' + t('Phone', 'Telefono') + '</span><a href="' + telHref(HOTEL.phone) + '">' + esc(HOTEL.phone) + '</a></li>');
    if (HOTEL.whatsapp) out.push('<li><span class="k">WhatsApp</span><a href="https://wa.me/' + esc(HOTEL.whatsapp) + '" rel="noopener">' + t('Message us', 'Scrivici') + '</a></li>');
    if (HOTEL.email) out.push('<li><span class="k">Email</span><a href="mailto:' + esc(HOTEL.email) + '">' + esc(HOTEL.email) + '</a></li>');
    out.push('<li><span class="k">' + t('Address', 'Indirizzo') + '</span><span>' + esc(HOTEL.address) + '<br><a href="' + HOTEL.mapsUrl + '" rel="noopener">' + t('Open in Google Maps', 'Apri in Google Maps') + ' →</a></span></li>');
    if (HOTEL.conciergeHours[lang]) out.push('<li><span class="k">Concierge</span><span>' + esc(HOTEL.conciergeHours[lang]) + '</span></li>');
    return '<ul class="contact-list">' + out.join('') + '</ul>';
  }

  /* ---------- Header ---------- */
  var enHref = lang === 'it' ? '../' + page : page;
  var itHref = lang === 'it' ? page : 'it/' + page;
  var header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML =
    '<div class="wrap">' +
      '<button type="button" class="menu-btn" aria-expanded="false" aria-controls="menu">Menu</button>' +
      '<a class="logo" href="index.html"><img src="' + BASE + 'assets/img/logo.png" alt="Villa Maria Hotel &amp; Spa" width="858" height="462"></a>' +
      '<div class="header-right">' +
        '<nav class="lang" aria-label="' + t('Language', 'Lingua') + '">' +
          '<a href="' + enHref + '" hreflang="en" lang="en"' + (lang === 'en' ? ' aria-current="true"' : '') + '>EN</a>' +
          '<a href="' + itHref + '" hreflang="it" lang="it"' + (lang === 'it' ? ' aria-current="true"' : '') + '>IT</a>' +
        '</nav>' +
        '<a class="btn btn-slate header-book" href="booking.html">' + t('Book Now', 'Prenota') + '</a>' +
      '</div>' +
    '</div>';

  /* ---------- Menu overlay ---------- */
  var menu = document.createElement('div');
  menu.className = 'menu';
  menu.id = 'menu';
  menu.setAttribute('role', 'dialog');
  menu.setAttribute('aria-modal', 'true');
  menu.setAttribute('aria-label', 'Menu');
  menu.innerHTML =
    '<div class="wrap menu-top"><button type="button" class="menu-close">' + t('Close ✕', 'Chiudi ✕') + '</button>' +
      '<a class="btn btn-sky" href="booking.html">' + t('Book Now', 'Prenota') + '</a></div>' +
    '<nav class="wrap menu-grid" aria-label="' + t('Main', 'Principale') + '">' +
      '<div><h3>' + t('For families', 'Per le famiglie') + '</h3><ul>' + links(PAGES.families) + '</ul></div>' +
      '<div><h3>' + t('For business', 'Per il business') + '</h3><ul>' + links(PAGES.business) + '</ul></div>' +
      '<div><h3>' + t('The hotel', "L'hotel") + '</h3><ul class="menu-photos">' + links(PAGES.hotel, true) + '</ul></div>' +
    '</nav>' +
    '<div class="wrap menu-foot"><span>' + esc(HOTEL.address) + '</span>' +
      (HOTEL.phone ? '<a href="' + telHref(HOTEL.phone) + '">' + esc(HOTEL.phone) + '</a>' : '') + '</div>';

  /* ---------- Footer ---------- */
  var legal = [];
  if (HOTEL.legalName) legal.push(esc(HOTEL.legalName));
  if (HOTEL.vat) legal.push('P.IVA ' + esc(HOTEL.vat));
  if (HOTEL.cin) legal.push('CIN ' + esc(HOTEL.cin));
  var footer = document.createElement('footer');
  footer.className = 'site-footer';
  footer.id = 'contact';
  footer.innerHTML =
    '<div class="wrap">' +
      '<div><div class="brand">Villa Maria<br>Hotel &amp; Spa</div>' + contactList() + '</div>' +
      '<div><h4>' + t('Families', 'Famiglie') + '</h4><ul>' + links(PAGES.families) + '</ul></div>' +
      '<div><h4>Business</h4><ul>' + links(PAGES.business) + '</ul></div>' +
      '<div><h4>' + t('The hotel', "L'hotel") + '</h4><ul>' + links(PAGES.hotel.slice(1)) + '</ul></div>' +
      '<div class="legal"><span>© 2026 ' + esc(HOTEL.name) + (legal.length ? ' · ' + legal.join(' · ') : '') + '</span>' +
        '<a href="privacy.html">' + t('Privacy & cookies', 'Privacy e cookie') + '</a></div>' +
    '</div>';

  /* ---------- Help panel: direct channels, quick answers, message ---------- */
  var ICONS = {
    phone: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    whatsapp: '<path d="M3 21l1.6-4.8A8.5 8.5 0 1 1 7.8 19.5z"/><path d="M9 9.5c.3 2 2.2 4.3 5 5l1.2-1.4-2-1-1 .8c-1-.4-1.9-1.3-2.3-2.3l.8-1-1-2z"/>',
    email: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'
  };
  function channel(kind, href, label, sub) {
    return '<a class="channel" href="' + href + '"' + (kind === 'whatsapp' ? ' rel="noopener"' : '') + '>' +
      '<svg viewBox="0 0 24 24" aria-hidden="true">' + ICONS[kind] + '</svg><span><b>' + label + '</b><small>' + esc(sub) + '</small></span></a>';
  }
  var channels = [];
  if (HOTEL.phone) channels.push(channel('phone', telHref(HOTEL.phone), t('Call us', 'Chiamaci'), HOTEL.phone));
  if (HOTEL.whatsapp) channels.push(channel('whatsapp', 'https://wa.me/' + HOTEL.whatsapp, 'WhatsApp', t('Chat now', 'Scrivici ora')));
  if (HOTEL.email) channels.push(channel('email', 'mailto:' + HOTEL.email, 'Email', HOTEL.email));

  var QUICK = [
    [t('Check-in & check-out times', 'Orari di check-in e check-out'),
      (HOTEL.checkIn && HOTEL.checkOut
        ? t('Check-in from ' + HOTEL.checkIn + ', check-out by ' + HOTEL.checkOut + '. ', 'Check-in dalle ' + HOTEL.checkIn + ', check-out entro le ' + HOTEL.checkOut + '. ')
        : t('Your check-in and check-out times are in your booking confirmation. ', 'Gli orari di check-in e check-out sono nella conferma di prenotazione. ')) +
      t('Need an early check-in or a late check-out? Ask us and we will do our best.', 'Ti serve un check-in anticipato o un check-out posticipato? Chiedicelo e faremo il possibile.')],
    [t('Parking & shuttle services', 'Parcheggio e navetta'),
      t('Free private parking on site, with EV charging. Family Discount guests get a free shuttle to our partner beach. Ask us about transfers from Pescara Airport or station.',
        'Parcheggio privato gratuito in hotel, con ricarica per auto elettriche. Con lo Sconto Famiglia la navetta per la spiaggia convenzionata è gratuita. Chiedici dei transfer dall\'aeroporto o dalla stazione di Pescara.')],
    [t('Cancellation policy', 'Politica di cancellazione'),
      t('Book your next stay during your visit (10% off) and you can cancel for free up to 6 months before arrival, and change dates up to 6 weeks before. For other bookings, the terms are in your booking confirmation.',
        'Prenota il prossimo soggiorno durante la tua visita (10% di sconto): cancellazione gratuita fino a 6 mesi prima dell\'arrivo e cambio date fino a 6 settimane prima. Per le altre prenotazioni, le condizioni sono nella conferma.')]
  ];

  var help = document.createElement('div');
  help.className = 'modal';
  help.hidden = true;
  help.setAttribute('role', 'dialog');
  help.setAttribute('aria-modal', 'true');
  help.setAttribute('aria-labelledby', 'help-title');
  help.innerHTML =
    '<div class="modal-box help-box">' +
      '<button type="button" class="modal-x" aria-label="' + t('Close', 'Chiudi') + '">×</button>' +
      '<p class="eb">' + t('Help', 'Aiuto') + '</p>' +
      '<h2 id="help-title">' + t('How can we help?', 'Come possiamo aiutarti?') + '</h2>' +
      (channels.length ? '<div class="channels">' + channels.join('') + '</div>' : '') +
      (HOTEL.conciergeHours[lang] ? '<p class="hours">' + t('Concierge desk', 'Concierge') + ': ' + esc(HOTEL.conciergeHours[lang]) + '</p>' : '') +
      '<button type="button" class="btn btn-sky btn-block help-msg" data-form="message">' + t('Send us a message', 'Scrivici un messaggio') + '</button>' +
      (HOTEL.replyTime[lang] ? '<p class="reply-time"><span class="dot" aria-hidden="true"></span>' + esc(HOTEL.replyTime[lang]) + '</p>' : '') +
      '<p class="eb" style="margin-top:22px">' + t('Quick answers', 'Risposte rapide') + '</p>' +
      '<div class="quick">' + QUICK.map(function (q) {
        return '<details><summary>' + q[0] + '</summary><p>' + q[1] + '</p></details>';
      }).join('') + '</div>' +
      '<section class="ai-chat" aria-label="' + t('Ask our assistant', 'Chiedi al nostro assistente') + '">' +
        '<div class="chat-head"><p class="eb">' + t('Ask our assistant', 'Chiedi al nostro assistente') + '</p><span class="chat-mode">' + t('Instant answers', 'Risposte immediate') + '</span></div>' +
        '<div class="chat-log" aria-live="polite"></div>' +
        '<div class="chat-chips">' +
          [t('Is there a Kids Club?', 'C’è un Kids Club?'), t('Can I get a company invoice?', 'Posso avere la fattura aziendale?'), t('How far is Pescara airport?', 'Quanto dista l’aeroporto di Pescara?')]
            .map(function (q) { return '<button type="button" class="chip">' + q + '</button>'; }).join('') +
        '</div>' +
        '<form class="chat-form"><label class="sr-only" for="chat-in">' + t('Your question', 'La tua domanda') + '</label>' +
          '<input id="chat-in" autocomplete="off" maxlength="500" placeholder="' + t('Ask about rooms, spa, parking…', 'Chiedi di camere, spa, parcheggio…') + '">' +
          '<button type="submit" class="btn btn-slate chat-send">' + t('Ask', 'Chiedi') + '</button></form>' +
        '<p class="chat-note">' + t('Answers come from our hotel information and can be wrong. Our team confirms bookings and anything important by email.',
          'Le risposte si basano sulle informazioni dell’hotel e possono contenere errori. Il nostro team conferma prenotazioni e dettagli importanti via email.') + '</p>' +
      '</section>' +
      '<a class="btn btn-slate btn-block" style="margin-top:18px" href="booking.html">' + t('Book your stay', 'Prenota il soggiorno') + '</a>' +
    '</div>';


  /* ---------- AI chat (Help) ---------- */
  // Hotel facts the assistant may use — the same facts as the FAQ. [match, EN, IT]
  var KB = [
    [/where|locat|address|airport|train|station|motorway|a14|get there|reach|dove|indirizz|aeroporto|stazione|autostrada|arrivare|pescara/i,
      'Villa Maria is on the hill above Francavilla al Mare, just south of Pescara in Abruzzo. Abruzzo Airport (Pescara) is a short drive away, Pescara Centrale station has easy rail connections, and the A14 Pescara Sud exit is close by.',
      'Villa Maria è sulla collina sopra Francavilla al Mare, appena a sud di Pescara, in Abruzzo. L’aeroporto d’Abruzzo (Pescara) è a pochi minuti d’auto, la stazione di Pescara Centrale ha comodi collegamenti e l’uscita A14 Pescara Sud è vicina.'],
    [/check.?in|check.?out|arriv|depart|time|orari|partenza/i, QUICK[0][1], QUICK[0][1]],
    [/park|car\b|ev\b|charg|shuttle|beach|transfer|parchegg|navetta|spiaggia|ricarica/i, QUICK[1][1], QUICK[1][1]],
    [/cancel|refund|change.*date|cancell|rimbors|modific/i, QUICK[2][1], QUICK[2][1]],
    [/spa|sauna|pool|wellness|massage|treatment|linfa|piscin|benessere|massagg|trattament/i,
      'The Linfa wellness & spa has pools, a sauna, relaxation areas and treatments for one or two. The hotel also has two outdoor pools in a private park. For spa hours and treatment prices, send us a message.',
      'La spa Linfa ha piscine, sauna, aree relax e trattamenti per uno o per due. L’hotel ha anche due piscine all’aperto in un parco privato. Per orari e prezzi dei trattamenti, scrivici un messaggio.'],
    [/kid|child|family|teen|famil|bambin|ragazz/i,
      'Families have two outdoor pools in a private park, a Kids Club, padel, a free shuttle to our partner beach and family dinners with Abruzzo recipes. The Family Discount includes room, breakfast and spa.',
      'Le famiglie hanno due piscine all’aperto in un parco privato, un Kids Club, il padel, una navetta gratuita per la spiaggia convenzionata e cene con ricette abruzzesi. Lo Sconto Famiglia include camera, colazione e spa.'],
    [/discount|voucher|€\s?20|20\s?€|offer|sconto|offerta/i,
      'With the Family Discount, first-time guests who book directly get a €20 in-house voucher for food and drink or the spa (valid during that stay). Book your next stay during your visit and get 10% off the room rate.',
      'Con lo Sconto Famiglia, chi prenota direttamente per la prima volta riceve un voucher da 20 € per food and beverage o spa (valido durante il soggiorno). Prenota il prossimo soggiorno durante la visita e hai il 10% sulla camera.'],
    [/meeting|conference|auditorium|room for.*people|video|riunion|conferenz|sala/i,
      'We have private meeting rooms and an auditorium, with video-conferencing and fast Wi-Fi. Send us a message with your group size and we will confirm the right room.',
      'Abbiamo sale riunioni riservate e un auditorium, con videoconferenza e Wi-Fi veloce. Scrivici il numero di partecipanti e ti confermiamo la sala giusta.'],
    [/invoice|company|corporate|business|fattur|aziend|lavoro/i,
      'Yes, we invoice your company directly and accept corporate cards. If you have a company code, add it when you book. The Executive Business Stay Package includes early breakfast, fast Wi-Fi, spa and a meeting room on request.',
      'Sì, fatturiamo direttamente alla tua azienda e accettiamo carte aziendali. Se hai un codice aziendale, inseriscilo quando prenoti. Il Pacchetto Executive Business Stay include colazione presto, Wi-Fi veloce, spa e sala riunioni su richiesta.'],
    [/padel/i,
      'Our padel courts are in the gardens above the Adriatic. The Padel Experience pairs a match with the spa, an aperitivo at the bar and dinner at the chef’s table.',
      'I campi da padel sono nei giardini sopra l’Adriatico. La Padel Experience abbina la partita a spa, aperitivo al bar e cena alla tavola dello chef.'],
    [/breakfast|restaurant|dinner|lunch|food|eat|colazion|ristorant|cena|pranzo|mangiare/i,
      'Breakfast is a local buffet and is included in our packages. The hotel restaurant serves Abruzzo recipes, and the bar serves aperitivo in the evening.',
      'La colazione è a buffet con prodotti locali ed è inclusa nei pacchetti. Il ristorante dell’hotel propone ricette abruzzesi e il bar serve l’aperitivo la sera.'],
    [/room|suite|superior|deluxe|view|camer|vista/i,
      'The Superior Room has a garden or partial sea view and a desk, good for 1–2 nights. The Deluxe Room and Suites have more space and Adriatic views; the Suite has a private terrace with a hot tub.',
      'La Camera Superior ha vista giardino o parziale vista mare e scrivania, ideale per 1–2 notti. Le Camere Deluxe e le Suite hanno più spazio e vista Adriatico; la Suite ha una terrazza privata con vasca idromassaggio.'],
    [/price|cost|rate|how much|cheap|prezz|costo|tariff|quanto/i,
      'Prices depend on your dates and room. Choose them on our booking page and we confirm the price by email. Nothing is charged when you send the request.',
      'I prezzi dipendono da date e camera. Sceglile nella pagina di prenotazione e ti confermiamo il prezzo via email. Inviare la richiesta non comporta alcun pagamento.'],
    [/book|reserv|availab|prenot|disponib/i,
      'You can book on our booking page: pick your dates in the calendar, choose a package and room, and send the request. We reply by email with the price and confirmation.',
      'Puoi prenotare nella nostra pagina di prenotazione: scegli le date nel calendario, il pacchetto e la camera, e invia la richiesta. Ti rispondiamo via email con prezzo e conferma.']
  ];
  var FACTS = KB.map(function (k) { return '- ' + k[1]; }).join('\n') +
    (HOTEL.phone ? '\n- Phone: ' + HOTEL.phone : '') + (HOTEL.email ? '\n- Email: ' + HOTEL.email : '') +
    (HOTEL.whatsapp ? '\n- WhatsApp: +' + HOTEL.whatsapp : '') + (HOTEL.conciergeHours.en ? '\n- Concierge desk: ' + HOTEL.conciergeHours.en : '');
  var RULES = 'You are the online assistant of Villa Maria Hotel & Spa, a four-star seaside hotel in Francavilla al Mare, Abruzzo, Italy. ' +
    'Answer guest questions using ONLY the HOTEL FACTS below. If the answer is not in the facts, say you are not sure and suggest the "Send us a message" button above the chat, or the booking page for dates and prices. ' +
    'Never invent prices, availability, opening hours, phone numbers or policies. Reply in the guest\'s language (Italian or English; default ' + (lang === 'it' ? 'Italian' : 'English') + '). ' +
    'Keep replies to 1-3 short sentences, warm and plain, with no markdown, lists or headings.\n\nHOTEL FACTS:\n' + FACTS;

  var chatBox = help.querySelector('.ai-chat'), log = chatBox.querySelector('.chat-log'),
      chatForm = chatBox.querySelector('.chat-form'), chatIn = chatBox.querySelector('#chat-in'),
      sendBtn = chatBox.querySelector('.chat-send'), modeEl = chatBox.querySelector('.chat-mode');
  var turns = [], engine = CHAT_ENDPOINT ? 'server' : 'faq', sampleFn = null, ctl = null;
  function setMode() { modeEl.textContent = engine === 'faq' ? t('Instant answers', 'Risposte immediate') : t('AI assistant', 'Assistente AI'); }
  setMode();
  if (!CHAT_ENDPOINT && window.claude && typeof window.claude.use === 'function') {
    window.claude.use('sample').then(function (fn) { if (fn) { sampleFn = fn; engine = 'claude'; setMode(); } }).catch(function () {});
  }
  function bubble(role, text) {
    var b = document.createElement('div');
    b.className = 'msg msg-' + role;
    b.textContent = text;
    log.appendChild(b);
    log.scrollTop = log.scrollHeight;
    return b;
  }
  function faqAnswer(q) {
    for (var i = 0; i < KB.length; i++) if (KB[i][0].test(q)) return t(KB[i][1], KB[i][2]);
    return t('I am not sure about that one. Use "Send us a message" above and our team will reply.', 'Su questo non sono sicuro. Usa "Scrivici un messaggio" qui sopra e il nostro team ti risponderà.');
  }
  function busy(on) {
    sendBtn.textContent = on ? t('Stop', 'Stop') : t('Ask', 'Chiedi');
    sendBtn.classList.toggle('is-stop', on);
    chatIn.disabled = on;
  }
  function ask(q) {
    q = String(q || '').trim();
    if (!q) return;
    chatBox.querySelector('.chat-chips').hidden = true;
    bubble('user', q);
    turns.push({ role: 'user', content: q });
    turns = turns.slice(-10);
    var out = bubble('bot', t('Thinking…', 'Sto pensando…'));
    out.classList.add('is-pending');
    function done(text) { out.classList.remove('is-pending'); out.textContent = text; turns.push({ role: 'assistant', content: text }); busy(false); chatIn.focus(); }
    if (engine === 'faq') { setTimeout(function () { done(faqAnswer(q)); }, 250); return; }
    busy(true);
    ctl = new AbortController();
    var history = turns[0].role === 'user' ? turns : turns.slice(1);
    var call = engine === 'server'
      ? fetch(CHAT_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, signal: ctl.signal,
          body: JSON.stringify({ messages: history, lang: lang, facts: FACTS }) })
          .then(function (r) { if (!r.ok) throw { code: 'upstream_error' }; return r.json(); }).then(function (j) { return { text: String(j.reply || '') }; })
      : sampleFn([{ role: 'user', content: RULES }].concat(history), {
          modelTier: 'quick', cache: false, signal: ctl.signal,
          onText: function (u) { out.classList.remove('is-pending'); out.textContent = u.text; log.scrollTop = log.scrollHeight; } });
    call.then(function (r) { done(r.text || faqAnswer(q)); }).catch(function (e) {
      var code = e && e.code;
      if (code === 'cancelled' || (e && e.name === 'AbortError')) { done(e.text || t('Stopped.', 'Interrotto.')); return; }
      if (['not_granted', 'sampling_disabled', 'not_declared', 'capability_disabled', 'capability_removed'].indexOf(code) >= 0) {
        engine = 'faq'; setMode(); done(faqAnswer(q)); return;          // AI not allowed here: answer from the FAQ instead
      }
      if (code === 'rate_limited') { done(t('Lots of questions right now. Please try again in a minute, or send us a message.', 'Troppe domande in questo momento. Riprova tra un minuto o scrivici un messaggio.')); return; }
      done(faqAnswer(q));
    });
  }
  chatForm.addEventListener('submit', function (e) {
    e.preventDefault();
    if (sendBtn.classList.contains('is-stop')) { if (ctl) ctl.abort(); return; }
    var q = chatIn.value; chatIn.value = ''; ask(q);
  });
  chatBox.querySelectorAll('.chip').forEach(function (c) { c.addEventListener('click', function () { ask(c.textContent); }); });

  /* ---------- Phone booking bar ---------- */
  var bar = document.createElement('div');
  bar.className = 'book-bar';
  bar.innerHTML =
    '<button type="button" class="btn btn-line" data-help>' + t('Help', 'Aiuto') + '</button>' +
    '<a class="btn btn-slate" href="booking.html">' + t('Book Now', 'Prenota') + '</a>';

  var fab = document.createElement('button');
  fab.type = 'button';
  fab.className = 'btn btn-slate help-fab';
  fab.setAttribute('data-help', '');
  fab.textContent = t('Help', 'Aiuto');

  /* ---------- Our own forms: review, community, referral, message ---------- */
  // [name, type, EN label, IT label, required]
  var FORMS = {
    review: {
      title: t('Write a review', 'Scrivi una recensione'),
      intro: t('Your stay is verified. Tell other guests what it was like.', 'Il tuo soggiorno è verificato. Racconta agli altri ospiti com’è stato.'),
      fields: [['rating', 'stars', 'Your rating', 'Il tuo voto', true], ['name', 'text', 'Name (as shown with your review)', 'Nome (visibile con la recensione)', true],
               ['review', 'textarea', 'Your review', 'La tua recensione', true]],
      thanks: t('Thank you. Your review will appear after we check your stay.', 'Grazie. La tua recensione apparirà dopo la verifica del soggiorno.')
    },
    verify: {
      title: t('Reviews from our guests', 'Recensioni dei nostri ospiti'),
      intro: t('Only guests who have stayed with us can write a review. Enter the booking reference from your confirmation email and the email you booked with. After check-out we also email you a personal review link.',
               'Solo gli ospiti che hanno soggiornato da noi possono scrivere una recensione. Inserisci il codice della conferma di prenotazione e l’email usata per prenotare. Dopo il check-out ti inviamo anche un link personale per la recensione.'),
      fields: [['reference', 'text', 'Booking reference (e.g. VM-AB12CD)', 'Codice di prenotazione (es. VM-AB12CD)', true], ['email', 'email', 'Email used for the booking', 'Email usata per la prenotazione', true]],
      submit: t('Check my stay', 'Verifica il soggiorno'),
      noConsent: true
    },
    join: {
      title: t('Join the Villa Maria family', 'Entra nella famiglia Villa Maria'),
      intro: t('Loyalty thank-yous, new seasons first and moments kept for returning guests.', 'Ringraziamenti fedeltà, nuove stagioni in anteprima e momenti riservati agli ospiti che tornano.'),
      fields: [['name', 'text', 'Name', 'Nome', true], ['email', 'email', 'Email', 'Email', true]],
      thanks: t('Welcome to the family. We will be in touch.', 'Benvenuto in famiglia. Ti scriveremo presto.')
    },
    refer: {
      title: t('Refer a colleague', 'Consiglia un collega'),
      intro: t('We will send your colleague a short welcome and look after them the way we look after you.', 'Invieremo al tuo collega un breve benvenuto e ci prenderemo cura di lui come facciamo con te.'),
      fields: [['name', 'text', 'Your name', 'Il tuo nome', true], ['email', 'email', 'Your email', 'La tua email', true],
               ['colleague', 'text', 'Colleague\'s name', 'Nome del collega', true], ['colleagueEmail', 'email', 'Colleague\'s email', 'Email del collega', true]],
      thanks: t('Thank you. We will welcome your colleague.', 'Grazie. Daremo il benvenuto al tuo collega.')
    },
    message: {
      title: t('Send us a message', 'Scrivici un messaggio'),
      intro: t('Questions about rooms, the spa, meetings or company rates? Our team replies by email.', 'Domande su camere, spa, riunioni o tariffe aziendali? Il nostro team risponde via email.'),
      fields: [['name', 'text', 'Name', 'Nome', true], ['email', 'email', 'Email', 'Email', true], ['message', 'textarea', 'Message', 'Messaggio', true]],
      thanks: t('Thank you. We will reply by email.', 'Grazie. Ti risponderemo via email.')
    }
  };

  /* Send a form to FORMS_ENDPOINT. Resolves {sent: true} when delivered, {sent: false} in demo mode. */
  function send(formName, data) {
    if (!FORMS_ENDPOINT) return new Promise(function (ok) { setTimeout(function () { ok({ sent: false }); }, 400); });
    return fetch(FORMS_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({ form: formName, lang: lang, page: page, sentAt: new Date().toISOString(), data: data })
    }).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return { sent: true }; });
  }
  window.VM = { send: send };

  function demoNote(text) {
    return '<p class="demo-note">' + (text || t('Demo mode: nothing was sent yet. The site owner connects forms in assets/js/site.js (FORMS_ENDPOINT).',
      'Modalità demo: non è stato inviato nulla. Il gestore del sito collega i moduli in assets/js/site.js (FORMS_ENDPOINT).')) + '</p>';
  }

  var formModal = document.createElement('div');
  formModal.className = 'modal';
  formModal.hidden = true;
  formModal.setAttribute('role', 'dialog');
  formModal.setAttribute('aria-modal', 'true');
  formModal.setAttribute('aria-labelledby', 'form-title');

  function fieldHtml(f) {
    var id = 'f-' + f[0], req = f[4] ? ' required' : '', label = '<label for="' + id + '">' + t(f[2], f[3]) + (f[4] ? '' : ' <span class="opt">' + t('(optional)', '(facoltativo)') + '</span>') + '</label>';
    if (f[1] === 'textarea') return '<div class="field">' + label + '<textarea id="' + id + '" name="' + f[0] + '" rows="4"' + req + '></textarea></div>';
    if (f[1] === 'stars') {
      var st = '';
      for (var i = 5; i >= 1; i--) st += '<input type="radio" id="' + id + i + '" name="' + f[0] + '" value="' + i + '"' + (i === 5 ? req : '') + '><label for="' + id + i + '" title="' + i + '/5">★</label>';
      return '<fieldset class="field stars-field"><legend>' + t(f[2], f[3]) + '</legend><div class="stars-in">' + st + '</div></fieldset>';
    }
    return '<div class="field">' + label + '<input id="' + id + '" name="' + f[0] + '" type="' + f[1] + '"' + (f[1] === 'email' ? ' autocomplete="email"' : f[0] === 'name' ? ' autocomplete="name"' : '') + req + '></div>';
  }
  /* Check that a booking exists and the stay is over before the review form opens. */
  function verifyStay(reference, email) {
    if (!REVIEW_VERIFY_ENDPOINT) {
      return new Promise(function (ok) { setTimeout(function () { ok({ verified: /^VM-[A-Z0-9]{6}$/i.test(reference), demo: true }); }, 400); });
    }
    return fetch(REVIEW_VERIFY_ENDPOINT, {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({ reference: reference, email: email })
    }).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); });
  }

  function openForm(name, ctx) {
    if (name === 'review' && !(ctx && ctx.verified)) { name = 'verify'; }
    ctx = ctx || {};
    var def = FORMS[name];
    if (!def) return;
    formModal.innerHTML =
      '<div class="modal-box">' +
        '<button type="button" class="modal-x" aria-label="' + t('Close', 'Chiudi') + '">×</button>' +
        '<h2 id="form-title">' + def.title + '</h2><p>' + (name === 'review' && ctx.demo ? t('Tell other guests what your stay was like.', 'Racconta agli altri ospiti com’è stato il tuo soggiorno.') : def.intro) + '</p>' +
        (ctx.demo ? demoNote(t('Demo mode: stays are not checked yet. The site owner connects REVIEW_VERIFY_ENDPOINT in assets/js/site.js.',
            'Modalità demo: i soggiorni non vengono ancora verificati. Il gestore del sito collega REVIEW_VERIFY_ENDPOINT in assets/js/site.js.')) : '') +
        '<form class="own-form" novalidate>' + def.fields.map(fieldHtml).join('') +
          (def.noConsent ? '' : '<label class="check"><input type="checkbox" name="consent" required><span>' +
            t('I agree that Villa Maria uses these details for this request, as described in the <a href="privacy.html">privacy notice</a>.',
              'Accetto che Villa Maria usi questi dati per questa richiesta, come descritto nell\'<a href="privacy.html">informativa privacy</a>.') + '</span></label>') +
          '<p class="err" hidden>' + t('Please complete the highlighted fields.', 'Completa i campi evidenziati.') + '</p>' +
          '<button type="submit" class="btn btn-slate btn-block">' + (def.submit || t('Send', 'Invia')) + '</button>' +
        '</form>' +
      '</div>';
    formModal.querySelector('.modal-x').addEventListener('click', function () { closeModal(formModal); });
    var f = formModal.querySelector('form');
    var fRef = f.elements.namedItem('reference'), fName = f.elements.namedItem('name');
    if (ctx.reference && fRef) fRef.value = ctx.reference;
    if (ctx.name && fName) fName.value = ctx.name;
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = false;
      f.querySelectorAll('[required]').forEach(function (el) {
        var ok = el.type === 'radio' ? !!f.querySelector('[name="' + el.name + '"]:checked') : el.type === 'checkbox' ? el.checked : el.checkValidity() && el.value.trim();
        (el.closest('.check') || el.closest('.field') || el).classList.toggle('is-bad', !ok);
        if (!ok) bad = true;
      });
      f.querySelector('.err').hidden = !bad;
      if (bad) return;
      var data = {};
      new FormData(f).forEach(function (v, k) { data[k] = v; });
      var btn = f.querySelector('[type=submit]');
      if (name === 'verify') {
        btn.disabled = true; btn.textContent = t('Checking…', 'Verifica in corso…');
        var ref = String(data.reference).trim().toUpperCase();
        verifyStay(ref, String(data.email).trim()).then(function (res) {
          if (res && res.verified) {
            openForm('review', { verified: true, demo: !!res.demo, reference: ref, email: String(data.email).trim(), name: res.name || '' });
          } else {
            btn.disabled = false; btn.textContent = def.submit;
            f.querySelector('.err').hidden = false;
            f.querySelector('.err').textContent = t('We could not find a completed stay with this reference and email. Check your confirmation email, or contact us.',
              'Non troviamo un soggiorno concluso con questo codice e questa email. Controlla la conferma di prenotazione o contattaci.');
          }
        }).catch(function () {
          btn.disabled = false; btn.textContent = def.submit;
          f.querySelector('.err').hidden = false;
          f.querySelector('.err').textContent = t('We could not check your stay right now. Please try again.', 'Non riusciamo a verificare il soggiorno ora. Riprova.');
        });
        return;
      }
      if (name === 'review') { data.reference = ctx.reference; data.email = ctx.email; data.verified = !ctx.demo; }
      btn.disabled = true; btn.textContent = t('Sending…', 'Invio in corso…');
      send(name, data).then(function (res) {
        f.outerHTML = '<p class="thanks">' + def.thanks + '</p>' + (res.sent ? '' : demoNote());
      }).catch(function () {
        btn.disabled = false; btn.textContent = t('Send', 'Invia');
        f.querySelector('.err').hidden = false;
        f.querySelector('.err').textContent = t('We could not send this. Please try again.', 'Invio non riuscito. Riprova.');
      });
    });
    if (!help.hidden) help.hidden = true;
    openModal(formModal);
  }


  /* ---------- Photo galleries: full-screen viewer ---------- */
  var lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.hidden = true;
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', t('Photo viewer', 'Visualizzatore foto'));
  lb.innerHTML =
    '<button type="button" class="lb-close" aria-label="' + t('Close', 'Chiudi') + '">×</button>' +
    '<button type="button" class="lb-prev" aria-label="' + t('Previous photo', 'Foto precedente') + '">‹</button>' +
    '<figure><figcaption><span class="lb-cap"></span><span class="lb-count"></span></figcaption></figure>' +
    '<button type="button" class="lb-next" aria-label="' + t('Next photo', 'Foto successiva') + '">›</button>';
  var lbItems = [], lbIdx = 0, lbFocus = null;
  function lbShow(i) {
    lbIdx = (i + lbItems.length) % lbItems.length;
    var a = lbItems[lbIdx];
    var img = lb.querySelector('img');
    if (!img) { img = document.createElement('img'); lb.querySelector('figure').insertBefore(img, lb.querySelector('figcaption')); }
    img.src = a.getAttribute('href');
    img.alt = a.getAttribute('data-caption') || '';
    lb.querySelector('.lb-cap').textContent = a.getAttribute('data-caption') || '';
    lb.querySelector('.lb-count').textContent = (lbIdx + 1) + ' / ' + lbItems.length;
  }
  function lbOpen(a) {
    lbItems = Array.prototype.slice.call(a.closest('.gallery').querySelectorAll('.g-item'));
    lbFocus = a;
    lbShow(lbItems.indexOf(a));
    lb.hidden = false;
    body.classList.add('no-scroll');
    lb.querySelector('.lb-close').focus();
  }
  function lbClose() { lb.hidden = true; body.classList.remove('no-scroll'); if (lbFocus) lbFocus.focus(); }
  lb.querySelector('.lb-close').addEventListener('click', lbClose);
  lb.querySelector('.lb-prev').addEventListener('click', function () { lbShow(lbIdx - 1); });
  lb.querySelector('.lb-next').addEventListener('click', function () { lbShow(lbIdx + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) lbClose(); });
  var touchX = null;
  lb.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX; touchX = null;
    if (Math.abs(dx) > 40) lbShow(lbIdx + (dx < 0 ? 1 : -1));
  });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'ArrowLeft') lbShow(lbIdx - 1);
    else if (e.key === 'ArrowRight') lbShow(lbIdx + 1);
    else if (e.key === 'Escape') { e.stopImmediatePropagation(); lbClose(); }
  }, true);
  document.addEventListener('click', function (e) {
    var a = e.target.closest('.g-item');
    if (a) { e.preventDefault(); lbOpen(a); }
  });

  /* ---------- Mount ---------- */
  var body = document.body;
  body.insertBefore(header, body.firstChild);
  var skip = document.createElement('a');
  skip.className = 'skip'; skip.href = '#main'; skip.textContent = t('Skip to content', 'Vai al contenuto');
  body.insertBefore(skip, body.firstChild);
  [menu, footer, help, formModal, bar, fab, lb].forEach(function (el) { body.appendChild(el); });

  /* Book buttons open our own booking page; data-book="family-discount" etc. preselects the package. */
  document.querySelectorAll('[data-book]').forEach(function (a) {
    var key = a.getAttribute('data-book');
    if (a.tagName === 'A') a.href = 'booking.html' + (key ? '#' + key : '');
  });

  /* Offer terms: shown only for the fields that are filled in. */
  document.querySelectorAll('[data-terms]').forEach(function (el) {
    var x = OFFERS[el.getAttribute('data-terms')];
    var parts = [];
    if (x.fromPrice) parts.push(t('From ' + x.fromPrice + ' per night', 'Da ' + x.fromPrice + ' a notte'));
    if (x.validFrom && x.validTo) parts.push(t('Stays ' + x.validFrom + ' – ' + x.validTo, 'Soggiorni dal ' + x.validFrom + ' al ' + x.validTo));
    if (x.minNights) parts.push(t('Minimum ' + x.minNights + ' nights', 'Minimo ' + x.minNights + ' notti'));
    if (parts.length) el.textContent = parts.join(' · ');
    else el.hidden = true;
  });

  /* Review score: shown only when the real numbers are filled in. */
  document.querySelectorAll('[data-review-score]').forEach(function (el) {
    var r = HOTEL.reviews;
    if (r.rating && r.count) {
      el.textContent = r.rating + '/5 ' + t('on ' + r.source + ' from ', 'su ' + r.source + ' da ') + r.count + t(' reviews', ' recensioni');
    } else el.hidden = true;
  });
  document.querySelectorAll('[data-hotel]').forEach(function (el) {
    var k = el.getAttribute('data-hotel');
    if (k === 'contact') el.innerHTML = contactList();
    else if (k === 'maps') el.href = HOTEL.mapsUrl;
    else if (k === 'address') el.textContent = HOTEL.address;
  });

  /* ---------- Menu ---------- */
  var menuBtn = header.querySelector('.menu-btn');
  var lastFocus = null;
  function openMenu() {
    lastFocus = document.activeElement;
    menu.classList.add('open');
    menuBtn.setAttribute('aria-expanded', 'true');
    body.classList.add('no-scroll');
    menu.querySelector('.menu-close').focus();
  }
  function closeMenu() {
    menu.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false');
    body.classList.remove('no-scroll');
    if (lastFocus) lastFocus.focus();
  }
  menuBtn.addEventListener('click', openMenu);
  menu.querySelector('.menu-close').addEventListener('click', closeMenu);
  menu.querySelectorAll('nav a').forEach(function (a) { a.addEventListener('click', closeMenu); });

  /* ---------- Modals ---------- */
  function openModal(m) {
    if (menu.classList.contains('open')) closeMenu();
    lastFocus = document.activeElement;
    m.hidden = false;
    body.classList.add('no-scroll');
    m.querySelector('.modal-x').focus();
  }
  function closeModal(m) {
    m.hidden = true;
    body.classList.remove('no-scroll');
    if (lastFocus) lastFocus.focus();
  }
  formModal.addEventListener('click', function (e) { if (e.target === formModal) closeModal(formModal); });
  [help].forEach(function (m) {
    m.querySelector('.modal-x').addEventListener('click', function () { closeModal(m); });
    m.addEventListener('click', function (e) { if (e.target === m) closeModal(m); });
    m.querySelectorAll('.help-links a').forEach(function (a) { a.addEventListener('click', function () { closeModal(m); }); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (!formModal.hidden) closeModal(formModal);
    else if (!help.hidden) closeModal(help);
    else if (menu.classList.contains('open')) closeMenu();
  });
  /* Personal review link sent after check-out: page.html#review-VM-AB12CD */
  function reviewLink() {
    var rv = /^#review-(VM-[A-Za-z0-9]{6})$/.exec(location.hash);
    if (rv) openForm('verify', { reference: rv[1].toUpperCase() });
  }
  setTimeout(reviewLink, 0);
  window.addEventListener('hashchange', reviewLink);

  document.addEventListener('click', function (e) {
    var fm = e.target.closest('[data-form]');
    if (fm) { e.preventDefault(); openForm(fm.getAttribute('data-form')); return; }
    if (e.target.closest('[data-help]')) { e.preventDefault(); openModal(help); }
  });

})();
