/* Villa Maria Hotel & Spa — shared header, MENU overlay, footer, €30 coupon, welcome chooser and EN/IT toggle. */
(function () {
  'use strict';

  var CONFIG = {
    bookingUrl: 'https://www.hvillamaria.it/',
    couponCode: 'RESET30'
  };

  // Campaign names are used verbatim everywhere (menu, cards, pages).
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
        '<li><a href="#" data-chat data-it="Aiuto">Help</a></li>' +
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
      '<p class="eb">Family Reset</p>' +
      '<div class="amount">€30</div>' +
      '<h2 id="coupon-title" data-it="Il tuo coupon per la famiglia">Your family coupon</h2>' +
      '<p data-it="30 € di sconto sul Family Reset prenotando direttamente.">€30 off the Family Reset when you book direct.</p>' +
      '<form novalidate>' +
        '<label for="coupon-email" class="eb" style="color:var(--muted)">Email</label>' +
        '<input id="coupon-email" type="email" required autocomplete="email" placeholder="name@example.com">' +
        '<button type="submit" class="btn btn-coupon btn-block" data-it="Ricevi il coupon">Get my coupon</button>' +
      '</form>' +
      '<div class="coupon-done" hidden>' +
        '<div class="code">' + CONFIG.couponCode + '</div>' +
        '<p data-it="Inserisci il codice al momento della prenotazione.">Enter this code when you book.</p>' +
        '<a class="btn btn-slate btn-block" style="margin-top:16px" data-book data-it="Prenota il Family Reset">Book the Family Reset</a>' +
      '</div>' +
      '<small data-it="Valido per prenotazioni dirette. Un coupon per soggiorno.">Valid on direct bookings. One coupon per stay.</small>' +
    '</div>';

  /* ---------- Welcome: who's travelling? (opens on the homepage, and from "Help") ---------- */
  // [href, image, EN line, IT line] — names come from PAGES so they stay identical everywhere.
  var PKG = {
    'italian-memories.html': ['assets/img/people/family-pool.jpg', 'Time together by the sea.', 'Tempo insieme, sul mare.'],
    'family-reset-package.html': ['assets/img/people/family-terrace.jpg', 'Room, breakfast and spa in one booking.', 'Camera, colazione e spa in una prenotazione.'],
    'ciao-again.html': ['assets/img/people/family-welcome-back.jpg', 'Welcome back. Your Italian story continues.', 'Bentornati. La tua storia italiana continua.'],
    'business-travel.html': ['assets/img/people/business-desk.jpg', 'Meetings, recovery and dinner in one address.', 'Riunioni, recupero e cena in un unico indirizzo.'],
    'executive-business-stay.html': ['assets/img/people/business-meeting.jpg', 'Room, breakfast, Wi-Fi, spa and meeting room.', 'Camera, colazione, Wi-Fi, spa e sala riunioni.'],
    'padel-experience.html': ['assets/img/people/business-padel.jpg', 'Win the match, win the client. Courts for you and your guests.', 'Vinci la partita, conquista il cliente. Campi per te e i tuoi ospiti.']
  };
  var GROUPS = {
    family: { en: 'Packages for families', it: 'Pacchetti per le famiglie', list: PAGES.families },
    business: { en: 'Packages for business', it: 'Pacchetti per il business', list: PAGES.business }
  };

  function choice(key, img, en, it, enS, itS) {
    return '<button type="button" class="w-choice" data-group="' + key + '">' +
      '<span class="w-ph"><img src="' + img + '" alt=""></span>' +
      '<span class="w-t" data-it="' + esc(it) + '">' + en + '</span>' +
      '<span class="w-s" data-it="' + esc(itS) + '">' + enS + '</span></button>';
  }

  var welcome = document.createElement('div');
  welcome.className = 'welcome';
  welcome.hidden = true;
  welcome.setAttribute('role', 'dialog');
  welcome.setAttribute('aria-modal', 'true');
  welcome.setAttribute('aria-labelledby', 'welcome-title');
  welcome.innerHTML =
    '<div class="wrap w-top"><img src="assets/img/logo.png" alt="Villa Maria Hotel &amp; Spa" class="w-logo">' +
      '<div class="w-right"><div class="lang" role="group" aria-label="Language"><button type="button" data-lang="en" aria-pressed="true">EN</button><button type="button" data-lang="it" aria-pressed="false">IT</button></div>' +
      '<button type="button" class="w-skip" data-it="Salta →">Skip →</button></div></div>' +
    '<div class="wrap w-body">' +
      '<div class="w-step" data-step="ask">' +
        '<p class="eb" data-it="Benvenuti a Villa Maria">Welcome to Villa Maria</p>' +
        '<h2 class="h2" id="welcome-title" data-it="Chi viaggia <i>oggi?</i>">Who\'s travelling <i>today?</i></h2>' +
        '<p class="w-lead" data-it="Scegli e ti mostriamo i pacchetti giusti per te.">Choose one and we\'ll show you the packages made for you.</p>' +
        '<div class="w-choices">' +
          choice('family', 'assets/img/people/family-pool.jpg', 'Family', 'Famiglia', 'Holidays together by the sea', 'Vacanze insieme sul mare') +
          choice('business', 'assets/img/people/business-desk.jpg', 'Business', 'Business', 'Work, meetings and recovery', 'Lavoro, riunioni e recupero') +
        '</div>' +
      '</div>' +
      '<div class="w-step" data-step="list" hidden>' +
        '<button type="button" class="w-back" data-it="← Indietro">← Back</button>' +
        '<h2 class="h2 w-group-title"></h2>' +
        '<div class="w-pkgs"></div>' +
      '</div>' +
      '<button type="button" class="w-skip-low" data-it="Salta e vai al sito">Skip and go to the website</button>' +
    '</div>';

  var wGroup = null;
  function renderGroup() {
    var g = GROUPS[wGroup];
    welcome.querySelector('.w-group-title').textContent = lang === 'it' ? g.it : g.en;
    var pk = welcome.querySelector('.w-pkgs');
    pk.style.setProperty('--n', g.list.length);
    pk.innerHTML = g.list.map(function (p) {
      var d = PKG[p[0]];
      return '<a class="card" href="' + p[0] + '"><span class="ph"><img src="' + d[0] + '" alt=""></span>' +
        '<span class="t">' + esc(p[1]) + '</span><span class="s">' + esc(lang === 'it' ? d[2] : d[1]) + '</span>' +
        '<span class="more">' + (lang === 'it' ? 'Scopri →' : 'Discover →') + '</span></a>';
    }).join('');
  }
  function showStep(step) {
    welcome.querySelector('[data-step="ask"]').hidden = step !== 'ask';
    welcome.querySelector('[data-step="list"]').hidden = step !== 'list';
    var f = welcome.querySelector(step === 'ask' ? '.w-choice' : '.w-pkgs a');
    if (f && !welcome.hidden) f.focus();
  }
  welcome.querySelectorAll('.w-choice').forEach(function (b) {
    b.addEventListener('click', function () {
      wGroup = b.dataset.group;
      try { sessionStorage.setItem('vm-guest', wGroup); } catch (e) {}
      renderGroup();
      showStep('list');
    });
  });
  welcome.querySelector('.w-back').addEventListener('click', function () { showStep('ask'); });

  /* ---------- Mount ---------- */
  var body = document.body;
  body.insertBefore(header, body.firstChild);
  var skip = document.createElement('a');
  skip.className = 'skip'; skip.href = '#main'; skip.textContent = 'Skip to content';
  body.insertBefore(skip, body.firstChild);
  body.appendChild(menu);
  body.appendChild(footer);
  body.appendChild(coupon);
  body.appendChild(welcome);
  if (!body.hasAttribute('data-no-chat')) {
    var fab = document.createElement('button');
    fab.type = 'button';
    fab.className = 'btn btn-slate chat-fab';
    fab.setAttribute('data-chat', '');
    fab.setAttribute('data-it', 'Aiuto');
    fab.textContent = 'Help';
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
    if (wGroup) renderGroup();
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
  [coupon].forEach(function (m) {
    m.querySelector('.modal-x').addEventListener('click', function () { closeModal(m); });
    m.addEventListener('click', function (e) { if (e.target === m) closeModal(m); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (!coupon.hidden) closeModal(coupon);
    else if (!welcome.hidden) closeWelcome();
    else if (menu.classList.contains('open')) closeMenu();
  });

  document.addEventListener('click', function (e) {
    var c = e.target.closest('[data-coupon]');
    if (c) { e.preventDefault(); openModal(coupon); return; }
    var h = e.target.closest('[data-chat]');
    if (h) { e.preventDefault(); openWelcome(); }
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

  function openWelcome() {
    if (menu.classList.contains('open')) closeMenu();
    lastFocus = document.activeElement;
    welcome.hidden = false;
    body.classList.add('no-scroll');
    showStep('ask');
  }
  function closeWelcome() {
    welcome.hidden = true;
    body.classList.remove('no-scroll');
    try { sessionStorage.setItem('vm-welcomed', '1'); } catch (e) {}
    if (lastFocus && lastFocus !== body) lastFocus.focus();
  }
  welcome.querySelectorAll('.w-skip,.w-skip-low').forEach(function (b) { b.addEventListener('click', closeWelcome); });
  welcome.querySelector('.w-pkgs').addEventListener('click', function (e) {
    if (e.target.closest('a')) { try { sessionStorage.setItem('vm-welcomed', '1'); } catch (err) {} }
  });

  var exec = document.getElementById('exec-form');
  if (exec) exec.addEventListener('submit', function (e) { e.preventDefault(); });

  setLang(lang);

  // Ask once per visit, on the homepage only; campaign landing pages stay focused on their offer.
  var seen = false;
  try { seen = !!sessionStorage.getItem('vm-welcomed'); } catch (e) {}
  if (body.hasAttribute('data-welcome') && !seen) openWelcome();
})();
