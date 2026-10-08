# Villa Maria Hotel & Spa — website

Static site (HTML/CSS/JS, no build server). Serve the folder (`python3 -m http.server`) and open `index.html`.

## Pages
- Home: `index.html`
- Families: `italian-memories.html` (Italian Memories), `family-reset-package.html` (Family Discount), `ciao-again.html` (Ciao Again)
- Business: `business-travel.html` (Take the pressure out of business travel), `executive-business-stay.html` (Executive Business Stay Package), `padel-experience.html` (The Padel Experience)
- Package names and copy follow the Leisure and Business campaign emails (EN/IT PDFs).
- Booking: `booking.html` + `assets/js/booking.js` — our own booking-request page with a date-range calendar (nights counted automatically; no payment). Set nightly `RATES` in booking.js to show estimates.
- Hotel: `activities.html`, `rooms.html`, `spa.html`, `restaurant.html`, `contact.html` (getting here & contact), `privacy.html`
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
Every page has a longer description; Home, Rooms, Spa, Restaurant, Activities and Getting here
also have a gallery. Facts come from the campaign emails, the official site's pages (pools & beach,
kids, rooms, Linfa spa, meetings) and booking listings. Topics marked `# illustrative` in
`tools/about.py` are example copy for this concept site; the footer says so. Each page has (a short intro plus
topics that open on click) and a photo gallery with a full-screen viewer. The text (EN/IT) and the
photos live in `tools/about.py`. Home, Rooms, Spa, Restaurant, Activities and Getting here use
showcase carousels (`CARDS`): each card has its own photo slider with ‹ › arrows, and ← → moves
between cards. Add photos to a card's list to show more. After editing:

    python3 tools/about.py && python3 tools/build-it.py

## FAQ ("Good to know") sections
Every page has a question-and-answer accordion just before the footer. Questions and answers
(English and Italian) live in `tools/faq.py`. After editing them:

    python3 tools/faq.py && python3 tools/build-it.py

The build also adds Google's FAQPage data, generated from the visible questions.

## Email marketing
- **Sign-up pop-up** (home page only, once per visitor, after 8 seconds or 40% scroll): two lists, *I travel with family* and *I travel for business*. It opens on Business for visitors who have read the business pages. "No thanks" hides it for 30 days. Every page has a "Get our emails" link in the footer. Settings: `NEWSLETTER` in `assets/js/site.js` (the €30 family welcome coupon and its code `FAMILY30`).
- Sign-ups go to `FORMS_ENDPOINT` as form `newsletter` with `{list: 'family'|'business', firstName, email, consent, source}`. Add them to the matching list in your email tool (Brevo, Mailchimp…).
- **The emails** are in `emails/en/` and `emails/it/`, built from the campaign PDFs by `python3 tools/emails.py`. Preview them all at `emails/index.html`.
  - Family: 1 Italian Memories with the €30 coupon (right after sign-up), 2 Family Discount (7 days later), 3 Ciao Again (after check-out).
  - Business: 1 Take the pressure out of business travel (right after sign-up), 2 Executive Business Stay (7 days later), 3 The Padel Experience (after check-out).
- Before sending, set `SITE_URL` in `tools/emails.py` (images and links must be absolute in email), set `FIRST_NAME` and `UNSUBSCRIBE` to your email tool's merge tags, and rebuild. Links carry `utm_source=newsletter` and the email name.
- Email links can open things on the site: `#help`, `#review`, `#join`, `#refer`, `#message`, `#newsletter`, and `booking.html?code=FAMILY30#family-discount` fills in the coupon.

## Servers to connect (all optional; the site says "demo mode" until they are set)
In `assets/js/site.js`:
- `FORMS_ENDPOINT` — receives booking requests, messages, reviews, sign-ups and referrals as JSON `{form, lang, page, sentAt, data}`.
- `REVIEW_VERIFY_ENDPOINT` — receives `{reference, email}` and answers `{verified: true|false, name?}`. Only answer `true` when the booking exists and its check-out date has passed, so only real guests can review. After check-out, email each guest a personal link such as `index.html#review-VM-AB12CD`; it opens the review check with the reference filled in.
- `CHAT_ENDPOINT` — the Help chat sends `{messages, lang, facts}` and expects `{reply}`. Your server should call an AI model with `facts` as its only source. Without it, the chat uses Claude inside the claude.ai preview, and instant FAQ answers everywhere else (labelled "Instant answers").
