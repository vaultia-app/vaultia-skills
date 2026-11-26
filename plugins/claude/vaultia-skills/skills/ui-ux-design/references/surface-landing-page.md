# Surface: Landing Page

Marketing sites, product and feature launches, campaign pages, and single-page sites: first-time visitors who decide in seconds whether to stay.

## What good looks like

- **One goal, one primary call to action** (sign up, book a demo, download, buy, contact), repeated down the page.
- **The message lands above the fold:** who it is for, what it does, why it is better, and the CTA, readable in about five seconds.
- **Fast and findable:** loads quickly on mobile networks and ranks for its key search terms.

Success is measured by conversion rate on the primary CTA, bounce rate, and Core Web Vitals.

## Content first

Copy and structure come before visuals. Ask (or confirm) before building:

| Decision | Why |
|---|---|
| Audience and their main problem | Sets the headline and the order of sections |
| The offer and the one primary CTA | Every section supports it |
| Proof available (customers, logos, numbers, reviews) | Trust sections need real content; never invent testimonials or logos |
| Brand (colors, logo, typography, imagery) | Landing pages express the brand more strongly than an app |

Use the user's real copy when they have it. When you draft copy, mark it as a draft and keep claims verifiable. Never ship placeholder text such as lorem ipsum.

## Section structure

A typical order; drop sections that have no real content:

| Section | Contains |
|---|---|
| Header | Logo, at most 4–5 links (anchors to sections), the primary CTA; sticky on scroll |
| Hero | Headline (benefit, not feature), one-sentence subheadline, primary CTA, optional secondary CTA, product visual |
| Social proof | Customer logos, a key number, or a rating |
| Problem → benefits | 3 benefits with icon, title, and one sentence each |
| Features / how it works | Steps or feature blocks with visuals, alternating layout |
| Testimonials | Quote, name, role, photo; real only |
| Pricing | Plans in `Card`s, recommended plan highlighted, monthly/yearly toggle (`Tabs` or `ToggleGroup`) |
| FAQ | `Accordion` answering objections (price, setup, security, cancellation) |
| Final CTA | Restate the offer and the CTA |
| Footer | Navigation, legal (privacy, terms), contact, social links |

## Building with the kit

- Use the kit's tokens, theme, and atoms (`Button`, `Badge`, `Card`, `Accordion`, `Tabs`, `Field`, `Input`, `Separator`, `Avatar`).
- Sections are app code: put them in the app (for example `components/sections/hero.tsx`), composed from kit components. Do not add marketing sections to `packages/ui`.
- No app shell, sidebar, or dense tables.

## Visual defaults

- Larger type scale: hero headline `text-4xl`–`text-6xl`, section titles `text-3xl`, generous line height.
- More whitespace: section padding `py-16`–`py-24`; content width `max-w-6xl`, text blocks `max-w-2xl`.
- Stronger brand: a brand theme from tokens, real product imagery, consistent illustration or photo style.
- Motion: subtle reveal on scroll at most; respect reduced-motion; never delay the content.

## Technical priorities

- **Rendering:** static generation or server rendering (for example Next.js static pages); no client-only rendering of content.
- **Performance budget:** LCP under 2.5 s, CLS under 0.1, INP under 200 ms on mobile. Optimized and sized images (`next/image` or equivalent), the hero image preloaded, fonts with `font-display: swap`, minimal client JavaScript.
- **SEO:** unique `title` and meta description, one `h1`, semantic sections, Open Graph and social images, canonical URL, `sitemap.xml` and `robots.txt`, structured data where it fits (`Organization`, `Product`, `FAQPage`).
- **Analytics:** track CTA clicks and form submissions as events, through the project's analytics setup.
- **Forms:** as few fields as possible (often just email); clear success state; spam protection; consent text when required.

## Checklist additions

- [ ] The hero states audience, benefit, and CTA without scrolling, on mobile and desktop.
- [ ] Exactly one primary CTA style across the page; secondary actions look secondary.
- [ ] Every claim, logo, testimonial, and number is real or marked as a placeholder for the user to replace.
- [ ] Lighthouse (mobile) Performance, Accessibility, Best Practices, and SEO at 90 or above.
- [ ] Images have meaningful `alt`; decorative images have empty `alt`.
- [ ] Legal links present; cookie consent when the analytics setup requires it.
