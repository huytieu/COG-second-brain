# The Getty — Open-Access Image Recipe (VERIFIED)

## TL;DR
- **Base URL (Linked Art / JSON-LD API):** `https://data.getty.edu/museum/collection/`
- **API key:** NOT required. All endpoints below returned `HTTP 200` with a plain unauthenticated `curl`.
- **License:** Dataset/collection metadata is **CC0 1.0** (confirmed live in every record's `subject_to` "License for Collection Metadata" block, and in the official docs text). Images come from the **Getty Open Content Program** — most are CC0/public domain, but **not all**; each image reference should be checked (see Gotchas).
- **Images:** served via **IIIF Image API** at `https://media.getty.edu/iiif/image/<image-id>/...` — full resolution, no key, `Access-Control-Allow-Origin: *`.
- **Search:** there is **no keyword/full-text REST search endpoint** (the docs explicitly say so — see Gotchas). Discovery is via the public **SPARQL endpoint** `https://data.getty.edu/museum/collection/sparql`, which I ran live and got real results back.

---

## 1. What the API actually is
Official docs: https://data.getty.edu/museum/collection/docs/ (a Nuxt SPA; scraped its raw payload to get the real text since WebFetch truncates it — Bash `curl` worked fine).

- Model: **Linked.Art** (a CIDOC-CRM profile) + **JSON-LD**.
- Entity types: `object`, `place`, `document`, `group`, `person`, `exhibition`, `activity`.
- Record URL pattern: `https://data.getty.edu/museum/collection/<ENTITY_TYPE>/<ENTITY_ID>` — returns JSON-LD directly, no `Accept` header needed.
- Change tracking: ActivityStreams feed at `https://data.getty.edu/museum/collection/activity-stream`.
- Graph queries: public **SPARQL** endpoint + a browser UI at `https://data.getty.edu/museum/collection/sparql-ui`.
- Images: Getty-wide **IIIF** API at `https://media.getty.edu` (Image API 2.1.1 + Presentation API 2.1.1/3).

Docs quote (verbatim, from the rendered page): *"With some exceptions, the data available from this API is made available under [CC0]. Check the Usage Guidelines section... for more details."* and *"We currently don't provide a way to get a list of all of the objects or other entity types in the dataset... We also don't provide a way to download all the data in the dataset."* — i.e. **no bulk list, no keyword search REST endpoint**, by design, confirmed straight from their own docs.

## 2. Key requirement
None. Every call in this recipe (`object` record fetch, SPARQL query, IIIF image fetch) succeeded with plain unauthenticated HTTP GET. No signup, no token, no rate-limit header observed.

## 3. License — precisely
- **Dataset/metadata:** CC0 1.0 Universal, unconditionally, per Getty's own statement and confirmed live in every object record I pulled (`subject_to` → `Right` → `classified_as` → `http://creativecommons.org/publicdomain/zero/1.0/`, display name `"Public Domain"`, description `"No Copyright"`).
- **Images (Exception #1 in the docs):** *"Many of the linked images are part of Getty's Open Content program and can also be used without permission under CC0 — but not all of the images are."* The docs say each image reference should carry its own rights block (`VisualItem` → `subject_to` → `classified_as` with the CC0 URI, or something else if restricted). In practice, on the two live records I sampled, that per-image rights sub-block was not populated (older TMS-migrated records) — so **don't assume every image is CC0 purely from the API response**; cross-check on the object's public page at `getty.edu` (Open Content items show a "Download" button) if you need certainty for a specific artwork, or prefer objects you already know are Open Content (e.g. van Gogh's *Irises*, used below).
- **Written descriptions/biographies (Exception #2):** mixed — some CC BY 4.0, some third-party copyright. Same per-block check pattern (`referred_to_by[].subject_to[].classified_as[].id`).
- Attribution is **not required** but requested/appreciated (no fixed credit-line string was given beyond "provided by the J. Paul Getty Museum").
- Official program description (from `getty.edu/projects/open-content-program`, verified fetch): *"Initiative granting free access to images of public domain artworks in Getty's collections."*

## 4. Search recipe (concrete, step-by-step)

There is no `?q=keyword` REST search. Use the SPARQL endpoint to discover objects that have an image, then pull each object's full record for metadata + rights + all image links.

**Step A — find N objects that have a representation image (SPARQL, GET, JSON by default):**

```
GET https://data.getty.edu/museum/collection/sparql?query=<url-encoded SPARQL>
```

SPARQL body used (real, tested):
```sparql
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
SELECT ?obj ?label ?img WHERE {
  ?obj a crm:E22_Human-Made_Object .
  ?obj rdfs:label ?label .
  ?obj crm:P138i_has_representation ?img .
} LIMIT 5
```
This returns the object's URI, its label, and a ready-to-use IIIF image URL — no follow-up call needed for a quick image grab.

**Step B — get the full record (metadata + rights + every image/IIIF manifest link) for one object:**
```
GET https://data.getty.edu/museum/collection/object/<uuid-from-step-A>
```
Look in the JSON for:
- `representation[].id` → direct JPEG (deprecated field, still live, smaller res)
- `subject_of[]` where `_label` = "IIIF Manifest URL" → full IIIF Presentation manifest (has every canvas/image + real per-canvas dims)
- `subject_to[]` → the rights/license block (check `classified_as[].id` for the CC0 URI)

**Step C — full-resolution image URL (IIIF Image API), from any `image-id` you have:**
```
https://media.getty.edu/iiif/image/<image-id>/full/full/0/default.jpg   # full native resolution
https://media.getty.edu/iiif/image/<image-id>/full/!600,/0/default.jpg  # thumbnail, max 600px, aspect preserved
https://media.getty.edu/iiif/image/<image-id>/<x,y,w,h>/<w,h>/0/default.jpg  # cropped region (used on Getty's own site)
```

**Step D — filter for CC0/public domain with confidence:** either (a) rely on the per-image `subject_to`/`classified_as` block when populated, or (b) pick artworks you can confirm are in the Open Content Program via the human-facing collection page (`getty.edu/art/collection/object/...`), which flags Open Content items with a visible "Download" affordance.

## 5. Verified example URLs

**exampleApiUrl** (SPARQL — real results, confirmed via curl, HTTP 200, default response is already `application/sparql-results+json` even with no Accept header):
```
https://data.getty.edu/museum/collection/sparql?query=PREFIX%20crm%3A%20%3Chttp%3A//www.cidoc-crm.org/cidoc-crm/%3E%0ASELECT%20%3Fobj%20%3Flabel%20%3Fimg%20WHERE%20%7B%0A%20%20%3Fobj%20a%20crm%3AE22_Human-Made_Object%20.%0A%20%20%3Fobj%20rdfs%3Alabel%20%3Flabel%20.%0A%20%20%3Fobj%20crm%3AP138i_has_representation%20%3Fimg%20.%0A%7D%20LIMIT%205
```
Live sample of what it returns (first row):
```json
{"obj":"https://data.getty.edu/museum/collection/object/84eb7a1d-f806-4da9-a0ed-77d6b355df7e",
 "label":"West Front, Looking North (84.XB.950.7.28)",
 "img":"https://media.getty.edu/iiif/image/f45355f5-8ae6-4813-bf7a-dc94997f76f0/full/full/0/default.jpg"}
```

Also a plain record fetch, no query params, well-known Open Content artwork (van Gogh's *Irises*, 90.PA.20):
```
https://data.getty.edu/museum/collection/object/c88b3df0-de91-4f5b-a9ef-7b2b9a6d8abb
```

**exampleImageUrl** (full resolution — verified with `curl -I`: `HTTP/2 200`, `content-type: image/jpeg`, `content-disposition: inline; filename="8c255d80-7382-46db-9fa8-892c0d37247e_9021x7122.jpg"`, `access-control-allow-origin: *`):
```
https://media.getty.edu/iiif/image/8c255d80-7382-46db-9fa8-892c0d37247e/full/full/0/default.jpg
```
(This is the Irises main image, 9021×7122px native.)

## 6. Gotchas
- **No full-text/faceted search REST endpoint, no bulk listing/dump.** Explicitly stated as a current limitation in Getty's own docs ("it's on our roadmap"). SPARQL is the only queryable discovery mechanism from the API itself; the human search UI at `getty.edu/art/collection/search/` is the practical alternative for browsing by keyword and then feeding object IDs back into the JSON API.
- **Per-image rights blocks are inconsistently populated.** The docs describe a `VisualItem.subject_to.classified_as` CC0 marker per image, but live sampled records didn't always carry it — don't blanket-assume every image is CC0 just because the record fetch succeeded; verify against the public object page or stick to artworks you know are Open Content.
- **The `representation` field is marked deprecated** in favor of the `shows` → IIIF Manifest route for full-size images going forward (Getty's own deprecation note: future `representation` images "will be smaller than that currently offered"). The `full/full/0/default.jpg` IIIF Image API URL is the durable way to get max resolution regardless.
- **IIIF sizing syntax:** `/full/full/...` = native size; `/full/!W,/...` = fit within width W preserving aspect (the `!` matters); `/full/W,/...` = force width W; region can be `x,y,w,h` pixels instead of `full` to crop.
- **The `docs/` page is a client-rendered SPA** — plain `WebFetch`/simple scrapers get truncated boilerplate; had to pull the Nuxt `_payload.json` directly to get the real doc text. If automating doc reads again, target that payload endpoint, not the rendered HTML.
- **No observed rate limiting** in this session, but Getty gives no published quota — be a reasonable citizen (this is a small non-profit-run API, not a commercial CDN).
- Attribution not contractually required (CC0) but Getty explicitly asks to be told how you used the data (`MuseumCollections@getty.edu`) and offers a courtesy credit line: "J. Paul Getty Museum".

## Sources
- https://data.getty.edu/museum/collection/docs/ (API docs, scraped via curl on `_payload.json`)
- https://www.getty.edu/projects/open-content-program/ (Open Content Program description)
- https://www.getty.edu/projects/open-data-apis/ (open data/APIs overview)
- Live verified endpoints: `data.getty.edu/museum/collection/object/*`, `data.getty.edu/museum/collection/sparql`, `media.getty.edu/iiif/image/*`
