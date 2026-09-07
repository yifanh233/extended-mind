# Build standalone light/dark SVGs from an archify HTML artifact (archify exports SVG only from its viewer).
# Usage: python build_svgs.py <architecture.html> <out-prefix> "<title as a question>" "<long description, one paragraph>"
# Writes <out-prefix>-light.svg and <out-prefix>-dark.svg next to the HTML: the diagram <svg> with the viewer's CSS
# variables and class rules inlined, an opaque background, a real <title>/<desc>, and viewer-only ARIA noise removed.
import io, re, sys
html_path, prefix, title, desc = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
h = io.open(html_path, encoding="utf-8").read()
svg = (re.search(r'<svg[^>]*data-engineering-profile[^>]*>.*?</svg>', h, re.S) or re.search(r'<svg[^>]*viewBox[^>]*>.*?</svg>', h, re.S)).group(0)
if 'xmlns="http://www.w3.org/2000/svg"' not in svg[:300]: svg = svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
css = "\n".join(re.findall(r'<style[^>]*>(.*?)</style>', h, re.S))
toks = set(t for c in re.findall(r'class="([^"]+)"', svg) for t in c.split())
rules = re.findall(r'([^{}]+)\{([^{}]*)\}', css)
keep = [(s.strip(), b.strip()) for s, b in rules if any(('.' + t) in s for t in toks) or 'svg' in s]
PRESET = '[data-preset="editorial"]'
plain = [s + "{" + b + "}" for s, b in keep if '[data-theme' not in s and '[data-preset' not in s]
pres = [s.replace(PRESET, '') + "{" + b + "}" for s, b in keep if PRESET in s and '[data-theme' not in s]
def vars_from(rx):
    out = {}
    for m in re.finditer(rx + r'\s*\{([^{}]*)\}', css):
        for k, v in re.findall(r'(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);', m.group(1)): out[k] = v.strip()
    return out
base = vars_from(r':root'); dark = vars_from(r'\[data-theme="dark"\]'); light = vars_from(r'\[data-theme="light"\]')
ed = vars_from(r'\[data-preset="editorial"\]'); edl = vars_from(r'\[data-preset="editorial"\]\[data-theme="light"\]'); edd = vars_from(r'\[data-preset="editorial"\]\[data-theme="dark"\]')
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def build(theme_vars, name):
    allv = dict(base); allv.update(theme_vars)
    root = ":root,svg{" + ";".join(f"{k}:{v}" for k, v in allv.items()) + "}"
    out = svg.replace("<defs>", "<defs><style>" + root + "\n" + "\n".join(plain) + "\n" + "\n".join(pres) + "</style>", 1)
    vb = re.search(r'viewBox="([^"]+)"', out).group(1).split()
    out = out.replace("</defs>", '</defs><rect x="0" y="0" width="%s" height="%s" fill="%s"/>' % (vb[2], vb[3], allv.get("--bg", "#ffffff")), 1)
    out = re.sub(r'<title id="archify-diagram-title">.*?</title>', '<title id="archify-diagram-title">' + esc(title) + '</title>', out, count=1, flags=re.S)
    out = re.sub(r'<desc id="archify-diagram-description">.*?</desc>', '<desc id="archify-diagram-description">' + esc(desc) + '</desc>', out, count=1, flags=re.S)
    out = re.sub(r'\s(role="button"|aria-pressed="[^"]*"|tabindex="[^"]*")', '', out)
    io.open(name, "w", encoding="utf-8", newline="\n").write(out); print(name, len(out), "bytes")
lv = dict(light); lv.update(ed); lv.update(edl)
dv = dict(dark); dv.update(ed); dv.update(edd)
build(lv, prefix + "-light.svg"); build(dv, prefix + "-dark.svg")
