# Rijksmuseum — Open-Access Image Recipe (VERIFIED 2026-07-24)

## TL;DR
- **Starting hint was stale.** `rijksmuseum.nl/api/en/collection` (the old apikey-based "Collection API") is **deprecated**. The current, live, documented API is the **Linked Art Search API** at `data.rijksmuseum.nl/search/collection`.
- **No API key needed** for the current API. It's fully open.
- Images come via a separate **IIIF** image service (`iiif.micr.io`), reached by walking the linked-art graph from a search result.
- License: **CC0 / Public Domain** for the vast majority of digitized objects (confirmed on the test object). Attribution is requested but not legally required for CC0/PD items.

## Base URL
- Search: `https://data.rijksmuseum.nl/search/collection`
- Object resolver (linked data / JSON-LD): `https://id.rijksmuseum.nl/{objectId}`
- Image (IIIF, via Micrio): `https://iiif.micr.io/{imageId}/{region}/{size}/{rotation}/{quality}.{format}`

## API Key
**Not required.** The new Search API (`data.rijksmuseum.nl`) is public, no registration, no key, no auth header. (The legacy `rijksmuseum.nl/api/en/collection` API *did* require a free key via account registration + profile settings — but that endpoint is marked DEPRECATED in the current docs and should not be used for new integrations.)

## License
- **CC0 / Public Domain** for most digitized collection objects — confirmed directly on the test object's `VisualItem` record: `subject_to` → `classified_as` → `https://creativecommons.org/publicdomain/mark/1.0/` ("Public Domain") and a nested `subject_of` rights block citing `https://creativecommons.org/publicdomain/zero/1.0/` (CC0).
- Some items are CC BY 4.0 (attribution required) or fully copyrighted/restricted — always read the object's own rights block rather than assuming.
- Museum's policy page (`data.rijksmuseum.nl/policy/`): attribution is *requested* ("kindly ask you to credit the Rijksmuseum") but not legally mandatory for CC0/PD works.

## Search Recipe (step by step)

### (a) Search for public-domain artworks that have images
1. Call `GET https://data.rijksmuseum.nl/search/collection?type=painting&imageAvailable=true`
   - `imageAvailable=true` filters to objects with a digital reproduction.
   - Other useful params: `creator`, `creationDate` (wildcards `*`/`?`), `description`, `material`, `technique`, `title`, `type`, `objectNumber`, `memberOfSetId`, `aboutActor`. Repeat a param to OR multiple values (e.g. two `material=`).
   - There is **no direct license/CC0 filter param** — the API doesn't expose rights as a search facet. In practice, filter/verify license per-object (see step 4 below) since almost everything with `imageAvailable=true` in the general collection is Public Domain/CC0.
   - Response is a Linked-Art `OrderedCollectionPage`: `orderedItems: [{id: "https://id.rijksmuseum.nl/{objectId}", type: "HumanMadeObject"}, ...]`, plus `partOf.totalItems` and a `next.id` URL (contains an opaque `pageToken`) for pagination — just follow `next.id` verbatim for the next page. Page size is capped at 100.

2. Pick an object id from `orderedItems`, e.g. `https://id.rijksmuseum.nl/200105887`.

### (b) Get a full-resolution downloadable image URL from a result
3. `GET https://id.rijksmuseum.nl/{objectId}` (Accept: application/json) → JSON-LD `HumanMadeObject` record. Find the `shows` array → `{id: "https://id.rijksmuseum.nl/{visualItemId}", type: "VisualItem"}`.
4. `GET https://id.rijksmuseum.nl/{visualItemId}` → `VisualItem` record. Check:
   - `subject_to[].classified_as[].id` for the rights statement (look for `creativecommons.org/publicdomain/...`).
   - `digitally_shown_by` → `{id: "https://id.rijksmuseum.nl/{digitalObjectId}", type: "DigitalObject"}`.
5. `GET https://id.rijksmuseum.nl/{digitalObjectId}` → `DigitalObject` record. Its `access_point[0].id` is the **ready-to-use full-resolution IIIF image URL**, already in the form `https://iiif.micr.io/{imageId}/full/max/0/default.jpg` — no further construction needed, just use it as-is.

### IIIF sizing (if you want other resolutions/crops)
Template: `https://iiif.micr.io/{imageId}/{region}/{size}/{rotation}/{quality}.{format}`
- `region`: `full` (whole image) or `x,y,w,h` pixel box
- `size`: `max` (native full res), `!2000,2000` (fit within box), `800,` (width 800, auto height)
- `rotation`: `0` normally
- `quality`: `default` (or `gray`, `bitonal`)
- `format`: `jpg`, `png`, `webp`, etc.
Docs: `data.rijksmuseum.nl/docs/iiif/image` (IIIF Image API), `data.rijksmuseum.nl/docs/iiif/presentation` (manifests), `data.rijksmuseum.nl/docs/iiif/` (overview).

## Concrete Example (fully verified live, 2026-07-24)

**exampleApiUrl** (search):
```
https://data.rijksmuseum.nl/search/collection?type=painting&imageAvailable=true
```
Verified via `curl` → HTTP 200, valid JSON, `totalItems: 4916`, first result `https://id.rijksmuseum.nl/200100988`.

**Object chain used for the image example:**
- Object: `https://id.rijksmuseum.nl/200105887` → "Cat at Play" (Katjesspel), Henriëtte Ronner-Knip, c.1860-1878, object number SK-A-3089
- VisualItem: `https://id.rijksmuseum.nl/202105887` → rights = Public Domain / CC0
- DigitalObject: `https://id.rijksmuseum.nl/5001087555671055286110` → `access_point[0].id`

**exampleImageUrl**:
```
https://iiif.micr.io/YAxov/full/max/0/default.jpg
```
Verified via `curl -I` and full download:
- HTTP/2 200, `content-type: image/jpeg`, `content-length: 1,463,989 bytes`
- Actual pixel dimensions: **3720×2696**, baseline JPEG
- `access-control-allow-origin: *` (CORS-open, safe to hotlink/fetch client-side)
- Served via Cloudflare, `cache-control: public, max-age=31536000` (1yr cache — fine to cache aggressively)

## Gotchas
- **Two generations of API coexist in search results/docs.** Don't follow the old `rijksmuseum.nl/api/en/collection` (`key=...&imgonly=True` style) — it's the deprecated Collection API. Use `data.rijksmuseum.nl/search/collection` instead.
- **No single-call shortcut for the image.** Unlike some museum APIs (e.g. a flat `webImage.url` field), Rijksmuseum's linked-art model requires **3 sequential GETs** (object → VisualItem → DigitalObject) to reach the actual image URL. Budget for that in any pipeline (or cache the chain).
- **No license filter in search params.** `imageAvailable=true` gets you images, not necessarily license — verify CC0/PD per object via the VisualItem's `subject_to` block if you need to be strict (though in practice public-collection paintings/prints are overwhelmingly Public Domain/CC0).
- **Library/archive records excluded** from the Search API (museum objects only).
- **Pagination**: don't hand-build `pageToken` — always follow the exact `next.id` URL returned in the response.
- **Rate limits**: not documented/published for the new API; no auth means no per-key throttling was observed in this test, but be a good citizen (no aggressive parallel hammering).
- **Attribution**: not legally required for CC0/PD, but the museum requests a credit line ("Rijksmuseum") — cheap to add and avoids any ambiguity for CC BY items mixed into broader queries.
- **IIIF host is `iiif.micr.io`** (third-party Micrio infrastructure), not `data.rijksmuseum.nl` itself — don't assume same-origin/rate-limit policy as the main API.

## Sources
- https://data.rijksmuseum.nl/docs/ (API overview)
- https://data.rijksmuseum.nl/docs/search (Search API reference)
- https://data.rijksmuseum.nl/docs/api/collection (old Collection API — marked DEPRECATED)
- https://data.rijksmuseum.nl/docs/iiif/ , /docs/iiif/image , /docs/iiif/presentation (IIIF docs)
- https://data.rijksmuseum.nl/policy/ (licensing/rights policy)
- Live verified via `curl`: `data.rijksmuseum.nl/search/collection`, `id.rijksmuseum.nl/200105887`, `id.rijksmuseum.nl/202105887`, `id.rijksmuseum.nl/5001087555671055286110`, `iiif.micr.io/YAxov/full/max/0/default.jpg`
