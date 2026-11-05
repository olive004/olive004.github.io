# olive004.github.io

Personal academic website of Olivia Gallup, served with GitHub Pages.

## Structure

| Path | Purpose |
| --- | --- |
| `index.html`, `publications.html`, `projects.html` | Site pages (plain HTML, no build step) |
| `404.html` | "Page not found" page served by GitHub Pages |
| `styles.css` | All styles; colours and fonts are CSS variables at the top |
| `site.js` | Light/dark theme toggle |
| `assets/` | Profile photo, favicon, `Custom_Regular.ttf` and self-hosted IBM Plex Sans (`assets/fonts/`) |
| `_font-previews/` | Offline font-comparison previews (not published: underscore folders are skipped by Jekyll) |

## Editing

The header and sidebar are repeated in each page, so change them in all three files.

- Default font: Custom. Add `?font=plex` to any URL to view the site in IBM Plex Sans (`?font=custom` resets).
- Rebuild the previews: `python3 _font-previews/build_previews.py path/to/fontawesome-free`

## Preview locally

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy

Push to the `main` branch of the `olive004.github.io` repository and enable
GitHub Pages (Settings → Pages → Deploy from branch → `main` / root).
