# ANTIQUE brand assets

Supplied by the ANTIQUE owner on 2026-10-11 and kept here for upcoming videos. Used exactly as supplied.

- `products/` — real photographs of the three products (1125×2000, effectively 9:16): `hardener-1000ml.jpg`, `sealer-240ml.jpg`, `french-plaster-2kg.jpg`.
- `posters/` — the owner's poster graphics (4:5, headline text is part of the image) and `sample-post-reference.jpg`, the style reference.
- **No logo is drawn inside the videos** (owner's instruction, 2026-10-11), and the logo file is deliberately not stored here.

Provenance note for story plans: `"source": "ANTIQUE's own photo, supplied by the owner"`.

## Using a photo in a story plan

`story` only accepts images inside the plan's own folder, so copy the photos you need next to `story.json` (for example `work/<story>/`). Then:

```json
{"start": 0.3, "end": 3.5, "kind": "asset", "title": "مصلب الكونكريت", "path": "hardener-1000ml.jpg",
 "source": "ANTIQUE's own photo, supplied by the owner"}
```

Without `zoom` the photo is full-bleed. With `zoom` (antique style only) the scene shows a close-up of part of the same photo, as fractions of the image, under the `title` as a pill. Approximate label areas, to be checked by eye:

| Photo | zoom |
|---|---|
| `french-plaster-2kg.jpg` | `{"x":0.12,"y":0.51,"w":0.65,"h":0.31}` |
| `sealer-240ml.jpg` | `{"x":0.36,"y":0.36,"w":0.39,"h":0.39}` |
| `hardener-1000ml.jpg` | `{"x":0.25,"y":0.24,"w":0.42,"h":0.45}` |

Render with `--style antique --faceless`.
