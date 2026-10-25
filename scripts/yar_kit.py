#!/usr/bin/env python3
"""Yaroslava's look (Masha's SMM, @mari.ivanuk) as HTML building blocks rendered to PNG by headless Chrome.

    import os, sys
    sys.path.insert(0, os.path.expanduser("~/.claude/skills/styl-yaroslavy/scripts"))
    from yar_kit import *

    d = Deck("carousel")                     # carousel | post | square | story | cover
    d.add(wrap(eyebrow("ситуація"), head("Реклама працює, а записів [одиниці]"), sub("Клієнт думає, що **проблема в рекламі**.")),
          obj=prop("/abs/path/robot.png", "right:60px; bottom:40px; height:420px"))
    d.render("/abs/out/dir")                 # 01.png, 02.png ... (+ the .html beside each, for tweaking)

Text markup everywhere: [слово] -> red accent, **слово** -> bold; everything else is HTML-escaped.
Image arguments take absolute paths (or file:// / https URLs).
Run `python3 yar_kit.py --demo <out_dir>` to render one slide of every element as a quick visual check.
"""
import html, os, re, shutil, subprocess, sys

KIT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(KIT), "assets", "fonts")

SIZES = {"carousel": (1080, 1350), "post": (1080, 1350), "square": (1080, 1080), "story": (1080, 1920), "cover": (1080, 1920)}
RED, ACC, INK, GREY, TXT2 = "#e1141b", "#ff2a2a", "#0d0d0e", "#1c1c1d", "#cfcaca"

CHROMES = [
    os.path.expanduser("~/Projects/Інструменти/ai-video-editor/node_modules/.remotion/chrome-headless-shell/mac-arm64/"
                       "chrome-headless-shell-mac-arm64/chrome-headless-shell"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("chromium") or "", shutil.which("google-chrome") or "",
]

# Montserrat from Google Fonts is a variable font: one file per script carries every weight 100-900.
_RANGES = {
    "cyrillic-ext": "U+0460-052F, U+1C80-1C8A, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F",
    "cyrillic": "U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116",
    "latin": "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, "
             "U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD",
}
FONT_CSS = "".join(
    f"@font-face{{font-family:'M';font-weight:100 900;src:url('file://{FONTS}/Montserrat-{k}.woff2') format('woff2');unicode-range:{r};}}\n"
    for k, r in _RANGES.items()) + "@font-face{font-family:'E';src:local('Apple Color Emoji');}\n"

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: __W__px; height: __H__px; overflow: hidden; background: #0d0d0e; font-family: 'M', 'E', sans-serif; color: #fff; }
.bg { position: absolute; inset: 0; }
.bg.glow { background: linear-gradient(158deg, #9b0a0f 0%, #3a0507 32%, #120708 55%, #0d0d0e 72%); }
.bg.dark { background: #0d0d0e; }
.bg.grey { background: #1c1c1d; }
.bg.red { background: #e1141b; }
.halo { position: absolute; left: -320px; top: -320px; width: 1100px; height: 1100px; border-radius: 50%;
  background: radial-gradient(circle, rgba(225,20,27,.5) 0%, rgba(225,20,27,.1) 45%, rgba(225,20,27,0) 70%); }
.count { position: absolute; right: 64px; top: 52px; font-size: 30px; font-weight: 500; color: #d8d2d2; letter-spacing: .04em; z-index: 5; }
.count b { color: #ff2a2a; font-weight: 800; }
.handle { position: absolute; left: 0; right: 0; bottom: 44px; text-align: center; font-size: 26px; color: #bdb6b6; z-index: 5; }
.wrap { position: absolute; left: 72px; right: 72px; display: flex; flex-direction: column; gap: 34px; z-index: 3; }
.wrap.center { align-items: center; text-align: center; }
.wrap > * { max-width: 100%; }
.r { color: #ff2a2a; }
.bg.red ~ .wrap .r, .on-red .r { color: #0d0d0e; }
.bg.red ~ .count, .bg.red ~ .handle { color: #ffe9e9; }
.bg.red ~ .count b { color: #0d0d0e; }
.eb { align-self: flex-start; display: inline-block; background: #e1141b; color: #fff; font-weight: 800; font-size: 30px; letter-spacing: .05em;
  text-transform: uppercase; padding: 11px 30px 12px; border-radius: 999px; box-shadow: 0 0 34px rgba(225,20,27,.6); }
.center .eb, .center .pill, .center .cta, .center .label { align-self: center; }
.h { font-weight: 900; line-height: 1.04; letter-spacing: -0.012em; text-transform: uppercase; }
.qh { font-weight: 900; line-height: 1.06; text-transform: uppercase; color: #ff2a2a; }
.sub { line-height: 1.32; font-weight: 400; color: #eae6e6; }
.sub b { font-weight: 800; color: #fff; }
.pill { position: relative; align-self: flex-start; display: inline-block; padding: 18px 40px 20px; border-radius: 999px; line-height: 1.2; }
.pill.red { background: #e1141b; color: #fff; font-weight: 700; box-shadow: 0 0 46px rgba(225,20,27,.65), inset 0 2px 0 rgba(255,255,255,.2); }
.pill.glass { background: rgba(255,255,255,.07); border: 2px solid rgba(255,255,255,.22); color: #e9e4e4; font-weight: 500; }
.pill.glass .rd { position: absolute; left: 22px; top: -6px; width: 22px; height: 22px; border-radius: 50%; background: #e1141b; box-shadow: 0 0 14px rgba(225,20,27,.8); }
.pill.dim { opacity: .5; }
.strike { position: absolute; left: 28px; right: 28px; top: 52%; height: 6px; border-radius: 4px; background: #ff2a2a; }
.banner { align-self: flex-start; margin-left: -72px; padding: 22px 46px 24px 72px; border-radius: 0 999px 999px 0; background: #e1141b; color: #fff;
  line-height: 1.25; font-weight: 500; box-shadow: 0 0 46px rgba(225,20,27,.55); }
.banner b { font-weight: 800; }
.bar { position: absolute; left: 0; right: 0; background: #e1141b; color: #fff; text-align: center; font-weight: 900; text-transform: uppercase;
  line-height: 1.2; padding: 30px 60px; z-index: 4; }
.card { position: relative; align-self: stretch; background: #fff; border-radius: 30px; padding: 38px 44px 34px; color: #121212; }
.card h3 { font-weight: 900; font-size: 42px; text-transform: uppercase; margin-bottom: 14px; }
.card ul { list-style: none; }
.tk { display: flex; align-items: center; gap: 18px; font-size: 38px; font-weight: 500; padding: 7px 0; color: #1b1b1b; }
.dot { flex: none; width: 34px; height: 34px; border-radius: 50%; background: #e1141b; position: relative; }
.dot::after { content: ""; position: absolute; left: 11px; top: 6px; width: 9px; height: 16px; border: solid #fff; border-width: 0 4px 4px 0; transform: rotate(45deg); }
.badge { position: absolute; right: -24px; top: -32px; width: 100px; height: 100px; border-radius: 50%; background: #e1141b; display: flex;
  align-items: center; justify-content: center; font-family: 'E'; font-size: 48px; box-shadow: 0 0 34px rgba(225,20,27,.6); }
.num { display: flex; flex-direction: column; gap: 26px; align-self: stretch; }
.num .it { position: relative; background: rgba(255,255,255,.06); border: 2px solid rgba(255,255,255,.14); border-radius: 22px;
  padding: 24px 32px 24px 40px; font-size: 34px; line-height: 1.28; color: #ece8e8; }
.num .n { position: absolute; left: -16px; top: -18px; width: 44px; height: 44px; border-radius: 50%; background: #e1141b; color: #fff;
  font-weight: 800; font-size: 26px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 18px rgba(225,20,27,.7); }
.stats { display: flex; gap: 22px; align-self: stretch; justify-content: center; }
.stat { flex: 1; background: rgba(255,255,255,.07); border: 2px solid rgba(255,255,255,.14); border-radius: 26px; padding: 26px 18px; text-align: center; }
.stat .big { color: #ff2a2a; font-weight: 900; font-size: 64px; line-height: 1; text-transform: uppercase; }
.stat .sm { margin-top: 10px; font-size: 26px; line-height: 1.25; color: #d9d4d4; }
.cta { align-self: flex-start; display: inline-flex; align-items: center; gap: 22px; border: 2px solid rgba(255,255,255,.4); border-radius: 999px;
  padding: 14px 40px 14px 16px; font-size: 36px; font-weight: 500; }
.cta .ar { width: 56px; height: 56px; border-radius: 50%; background: #e1141b; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 32px; }
.label { align-self: flex-start; color: #ff2a2a; font-weight: 900; font-size: 34px; text-transform: uppercase; letter-spacing: .02em; }
.fire { font-family: 'E'; font-size: 84px; letter-spacing: .08em; }
.circ { align-self: center; border-radius: 50%; overflow: hidden; border: 8px solid #e1141b; box-shadow: 0 0 60px rgba(225,20,27,.65); }
.circ img { width: 100%; height: 100%; object-fit: cover; display: block; }
.shots { position: relative; align-self: stretch; }
.shot { position: absolute; background: #fff; border-radius: 22px; padding: 10px; box-shadow: 0 24px 60px rgba(0,0,0,.55); }
.shot img { display: block; width: 100%; border-radius: 14px; }
.shot.redline { box-shadow: 0 0 0 5px #e1141b, 0 24px 60px rgba(0,0,0,.55); }
.photo { position: absolute; filter: drop-shadow(0 30px 60px rgba(0,0,0,.6)); z-index: 2; }
.bleed { position: absolute; z-index: 1; -webkit-mask-image: linear-gradient(to right, transparent 0%, #000 34%), linear-gradient(to bottom, transparent 0%, #000 16%);
  -webkit-mask-composite: source-in; mask-composite: intersect; }
.bleed.left { -webkit-mask-image: linear-gradient(to left, transparent 0%, #000 34%), linear-gradient(to bottom, transparent 0%, #000 16%); }
.full { position: absolute; z-index: 1; }
.shade { position: absolute; left: 0; right: 0; bottom: 0; z-index: 2; background: linear-gradient(180deg, rgba(13,13,14,0) 0%, rgba(13,13,14,.55) 30%, rgba(13,13,14,.9) 72%); }
.obj { position: absolute; z-index: 4; filter: drop-shadow(0 40px 50px rgba(0,0,0,.6)) drop-shadow(0 0 60px rgba(225,20,27,.28)); }
.emo { font-family: 'E'; }
.bigcaps { font-weight: 900; line-height: .98; letter-spacing: -0.015em; text-transform: uppercase; text-shadow: 0 10px 40px rgba(0,0,0,.5); }
"""


# ---------- text ----------
def t(s):
    """[x] -> red accent, **x** -> bold; the rest escaped."""
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"\[(.+?)\]", r'<span class="r">\1</span>', s)


def _src(p):
    return p if re.match(r"^(file|https?|data):", p) else "file://" + os.path.abspath(os.path.expanduser(p))


# ---------- blocks (return HTML strings) ----------
def eyebrow(s, style=""):
    return f'<div class="eb" style="{style}">{t(s)}</div>'


def head(s, size=84, style=""):
    return f'<div class="h" style="font-size:{size}px; {style}">{t(s)}</div>'


def quote_head(s, size=76):
    return f'<div class="qh" style="font-size:{size}px">«{t(s)}»</div>'


def sub(s, size=40, color=None, style=""):
    c = f"; color:{color}" if color else ""
    return f'<div class="sub" style="font-size:{size}px{c}; {style}">{t(s)}</div>'


def pill(s, size=40, style=""):
    return f'<div class="pill red" style="font-size:{size}px; {style}">{t(s)}</div>'


def glass(s, size=40, dot=True, style=""):
    return f'<div class="pill glass" style="font-size:{size}px; {style}">{"<i class=rd></i>" if dot else ""}{t(s)}</div>'


def wrong(s, size=40):
    """A struck-through dim glass pill: the bad option before the right one."""
    return f'<div class="pill glass dim" style="font-size:{size}px"><i class="rd"></i>{t(s)}<i class="strike"></i></div>'


def banner(s, size=36):
    """Red banner glued to the left edge (flat left side): a longer thesis, **bold** line inside."""
    return f'<div class="banner" style="font-size:{size}px">{t(s)}</div>'


def bar(s, bottom=110, size=40):
    """Full-width red strip; pass it as `extra=` to Deck.add (it is positioned on the page, not in the column)."""
    return f'<div class="bar" style="bottom:{bottom}px; font-size:{size}px">{t(s)}</div>'


def corner_pill(s, bottom=120, left=72, size=34):
    """The cover's «гортай карусель, покажу …)» pill pinned to the bottom-left; pass as extra=."""
    return f'<div class="pill red" style="position:absolute; left:{left}px; bottom:{bottom}px; font-size:{size}px; z-index:4">{t(s)}</div>'


def card(title, items, badge="👍"):
    li = "".join(f'<li class="tk"><i class="dot"></i><span>{t(x)}</span></li>' for x in items)
    b = f'<div class="badge">{badge}</div>' if badge else ""
    return f'<div class="card">{b}<h3>{t(title)}</h3><ul>{li}</ul></div>'


def numbered(items, size=34):
    return '<div class="num">' + "".join(
        f'<div class="it" style="font-size:{size}px"><span class="n">{i}</span>{t(x)}</div>' for i, x in enumerate(items, 1)) + "</div>"


def stats(pairs):
    """[("5 днів", "коротких уроків у Telegram"), ("0 грн", "повністю безкоштовно")]"""
    return '<div class="stats">' + "".join(
        f'<div class="stat"><div class="big">{t(a)}</div><div class="sm">{t(b)}</div></div>' for a, b in pairs) + "</div>"


def cta(s, size=36, style=""):
    return f'<div class="cta" style="font-size:{size}px; {style}"><span class="ar">→</span>{t(s)}</div>'


def label(s):
    return f'<div class="label">{t(s)}</div>'


def fire(n=3):
    return f'<div class="fire">{"🔥" * n}</div>'


def circle_photo(src, size=320, pos="50% 25%"):
    return f'<div class="circ" style="width:{size}px; height:{size}px"><img src="{_src(src)}" style="object-position:{pos}"></div>'


def shots(srcs, height=700, width=560, spread=None):
    """Screenshots (chats, reviews, tables) as white rounded cards, slightly fanned. spread=[(x, y, rot), ...]."""
    spread = spread or [(0, 0, -4), (300, 70, 3), (120, 260, -1), (380, 330, 5)]
    out = []
    for i, s in enumerate(srcs):
        x, y, r = spread[i % len(spread)]
        out.append(f'<div class="shot" style="left:{x}px; top:{y}px; width:{width}px; transform:rotate({r}deg); z-index:{i + 1}">'
                   f'<img src="{_src(s)}"></div>')
    return f'<div class="shots" style="height:{height}px">{"".join(out)}</div>'


def bigcaps(s, size=132):
    return f'<div class="bigcaps" style="font-size:{size}px">{t(s).replace(chr(10), "<br>")}</div>'


def wrap(*blocks, top=150, align="left", right=72, gap=34, bottom=None):
    """A text column. Several columns on one slide are fine: body = wrap(head(...), right=72) + wrap(sub(...), top=420, right=460)."""
    pos = f"top:{top}px" if bottom is None else f"bottom:{bottom}px"
    return f'<div class="wrap {"center" if align == "center" else ""}" style="{pos}; right:{right}px; gap:{gap}px">{"".join(blocks)}</div>'


def row(*blocks, gap=22):
    return f'<div style="display:flex; gap:{gap}px; flex-wrap:wrap; align-items:center">{"".join(blocks)}</div>'


# ---------- pictures placed on the page (pass as photo= / obj= / extra=) ----------
def bleed(src, style="right:0; bottom:0; height:1010px", side="right"):
    """A photo that melts into the dark background (no cut-out needed for dark/red-lit photos)."""
    return f'<img class="bleed {"left" if side == "left" else ""}" src="{_src(src)}" style="{style}">'


def cutout(src, style="right:-70px; bottom:-60px; height:900px"):
    """A person cut out on transparency (scripts/cutout.swift) standing over the background."""
    return f'<img class="photo" src="{_src(src)}" style="{style}">'


def full(src, style="left:0; top:0; width:100%; height:100%; object-fit:cover", shade_from=None):
    """Full-bleed photo; shade_from=960 adds the dark fade under text from that y down."""
    sh = f'<div class="shade" style="top:{shade_from}px"></div>' if shade_from is not None else ""
    return f'<img class="full" src="{_src(src)}" style="{style}">{sh}'


def prop(src, style):
    """A glossy 3D object (Higgsfield, transparent PNG trimmed to its bounds) with shadow and red glow."""
    return f'<img class="obj" src="{_src(src)}" style="{style}">'


# ---------- deck ----------
class Deck:
    def __init__(self, kind="carousel", handle=None, counter=None):
        self.kind = kind
        self.W, self.H = SIZES[kind]
        self.handle = handle if handle is not None else (kind in ("carousel", "post", "square"))
        self.counter = counter if counter is not None else (kind == "carousel")
        self.slides = []

    def add(self, body, photo="", obj="", extra="", bg="glow"):
        """bg: glow (dark + red light from the top-left corner, default) | dark | grey (stories with screenshots) | red ("explosion")."""
        self.slides.append((body, photo, obj, extra, bg))
        return self

    def _count(self, i):
        n = len(self.slides)
        return "".join(f"<b>{{{k}}}</b> " if k == i else f"({k}) " for k in range(1, n + 1)).strip()

    def page(self, i):
        body, photo, obj, extra, bg = self.slides[i - 1]
        css = CSS.replace("__W__", str(self.W)).replace("__H__", str(self.H))
        halo = '<div class="halo"></div>' if bg in ("glow", "dark") else ""
        cnt = f'<div class="count">{self._count(i)}</div>' if self.counter and len(self.slides) > 1 else ""
        hnd = '<div class="handle">@mari.ivanuk</div>' if self.handle else ""
        return (f'<!doctype html><html lang="uk"><head><meta charset="utf-8"><style>{FONT_CSS}{css}</style></head><body>'
                f'<div class="bg {bg}"></div>{halo}{photo}{cnt}{body}{obj}{extra}{hnd}</body></html>')

    def render(self, out_dir, names=None):
        out_dir = os.path.abspath(os.path.expanduser(out_dir))
        os.makedirs(out_dir, exist_ok=True)
        chrome = next((c for c in CHROMES if c and os.path.exists(c)), None)
        if not chrome:
            sys.exit("no headless Chrome found (see CHROMES in yar_kit.py)")
        paths = []
        for i in range(1, len(self.slides) + 1):
            name = names[i - 1] if names else f"{i:02d}"
            hp, png = os.path.join(out_dir, f"{name}.html"), os.path.join(out_dir, f"{name}.png")
            open(hp, "w", encoding="utf-8").write(self.page(i))
            flags = ["--headless=new"] if "Google Chrome.app" in chrome else ["--headless"]
            subprocess.run([chrome, *flags, "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                            "--force-device-scale-factor=1", f"--window-size={self.W},{self.H}", "--virtual-time-budget=6000",
                            f"--screenshot={png}", "file://" + hp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            paths.append(png)
        return paths


def _demo(out):
    d = Deck("carousel")
    d.add(wrap(eyebrow("ситуація"), head("Реклама працює, а записів [одиниці]"), sub("Заявки йдуть, переписок купа. Клієнт думає, що **проблема в рекламі**."),
               glass("реклама працювала"), wrong("«коли вам зручно?»"), pill("«завтра о 17:00 чи в неділю об 11:00?»")))
    d.add(wrap(eyebrow("думка №3"), quote_head("без блогу ніхто не прийде"), card("А головне тут:", ["відповідати швидко", "давати два часи"]),
               cta("збережи, щоб не загубити")))
    d.add(wrap(head("Що на тебе [чекає]:", 72), numbered(["Розберешся, хто такий таргетолог", "Подивишся на рекламу очима таргетолога",
                                                         "Зрозумієш, яку першу послугу запропонувати"]), banner("Не треба вирішувати одразу. **Спочатку просто спробуй)**"))
          )
    d.add(wrap(head("Перевір не в голові, [а на практиці]", 70), stats([("5 днів", "коротких уроків"), ("20 хв", "на день"), ("0 грн", "безкоштовно")]),
               label("бонус:"), sub("чек-лист за всі 5 завдань", 34), align="center"), extra=bar("Якщо давно думаєш про таргет, час перевірити на собі!"))
    d.add(wrap(fire(), head("Заявки на тест-драйв летять одна за одною", 64), align="center", top=200), bg="red")
    return d.render(out)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--demo":
        print("\n".join(_demo(sys.argv[2])))
    else:
        print(__doc__)
