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

W = H = 1024
PAPER = (247, 242, 231)
INK = (20, 18, 14)
RED = (179, 32, 42)
GREY = (92, 86, 76)
BAND = (20, 18, 14)
WHITE = (250, 248, 243)

FONT_DIR = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_BLACK = "NotoSerif-Black.ttf"
SERIF_BOLD = "NotoSerif-Bold.ttf"
SANS_BLACK = "NotoSans-Black.ttf"
SANS_BOLD = "NotoSans-Bold.ttf"
SANS = "NotoSans-Regular.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, x, y, w, kicker, headline, blurb, head_size=27, blurb_size=18):
    """One news block: red kicker, serif headline, sans blurb. Returns height used."""
    draw.text((x, y), kicker, font=font(SANS_BLACK, 18), fill=RED)
    y += 27
    hf = font(SERIF_BOLD, head_size)
    for line in wrap(draw, headline, hf, w):
        draw.text((x, y), line, font=hf, fill=INK)
        y += int(head_size * 1.15)
    y += 3
    bf = font(SANS, blurb_size)
    for line in wrap(draw, blurb, bf, w):
        draw.text((x, y), line, font=bf, fill=(52, 48, 40))
        y += int(blurb_size * 1.3)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40
    CW = W - 2 * M

    # --- top hairline + dateline strip -----------------------------------
    d.line([(M, 26), (W - M, 26)], fill=INK, width=3)
    d.text((M, 34), "ONE DAY · ONE IMAGE · THE WHOLE WORLD", font=font(SANS_BOLD, 19), fill=GREY)
    right = "EST. 2026"
    d.text((W - M - d.textlength(right, font=font(SANS_BOLD, 19)), 34), right,
           font=font(SANS_BOLD, 19), fill=GREY)

    # --- masthead ---------------------------------------------------------
    mast = "THE WORLD IN ONE PAGE"
    mf = font(SERIF_BLACK, 71)
    d.text(((W - d.textlength(mast, font=mf)) / 2, 58), mast, font=mf, fill=INK)

    # --- red date band ----------------------------------------------------
    d.rectangle([M, 148, W - M, 204], fill=RED)
    date_line = "WEDNESDAY · 25 NOVEMBER 2026"
    df = font(SANS_BLACK, 38)
    d.text(((W - d.textlength(date_line, font=df)) / 2, 157), date_line, font=df, fill=WHITE)

    # --- lead story -------------------------------------------------------
    y = 222
    d.text((M, y), "TOP STORY — STRAIT OF HORMUZ · IRAN", font=font(SANS_BLACK, 21), fill=RED)
    y += 30
    hf = font(SERIF_BLACK, 46)
    for line in ["Two Tankers Hit Mines", "in Strait of Hormuz"]:
        d.text((M, y), line, font=hf, fill=INK)
        y += 52
    y += 4
    bf = font(SANS, 22)
    lead = ("Iran's Revolutionary Guard said two oil tankers struck naval mines "
            "and caught fire in the strait. Tehran said the vessels had taken "
            "an unauthorised route, as fears for energy shipping grew.")
    for line in wrap(d, lead, bf, CW):
        d.text((M, y), line, font=bf, fill=(52, 48, 40))
        y += 26
    y += 8
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 16

    # --- two-column grid --------------------------------------------------
    col_w = (CW - 40) // 2
    x1, x2 = M, M + col_w + 40
    grid_top = y
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
    row_h = 140
    for i in range(3):
        draw_block(d, x1, grid_top + i * row_h, col_w, *blocks_left[i])
        draw_block(d, x2, grid_top + i * row_h, col_w, *blocks_right[i])
    # column divider
    mid = M + col_w + 20
    d.line([(mid, grid_top + 2), (mid, grid_top + 3 * row_h - 22)], fill=(196, 188, 168), width=2)
    y = grid_top + 3 * row_h - 4

    # --- markets band -----------------------------------------------------
    d.rectangle([M, y, W - M, y + 52], fill=BAND)
    markets = "MARKETS  ·  S&P 500 -0.5%  ·  NASDAQ -1.5%  ·  DOW +0.9%  ·  NIKKEI -2.8%  ·  KOSPI -6.2%  ·  BRENT $87.8"
    size = 23
    while size > 12 and d.textlength(markets, font=font(SANS_BOLD, size)) > CW - 32:
        size -= 1
    mkf = font(SANS_BOLD, size)
    d.text(((W - d.textlength(markets, font=mkf)) / 2, y + 14), markets, font=mkf, fill=WHITE)
    y += 58

    # --- in brief ---------------------------------------------------------
    brief = ("IN BRIEF — Shenzhou-24 docks at Tiangong with Pakistan's first astronaut aboard · "
             "Pope Leo XIV laments COP31 failure · Colombia police free supermarket hostages · "
             "Dell's record quarter on AI servers")
    brf = font(SANS, 19)
    for line in wrap(d, brief, brf, CW):
        d.text((M, y), line, font=brf, fill=(52, 48, 40))
        y += 24
    y += 4
    d.line([(M, y), (W - M, y)], fill=INK, width=3)
    foot = "Every story on this page was reported on Wednesday 25 November 2026."
    ff = font(SANS_BOLD, 18)
    d.text(((W - d.textlength(foot, font=ff)) / 2, y + 8), foot, font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
