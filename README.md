# Villa Maria Hotel & Spa — website

Static site (HTML/CSS/JS, no build step). Open `index.html` or serve the folder (`python3 -m http.server`).

## Structure
- `index.html` — homepage: persona split (families / business), all six campaigns, the hotel, €30 coupon
- Families: `italian-memories.html` (La Dolce Family), `family-reset-package.html` (Family Reset: €30 Off), `ciao-again.html` (Ciao Again)
- Business: `business-travel.html` (Business, Minus the Stress), `executive-business-stay.html` (Office With a Sea View), `padel-experience.html` (Padel & Prosecco)
- `assets/js/site.js` — shared header (MENU top-left), menu overlay, footer, €30 coupon modal, EN/IT toggle, and the welcome chooser (Family / Business / Stayed before, with Skip). It opens once per visit on the homepage (`<body data-welcome>`) and from every "Chat with us" button
- `assets/css/style.css` — design tokens and components

## Editing
- Booking link and coupon code: `CONFIG` at the top of `assets/js/site.js`.
- Italian copy lives next to the English in `data-it="…"` attributes.
- The coupon form is front-end only: it shows the code and does not send the email anywhere.
