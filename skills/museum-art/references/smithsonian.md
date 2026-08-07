# Smithsonian Open Access API — Verified Recipe

Status: **VERIFIED** (live queries executed 2026-07-24, all succeeded with real data and a resolvable full-res image).

## Base URL

```
https://api.si.edu/openaccess/api/v1.0/
```

Key endpoints:
- `search` — full-text/field search across ~7.5M+ records (Solr-backed)
- `content/{id}` — fetch one record by its `id` (from a search result)
- `stats` — collection unit counts
- `metadata/v2.0/terms/{category}` — controlled-vocabulary term lists

All requests go through **api.data.gov** as the API gateway (hostname is `api.si.edu` but auth/quota is api.data.gov's).

## API Key

**Required: yes**, via the query param `api_key`.

- Free signup: https://api.data.gov/signup/ (name + email, key emailed immediately — standard api.data.gov self-serve flow, no approval wait, no cost).
- For quick testing without signing up, the shared `DEMO_KEY` works (used below) but is rate-limited much harder.
- Rate limits: `DEMO_KEY` = 30 requests/hour/IP; a registered personal key = 1,000 requests/hour. (Per api.data.gov standard tiers; Smithsonian doesn't publish a separate limit.)

## License

**CC0 1.0 Universal (public domain dedication)** for everything tagged Open Access. No attribution legally required, though crediting "Smithsonian Institution" is good practice.

Two places the CC0 flag shows up in the JSON, both worth checking:
- `content.descriptiveNonRepeating.metadata_usage.access` = `"CC0"` (record-level)
- `content.descriptiveNonRepeating.online_media.media[].usage.access` = `"CC0"` (per-image-level — check this one, since a record can be CC0 but an individual attached media item can carry different rights)

Not every one of the Smithsonian's ~157M total records is Open Access — only records with `metadata_usage.access: "CC0"` are released for unrestricted reuse. Filtering on this field (or the `online_media_type` field, see below) is what separates "any record" from "downloadable public-domain asset."

## Search Recipe

### (a) Search for public-domain artworks that have images

```
GET https://api.si.edu/openaccess/api/v1.0/search
    ?q=<TERMS> AND online_media_type:Images AND unit_code:<UNIT>
    &rows=10
    &start=0
    &api_key=<YOUR_KEY>
```

- `online_media_type:Images` — restricts to records that have at least one attached image-type media object. (This is the field that matters; do **not** rely on adding `cc0:CC0` alone — that clause was accepted by the query parser without error but did not reliably filter, see Gotchas.)
- `unit_code:<UNIT>` — scope to one museum, e.g. `SAAM` (Smithsonian American Art Museum), `NPG` (National Portrait Gallery), `FSG` (Freer|Sackler), `CHNDM` (Cooper Hewitt), `NMNHBIRDS`, etc. Omit for cross-collection search.
- Free-text `q=` terms combine with `AND`/`OR` Solr syntax, e.g. `q=sunflower AND online_media_type:Images`.
- **After getting results, always check `content.descriptiveNonRepeating.online_media.media[].usage.access == "CC0"`** on each hit before treating its image as free-to-use — some non-Open-Access records still surface in a broad search.

### (b) Get a full-resolution downloadable image URL from a result

For each hit, walk: `content.descriptiveNonRepeating.online_media.media[]` — an array (a record can have multiple images). Each media object has:

- `media.usage.access` — CC0 check (per above)
- `media.content` — an IDS delivery-service URL, e.g. `https://ids.si.edu/ids/deliveryService?id=<idsId>` — **calling this with no size param returns the full-resolution original** (verified: 1.8MB JPEG).
- `media.resources[]` — explicit named download links when the record has them pre-generated: `"High-resolution TIFF"`, `"High-resolution JPEG"` (with `width`/`height` in pixels), `"Screen Image"`, `"Thumbnail Image"`. Not every record has the high-res TIFF/JPEG resources array populated — some only expose `Screen Image`/`Thumbnail Image`, in which case use the `deliveryService` content URL directly for full res.

**IIIF-style resizing**: append `&max=<pixels>` to the `deliveryService` URL to cap the longest edge, e.g. `&max=2000` (verified: dropped a 1.8MB image to 828KB at max=2000). Omit `max` entirely for the original full-size file.

## Example URLs (both verified live, 2026-07-24)

**exampleApiUrl** (search — Smithsonian American Art Museum CC0 images):
```
https://api.si.edu/openaccess/api/v1.0/search?q=cc0:CC0%20AND%20online_media_type:Images%20AND%20unit_code:SAAM&api_key=DEMO_KEY&rows=5
```
Verified response: HTTP 200, `rowCount: 12999`, returned real SAAM artwork records (e.g. "A Chiefe Herowan," object id `saam_1985.66.403_410`, record link https://americanart.si.edu/collections/search/artwork/?id=18695) each carrying `metadata_usage.access: "CC0"` and an `online_media.media[]` array.

**exampleImageUrl** (full-resolution, from a National Museum of Natural History Birds specimen record returned by the broader query `q=cc0:CC0 AND online_media_type:Images`):
```
https://ids.si.edu/ids/download?id=NMNH-vol.090_449776-449800.jpg
```
Verified: `curl -sL` → HTTP 200, `image/jpeg`, 23,659,074 bytes, resolves (307 redirect) to `https://smithsonian-open-access.s3-us-west-2.amazonaws.com/media/nmnh/NMNH-vol.090_449776-449800.jpg`. `usage.access: "CC0"` on the media object.

Alternate example (SAAM artwork, screen-res since no TIFF resource present, still CC0):
```
https://ids.si.edu/ids/deliveryService?id=SAAM-1985.66.403410_1
```
Verified: HTTP 200, `image/jpeg`, 1,833,356 bytes.

## Gotchas

- **`cc0:CC0` as a query clause is not a reliable filter.** It doesn't error, but adding it to a query did not change result counts predictably in testing — always independently verify `metadata_usage.access` / `media.usage.access` == `"CC0"` in the returned JSON rather than trusting the query string to have filtered correctly.
- **`online_media_type:Images` also isn't a guaranteed hard filter on every unit.** Several paintings-category test queries returned zero records with a populated `online_media` object despite the filter term, while bird/NMNH and SAAM units reliably returned populated media. Best practice: request extra rows and skip any result whose `descriptiveNonRepeating` lacks an `online_media` key.
- **Rate limits are api.data.gov's, not Smithsonian's**: DEMO_KEY = 30 req/hr/IP (easy to exhaust in a scripting loop — get a real key for anything beyond a handful of test calls).
- **IDS delivery URLs sometimes 307-redirect to S3** (`smithsonian-open-access.s3-us-west-2.amazonaws.com`) — follow redirects (`curl -L`) or your HTTP client's default redirect-follow.
- **Attribution not legally required** under CC0, but Smithsonian's own guidance asks for a credit line where practical (e.g. "Smithsonian American Art Museum").
- **Two rights fields to reconcile**: record-level `metadata_usage.access` and per-media `media.usage.access` can theoretically diverge (a CC0 record could contain a rights-restricted third-party image) — always check the media-level flag before using a specific image.
- Full docs referenced (not independently fetchable due to JS-rendered pages, but corroborated via GitHub/Postman/search): https://www.si.edu/openaccess/devfaq, https://edan.si.edu/openaccess/docs/, https://github.com/Smithsonian/OpenAccess

## Sources
- https://www.si.edu/openaccess/faq
- https://edan.si.edu/openaccess/docs/
- https://github.com/Smithsonian/OpenAccess
- https://github.com/Smithsonian/smithsonian-openaccess (Python client)
- https://api.data.gov/signup/
- Live API responses captured via curl, 2026-07-24 (this session)
