"""Build Five Blocks, Web3 from first principles, into site/.

    python _src/build.py

The site is a real hash chain. Each topic page is a block whose hash is
SHA-256(previous block's hash, as 64 hex characters, followed by the exact bytes of
its original source files in site/data/). Block 0's previous hash is 64 zeros. The
home page re-computes the chain in the browser, so anyone can check it.

Blocks are listed in _src/blocks.json; each page body is _src/pages/<slug>.html with
a front-matter block (title, description) ended by a line of three dashes.
Standard library only; refuses to finish on a dead local link, a duplicate id or a
broken in-page anchor.
"""
import hashlib
import html
import json
import pathlib
import re

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent
SITE = ROOT / "site"
BOOK = json.loads((SRC / "blocks.json").read_text(encoding="utf-8"))
BLOCKS = BOOK["blocks"]
GENESIS = "0" * 64
e = html.escape


def chain():
    prev = GENESIS
    for b in BLOCKS:
        payload = b"".join((SITE / "data" / f).read_bytes() for f in b["files"])
        assert b"\r" not in payload, f"{b['slug']}: CRLF in site/data would break the hash on other machines"
        b["prev"], b["size"] = prev, len(payload)
        b["hash"] = prev = hashlib.sha256(prev.encode("ascii") + payload).hexdigest()


def identicon(h, size=40, cls="idn"):
    """A 5x5 mirrored pattern drawn from the block's own hash, like an Ethereum blockie."""
    bits = bin(int(h[:16], 16))[2:].zfill(64)
    hue = int(h[16:20], 16) % 360
    cells = []
    for row in range(5):
        for col in range(3):
            if bits[row * 3 + col] == "1":
                for c in {col, 4 - col}:
                    cells.append(f'<rect x="{c}" y="{row}" width="1" height="1"/>')
    return (f'<svg class="{cls}" viewBox="-.5 -.5 6 6" width="{size}" height="{size}" aria-hidden="true" focusable="false" '
            f'style="--hue:{hue}"><rect x="-.5" y="-.5" width="6" height="6" class="idn-bg"/><g class="idn-fg">{"".join(cells)}</g></svg>')


def short(h):
    return f"{h[:10]}…{h[-6:]}"


def read_page(slug):
    raw = (SRC / "pages" / f"{slug}.html").read_text(encoding="utf-8")
    head, body = raw.split("\n---\n", 1)
    return dict(l.split(": ", 1) for l in head.strip().splitlines()), body.strip()


def layout(title, desc, body, current=None):
    out = (SRC / "layout.html").read_text(encoding="utf-8")
    nav = "".join(
        f'<li><a href="{b["slug"]}.html"{" aria-current=\"page\"" if current == b["slug"] else ""}>'
        f'<span class="h" aria-hidden="true">#{i}</span>{e(b["short"])}</a></li>' for i, b in enumerate(BLOCKS))
    out = (out.replace("{{nav}}", nav).replace("{{title}}", e(title)).replace("{{description}}", e(desc))
           .replace("{{cur:about}}", ' aria-current="page"' if current == "about" else "").replace("{{body}}", body))
    assert "{{" not in out, title
    return out


def block_page(b, i):
    meta, body = read_page(b["slug"])
    ids = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    toc = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in ids) + '<li><a href="#record">The original record</a></li>'
    prev_b = BLOCKS[i - 1] if i else None
    next_b = BLOCKS[i + 1] if i + 1 < len(BLOCKS) else None
    files = "".join(
        f'<details class="rec"><summary><span class="mono">{e(f)}</span> <span class="muted">· {(SITE / "data" / f).stat().st_size:,} bytes</span></summary>'
        f'<div class="code" tabindex="0" aria-label="{e(f)}, scrolls sideways"><pre>{e((SITE / "data" / f).read_text(encoding="utf-8"))}</pre></div>'
        f'<p><a href="data/{e(f)}" download>Download {e(f)}</a></p></details>' for f in b["files"])
    prev_link = f'<a href="{prev_b["slug"]}.html" class="mono">{short(b["prev"])}</a>' if prev_b else f'<span class="mono">{short(b["prev"])}</span> <span class="muted">(genesis)</span>'
    pager = "".join([
        f'<a class="pg prev" href="{prev_b["slug"]}.html"><small>← Block #{i - 1}</small>{e(prev_b["title"])}</a>' if prev_b else "",
        f'<a class="pg next" href="{next_b["slug"]}.html"><small>Block #{i + 1} →</small>{e(next_b["title"])}</a>' if next_b else
        '<a class="pg next" href="index.html"><small>Chain tip</small>Back to all five blocks</a>'])
    page = f'''<header class="bhead">
  <div class="wrap bhead-in">
    <div class="bh-title">
      <p class="height">Block <span class="mono">#{i}</span> of {len(BLOCKS)}</p>
      <h1>{e(b["title"])}</h1>
      <p class="lede">{e(b["summary"])}</p>
    </div>
    <dl class="header-card" aria-label="Block header">
      <div class="hc-id">{identicon(b["hash"], 72)}</div>
      <div><dt>Hash</dt><dd class="mono hash" title="{b["hash"]}">{short(b["hash"])}</dd></div>
      <div><dt>Previous</dt><dd>{prev_link}</dd></div>
      <div><dt>Payload</dt><dd class="mono">{", ".join(e(f) for f in b["files"])} · {b["size"]:,} bytes</dd></div>
      <div><dt>First committed</dt><dd class="mono">{b["committed"]}</dd></div>
    </dl>
  </div>
</header>
<div class="wrap article">
  <nav class="toc" aria-label="In this block"><p class="toc-h">In this block</p><ol>{toc}</ol></nav>
  <article class="prose">
{body}
<section class="record" aria-labelledby="record">
  <h2 id="record">The original record</h2>
  <p>This page grew from the note{"s" if len(b["files"]) > 1 else ""} below, kept byte for byte. They are this block's payload, so changing one character would change its hash and break every block after it.</p>
  {files}
</section>
  </article>
</div>
<div class="wrap"><nav class="pager" aria-label="Blocks">{pager}</nav></div>'''
    return layout(meta["title"], meta["description"], page, b["slug"])


def main():
    chain()
    SITE.mkdir(exist_ok=True)
    written = []
    for i, b in enumerate(BLOCKS):
        (SITE / f'{b["slug"]}.html').write_text(block_page(b, i), encoding="utf-8", newline="\n")
        written.append(f'{b["slug"]}.html')

    links = "".join(f'''<li class="blk" data-i="{i}">
  <a href="{b["slug"]}.html">
    <span class="blk-top"><span class="height mono">#{i}</span>{identicon(b["hash"], 44)}<span class="state" data-state="{i}" aria-hidden="true"></span></span>
    <span class="blk-title">{e(b["title"])}</span>
    <span class="blk-sum">{e(b["summary"])}</span>
    <span class="blk-meta"><span class="k">hash</span> <span class="mono">{short(b["hash"])}</span></span>
    <span class="blk-meta"><span class="k">prev</span> <span class="mono">{short(b["prev"])}</span></span>
  </a>
</li>''' for i, b in enumerate(BLOCKS))
    manifest = json.dumps([{"slug": b["slug"], "files": b["files"], "prev": b["prev"], "hash": b["hash"]} for b in BLOCKS])
    meta, intro = read_page("index")
    home = f'''<header class="hero wrap">
  <p class="kicker mono">{e(BOOK["tagline"])}</p>
  <h1>Five blocks, <span class="nowrap">hash to oracle.</span></h1>
  <p class="lede">Web3 is built from a few old ideas in computer science. This site walks through them in order, one block at a time: fingerprints, replicas, traitors, a world computer, and the oracles that let it see out.</p>
</header>
<section class="chainwrap" aria-labelledby="chain-h">
  <div class="wrap">
    <div class="chain-head"><h2 id="chain-h">The chain</h2>
      <button type="button" class="btn" id="verify">Verify the chain in your browser</button></div>
    <ol class="chain">{links}</ol>
    <div class="verify-out" id="verify-out" role="status"><p>Each block's hash is SHA-256 of the previous hash and its source files. Press verify to recompute all five here, using your browser's own crypto. The empty circles fill in as each block checks out.</p></div>
  </div>
</section>
<script type="application/json" id="manifest">{manifest}</script>
{intro}'''
    (SITE / "index.html").write_text(layout(meta["title"], meta["description"], home), encoding="utf-8", newline="\n")

    meta, about = read_page("about")
    about = about.replace("{{genesis}}", GENESIS)
    (SITE / "about.html").write_text(layout(meta["title"], meta["description"], about, "about"), encoding="utf-8", newline="\n")
    meta, nf = read_page("404")
    (SITE / "404.html").write_text(layout(meta["title"], meta["description"], nf), encoding="utf-8", newline="\n")
    written += ["index.html", "about.html", "404.html"]

    problems = []
    for w in written:
        text = (SITE / w).read_text(encoding="utf-8")
        for ref in re.findall(r'(?:href|src)="([^"#?]+)', text):
            if not re.match(r"[a-z]+:|//", ref) and not (SITE / ref).is_file():
                problems.append(f"{w}: dead link {ref}")
        ids = re.findall(r'\sid="([^"]+)"', text)
        problems += [f"{w}: duplicate id {i}" for i in {i for i in ids if ids.count(i) > 1}]
        problems += [f"{w}: missing anchor #{a}" for a in re.findall(r'href="#([^"]+)"', text) if a not in ids]
    assert not problems, "\n".join(problems)
    print(f"built {len(written)} pages; chain tip {BLOCKS[-1]['hash']}")


if __name__ == "__main__":
    main()
