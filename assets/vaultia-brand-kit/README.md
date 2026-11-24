# Vaultia Brand Assets

The mark is a bookmark inside a frame with two beveled corners. The wordmark is converted to vector paths with slightly rounded stroke ends, so the SVGs do not depend on installed fonts.

This folder contains only the assets this repository uses.

## Files

| File | Used by |
| --- | --- |
| `logos/vaultia-horizontal-light.svg` | Repository README logo, light theme |
| `logos/vaultia-horizontal-dark.svg` | Repository README logo, dark theme |
| `openai/logo-512.png` | Codex / ChatGPT plugin listing icon (`interface.logo`) |
| `openai/composer-light-192.png` | Codex composer icon, light theme (`interface.composerIcon`) |
| `openai/composer-dark-192.png` | Codex composer icon, dark theme (`interface.composerIconDark`) |
| `openai/interface-snippet.json` | Interface fields merged into every OpenAI plugin manifest |

## README logo

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/vaultia-brand-kit/logos/vaultia-horizontal-dark.svg">
  <img src="assets/vaultia-brand-kit/logos/vaultia-horizontal-light.svg" alt="Vaultia" width="260">
</picture>
```

## OpenAI plugins

`scripts/build_plugins.py` reads `openai/interface-snippet.json`, merges its fields into `extensions.com.openai.interface` of each generated `plugins/openai/<plugin>/plugin.json`, and copies every file it references to `plugins/openai/<plugin>/assets/brand/`. Change the images or colors here, then run `python3 scripts/build_plugins.py`. Never edit the copies under `plugins/`.

OpenAI accepts PNG, JPEG, WebP, and SVG icons. Icons must be square and at least 48 × 48 px, at most 5 MiB per file, and at most 4096 px per side for raster images. This kit uses a 512 px PNG for the listing and 192 px PNGs for the composer. The declared brand color is charcoal for the light theme and gold for the dark theme.

The Claude Code plugin manifest has no documented icon or logo field, so Claude plugins carry no brand assets.

## Colors

| Color | Hex |
| --- | --- |
| Vaultia gold | `#FFC533` |
| Charcoal | `#141414` |
| Cream white | `#F7F3E7` |

## Platform documentation

- [OpenAI plugin submission](https://developers.openai.com/plugins/deploy/submission)
- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Claude Code plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)
