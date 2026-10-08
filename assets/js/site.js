/* Villa Maria Hotel & Spa — shared header, MENU overlay, footer, Help (contact) panel,
   €30 coupon panel, phone booking bar and EN/IT switch. */
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
    email: '',                // e.g. 'info@hvillamaria.it'
    receptionHours: { en: '', it: '' },   // e.g. { en: 'Reception open 24 hours', it: 'Reception aperta 24 ore su 24' }
    // Address as shown on booking sites. Confirm before going live.
    address: 'Contrada Pretaro, Via San Paolo, 66023 Francavilla al Mare (CH), Italy',
    mapsUrl: 'https://www.google.com/maps/search/?api=1&query=Villa+Maria+Hotel+%26+Spa+Francavilla+al+Mare',
    website: 'https://www.hvillamaria.it/',
    reviews: {
      googleRating: '',       // e.g. '4.6' — shown only together with googleCount
      googleCount: '',        // e.g. '1,240'
      googleUrl: 'https://www.google.com/maps/search/?api=1&query=Villa+Maria+Hotel+%26+Spa+Francavilla+al+Mare',
      tripadvisorUrl: 'https://www.tripadvisor.com/Search?q=Villa+Maria+Hotel+Spa+Francavilla+al+Mare',
      bookingUrl: 'https://www.booking.com/hotel/it/sportinghotelvillamaria.html'
    },
    booking: {
      // Replace with the booking engine's own address (the page with dates and rooms).
      url: 'https://www.hvillamaria.it/',
      // Name of the engine's promo-code parameter, e.g. 'promo' or 'coupon'.
      // When set, family "Book" buttons open the engine with the code already applied.
      promoParam: ''
    }
  };

  var OFFERS = {
    familyReset: {
      code: 'RESET30',
      amount: '€30',
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
      ['italian-memories.html', 'La Dolce Family', 'La Dolce Family'],
      ['family-reset-package.html', 'Family Reset: €30 Off', 'Family Reset: 30 € di sconto'],
      ['ciao-again.html', 'Ciao Again', 'Ciao Again']
    ],
    business: [
      ['business-travel.html', 'Business, Minus the Stress', 'Business, senza stress'],
      ['executive-business-stay.html', 'Office With a Sea View', 'Ufficio vista mare'],
      ['padel-experience.html', 'Padel & Partners', 'Padel & Partner']
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
  function bookingHref(promo) {
    var u = HOTEL.booking.url;
    if (promo && HOTEL.booking.promoParam) {
      u += (u.indexOf('?') < 0 ? '?' : '&') + encodeURIComponent(HOTEL.booking.promoParam) + '=' + encodeURIComponent(promo);
    }
    return u;
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
        '<a class="btn btn-slate header-book" data-book>' + t('Book Now', 'Prenota') + '</a>' +
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
      '<a class="btn btn-sky" data-book>' + t('Book Now', 'Prenota') + '</a></div>' +
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
      '<p class="eb" style="margin-top:22px">' + t('Quick answers', 'Risposte rapide') + '</p>' +
      '<ul class="help-links">' + links(PAGES.hotel.slice(1)) + '</ul>' +
      '<a class="btn btn-slate btn-block" style="margin-top:18px" data-book>' + t('Book direct', 'Prenota diretto') + '</a>' +
    '</div>';

  /* ---------- Coupon panel (no email needed; the code is a public promo code) ---------- */
  var o = OFFERS.familyReset;
  var coupon = document.createElement('div');
  coupon.className = 'modal';
  coupon.hidden = true;
  coupon.setAttribute('role', 'dialog');
  coupon.setAttribute('aria-modal', 'true');
  coupon.setAttribute('aria-labelledby', 'coupon-title');
  coupon.innerHTML =
    '<div class="modal-box">' +
      '<button type="button" class="modal-x" aria-label="' + t('Close', 'Chiudi') + '">×</button>' +
      '<p class="eb">Family Reset</p>' +
      '<div class="amount">' + esc(o.amount) + '</div>' +
      '<h2 id="coupon-title">' + t('Your family coupon', 'Il tuo coupon per la famiglia') + '</h2>' +
      '<p>' + (HOTEL.booking.promoParam
          ? t('Applied automatically when you book with the button below.', 'Applicato automaticamente quando prenoti con il pulsante qui sotto.')
          : t('Enter this code when you book on our website.', 'Inserisci questo codice quando prenoti sul nostro sito.')) + '</p>' +
      '<div class="code">' + esc(o.code) + '</div>' +
      '<p class="terms" data-terms="familyReset"></p>' +
      '<a class="btn btn-coupon btn-block" style="margin-top:16px" data-book="familyReset">' + t('Book the Family Reset', 'Prenota il Family Reset') + '</a>' +
      '<small>' + t('Valid on direct bookings only. One coupon per stay.', 'Valido solo per prenotazioni dirette. Un coupon per soggiorno.') + '</small>' +
    '</div>';

  /* ---------- Phone booking bar ---------- */
  var bar = document.createElement('div');
  bar.className = 'book-bar';
  bar.innerHTML =
    '<button type="button" class="btn btn-line" data-help>' + t('Help', 'Aiuto') + '</button>' +
    '<a class="btn btn-slate" data-book' + (page === 'family-reset-package.html' ? '="familyReset"' : '') + '>' + t('Book Now', 'Prenota') + '</a>';

  var fab = document.createElement('button');
  fab.type = 'button';
  fab.className = 'btn btn-slate help-fab';
  fab.setAttribute('data-help', '');
  fab.textContent = t('Help', 'Aiuto');

  /* ---------- Mount ---------- */
  var body = document.body;
  body.insertBefore(header, body.firstChild);
  var skip = document.createElement('a');
  skip.className = 'skip'; skip.href = '#main'; skip.textContent = t('Skip to content', 'Vai al contenuto');
  body.insertBefore(skip, body.firstChild);
  [menu, footer, help, coupon, bar, fab].forEach(function (el) { body.appendChild(el); });

  /* Booking links: data-book (plain) or data-book="familyReset" (promo applied when the engine supports it). */
  document.querySelectorAll('[data-book]').forEach(function (a) {
    var key = a.getAttribute('data-book');
    var promo = key && OFFERS[key] ? OFFERS[key].code : '';
    if (a.tagName === 'A') { a.href = bookingHref(promo); a.rel = 'noopener'; }
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
    if (r.googleRating && r.googleCount) {
      el.innerHTML = '<a href="' + r.googleUrl + '" rel="noopener">' + esc(r.googleRating) + '/5 ' + t('on Google from ', 'su Google da ') + esc(r.googleCount) + t(' reviews', ' recensioni') + ' →</a>';
    } else el.hidden = true;
  });
  document.querySelectorAll('[data-review-link]').forEach(function (a) {
    var u = HOTEL.reviews[a.getAttribute('data-review-link') + 'Url'];
    if (u) { a.href = u; a.rel = 'noopener'; } else a.hidden = true;
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
  [help, coupon].forEach(function (m) {
    m.querySelector('.modal-x').addEventListener('click', function () { closeModal(m); });
    m.addEventListener('click', function (e) { if (e.target === m) closeModal(m); });
    m.querySelectorAll('.help-links a').forEach(function (a) { a.addEventListener('click', function () { closeModal(m); }); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (!coupon.hidden) closeModal(coupon);
    else if (!help.hidden) closeModal(help);
    else if (menu.classList.contains('open')) closeMenu();
  });
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-coupon]')) { e.preventDefault(); openModal(coupon); return; }
    if (e.target.closest('[data-help]')) { e.preventDefault(); openModal(help); }
  });
})();
