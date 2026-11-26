# Surface: Storefront

Online shops and catalogs: visitors who search, compare, and buy, often on mobile and often as guests.

## What good looks like

- **Find fast:** search and categories lead to the right product in a few steps.
- **Decide with confidence:** price, variants, stock, delivery, returns, and reviews are visible before adding to cart.
- **Checkout without friction:** guest checkout, few fields, the full cost before the last step, clear recovery from payment errors.

Success is measured by conversion rate, add-to-cart rate, checkout abandonment, and average order value.

## Screen set

| Screen | Essentials |
|---|---|
| Home | Search, main categories, promotions, best sellers; not a wall of banners |
| Category / product list (PLP) | Product grid, filters (price, size, brand, rating…), sort, result count, pagination or "load more" |
| Search | Autocomplete with products and categories, typo tolerance, helpful "no results" with suggestions |
| Product detail (PDP) | Gallery with zoom, title, price (sale and original), variant selectors, stock, quantity, add to cart, delivery and return info, description, specs, reviews, related products |
| Cart | Line items with variant, quantity (`NumberInput`), remove, subtotal, shipping estimate, promo code, checkout CTA; mini cart in a `Sheet` |
| Checkout | Contact → shipping → payment → review; order summary always visible; guest checkout by default |
| Order confirmation | Order number, summary, delivery estimate, next steps, account creation offer |
| Account | Orders and tracking, addresses, payment methods, wishlist; follow `surface-portal.md` for this area |

## Patterns and components

- **Product card** (app component): image with fixed aspect ratio, name, price, rating, a sale or stock `Badge`, quick add; the whole card links to the PDP.
- **Variants:** `ToggleGroup` or `RadioGroup` for size and color, with unavailable options disabled and explained.
- **Filters:** a sidebar on desktop, a `Sheet` or `BottomSheet` on mobile, with applied filters as removable chips and a result count.
- **Mobile PDP:** sticky add-to-cart bar; gallery swipe; key info above the fold.
- **Price:** format with the UI locale's currency (`CurrencyInput`/`Intl`); show taxes and shipping clearly as the market requires.
- **Trust:** return policy, delivery times and costs, secure payment methods, contact options, and real reviews near the buying decision.
- Product cards, cart, and checkout steps are app components composed from kit atoms and molecules; do not put commerce components in `packages/ui`.

## Checkout rules

- Never force account creation before purchase; offer it after.
- Show shipping options and costs before payment; show the final total before the user confirms.
- Use one column, autocomplete attributes (`autocomplete="email"`, `"street-address"`…), address formats for the market, and inline validation.
- Keep the cart and entered data if payment fails; explain the failure and how to retry or switch method.
- Offer the payment methods the market expects (cards, wallets, bank transfer, QR payments, cash on delivery) as the requirements specify.

## Visual defaults

- Product imagery leads: consistent aspect ratios and backgrounds; the UI stays neutral around it.
- Brand theme from tokens; sale, stock, and error states use semantic status colors.
- Comfortable density on PLP and PDP; generous touch targets.

## Technical priorities

- **Rendering:** server rendering or incremental static regeneration for home, PLP, and PDP; client rendering for cart and checkout interactions.
- **Performance:** LCP under 2.5 s on mobile; optimized responsive images; lazy-load below-the-fold images; avoid layout shift in grids.
- **SEO:** unique titles and descriptions per product and category, canonical URLs for filtered and sorted lists, `BreadcrumbList`, `Product` and `Offer` structured data (price, availability, rating).
- **Analytics:** e-commerce funnel events (view item, add to cart, begin checkout, add payment info, purchase) through the project's analytics setup.

## Checklist additions

- [ ] Price, availability, delivery, and returns are visible on the PDP without hunting.
- [ ] Out-of-stock and unavailable variants are clear and offer an alternative (notify me, similar items).
- [ ] Guest checkout works end to end; the total never changes unexpectedly on the last step.
- [ ] Payment failure keeps the cart and input and explains the next step.
- [ ] Filters work on mobile, show counts, and can be cleared in one action.
- [ ] Product, category, and breadcrumb structured data validate.
