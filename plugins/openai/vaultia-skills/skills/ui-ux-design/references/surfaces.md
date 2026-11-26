# Surfaces

Every page belongs to one of three surfaces. Pages with the same design intent share a surface, and the surface decides how much visual polish, motion, content, and interaction the page gets. Classify each page before planning; a product can mix surfaces (a marketing site in front of a portal, a storefront with an account area).

| | Landing page | Storefront | Portal |
|---|---|---|---|
| Design intent | Impress and persuade | Inform and sell | Get work done |
| Pages | Marketing and launch pages, campaigns, company sites, blogs, editorial content | Product, category, promotion, and pricing pages; ads and sales pages; cart and checkout | Admin, dashboards, back offices, SaaS apps, account areas, internal tools |
| Visual polish | High: distinctive, brand-led, expressive typography and imagery | Medium: clean and trustworthy; product and price stand out | Just enough: consistent and plain, defaults from the kit |
| Motion | Rich: scroll reveals, transitions, micro-interactions, hero animation | Minimal: hover and feedback only | Functional only: feedback and state changes |
| Content | Storytelling and brand voice; long-form for blogs | Clear and specific: price, specs, availability, delivery, offers | Data, labels, and status; no marketing copy |
| Interaction | Low: read, scroll, one call to action | Medium: browse, filter, choose options, buy | High: tables, forms, filters, bulk actions, permissions, keyboard |
| Rendering | Static or server-rendered; SEO and speed matter | Server-rendered catalog; SEO and speed matter | Client-side is fine; no SEO |

## Landing page

- Design is the product: invest in layout, typography, imagery, and motion that make the brand memorable.
- One primary call to action, repeated down the page; every section supports it. Blogs and editorial pages focus on readability: comfortable line length, clear headings, related content.
- Animation is welcome but never blocks content: content is readable without it, it respects reduced-motion settings, and the page stays fast (LCP under 2.5 s on mobile).
- Never invent testimonials, logos, or numbers, and never ship placeholder text.

## Storefront

- Clarity sells: price, variants, stock, delivery, returns, and offers are visible and specific before the user decides.
- Keep motion to hover states and feedback (added to cart, loading); nothing that delays browsing or buying.
- The path to purchase is short: guest checkout, the full total before the last step, and the cart kept when payment fails.
- Product imagery leads; the interface around it stays neutral and consistent.

## Portal

- Focus on business logic and interaction: every rule, status, permission, and edge case in the requirements is visible and handled in the UI.
- Visuals are just enough: kit defaults, semantic colors for status, no decorative imagery or animation.
- Design for repeat use: frequent tasks in few clicks, keyboard support, filters kept in the URL, compact density when data is heavy.
- Show only what the role may use; confirm destructive and bulk actions with their scope.

## Shared rule

Surface-specific blocks (marketing sections and animations, product cards, cart and checkout steps, dashboard widgets) are app components composed from the kit, never added to the kit package. Templates for a surface follow the column above that matches it.
