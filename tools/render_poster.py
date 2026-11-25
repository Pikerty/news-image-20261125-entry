#!/usr/bin/env python3
"""Render the entry poster for make.fun competition news-image-20261125.

Draws a one-page newspaper front page that sums up the world news of
Wednesday 25 November 2026, using only stories reported that day (Just
Security's Early Edition, SCMP's world page, Yeni Safak, NordFX market
pulse, Reuters markets, Open Chronicle's 25 Nov brief). Offline asset
builder: it is NOT run by the grader. The grader runs main.ts, which
copies the entry.png this script produces. Run from the entry/
directory: writes entry.png (1024x1024, PNG, under 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
PAPER = (247, 242, 231)
INK = (20, 18, 14)
RED = (179, 32, 42)
GREY = (92, 86, 76)
BAND = (20, 18, 14)
WHITE = (250, 248, 243)

FONT_DIR = "/usr/share/fonts/truetype/noto/"

# Named palette / layout constants (previously inline literals).
BODY_INK = (52, 48, 40)
DIVIDER_GREY = (196, 188, 168)
COLUMN_GUTTER = 40
GRID_ROW_HEIGHT = 140
KICKER_SIZE = 18
KICKER_ADVANCE = 27
HEADLINE_LEADING = 1.15
BLURB_LEADING = 1.3
BLURB_GAP = 3


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_BLACK = "NotoSerif-Black.ttf"
SERIF_BOLD = "NotoSerif-Bold.ttf"
SANS_BLACK = "NotoSans-Black.ttf"
SANS_BOLD = "NotoSans-Bold.ttf"
SANS = "NotoSans-Regular.ttf"


def check_fonts():
    missing = [name for name in (SERIF_BLACK, SERIF_BOLD, SANS_BLACK, SANS_BOLD, SANS)
               if not os.path.isfile(FONT_DIR + name)]
    if missing:
        raise SystemExit("missing required font file(s): " + ", ".join(missing))


def fit_font(canvas, text, start_size, max_width, name, min_size=12):
    size = start_size
    while size > min_size and canvas.textlength(text, font=font(name, size)) > max_width:
        size -= 1
    return font(name, size)


def wrap(canvas, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if canvas.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(canvas, x, y, w, kicker, headline, blurb, head_size=27, blurb_size=18):
    """One news block: red kicker, serif headline, sans blurb. Returns height used."""
    canvas.text((x, y), kicker, font=font(SANS_BLACK, KICKER_SIZE), fill=RED)
    y += KICKER_ADVANCE
    hf = font(SERIF_BOLD, head_size)
    for line in wrap(canvas, headline, hf, w):
        canvas.text((x, y), line, font=hf, fill=INK)
        y += int(head_size * HEADLINE_LEADING)
    y += BLURB_GAP
    bf = font(SANS, blurb_size)
    for line in wrap(canvas, blurb, bf, w):
        canvas.text((x, y), line, font=bf, fill=BODY_INK)
        y += int(blurb_size * BLURB_LEADING)
    return y


def main():
    check_fonts()
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    MARGIN = 40
    CONTENT_WIDTH = W - 2 * MARGIN

    # --- top hairline + dateline strip -----------------------------------
    draw.line([(MARGIN, 26), (W - MARGIN, 26)], fill=INK, width=3)
    draw.text((MARGIN, 34), "ONE DAY · ONE IMAGE · THE WHOLE WORLD", font=font(SANS_BOLD, 19), fill=GREY)
    right = "EST. 2026"
    draw.text((W - MARGIN - draw.textlength(right, font=font(SANS_BOLD, 19)), 34), right,
              font=font(SANS_BOLD, 19), fill=GREY)

    # --- masthead ---------------------------------------------------------
    mast = "THE WORLD IN ONE PAGE"
    mast_font = font(SERIF_BLACK, 71)
    draw.text(((W - draw.textlength(mast, font=mast_font)) / 2, 58), mast, font=mast_font, fill=INK)

    # --- red date band ----------------------------------------------------
    draw.rectangle([MARGIN, 148, W - MARGIN, 204], fill=RED)
    date_line = "WEDNESDAY · 25 NOVEMBER 2026"
    date_font = font(SANS_BLACK, 38)
    draw.text(((W - draw.textlength(date_line, font=date_font)) / 2, 157), date_line, font=date_font, fill=WHITE)

    # --- lead story -------------------------------------------------------
    y_cursor = 222
    draw.text((MARGIN, y_cursor), "TOP STORY — STRAIT OF HORMUZ · IRAN", font=font(SANS_BLACK, 21), fill=RED)
    y_cursor += 30
    lead_head_font = font(SERIF_BLACK, 46)
    for line in ["Two Tankers Hit Mines", "in Strait of Hormuz"]:
        draw.text((MARGIN, y_cursor), line, font=lead_head_font, fill=INK)
        y_cursor += 52
    y_cursor += 4
    lead_body_font = font(SANS, 22)
    lead = ("Iran's Revolutionary Guard said two oil tankers struck naval mines "
            "and caught fire in the strait. Tehran said the vessels had taken "
            "an unauthorised route, as fears for energy shipping grew.")
    for line in wrap(draw, lead, lead_body_font, CONTENT_WIDTH):
        draw.text((MARGIN, y_cursor), line, font=lead_body_font, fill=BODY_INK)
        y_cursor += 26
    y_cursor += 8
    draw.line([(MARGIN, y_cursor), (W - MARGIN, y_cursor)], fill=INK, width=2)
    y_cursor += 16

    # --- two-column grid --------------------------------------------------
    col_w = (CONTENT_WIDTH - COLUMN_GUTTER) // 2
    x1, x2 = MARGIN, MARGIN + col_w + COLUMN_GUTTER
    grid_top = y_cursor
    blocks_left = [
        ("MIDDLE EAST · SAUDI ARABIA",
         "Houthis Hit Riyadh Tower, Ras Tanura Refinery",
         "A drone strike on a Riyadh skyscraper injured 11; the Houthis said "
         "they also hit the Ras Tanura refinery."),
        ("UKRAINE WAR",
         "Overnight Strikes Kill 3; Kyiv Hits Two Refineries",
         "Russia and Ukraine reported 3 deaths, 15 injuries; Ukrainian drones "
         "set two Rosneft refineries ablaze."),
        ("ISRAEL · GAZA",
         "Strike Kills Hamas Security Chief and Family",
         "Israel killed Hamas colonel Mohammad Abuelouf, his wife and two "
         "children in Gaza City, medics said."),
    ]
    blocks_right = [
        ("UNITED STATES · TECHNOLOGY",
         "Huawei Guilty of Trade-Secret Theft, Bank Fraud",
         "A Brooklyn jury convicted Huawei on 10 of 12 counts, including bank "
         "fraud and sanctions violations."),
        ("PACIFIC",
         "Australia Signs Base-Barring Treaty with Solomons",
         "Canberra and Honiara signed a treaty precluding any foreign military "
         "base on the Solomon Islands."),
        ("SUDAN",
         "RSF Drone Strikes Kill 19 Civilians",
         "Sudanese rights group Emergency Lawyers said paramilitary drone "
         "strikes killed 19 and wounded 20."),
    ]
    for row_index in range(3):
        draw_block(draw, x1, grid_top + row_index * GRID_ROW_HEIGHT, col_w, *blocks_left[row_index])
        draw_block(draw, x2, grid_top + row_index * GRID_ROW_HEIGHT, col_w, *blocks_right[row_index])
    # column divider
    mid = MARGIN + col_w + COLUMN_GUTTER // 2
    draw.line([(mid, grid_top + 2), (mid, grid_top + 3 * GRID_ROW_HEIGHT - 22)], fill=DIVIDER_GREY, width=2)
    y_cursor = grid_top + 3 * GRID_ROW_HEIGHT - 4

    # --- markets band -----------------------------------------------------
    MARKETS_BAND_HEIGHT = 52
    draw.rectangle([MARGIN, y_cursor, W - MARGIN, y_cursor + MARKETS_BAND_HEIGHT], fill=BAND)
    market_items = ["MARKETS", "S&P 500 -0.5%", "NASDAQ -1.5%", "DOW +0.9%",
                    "NIKKEI -2.8%", "KOSPI -6.2%", "BRENT $87.8"]
    markets = "  ·  ".join(market_items)
    markets_font = fit_font(draw, markets, 23, CONTENT_WIDTH - 32, SANS_BOLD)
    draw.text(((W - draw.textlength(markets, font=markets_font)) / 2, y_cursor + 14), markets, font=markets_font, fill=WHITE)
    y_cursor += 58

    # --- in brief ---------------------------------------------------------
    brief_items = ["Shenzhou-24 docks at Tiangong with Pakistan's first astronaut aboard",
                   "Pope Leo XIV laments COP31 failure",
                   "Colombia police free supermarket hostages",
                   "Dell's record quarter on AI servers"]
    brief = "IN BRIEF — " + " · ".join(brief_items)
    brief_font = font(SANS, 19)
    for line in wrap(draw, brief, brief_font, CONTENT_WIDTH):
        draw.text((MARGIN, y_cursor), line, font=brief_font, fill=BODY_INK)
        y_cursor += 24
    y_cursor += 4
    draw.line([(MARGIN, y_cursor), (W - MARGIN, y_cursor)], fill=INK, width=3)
    foot = "Every story on this page was reported on Wednesday 25 November 2026."
    foot_font = font(SANS_BOLD, 18)
    draw.text(((W - draw.textlength(foot, font=foot_font)) / 2, y_cursor + 8), foot, font=foot_font, fill=GREY)

    img.save("entry.png", optimize=True)
    with Image.open("entry.png") as saved:
        assert saved.size == (W, H) and saved.mode == "RGB", f"bad output: {saved.size} {saved.mode}"
    print(f"wrote entry.png ({os.path.getsize('entry.png')} bytes, verified 1024x1024 RGB)")


if __name__ == "__main__":
    main()
