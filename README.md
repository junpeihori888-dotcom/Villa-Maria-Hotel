# Villa Maria Hotel & Spa — website

Static site (HTML/CSS/JS, no build server). Serve the folder (`python3 -m http.server`) and open `index.html`.

## Pages
- Home: `index.html`
- Families: `italian-memories.html` (La Dolce Family), `family-reset-package.html` (Family Reset: €30 Off), `ciao-again.html` (Ciao Again)
- Business: `business-travel.html` (Business, Minus the Stress), `executive-business-stay.html` (Office With a Sea View), `padel-experience.html` (Padel & Partners)
- Hotel: `rooms.html`, `spa.html`, `restaurant.html`, `contact.html` (getting here & contact), `privacy.html`
- Italian: the same pages in `it/`, generated — do not edit them by hand

## Hotel facts — edit in one place
All contact details, legal numbers, review score, booking-engine address and offer terms live in
the `HOTEL` and `OFFERS` blocks at the top of `assets/js/site.js`. Any field left empty is hidden on
the site, so nothing invented is ever shown. Fill in before going live:
`phone`, `email`, `whatsapp`, `legalName`, `vat` (P.IVA), `cin`, `receptionHours`,
`reviews.googleRating` + `googleCount`, `booking.url` + `booking.promoParam`,
and `OFFERS.familyReset` (`fromPrice`, `validFrom`, `validTo`, `minNights`). Confirm `address`.

## Italian pages
English pages are the source; Italian text sits next to it in `data-it="…"` attributes.
After editing any page, rebuild the Italian site:

    python3 tools/build-it.py

This writes `it/*.html` with the Italian text baked in (so Google indexes it), Italian titles and
descriptions, and hreflang links. Set `SITE_URL` in the script to the live address.
