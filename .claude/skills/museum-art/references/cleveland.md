# Cleveland Museum of Art — Open Access Image Recipe (VERIFIED)

## TL;DR
- **Base URL:** `https://openaccess-api.clevelandart.org/api/artworks/`
- **Key required:** No — fully open, no key/token.
- **License:** CC0 (public domain), designated by CMA. No attribution required for CC0 works.
- **Verified 2026-07-24:** live API call returned real JSON with CC0 records; the returned image URL resolves to a real JPEG (396.3KB, confirmed via fetch).

## API Basics
- Docs: https://openaccess-api.clevelandart.org/ (interactive docs, last updated 2025-07-11)
- GitHub mirror (full dataset dump, JSON/CSV, updated weekly): https://github.com/ClevelandMuseumArt/openaccess
- Program overview / license page: https://www.clevelandart.org/open-access
- Endpoints:
  - `GET /api/artworks/` — search/list artworks
  - `GET /api/artworks/{id}` — single artwork
  - `GET /api/creators/`, `/api/creators/{id}`
  - `GET /api/exhibitions/`, `/api/exhibitions/{id}`

## Key Query Params (for CC0 + image)
| Param | Meaning |
|---|---|
| `cc0=1` | only works licensed CC0 (public domain, no restrictions) |
| `has_image=1` | only artworks that have a web image asset |
| `q=<term>` | free-text search |
| `limit=<n>` | page size |
| `skip=<n>` | pagination offset |
| `copyrighted` (opposite of cc0) | filters copyrighted works instead — do NOT use if you want open images |

Response field `share_license_status` will read `"CC0"`, `"Copyrighted"`, or `"Other"` — filter/inspect this if double-checking after the fact.

## Image URL Fields
Each artwork's `images` object contains up to 3 renditions, each with `url`, `filename`, `filesize`, `width`, `height`:
- `images.web` — JPEG, 900px longest side, 300dpi (good default "full-res-enough" download)
- `images.print` — JPEG, 3400px longest side, 300dpi (high-res)
- `images.full` — TIFF, variable dimensions/dpi (archival max-res)

`alternate_images` may hold extra views in the same 3 renditions.

Image CDN host: `https://openaccess-cdn.clevelandart.org/...` — direct hotlinkable JPEG/TIFF, no auth.

## Step-by-Step Recipe

**(a) Search for public-domain artworks with images:**
```
GET https://openaccess-api.clevelandart.org/api/artworks/?cc0=1&has_image=1&limit=10
```
Optional: add `&q=monet` (or any term) to narrow by keyword; add `&skip=10` to paginate.

**(b) Get a full-res image URL from a result:**
From each returned artwork object, read:
```
result.images.print.url   # high-res JPEG (3400px)
result.images.full.url    # archival TIFF (max res), if present
result.images.web.url     # 900px JPEG, smaller/fast
```
No further auth or signing needed — the URL is directly downloadable.

## Concrete Verified Example
**exampleApiUrl** (fetched live, returned real data):
```
https://openaccess-api.clevelandart.org/api/artworks/?cc0=1&has_image=1&limit=3
```
Sample of what it returned:
```json
[
  {
    "id": 94979,
    "title": "Nathaniel Hurd",
    "share_license_status": "CC0",
    "images.web.url": "https://openaccess-cdn.clevelandart.org/1915.534/1915.534_web.jpg"
  },
  {
    "id": 92937,
    "title": "Stag at Sharkey's",
    "share_license_status": "CC0",
    "images.web.url": "https://openaccess-cdn.clevelandart.org/1922.1133/1922.1133_web.jpg"
  }
]
```

**exampleImageUrl** (verified resolves to a real JPEG, 396.3KB, image/jpeg):
```
https://openaccess-cdn.clevelandart.org/1915.534/1915.534_web.jpg
```
(This is the "web" 900px rendition for accession 1915.534, "Nathaniel Hurd," CC0. Swap `_web` for `_print` in the same path pattern for the 3400px rendition where available — but always trust the JSON's `images.print.url` field over guessing the filename pattern, since not every record has a print/full tier.)

## License & Attribution
- CMA designates open-access content as **CC0** — no copyright, no restriction, no attribution required.
- Non-CC0 records exist in the same API (`share_license_status: "Copyrighted"` or `"Other"`) — always filter with `cc0=1` (or check the field) before treating an image as free-use.
- CMA suggests (optional, not required for CC0) citing: Artist, Title, Date, Medium, Dimensions, Institution, Credit Line, Accession Number, URL.

## Gotchas
- **No rate limit documented** — be a good citizen anyway (add delays for bulk scraping); no official published number.
- **Not every record has all 3 image tiers.** Always read the actual `images.*.url` fields from the JSON rather than assuming a naming convention holds for every accession — some records only have `web`, not `print`/`full`.
- **No IIIF image API** — CMA does NOT expose IIIF (no `/iiif/.../full/full/0/default.jpg` sizing syntax). Sizing is fixed to the 3 pre-rendered tiers (web/print/full), not parametric.
- **`cc0` vs `copyrighted` params are opposite filters** — don't confuse them; use `cc0=1` for open images.
- **Full dataset dump available on GitHub** (`ClevelandMuseumArt/openaccess`, JSON/CSV, updated weekly) if you want to avoid live API pagination for bulk work.
- Image CDN (`openaccess-cdn.clevelandart.org`) is a separate host from the API host (`openaccess-api.clevelandart.org`) — don't assume same-origin for CORS purposes if building a browser app.

## Sources
- https://openaccess-api.clevelandart.org/ (API docs)
- https://www.clevelandart.org/open-access (license/program page)
- https://github.com/ClevelandMuseumArt/openaccess (dataset mirror)
- Live verification: `GET https://openaccess-api.clevelandart.org/api/artworks/?cc0=1&has_image=1&limit=3` fetched 2026-07-24, returned real JSON.
- Live verification: `https://openaccess-cdn.clevelandart.org/1915.534/1915.534_web.jpg` fetched 2026-07-24, confirmed real JPEG (image/jpeg, 396.3KB).
