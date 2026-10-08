/* Villa Maria Hotel & Spa — shared header, MENU overlay, footer, Help (contact) panel,
   welcome chooser (Family / Business), phone booking bar and EN/IT switch. */
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
    receptionHours: { en: '', it: '' },   // e.g. { en: 'Reception open 24 hours', it: 'Reception aperta 24 ore su 24' }
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
      ['index.html', 'Home', 'Home'],
      ['rooms.html', 'Rooms & Suites', 'Camere e Suite'],
      ['spa.html', 'Linfa Wellness & Spa', 'Linfa Wellness & Spa'],
      ['restaurant.html', 'Restaurant', 'Ristorante'],
      ['contact.html', 'Getting here & contact', 'Come arrivare e contatti']
    ]
  };

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }
  function links(list) {
    return list.map(function (p) {
      var cur = p[0] === page ? ' aria-current="page"' : '';
      return '<li><a href="' + p[0] + '"' + cur + '>' + esc(t(p[1], p[2])) + '</a></li>';
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
    if (HOTEL.receptionHours[lang]) out.push('<li><span class="k">Reception</span><span>' + esc(HOTEL.receptionHours[lang]) + '</span></li>');
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
      '<div><h3>' + t('The hotel', "L'hotel") + '</h3><ul>' + links(PAGES.hotel) + '</ul></div>' +
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

  /* ---------- Help panel: real contact details + quick answers ---------- */
  var help = document.createElement('div');
  help.className = 'modal';
  help.hidden = true;
  help.setAttribute('role', 'dialog');
  help.setAttribute('aria-modal', 'true');
  help.setAttribute('aria-labelledby', 'help-title');
  help.innerHTML =
    '<div class="modal-box">' +
      '<button type="button" class="modal-x" aria-label="' + t('Close', 'Chiudi') + '">×</button>' +
      '<p class="eb">' + t('Help', 'Aiuto') + '</p>' +
      '<h2 id="help-title">' + t('Talk to our team', 'Parla con il nostro team') + '</h2>' +
      contactList() +
      '<button type="button" class="btn btn-sky btn-block" style="margin-top:18px" data-form="message">' + t('Send us a message', 'Scrivici un messaggio') + '</button>' +
      '<p class="eb" style="margin-top:22px">' + t('Quick answers', 'Risposte rapide') + '</p>' +
      '<ul class="help-links">' + links(PAGES.hotel.slice(1)) + '</ul>' +
      '<a class="btn btn-slate btn-block" style="margin-top:18px" href="booking.html">' + t('Book your stay', 'Prenota il soggiorno') + '</a>' +
    '</div>';

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

  /* ---------- Welcome: who's travelling? (homepage, once per visit, with Skip) ---------- */
  // [image, EN line, IT line] for each package; names come from PAGES.
  var PKG = {
    'italian-memories.html': ['assets/img/people/moment-pool.jpg', 'Rest and time together by the sea.', 'Relax e tempo insieme, sul mare.'],
    'family-reset-package.html': ['assets/img/suite-terrace.jpg', 'Room, breakfast and spa included when you book direct.', 'Camera, colazione e spa inclusi prenotando direttamente.'],
    'ciao-again.html': ['assets/img/people/family-welcome-back.jpg', 'Your Italian story continues.', 'La tua storia italiana continua.'],
    'business-travel.html': ['assets/img/auditorium.jpg', 'Meetings, recovery and a proper dinner, already arranged.', 'Riunioni, relax e una buona cena, già organizzati.'],
    'executive-business-stay.html': ['assets/img/people/business-meeting.jpg', 'Your business stay, already arranged.', 'Il tuo soggiorno di lavoro, già organizzato.'],
    'padel-experience.html': ['assets/img/people/business-padel.jpg', 'Relationships that continue beyond the meeting room.', 'Relazioni che continuano oltre la sala riunioni.']
  };
  var GROUPS = {
    family: { title: t('Packages for families', 'Pacchetti per le famiglie'), list: PAGES.families },
    business: { title: t('Packages for business', 'Pacchetti per il business'), list: PAGES.business }
  };
  function choice(key, img, name, line) {
    return '<button type="button" class="w-choice" data-group="' + key + '">' +
      '<span class="w-ph"><img src="' + BASE + img + '" alt=""></span>' +
      '<span class="w-t">' + name + '</span><span class="w-s">' + line + '</span></button>';
  }
  var welcome = document.createElement('div');
  welcome.className = 'welcome';
  welcome.hidden = true;
  welcome.setAttribute('role', 'dialog');
  welcome.setAttribute('aria-modal', 'true');
  welcome.setAttribute('aria-labelledby', 'welcome-title');
  welcome.innerHTML =
    '<div class="wrap w-top"><img src="' + BASE + 'assets/img/logo.png" alt="Villa Maria Hotel &amp; Spa" class="w-logo">' +
      '<div class="w-right">' + header.querySelector('.lang').outerHTML +
      '<button type="button" class="w-skip">' + t('Skip →', 'Salta →') + '</button></div></div>' +
    '<div class="wrap w-body">' +
      '<div class="w-step" data-step="ask">' +
        '<p class="eb">' + t('Welcome to Villa Maria', 'Benvenuti a Villa Maria') + '</p>' +
        '<h2 class="h2" id="welcome-title">' + t('Who\'s travelling <i>today?</i>', 'Chi viaggia <i>oggi?</i>') + '</h2>' +
        '<p class="w-lead">' + t('Choose one and we\'ll show you the packages made for you.', 'Scegli e ti mostriamo i pacchetti giusti per te.') + '</p>' +
        '<div class="w-choices">' +
          choice('family', 'assets/img/people/moment-pool.jpg', t('Family', 'Famiglia'), t('Holidays together by the sea', 'Vacanze insieme sul mare')) +
          choice('business', 'assets/img/people/business-meeting.jpg', 'Business', t('Work, meetings and recovery', 'Lavoro, riunioni e recupero')) +
        '</div>' +
      '</div>' +
      '<div class="w-step" data-step="list" hidden>' +
        '<button type="button" class="w-back">' + t('← Back', '← Indietro') + '</button>' +
        '<h2 class="h2 w-group-title"></h2>' +
        '<div class="w-pkgs"></div>' +
      '</div>' +
      '<button type="button" class="w-skip-low">' + t('Skip and go to the website', 'Salta e vai al sito') + '</button>' +
    '</div>';

  function renderGroup(key) {
    var g = GROUPS[key];
    welcome.querySelector('.w-group-title').textContent = g.title;
    welcome.querySelector('.w-pkgs').innerHTML = g.list.map(function (p) {
      var d = PKG[p[0]];
      return '<a class="card" href="' + p[0] + '"><span class="ph"><img src="' + BASE + d[0] + '" alt=""></span>' +
        '<span class="t">' + esc(t(p[1], p[2])) + '</span><span class="s">' + esc(t(d[1], d[2])) + '</span>' +
        '<span class="more">' + t('Discover →', 'Scopri →') + '</span></a>';
    }).join('');
  }
  function showStep(step) {
    welcome.querySelector('[data-step="ask"]').hidden = step !== 'ask';
    welcome.querySelector('[data-step="list"]').hidden = step !== 'list';
    var f = welcome.querySelector(step === 'ask' ? '.w-choice' : '.w-pkgs a');
    if (f && !welcome.hidden) f.focus();
  }
  function markSeen() { try { sessionStorage.setItem('vm-welcomed', '1'); } catch (e) {} }
  function closeWelcome() {
    welcome.hidden = true;
    body.classList.remove('no-scroll');
    markSeen();
  }
  welcome.querySelectorAll('.w-choice').forEach(function (b) {
    b.addEventListener('click', function () { renderGroup(b.dataset.group); showStep('list'); });
  });
  welcome.querySelector('.w-back').addEventListener('click', function () { showStep('ask'); });
  welcome.querySelectorAll('.w-skip,.w-skip-low').forEach(function (b) { b.addEventListener('click', closeWelcome); });
  // Choosing a package counts as "seen". Switching language does not, so the screen reopens in that language.
  welcome.querySelector('.w-pkgs').addEventListener('click', function (e) { if (e.target.closest('a')) markSeen(); });

  /* ---------- Our own forms: review, community, referral, message ---------- */
  // [name, type, EN label, IT label, required]
  var FORMS = {
    review: {
      title: t('Write a review', 'Scrivi una recensione'),
      intro: t('Tell other guests about your stay. We publish reviews after checking the booking.', 'Racconta il tuo soggiorno agli altri ospiti. Pubblichiamo le recensioni dopo aver verificato la prenotazione.'),
      fields: [['rating', 'stars', 'Your rating', 'Il tuo voto', true], ['name', 'text', 'Name', 'Nome', true], ['email', 'email', 'Email (not published)', 'Email (non pubblicata)', true],
               ['stay', 'month', 'When did you stay?', 'Quando hai soggiornato?', false], ['review', 'textarea', 'Your review', 'La tua recensione', true]],
      thanks: t('Thank you. Your review will appear after we check your stay.', 'Grazie. La tua recensione apparirà dopo la verifica del soggiorno.')
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

  function demoNote() {
    return '<p class="demo-note">' + t('Demo mode: nothing was sent yet. The site owner connects forms in assets/js/site.js (FORMS_ENDPOINT).',
      'Modalità demo: non è stato inviato nulla. Il gestore del sito collega i moduli in assets/js/site.js (FORMS_ENDPOINT).') + '</p>';
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
  function openForm(name) {
    var def = FORMS[name];
    if (!def) return;
    formModal.innerHTML =
      '<div class="modal-box">' +
        '<button type="button" class="modal-x" aria-label="' + t('Close', 'Chiudi') + '">×</button>' +
        '<h2 id="form-title">' + def.title + '</h2><p>' + def.intro + '</p>' +
        '<form class="own-form" novalidate>' + def.fields.map(fieldHtml).join('') +
          '<label class="check"><input type="checkbox" name="consent" required><span>' +
            t('I agree that Villa Maria uses these details for this request, as described in the <a href="privacy.html">privacy notice</a>.',
              'Accetto che Villa Maria usi questi dati per questa richiesta, come descritto nell\'<a href="privacy.html">informativa privacy</a>.') + '</span></label>' +
          '<p class="err" hidden>' + t('Please complete the highlighted fields.', 'Completa i campi evidenziati.') + '</p>' +
          '<button type="submit" class="btn btn-slate btn-block">' + t('Send', 'Invia') + '</button>' +
        '</form>' +
      '</div>';
    formModal.querySelector('.modal-x').addEventListener('click', function () { closeModal(formModal); });
    var f = formModal.querySelector('form');
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

  /* ---------- Mount ---------- */
  var body = document.body;
  body.insertBefore(header, body.firstChild);
  var skip = document.createElement('a');
  skip.className = 'skip'; skip.href = '#main'; skip.textContent = t('Skip to content', 'Vai al contenuto');
  body.insertBefore(skip, body.firstChild);
  [menu, footer, help, formModal, bar, fab, welcome].forEach(function (el) { body.appendChild(el); });

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
    else if (!welcome.hidden) closeWelcome();
    else if (menu.classList.contains('open')) closeMenu();
  });
  document.addEventListener('click', function (e) {
    var fm = e.target.closest('[data-form]');
    if (fm) { e.preventDefault(); openForm(fm.getAttribute('data-form')); return; }
    if (e.target.closest('[data-help]')) { e.preventDefault(); openModal(help); }
  });

  /* Open the welcome screen on the homepage, once per visit. */
  var seen = false;
  try { seen = !!sessionStorage.getItem('vm-welcomed'); } catch (e) {}
  if (page === 'index.html' && document.querySelector('[data-welcome]') && !seen) {
    welcome.hidden = false;
    body.classList.add('no-scroll');
    showStep('ask');
  }
})();
