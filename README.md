# Stitch Pattern Maker

Turns a logo into a hand-embroidery pattern at exact size, ready to print on washable
embroidery paper (water-soluble stabilizer, "stick and stitch" sheets). English and Arabic.
Everything runs in the browser; no image ever leaves the device.

## Use it

- **iPhone / iPad:** open https://ahmadoudeh.github.io/stitch-pattern-maker/ in Safari,
  tap Share → *Add to Home Screen*. After the first visit it works without internet.
- **Computer, offline:** double-click `dist/stitch-pattern-maker.html`. It is one file with
  everything inside, so you can also copy it to a USB stick.

## Printing on washable embroidery paper

| Sheet size | Typical products |
|---|---|
| A4, 21 × 29.7 cm | Vlieseline Solufix (A4 packs), most packs sold in Europe |
| US Letter, 21.6 × 27.9 cm | Sulky Stick'n Stitch, Sulky Sticky Fabri-Solvy, Pellon Print-Stitch-Dissolve |

Pick the same size in step 4. The page tells you the widest logo that fits on one sheet
(A4: 26 cm, Letter: 24 cm for a wide logo) and offers a button to shrink to it.
Print at 100 % / Actual size and check the 5 cm bar on a plain-paper test print first.

## Change it

Edit `src/index.html` (layout, styles, logic) or `src/strings.js` (all texts, EN + AR), then:

    python3 build.py

This writes `dist/stitch-pattern-maker.html` (single offline file) and `docs/`
(the web app GitHub Pages serves). `vendor/` holds jsPDF 2.5.1 and the fonts (OFL).
