/* Villa Maria Hotel & Spa — shared header, MENU overlay, footer, €30 coupon, chat and EN/IT toggle. */
(function () {
  'use strict';

  var CONFIG = {
    bookingUrl: 'https://www.hvillamaria.it/',
    couponCode: 'RESET30'
  };

  // Campaign names are used verbatim everywhere (menu, cards, pages).
  var PAGES = {
    families: [
      ['italian-memories.html', 'Italian Memories', 'Italian Memories'],
      ['family-reset-package.html', 'Family Reset Package', 'Family Reset Package'],
      ['ciao-again.html', 'Ciao Again', 'Ciao Again']
    ],
    business: [
      ['business-travel.html', 'Take the pressure out of business travel', 'Take the pressure out of business travel'],
      ['executive-business-stay.html', 'Executive Business Stay Package', 'Executive Business Stay Package'],
      ['padel-experience.html', 'The Padel Experience', 'The Padel Experience']
    ],
    hotel: [
      ['index.html', 'Home', 'Home'],
      ['index.html#rooms', 'Rooms & Suites', 'Camere e Suite'],
      ['index.html#spa', 'Linfa Wellness & Spa', 'Linfa Wellness & Spa'],
      ['index.html#dining', 'Restaurant', 'Ristorante'],
      ['#contact', 'Contact', 'Contatti']
    ]
  };

  var current = (location.pathname.split('/').pop() || 'index.html');

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }
  function links(list) {
    return list.map(function (p) {
      var cur = p[0] === current ? ' aria-current="page"' : '';
      var it = p[2] !== p[1] ? ' data-it="' + esc(p[2]) + '"' : '';
      return '<li><a href="' + p[0] + '"' + cur + it + '>' + esc(p[1]) + '</a></li>';
    }).join('');
  }

  /* ---------- Header ---------- */
  var header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML =
    '<div class="wrap">' +
      '<button type="button" class="menu-btn" aria-expanded="false" aria-controls="menu" data-it="Menu">Menu</button>' +
      '<a class="logo" href="index.html"><img src="assets/img/logo.png" alt="Villa Maria Hotel &amp; Spa" width="858" height="462"></a>' +
      '<div class="header-right">' +
        '<div class="lang" role="group" aria-label="Language"><button type="button" data-lang="en" aria-pressed="true">EN</button><button type="button" data-lang="it" aria-pressed="false">IT</button></div>' +
        '<a class="btn btn-slate header-book" data-book data-it="Prenota">Book Now</a>' +
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
    '<div class="wrap menu-top"><button type="button" class="menu-close" data-it="Chiudi ✕">Close ✕</button>' +
      '<a class="btn btn-sky" data-book data-it="Prenota">Book Now</a></div>' +
    '<nav class="wrap menu-grid" aria-label="Main">' +
      '<div><h3 data-it="Per le famiglie">For families</h3><ul>' + links(PAGES.families) + '</ul></div>' +
      '<div><h3 data-it="Per il business">For business</h3><ul>' + links(PAGES.business) + '</ul></div>' +
      '<div><h3 data-it="L\'hotel">The hotel</h3><ul>' + links(PAGES.hotel) + '</ul></div>' +
    '</nav>' +
    '<div class="wrap menu-foot"><span>Villa Maria Hotel &amp; Spa · Francavilla al Mare (CH), Abruzzo</span>' +
      '<button type="button" class="btn btn-coupon" data-coupon><span class="tag">€</span><span data-it="Coupon da 30 €">30 Euro coupon</span></button></div>';

  /* ---------- Footer ---------- */
  var footer = document.createElement('footer');
  footer.className = 'site-footer';
  footer.id = 'contact';
  footer.innerHTML =
    '<div class="wrap">' +
      '<div><div class="brand">Villa Maria<br>Hotel &amp; Spa</div>' +
        '<p data-it="Hotel e spa 4 stelle sul mare.<br>Francavilla al Mare (CH), Abruzzo, Italia">Four-star hotel &amp; spa by the sea.<br>Francavilla al Mare (CH), Abruzzo, Italy</p></div>' +
      '<div><h4 data-it="Famiglie">Families</h4><ul>' + links(PAGES.families) + '</ul></div>' +
      '<div><h4>Business</h4><ul>' + links(PAGES.business) + '</ul></div>' +
      '<div><h4 data-it="Contatti">Contact</h4><ul>' +
        '<li><a href="#" data-chat data-it="Chatta con noi">Chat with us</a></li>' +
        '<li><a data-book data-it="Prenota diretto">Book direct</a></li>' +
        '<li><a href="https://www.hvillamaria.it/" rel="noopener">hvillamaria.it</a></li>' +
      '</ul></div>' +
      '<div class="legal"><span>© 2026 Villa Maria Hotel &amp; Spa</span><span data-it="Recensioni verificate su Google, Booking.com e TripAdvisor">Verified reviews on Google, Booking.com &amp; TripAdvisor</span></div>' +
    '</div>';

  /* ---------- €30 coupon modal ---------- */
  var coupon = document.createElement('div');
  coupon.className = 'modal';
  coupon.hidden = true;
  coupon.setAttribute('role', 'dialog');
  coupon.setAttribute('aria-modal', 'true');
  coupon.setAttribute('aria-labelledby', 'coupon-title');
  coupon.innerHTML =
    '<div class="modal-box">' +
      '<button type="button" class="modal-x" aria-label="Close">×</button>' +
      '<p class="eb">Family Reset Package</p>' +
      '<div class="amount">€30</div>' +
      '<h2 id="coupon-title" data-it="Il tuo coupon per la famiglia">Your family coupon</h2>' +
      '<p data-it="30 € di sconto sul Family Reset Package prenotando direttamente.">€30 off the Family Reset Package when you book direct.</p>' +
      '<form novalidate>' +
        '<label for="coupon-email" class="eb" style="color:var(--muted)">Email</label>' +
        '<input id="coupon-email" type="email" required autocomplete="email" placeholder="name@example.com">' +
        '<button type="submit" class="btn btn-coupon btn-block" data-it="Ricevi il coupon">Get my coupon</button>' +
      '</form>' +
      '<div class="coupon-done" hidden>' +
        '<div class="code">' + CONFIG.couponCode + '</div>' +
        '<p data-it="Inserisci il codice al momento della prenotazione.">Enter this code when you book.</p>' +
        '<a class="btn btn-slate btn-block" style="margin-top:16px" data-book data-it="Prenota il Family Reset Package">Book the Family Reset Package</a>' +
      '</div>' +
      '<small data-it="Valido per prenotazioni dirette. Un coupon per soggiorno.">Valid on direct bookings. One coupon per stay.</small>' +
    '</div>';

  /* ---------- Chat (quick answers) ---------- */
  var chat = document.createElement('div');
  chat.className = 'modal';
  chat.hidden = true;
  chat.setAttribute('role', 'dialog');
  chat.setAttribute('aria-modal', 'true');
  chat.setAttribute('aria-labelledby', 'chat-title');
  chat.innerHTML =
    '<div class="modal-box">' +
      '<button type="button" class="modal-x" aria-label="Close">×</button>' +
      '<p class="eb" data-it="Chatta con noi">Chat with us</p>' +
      '<h2 id="chat-title" data-it="Come possiamo aiutarti?">How can we help?</h2>' +
      '<div class="steps" style="flex-direction:column;gap:8px">' +
        '<button type="button" class="btn btn-line btn-block" data-q="fam" data-it="Viaggio con la famiglia">I\'m travelling with family</button>' +
        '<button type="button" class="btn btn-line btn-block" data-q="biz" data-it="Viaggio per lavoro">I\'m travelling for work</button>' +
        '<button type="button" class="btn btn-line btn-block" data-q="back" data-it="Ci sono già stato">I\'ve stayed before</button>' +
      '</div>' +
      '<p class="chat-a" aria-live="polite"></p>' +
    '</div>';

  var ANSWERS = {
    fam: ['The Family Reset Package: room, breakfast and spa in one booking — plus a €30 coupon.', 'Il Family Reset Package: camera, colazione e spa in un\'unica prenotazione — più un coupon da 30 €.', 'family-reset-package.html'],
    biz: ['The Executive Business Stay Package: room, early breakfast, Wi-Fi, spa and a meeting room.', 'L\'Executive Business Stay Package: camera, colazione presto, Wi-Fi, spa e sala riunioni.', 'executive-business-stay.html'],
    back: ['Welcome back! Ciao Again has what\'s new — and The Padel Experience awaits business guests.', 'Bentornati! Ciao Again racconta le novità — e The Padel Experience aspetta gli ospiti business.', 'ciao-again.html']
  };

  /* ---------- Mount ---------- */
  var body = document.body;
  body.insertBefore(header, body.firstChild);
  var skip = document.createElement('a');
  skip.className = 'skip'; skip.href = '#main'; skip.textContent = 'Skip to content';
  body.insertBefore(skip, body.firstChild);
  body.appendChild(menu);
  body.appendChild(footer);
  body.appendChild(coupon);
  body.appendChild(chat);
  if (!body.hasAttribute('data-no-chat')) {
    var fab = document.createElement('button');
    fab.type = 'button';
    fab.className = 'btn btn-slate chat-fab';
    fab.setAttribute('data-chat', '');
    fab.setAttribute('data-it', 'Chatta con noi');
    fab.textContent = 'Chat with us';
    body.appendChild(fab);
  }

  document.querySelectorAll('[data-book]').forEach(function (a) {
    if (a.tagName === 'A' && !a.getAttribute('href')) { a.href = CONFIG.bookingUrl; a.rel = 'noopener'; }
  });

  /* ---------- Language ---------- */
  var lang = 'en';
  try { lang = localStorage.getItem('vm-lang') || (/^it\b/i.test(navigator.language) ? 'it' : 'en'); } catch (e) {}

  function setLang(l) {
    lang = l === 'it' ? 'it' : 'en';
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-it]').forEach(function (el) {
      if (!el.hasAttribute('data-en')) el.setAttribute('data-en', el.innerHTML);
      el.innerHTML = lang === 'it' ? el.getAttribute('data-it') : el.getAttribute('data-en');
    });
    document.querySelectorAll('[data-it-alt]').forEach(function (el) {
      if (!el.hasAttribute('data-en-alt')) el.setAttribute('data-en-alt', el.alt);
      el.alt = lang === 'it' ? el.getAttribute('data-it-alt') : el.getAttribute('data-en-alt');
    });
    document.querySelectorAll('.lang button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.lang === lang));
    });
    var a = chat.querySelector('.chat-a');
    if (a.dataset.q) answer(a.dataset.q);
    try { localStorage.setItem('vm-lang', lang); } catch (e) {}
  }
  document.querySelectorAll('.lang button').forEach(function (b) {
    b.addEventListener('click', function () { setLang(b.dataset.lang); });
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
    var f = m.querySelector('input,button.btn');
    if (f) f.focus();
  }
  function closeModal(m) {
    m.hidden = true;
    body.classList.remove('no-scroll');
    if (lastFocus) lastFocus.focus();
  }
  [coupon, chat].forEach(function (m) {
    m.querySelector('.modal-x').addEventListener('click', function () { closeModal(m); });
    m.addEventListener('click', function (e) { if (e.target === m) closeModal(m); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (!coupon.hidden) closeModal(coupon);
    else if (!chat.hidden) closeModal(chat);
    else if (menu.classList.contains('open')) closeMenu();
  });

  document.addEventListener('click', function (e) {
    var c = e.target.closest('[data-coupon]');
    if (c) { e.preventDefault(); openModal(coupon); return; }
    var h = e.target.closest('[data-chat]');
    if (h) { e.preventDefault(); openModal(chat); }
  });

  var form = coupon.querySelector('form');
  var email = coupon.querySelector('#coupon-email');
  function showCode() {
    form.hidden = true;
    coupon.querySelector('.coupon-done').hidden = false;
  }
  try { if (localStorage.getItem('vm-coupon')) showCode(); } catch (e) {}
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!email.checkValidity()) { email.focus(); email.style.borderColor = '#B4532A'; return; }
    try { localStorage.setItem('vm-coupon', email.value); } catch (err) {}
    showCode();
  });

  function answer(q) {
    var a = chat.querySelector('.chat-a');
    var r = ANSWERS[q];
    a.dataset.q = q;
    a.innerHTML = esc(lang === 'it' ? r[1] : r[0]) +
      ' <a href="' + r[2] + '" style="color:var(--olive);font-weight:700">' + (lang === 'it' ? 'Scopri →' : 'Take a look →') + '</a>';
  }
  chat.querySelectorAll('[data-q]').forEach(function (b) {
    b.addEventListener('click', function () { answer(b.dataset.q); });
  });

  var exec = document.getElementById('exec-form');
  if (exec) exec.addEventListener('submit', function (e) { e.preventDefault(); });

  setLang(lang);
})();
