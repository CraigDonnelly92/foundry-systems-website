# Foundry Systems website

The live site is the files in this folder (index.html, pricing.html, etc.).
It's hosted on GitHub Pages and points at foundrysystems.ca.

## Quick settings (app.js, top of file)
- `stripe.core` / `stripe.complete`: paste your Stripe payment links to show "Pay now" buttons on the thank-you page.
- `promoEnd`: the $99/mo promo banner, strikethrough and countdown switch off on their own on Jan 1, 2027.

## Forms
Contact, checkup and project forms send to craig.foundrysystems@gmail.com through FormSubmit.co.
The first submission sends an activation email to that inbox. Click the link once and forms go live.

## Editing pages
Page text lives in `_build/build.py`, styles in `_build/styles.css`, scripts in `_build/app.js`.
After editing, run `python3 _build/build.py .` from this folder to rebuild, then commit and push.
