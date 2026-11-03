"""Build self-contained font-comparison previews of the site.

Run from the repo root:  python3 _font-previews/build_previews.py [path/to/fontawesome-free]
Outputs _font-previews/preview-plex.html and preview-harding.html. Each file inlines
CSS, fonts and images so it opens offline, and shows all three pages as tabs.
The leading underscore keeps this folder out of the published GitHub Pages site.
"""
import base64, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "_font-previews"
FA = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None

def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()

def inline_urls(css, base):
    def repl(m):
        p = (base / m.group(1)).resolve()
        mime = {".woff2": "font/woff2", ".ttf": "font/ttf"}.get(p.suffix, "application/octet-stream")
        return f"url('{data_uri(p, mime)}')"
    return re.sub(r"url\('?([^')]+?\.(?:woff2|ttf))'?\)", repl, css)

css = inline_urls((ROOT / "styles.css").read_text(), ROOT)
fa_css = ""
if FA:
    for name in ("fontawesome.min.css", "solid.min.css", "brands.min.css"):
        fa_css += inline_urls((FA / "css" / name).read_text(), FA / "css")

# Shrink the profile photo for the preview.
try:
    from PIL import Image
    im = Image.open(ROOT / "assets/profile.png").convert("RGB")
    im.thumbnail((360, 360))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=85)
    photo = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
except Exception:
    photo = data_uri(ROOT / "assets/profile.png", "image/png")

pages = {"home": "index.html", "pubs": "publications.html", "proj": "projects.html"}
src = {k: (ROOT / v).read_text() for k, v in pages.items()}

def between(html, start, end):
    i = html.index(start) + len(start)
    return html[i:html.index(end, i)]

header = "<header>" + between(src["home"], "<header>", "</header>") + "</header>"
sidebar = '<aside class="sidebar">' + between(src["home"], '<aside class="sidebar">', "</aside>") + "</aside>"
sections = "".join(
    f'<section class="main-content" data-page="{k}"{" hidden" if k != "home" else ""}>'
    + between(src[k], '<section class="main-content" id="main">', "</section>\n    </main>")
    + "</section>"
    for k in pages
)
site_js = (ROOT / "site.js").read_text()

for font in ("plex", "harding"):
    attr = ' data-font="plex"' if font == "plex" else ""
    label = "Harding (Regular, lightened)" if font == "harding" else "IBM Plex Sans"
    html = f"""<!DOCTYPE html>
<html lang="en"{attr}>
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Preview - {label}</title>
<style>{fa_css}</style>
<style>{css}
</style>
</head>
<body>
{header.replace('assets/profile.png', photo)}
<main class="container-with-sidebar">
{sidebar.replace('assets/profile.png', photo)}
{sections}
</main>
<footer><p>&copy; 2026 Olivia Gallup</p></footer>
<script>
document.querySelectorAll('a[href$=".html"], a[href^="index.html#"]').forEach(function(a){{
  var map={{'index.html':'home','publications.html':'pubs','projects.html':'proj'}};
  var key=map[a.getAttribute('href').split('#')[0]]; if(!key) return;
  a.addEventListener('click',function(e){{
    e.preventDefault();
    document.querySelectorAll('[data-page]').forEach(function(s){{s.hidden=s.dataset.page!==key;}});
    document.querySelectorAll('.nav-links a').forEach(function(n){{n.classList.toggle('active',map[n.getAttribute('href').split('#')[0]]===key && !n.getAttribute('href').includes('#'));}});
    var h=a.getAttribute('href').split('#')[1]; if(h) document.getElementById(h).scrollIntoView(); else window.scrollTo(0,0);
  }});
}});
{site_js}
</script>
</body>
</html>"""
    (OUT / f"preview-{font}.html").write_text(html)
    print("wrote", OUT / f"preview-{font}.html", len(html) // 1024, "KB")
