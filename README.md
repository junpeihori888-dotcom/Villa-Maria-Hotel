# Villa Maria Hotel & Spa — website

Static site (HTML/CSS/JS, no build server). Serve the folder (`python3 -m http.server`) and open `index.html`.

## Pages
- Home: `index.html`
- Families: `italian-memories.html` (Italian Memories), `family-reset-package.html` (Family Discount), `ciao-again.html` (Ciao Again)
- Business: `business-travel.html` (Take the pressure out of business travel), `executive-business-stay.html` (Executive Business Stay Package), `padel-experience.html` (The Padel Experience)
- Package names and copy follow the Leisure and Business campaign emails (EN/IT PDFs).
- Booking: `booking.html` + `assets/js/booking.js` — our own booking-request page with a date-range calendar (nights counted automatically; no payment). Set nightly `RATES` in booking.js to show estimates.
- Hotel: `rooms.html`, `spa.html`, `restaurant.html`, `contact.html` (getting here & contact), `privacy.html`
- Italian: the same pages in `it/`, generated — do not edit them by hand

## Hotel facts — edit in one place
All contact details, legal numbers, review score, booking-engine address and offer terms live in
the `HOTEL` and `OFFERS` blocks at the top of `assets/js/site.js`. Any field left empty is hidden on
the site, so nothing invented is ever shown. Fill in before going live:
`phone`, `email`, `whatsapp` (these become the Call / WhatsApp / Email buttons in Help), `conciergeHours`,
`checkIn`, `checkOut`, `replyTime`, `legalName`, `vat` (P.IVA), `cin`,
`reviews.rating` + `count`, `FORMS_ENDPOINT` (where booking requests and other forms are sent — until set, forms run in demo mode and say so),
and `OFFERS.familyDiscount` (`fromPrice`, `validFrom`, `validTo`, `minNights`). Confirm `address`.

## Italian pages
English pages are the source; Italian text sits next to it in `data-it="…"` attributes.
After editing any page, rebuild the Italian site:

    python3 tools/build-it.py

This writes `it/*.html` with the Italian text baked in (so Google indexes it), Italian titles and
descriptions, and (once `SITE_URL` is set to your own domain) hreflang links.

## Hotel descriptions and galleries
Home, Rooms, Spa, Restaurant and Getting here each have a longer description (a short intro plus
topics that open on click) and a photo gallery with a full-screen viewer. The text (EN/IT) and the
photos live in `tools/about.py`. Galleries look best with 5 or 9 photos. After editing:

    python3 tools/about.py && python3 tools/build-it.py

## FAQ ("Good to know") sections
Every page has a question-and-answer accordion just before the footer. Questions and answers
(English and Italian) live in `tools/faq.py`. After editing them:

    python3 tools/faq.py && python3 tools/build-it.py

The build also adds Google's FAQPage data, generated from the visible questions.

## Servers to connect (all optional; the site says "demo mode" until they are set)
In `assets/js/site.js`:
- `FORMS_ENDPOINT` — receives booking requests, messages, reviews, sign-ups and referrals as JSON `{form, lang, page, sentAt, data}`.
- `REVIEW_VERIFY_ENDPOINT` — receives `{reference, email}` and answers `{verified: true|false, name?}`. Only answer `true` when the booking exists and its check-out date has passed, so only real guests can review. After check-out, email each guest a personal link such as `index.html#review-VM-AB12CD`; it opens the review check with the reference filled in.
- `CHAT_ENDPOINT` — the Help chat sends `{messages, lang, facts}` and expects `{reply}`. Your server should call an AI model with `facts` as its only source. Without it, the chat uses Claude inside the claude.ai preview, and instant FAQ answers everywhere else (labelled "Instant answers").
