# Villa Maria Hotel & Spa — website

Static site (HTML/CSS/JS, no build server). Serve the folder (`python3 -m http.server`) and open `index.html`.

## Pages
- Home: `index.html`
- Families: `italian-memories.html` (Italian Memories), `family-reset-package.html` (Family Discount), `ciao-again.html` (Ciao Again)
- Business: `business-travel.html` (Take the pressure out of business travel), `executive-business-stay.html` (Executive Business Stay Package), `padel-experience.html` (The Padel Experience)
- Package names and copy follow the Leisure and Business campaign emails (EN/IT PDFs).
- Booking: `booking.html` + `assets/js/booking.js` — our own booking-request page (no payment). Set nightly `RATES` in booking.js to show estimates.
- Hotel: `rooms.html`, `spa.html`, `restaurant.html`, `contact.html` (getting here & contact), `privacy.html`
- Italian: the same pages in `it/`, generated — do not edit them by hand

## Hotel facts — edit in one place
All contact details, legal numbers, review score, booking-engine address and offer terms live in
the `HOTEL` and `OFFERS` blocks at the top of `assets/js/site.js`. Any field left empty is hidden on
the site, so nothing invented is ever shown. Fill in before going live:
`phone`, `email`, `whatsapp`, `legalName`, `vat` (P.IVA), `cin`, `receptionHours`,
`reviews.rating` + `count`, `FORMS_ENDPOINT` (where booking requests and other forms are sent — until set, forms run in demo mode and say so),
and `OFFERS.familyDiscount` (`fromPrice`, `validFrom`, `validTo`, `minNights`). Confirm `address`.

## Italian pages
English pages are the source; Italian text sits next to it in `data-it="…"` attributes.
After editing any page, rebuild the Italian site:

    python3 tools/build-it.py

This writes `it/*.html` with the Italian text baked in (so Google indexes it), Italian titles and
descriptions, and (once `SITE_URL` is set to your own domain) hreflang links.
