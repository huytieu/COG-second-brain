# National Gallery of Art (Washington) — Open Access Image Recipe

Status: VERIFIED (live IIIF fetch succeeded, real image bytes returned).

## Base URL(s)

- **Data/metadata**: CSV dumps in the GitHub repo `github.com/NationalGalleryOfArt/opendata` (data lives under `/data/*.csv`, fetch raw via `raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/<file>.csv`). No search API — this is a bulk CSV export, updated frequently (daily per the repo docs).
- **Image server (IIIF Image API 2.0, level1)**: `https://api.nga.gov/iiif/{uuid}/{region}/{size}/{rotation}/{quality}.{format}`
  - `info.json` at `https://api.nga.gov/iiif/{uuid}/info.json` confirms native width/height and supported sizes/qualities.

There is no public REST/search API beyond the CSV files + IIIF image server — no `api.nga.gov` object-search endpoint documented. Treat this as "CSV catalog + IIIF images," not a queryable API.

## Key requirement

**None.** No API key, no auth, no rate-limit header observed. CSVs are public GitHub raw files; the IIIF image server responds with `access-control-allow-origin: *` and no auth challenge.

## License

**CC0-1.0** (Creative Commons Zero / public domain dedication) for the dataset itself — repo `LICENSE` + README state NGA "waives any copyright or related rights that it might have in this dataset." Attribution is *requested* (not required) for research use citing "National Gallery of Art Open Data Program."

Per-image rights are **not uniformly CC0** — see gotcha below on the `openaccess` flag. Only rows where `published_images.openaccess = 1` are the institution's actual open-access (full-resolution, reuse-cleared) images; `openaccess = 0` rows are still shown via IIIF but resolution-capped (see `maxpixels`), meaning rights-restricted/third-party-copyright works.

## Relevant CSV files (from `data/` dir)

- `objects.csv` — one row per artwork: `objectid, uuid, title, attribution (artist), displaydate, medium, dimensions, classification, creditline, departmentabbr, wikidataid, ...`. No explicit "is public domain" column at the object level.
- `published_images.csv` — one row per digitized image: `uuid, iiifurl, iiifthumburl, viewtype, sequence, width, height, maxpixels, openaccess, depictstmsobjectid, assistivetext`. This is the file that actually gates open access:
  - `iiifurl` = the IIIF base identifier URL (append IIIF path params to get an image).
  - `iiifthumburl` = pre-built 200×200 thumbnail convenience URL.
  - `openaccess` = `1` → full resolution downloadable via IIIF `full/full` or `full/max`; `0` → IIIF still serves an image but the server enforces a `maxpixels` ceiling (e.g. 900px on the long edge) — these are NOT open access.
  - `depictstmsobjectid` = join key back to `objects.csv.objectid` for title/artist metadata.
  - `assistivetext` = an auto-generated alt-text description of the image (handy bonus field).

## Search recipe

### (a) Find public-domain artworks that have an image

No live search API — do it against the CSVs (download or stream them):

1. Fetch `https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/published_images.csv`.
2. Filter rows where `openaccess == "1"` (string "1") AND `viewtype == "primary"` (primary image, not alternate crops/details) → these are full-res, reuse-cleared images.
3. Take the `depictstmsobjectid` from each surviving row and join against `objects.csv.objectid` to pull `title`, `attribution` (artist), `displaydate`, `medium`, `classification`.
4. `uuid` (or equivalently `iiifurl`'s trailing path segment) is the identifier to build image-request URLs.

No pagination/rate-limit concerns since it's a flat file — just stream/filter client-side (Python `csv`/`pandas`, or `curl` + `awk`/`grep` for quick checks). Both CSVs are large (130k+ objects, more image rows); use streaming reads, not full in-memory loads if resource-constrained.

### (b) Get a full-resolution downloadable image URL from a result

Given a `uuid` (e.g. from `published_images.csv`, row with `openaccess=1`):

```
GET https://api.nga.gov/iiif/{uuid}/full/full/0/default.jpg
```
or equivalently
```
GET https://api.nga.gov/iiif/{uuid}/full/max/0/default.jpg
```
Both returned the object's native full resolution in testing (3365×4332 px, 2.57 MB JPEG for the example below). Use `info.json` first if you want to confirm native dimensions or pick a specific IIIF `size` token (e.g. `!1600,1600` to cap the long edge) instead of `full`.

## Example URLs (live-tested 2026-07-24)

- **exampleApiUrl** (metadata, first bytes of the open-access image catalog):
  `https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/published_images.csv`
  First data row: `uuid=00007f61-4922-417b-8f27-893ea328206c, iiifurl=https://api.nga.gov/iiif/00007f61-4922-417b-8f27-893ea328206c, openaccess=1, depictstmsobjectid=17387` (join to `objects.csv` objectid 17387 for title/artist).

- **info.json check**:
  `https://api.nga.gov/iiif/00007f61-4922-417b-8f27-893ea328206c/info.json` → returned valid IIIF Image API 2.0 descriptor, native size 3365×4332, level1 profile, jpg format, supports `sizeAboveFull`.

- **exampleImageUrl** (full-resolution, downloadable):
  `https://api.nga.gov/iiif/00007f61-4922-417b-8f27-893ea328206c/full/full/0/default.jpg`
  → `HTTP/2 200`, `content-type: image/jpeg`, `content-length: 2569142` (2.57 MB), served via Cloudflare + IIPImage, `access-control-allow-origin: *`.

## Verification performed

- Fetched `published_images.csv` raw (byte-range) — confirmed real header + rows, confirmed `openaccess`/`maxpixels` semantics by comparing an `openaccess=1` row (no maxpixels cap) against an `openaccess=0` row (maxpixels=900).
- Fetched `objects.csv` raw (byte-range) — confirmed schema and that title/artist metadata lives here, joined via `objectid`.
- `curl` GET `info.json` for a real uuid — valid IIIF descriptor returned.
- `curl -I` (HEAD) on `full/full/0/default.jpg` and `full/max/0/default.jpg` — both HTTP 200, image/jpeg, multi-MB content-length, i.e. genuinely full resolution, not a redirect or error page.
- `curl -I` on the `iiifthumburl` pattern (`full/!200,200/0/default.jpg`) — HTTP 200, small JPEG (9.7 KB), confirming the thumbnail convenience URL also works.

**verified = true.**

## Gotchas

- **`openaccess` flag is per-image, not per-object.** Always filter on it — do not assume every row in `published_images.csv` is reuse-cleared. Rows with `openaccess=0` are capped by IIIF server-side (`maxpixels`, e.g. 900px long edge) — these are rights-restricted (e.g. copyrighted contemporary works, loans) and should be excluded from a "CC0 image" pipeline.
- **IIIF profile is level1** — supports `sizeAboveFull` per the `info.json` profile, which is why `full/full` and `full/max` both return native resolution rather than erroring; not all IIIF servers allow this (level0 servers only serve pre-baked sizes).
- **No live object/artwork search API.** Anyone wanting "search by artist/title/date" must filter the CSV client-side (or load into SQLite/DuckDB — the repo ships `sql_tables/` schema helpers for exactly this). Don't assume a `?q=` REST endpoint exists.
- **CSV files are large** (130k+ objects across multiple linked tables — `objects.csv`, `published_images.csv`, `constituents.csv`, `objects_constituents.csv`, etc. per the repo's `data/` dir) — use streaming parses or DuckDB/SQLite rather than loading everything into memory naively.
- **Rate limits**: none encountered on either GitHub raw or `api.nga.gov` in this test; Cloudflare fronts `api.nga.gov` and sets `__cf_bm` cookies but did not block repeated HEAD requests. Be a reasonably polite bulk client anyway (the data updates frequently — no need to re-download the whole CSV more than daily).
- **Attribution**: not legally required (CC0) but NGA requests citing "National Gallery of Art Open Data Program" for datasets built on this data; for images, credit lines are in `objects.csv.creditline` per object (nice to surface even though not mandatory).
- **`assistivetext`** in `published_images.csv` is a free, pre-generated alt-text/description per image — useful if you need accessible captions without running your own vision model.
