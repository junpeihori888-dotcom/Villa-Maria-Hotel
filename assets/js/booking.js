/* Villa Maria Hotel & Spa — booking request page.
   Guests choose dates, package and room; the request is sent with VM.send()
   (see FORMS_ENDPOINT in site.js). No payment is taken on this page. */
(function () {
  'use strict';

  /* Nightly rates per room, e.g. superior: 140. Leave empty to show
     "confirmed by email" instead of an estimate. */
  var RATES = { superior: '', deluxe: '', suite: '' };

  var lang = document.documentElement.lang === 'it' ? 'it' : 'en';
  function t(en, it) { return lang === 'it' ? it : en; }

  var PACKAGES = {
    'room-only': [t('Room & breakfast', 'Camera e colazione')],
    'family-discount': [t('Family Discount', 'Sconto Famiglia'), [
      t('Room, breakfast and spa included', 'Camera, colazione e spa inclusi'),
      t('€20 in-house voucher on your first direct booking', 'Voucher da 20 € alla prima prenotazione diretta'),
      t('10% off your next stay when you book it here', '10% sul prossimo soggiorno prenotandolo qui')]],
    'executive': [t('Executive Business Stay Package', 'Pacchetto Executive Business Stay'), [
      t('Early breakfast and express check-out', 'Colazione presto e check-out rapido'),
      t('Spa & sauna access, meeting room on request', 'Spa e sauna, sala riunioni su richiesta'),
      t('Company invoicing', 'Fatturazione aziendale')]],
    'padel': [t('The Padel Experience', 'La Padel Experience'), [
      t('Padel court in the gardens', 'Campo da padel nei giardini'),
      t('Sauna, spa, aperitivo and the chef\'s dinner', 'Sauna, spa, aperitivo e cena dello chef')]]
  };
  var ROOMS = { superior: t('Superior Room', 'Camera Superior'), deluxe: t('Deluxe Room', 'Camera Deluxe'), suite: 'Suite' };
  var LINKS = { // booking.html#<token> preselects a package or room
    'family-discount': ['package', 'family-discount'], 'executive': ['package', 'executive'], 'padel': ['package', 'padel'],
    'returning': ['returning', true], 'superior': ['room', 'superior'], 'deluxe': ['room', 'deluxe'], 'suite': ['room', 'suite']
  };

  var form = document.getElementById('booking-form');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };
  var ci = $('checkin'), co = $('checkout');

  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function fmt(s) {
    if (!s) return '';
    return new Date(s + 'T12:00:00').toLocaleDateString(lang === 'it' ? 'it-IT' : 'en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
  }
  function nights() {
    if (!ci.value || !co.value) return 0;
    return Math.round((new Date(co.value + 'T12:00:00') - new Date(ci.value + 'T12:00:00')) / 864e5);
  }
  function val(name) { var el = form.querySelector('[name="' + name + '"]:checked'); return el ? el.value : ''; }

  /* Preselect the package or room from the link. */
  var tok = (location.hash || '').slice(1);
  if (LINKS[tok]) {
    var l = LINKS[tok];
    if (l[0] === 'returning') $('returning').checked = true;
    else { var r = form.querySelector('[name="' + l[0] + '"][value="' + l[1] + '"]'); if (r) r.checked = true; }
  }


  /* ---------- Calendar: click check-in, then check-out; nights are counted for you ---------- */
  var calEl = $('cal');
  var todayIso = iso(new Date());
  var view = new Date(); view.setDate(1); view.setHours(12, 0, 0, 0);
  var hover = '';
  var locale = lang === 'it' ? 'it-IT' : 'en-GB';
  function monthTitle(d) { return d.toLocaleDateString(locale, { month: 'long', year: 'numeric' }); }
  function nightsLabel(n) { return n === 1 ? t('1 night', '1 notte') : t(n + ' nights', n + ' notti'); }
  var WEEK = lang === 'it' ? ['L', 'M', 'M', 'G', 'V', 'S', 'D'] : ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

  function monthGrid(first) {
    var y = first.getFullYear(), m = first.getMonth();
    var lead = (new Date(y, m, 1, 12).getDay() + 6) % 7;      // Monday-first
    var days = new Date(y, m + 1, 0, 12).getDate();
    var a = ci.value, b = co.value, end = b || (a && hover > a ? hover : '');
    var cells = '';
    for (var i = 0; i < lead; i++) cells += '<span class="cal-pad"></span>';
    for (var d = 1; d <= days; d++) {
      var ds = iso(new Date(y, m, d, 12));
      var cls = ['cal-day'];
      var past = ds < todayIso;
      if (ds === todayIso) cls.push('is-today');
      if (ds === a) cls.push('is-start');
      if (ds === b || (!b && ds === end && end)) cls.push('is-end');
      if (a && end && ds > a && ds < end) cls.push('in-range');
      var label = new Date(ds + 'T12:00:00').toLocaleDateString(locale, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
      cells += '<button type="button" class="' + cls.join(' ') + '" data-date="' + ds + '"' + (past ? ' disabled' : '') +
        ' aria-label="' + label + '"' + ((ds === a || ds === b) ? ' aria-pressed="true"' : '') + '>' + d + '</button>';
    }
    return '<div class="cal-month"><p class="cal-title">' + monthTitle(first) + '</p>' +
      '<div class="cal-week">' + WEEK.map(function (w) { return '<span>' + w + '</span>'; }).join('') + '</div>' +
      '<div class="cal-days">' + cells + '</div></div>';
  }

  function renderCal() {
    var count = window.innerWidth < 700 ? 1 : 2;
    var months = '';
    for (var i = 0; i < count; i++) months += monthGrid(new Date(view.getFullYear(), view.getMonth() + i, 1, 12));
    var atStart = view.getFullYear() === new Date().getFullYear() && view.getMonth() === new Date().getMonth();
    var n = nights();
    var hint = !ci.value ? t('Choose your check-in day', 'Scegli il giorno di arrivo')
      : !co.value ? t('Now choose your check-out day', 'Ora scegli il giorno di partenza')
      : nightsLabel(n) + ' · ' + fmt(ci.value) + ' → ' + fmt(co.value);
    calEl.innerHTML =
      '<div class="cal-nav"><button type="button" class="cal-prev" aria-label="' + t('Previous month', 'Mese precedente') + '"' + (atStart ? ' disabled' : '') + '>‹</button>' +
        '<button type="button" class="cal-next" aria-label="' + t('Next month', 'Mese successivo') + '">›</button></div>' +
      '<div class="cal-months">' + months + '</div>' +
      '<div class="cal-foot"><span class="cal-hint" aria-live="polite">' + hint + '</span>' +
        (ci.value ? '<button type="button" class="linkish cal-clear">' + t('Clear dates', 'Cancella date') + '</button>' : '') +
        (ci.value && co.value ? '<button type="button" class="btn btn-slate cal-done">' + t('Done', 'Fatto') + '</button>' : '') + '</div>';
  }

  function showCal(open) {
    calEl.hidden = !open;
    $('ci-btn').setAttribute('aria-expanded', String(open));
    $('co-btn').setAttribute('aria-expanded', String(open));
    if (open) renderCal();
  }
  function syncFields() {
    $('ci-v').textContent = ci.value ? fmt(ci.value) : t('Select a date', 'Scegli una data');
    $('co-v').textContent = co.value ? fmt(co.value) + ' · ' + nightsLabel(nights()) : t('Select a date', 'Scegli una data');
    $('ci-btn').classList.toggle('has-value', !!ci.value);
    $('co-btn').classList.toggle('has-value', !!co.value);
  }

  calEl.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b || b.disabled) return;
    if (b.classList.contains('cal-prev')) { view.setMonth(view.getMonth() - 1); renderCal(); return; }
    if (b.classList.contains('cal-next')) { view.setMonth(view.getMonth() + 1); renderCal(); return; }
    if (b.classList.contains('cal-clear')) { ci.value = ''; co.value = ''; syncFields(); update(); renderCal(); return; }
    if (b.classList.contains('cal-done')) { showCal(false); $('co-btn').focus(); return; }
    var d = b.getAttribute('data-date');
    if (!d) return;
    if (!ci.value || co.value || d <= ci.value) { ci.value = d; co.value = ''; }
    else { co.value = d; }
    hover = '';
    syncFields(); update(); renderCal();
    if (ci.value) $('ci-btn').classList.remove('is-bad');
    if (co.value) { $('co-btn').classList.remove('is-bad'); $('err-dates').hidden = true; }
    var again = calEl.querySelector('[data-date="' + d + '"]');
    if (again) again.focus();
  });
  calEl.addEventListener('mouseover', function (e) {
    var b = e.target.closest('.cal-day');
    if (!b || !ci.value || co.value) return;
    var d = b.getAttribute('data-date');
    if (d !== hover) {
      hover = d;
      // repaint the range preview without rebuilding the buttons
      calEl.querySelectorAll('.cal-day').forEach(function (x) {
        var xd = x.getAttribute('data-date');
        x.classList.toggle('in-range', xd > ci.value && xd < hover);
        x.classList.toggle('is-end', xd === hover && hover > ci.value);
      });
    }
  });
  calEl.addEventListener('keydown', function (e) {
    var b = e.target.closest('.cal-day');
    if (!b) return;
    var step = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 }[e.key];
    if (!step) return;
    e.preventDefault();
    var target = iso(new Date(new Date(b.getAttribute('data-date') + 'T12:00:00').getTime() + step * 864e5));
    if (target < todayIso) return;
    var next = calEl.querySelector('[data-date="' + target + '"]');
    if (!next) { view.setMonth(view.getMonth() + (step > 0 ? 1 : -1)); renderCal(); next = calEl.querySelector('[data-date="' + target + '"]'); }
    if (next) next.focus();
  });
  ['ci-btn', 'co-btn'].forEach(function (id) {
    $(id).addEventListener('click', function () { showCal(calEl.hidden || true); });
  });
  var rT;
  window.addEventListener('resize', function () { clearTimeout(rT); rT = setTimeout(function () { if (!calEl.hidden) renderCal(); }, 150); });
  syncFields();
  showCal(true);

  /* Show the rate on each room card when rates are set. */
  document.querySelectorAll('[data-rate]').forEach(function (el) {
    var r = RATES[el.getAttribute('data-rate')];
    el.textContent = r ? t('From €' + r + ' per night', 'Da ' + r + ' € a notte') : '';
  });

  function update() {
    var n = nights();
    $('s-dates').textContent = ci.value && co.value ? fmt(ci.value) + ' → ' + fmt(co.value) : '—';
    $('s-nights').textContent = n > 0 ? String(n) : '—';
    var a = +$('adults').value, c = +$('children').value;
    $('s-guests').textContent = t(a + (a === 1 ? ' adult' : ' adults'), a + (a === 1 ? ' adulto' : ' adulti')) +
      (c ? t(', ' + c + (c === 1 ? ' child' : ' children'), ', ' + c + (c === 1 ? ' bambino' : ' bambini')) : '');
    var p = PACKAGES[val('package')];
    $('s-package').textContent = p[0];
    $('s-room').textContent = ROOMS[val('room')];
    var rate = RATES[val('room')];
    $('s-price').textContent = rate && n > 0
      ? t('About €' + rate * n + ' (confirmed by email)', 'Circa ' + rate * n + ' € (confermato via email)')
      : t('Confirmed by email', 'Confermato via email');
    $('s-perks').innerHTML = (p[1] || []).map(function (x) { return '<li>' + x + '</li>'; }).join('');
    var biz = val('package') === 'executive' || val('package') === 'padel';
    form.querySelector('.business-only').hidden = !biz;
  }
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  update();

  function invalid(el, bad) { el.classList.toggle('is-bad', bad); return bad; }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = false;
    ['name', 'email'].forEach(function (id) { if (invalid($(id), !$(id).checkValidity() || !$(id).value)) bad = true; });
    var datesBad = nights() <= 0;
    $('err-dates').hidden = !datesBad;
    invalid($('ci-btn'), !ci.value);
    invalid($('co-btn'), !co.value);
    if (datesBad) { bad = true; showCal(true); }
    var consentBad = !$('consent').checked;
    $('consent').closest('.check').classList.toggle('is-bad', consentBad);
    if (consentBad) bad = true;
    $('err-form').hidden = !bad;
    if (bad) { var first = form.querySelector('.is-bad'); if (first && first.focus) first.focus(); return; }

    var data = {
      checkin: ci.value, checkout: co.value, nights: nights(),
      adults: +$('adults').value, children: +$('children').value,
      package: PACKAGES[val('package')][0], room: ROOMS[val('room')],
      name: $('name').value.trim(), email: $('email').value.trim(), phone: $('phone').value.trim(),
      arrival: $('arrival').value, company: $('company').value.trim(), companyCode: $('companycode').value.trim(),
      notes: $('notes').value.trim(), returningGuest: $('returning').checked
    };
    var ref = 'VM-' + Math.random().toString(36).slice(2, 8).toUpperCase();
    data.reference = ref;
    var btn = form.querySelector('.book-submit');
    btn.disabled = true;
    btn.textContent = t('Sending…', 'Invio in corso…');

    window.VM.send('booking', data).then(function (res) {
      var done = $('book-done');
      done.innerHTML =
        '<p class="eb">' + t('Request received', 'Richiesta ricevuta') + '</p>' +
        '<h2 class="h2">' + t('Thank you, <i>' + escapeHtml(data.name.split(' ')[0]) + '.</i>', 'Grazie, <i>' + escapeHtml(data.name.split(' ')[0]) + '.</i>') + '</h2>' +
        '<p>' + t('Your reference is', 'Il tuo codice è') + ' <b class="ref">' + ref + '</b>. ' +
          t('We will email ' + escapeHtml(data.email) + ' with the price and confirmation.', 'Scriveremo a ' + escapeHtml(data.email) + ' con prezzo e conferma.') + '</p>' +
        '<dl class="done-sum"><dt>' + t('Dates', 'Date') + '</dt><dd>' + fmt(data.checkin) + ' → ' + fmt(data.checkout) + ' (' + data.nights + ')</dd>' +
          '<dt>' + t('Package', 'Pacchetto') + '</dt><dd>' + data.package + '</dd>' +
          '<dt>' + t('Room', 'Camera') + '</dt><dd>' + data.room + '</dd></dl>' +
        (res.sent ? '' : '<p class="demo-note">' + t('Demo mode: this request was not sent anywhere yet. The site owner connects it in assets/js/site.js (FORMS_ENDPOINT).',
          'Modalità demo: questa richiesta non è ancora stata inviata. Il gestore del sito la collega in assets/js/site.js (FORMS_ENDPOINT).') + '</p>') +
        '<div class="btns"><a class="btn btn-line" href="index.html">' + t('Back to home', 'Torna alla home') + '</a></div>';
      form.hidden = true;
      document.querySelector('.book-sum').hidden = true;
      done.hidden = false;
      done.focus();
      window.scrollTo(0, done.getBoundingClientRect().top + window.scrollY - 100);
    }).catch(function () {
      btn.disabled = false;
      btn.textContent = t('Send booking request', 'Invia la richiesta di prenotazione');
      $('err-form').hidden = false;
      $('err-form').textContent = t('We could not send your request. Please try again or contact us.', 'Non siamo riusciti a inviare la richiesta. Riprova o contattaci.');
    });
  });

  function escapeHtml(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
})();
