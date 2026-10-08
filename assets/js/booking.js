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

  function iso(d) { return d.toISOString().slice(0, 10); }
  function addDays(s, n) { var d = new Date(s + 'T12:00:00'); d.setDate(d.getDate() + n); return iso(d); }
  function fmt(s) {
    if (!s) return '';
    return new Date(s + 'T12:00:00').toLocaleDateString(lang === 'it' ? 'it-IT' : 'en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
  }
  function nights() {
    if (!ci.value || !co.value) return 0;
    return Math.round((new Date(co.value + 'T12:00:00') - new Date(ci.value + 'T12:00:00')) / 864e5);
  }
  function val(name) { var el = form.querySelector('[name="' + name + '"]:checked'); return el ? el.value : ''; }

  /* Sensible defaults: dates from tomorrow, and the package/room from the link. */
  var today = iso(new Date());
  ci.min = today;
  co.min = addDays(today, 1);
  var tok = (location.hash || '').slice(1);
  if (LINKS[tok]) {
    var l = LINKS[tok];
    if (l[0] === 'returning') $('returning').checked = true;
    else { var r = form.querySelector('[name="' + l[0] + '"][value="' + l[1] + '"]'); if (r) r.checked = true; }
  }

  /* Show the rate on each room card when rates are set. */
  document.querySelectorAll('[data-rate]').forEach(function (el) {
    var r = RATES[el.getAttribute('data-rate')];
    el.textContent = r ? t('From €' + r + ' per night', 'Da ' + r + ' € a notte') : '';
  });

  function update() {
    if (ci.value) {
      co.min = addDays(ci.value, 1);
      if (co.value && co.value <= ci.value) co.value = '';
    }
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
    ['checkin', 'checkout', 'name', 'email'].forEach(function (id) { if (invalid($(id), !$(id).checkValidity() || !$(id).value)) bad = true; });
    var datesBad = nights() <= 0;
    $('err-dates').hidden = !datesBad || !ci.value || !co.value;
    if (datesBad) { invalid(co, true); bad = true; }
    var consentBad = !$('consent').checked;
    $('consent').closest('.check').classList.toggle('is-bad', consentBad);
    if (consentBad) bad = true;
    $('err-form').hidden = !bad;
    if (bad) { var first = form.querySelector('.is-bad input, input.is-bad, .is-bad'); if (first && first.focus) first.focus(); return; }

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
