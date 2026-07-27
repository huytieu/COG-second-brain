# SMK (National Gallery of Denmark) — Open Access Image Recipe

Status: **VERIFIED working** (2026-07-24, live curl + WebFetch checks against the real API).

## Base URL

```
https://api.smk.dk/api/v1
```

Official docs (Swagger UI, embedded OpenAPI 3.0.3 spec — page itself is JS-rendered but the
spec JSON is inlined in `swagger-ui-init.js`):
- Human docs: https://api.smk.dk/api/v1/docs/
- Article: https://www.smk.dk/en/article/smk-api/
- Contact: smkapi@smk.dk

## API key

**None needed.** Confirmed empirically — 8+ unauthenticated GET requests in a row all returned
HTTP 200 with no `Authorization` header, no key, no `X-Api-Key`. The API is explicitly described
as "free to use." No signup, no throttling encountered in this test burst.

## License

Individual objects carry a `rights` field. For public-domain works it is:

```
"rights": "https://creativecommons.org/publicdomain/mark/1.0/"
```

i.e. **Public Domain Mark 1.0** (SMK calls it "Public Domain" on their license page,
https://www.smk.dk/en/license/public-domain/ — not literally the CC0 waiver, but functionally
equivalent: no copyright restrictions, reuse/modify/redistribute freely, attribution not
mandatory but good practice — credit "SMK / Statens Museum for Kunst"). Filter for it with the
`public_domain:true` facet filter (below) rather than parsing `rights` per item.

## The gotcha the starting hint got wrong

The hinted query shape `filters=[public_domain:true][has_image:true]` (both brackets
concatenated into ONE `filters=` value) is **accepted by the server (200 OK) but silently wrong**
— it does not AND the two conditions. Verified by comparing `found` counts:

| Query | `found` |
|---|---|
| `filters=[public_domain:true]` only | 150,301 |
| `filters=[has_image:true]` only | 54,393 |
| `filters=[public_domain:true][has_image:true]` (single concatenated value) | 150,301 (wrong — ignored the second bracket) |
| `filters=[public_domain:true]&filters=[has_image:true]` (**repeated param, one bracket each**) | **39,479** (correct intersection) |

**Rule: pass `filters` as a repeated query parameter, one `[field:value]` bracket per
occurrence, not concatenated.**

## Recipe

### (a) Search for public-domain artworks that have an image

```
GET https://api.smk.dk/api/v1/art/search
    ?keys=*
    &filters=[public_domain:true]
    &filters=[has_image:true]
    &offset=0
    &rows=10
```

URL-encoded (paste-able):
```
https://api.smk.dk/api/v1/art/search?keys=*&filters=%5Bpublic_domain:true%5D&filters=%5Bhas_image:true%5D&offset=0&rows=10
```

Other useful params (from the OpenAPI spec, `/art/search` GET):
- `keys` (required) — search keywords; `*` = match all.
- `rows` — page size, max 2000, default 10.
- `offset` — pagination start.
- `fields` — restrict returned fields (array param).
- `sort` — sort field, default relevance.
- Other facet filters follow the same `[field:value]` bracket syntax, e.g. `[has_3d_file:true]`,
  `[on_display:true]`, `[collection:...]`.

### (b) Get a full-resolution downloadable image from a result item

Each item in `items[]` already carries everything needed — no second API call required:

- `image_native` — direct downloadable full-res JPEG URL (this is the one to use for
  "download the image").
- `image_thumbnail` — pre-sized ~1024px-wide JPEG via the IIIF thumb server.
- `image_iiif_id` / `image_iiif_info` — the raw IIIF Image API base + `info.json`, for
  requesting any custom size/region/rotation via standard IIIF syntax
  `{iiif_id}/{region}/{size}/{rotation}/{quality}.{format}`.
- `image_width` / `image_height` / `image_size` — native pixel dimensions and byte size.

Example from a verified live item (object KKS5261, "Augustus og den tiburtinske sibylle"):
```json
{
  "id": "1170000001_object",
  "object_number": "KKS5261",
  "public_domain": true,
  "rights": "https://creativecommons.org/publicdomain/mark/1.0/",
  "image_width": 4992,
  "image_height": 6287,
  "image_size": 32476791,
  "image_thumbnail": "https://iip-thumb.smk.dk/iiif/jp2/qz20sx771_kks5261.tif.jp2/full/!1024,/0/default.jpg",
  "image_native": "https://api.smk.dk/api/v1/download/W3siaW1nX3VybCI6Imh0dHBzOi8vaWlwLnNtay5kay9paWlmL2pwMi9xejIwc3g3NzFfa2tzNTI2MS50aWYuanAyL2Z1bGwvZnVsbC8wL25hdGl2ZS5qcGciLCJwdWJsaWNfZG9tYWluIjp0cnVlLCJvYmplY3RfbnVtYmVyIjoiS0tTNTI2MSIsIm51bSI6IiJ9XQ==/KKS5261.jpg",
  "image_iiif_id": "https://iip.smk.dk/iiif/jp2/qz20sx771_kks5261.tif.jp2",
  "image_iiif_info": "https://iip.smk.dk/iiif/jp2/qz20sx771_kks5261.tif.jp2/info.json"
}
```

To fetch a specific single object later by its `object_number`, use:
```
GET https://api.smk.dk/api/v1/art?object_number=KKS5261
```
(the `object_url` field on every item is pre-built this way).

## Example URLs (both verified live, 2026-07-24)

**exampleApiUrl** (search query — returns JSON, confirmed 200 with 39,479 total matches):
```
https://api.smk.dk/api/v1/art/search?keys=*&filters=%5Bpublic_domain:true%5D&filters=%5Bhas_image:true%5D&offset=0&rows=2
```

**exampleImageUrl** (full-resolution downloadable JPEG, confirmed HTTP 200, `Content-Type:
image/jpeg`, `Content-Length: 24043853` bytes, 4992x6287 px):
```
https://api.smk.dk/api/v1/download/W3siaW1nX3VybCI6Imh0dHBzOi8vaWlwLnNtay5kay9paWlmL2pwMi9xejIwc3g3NzFfa2tzNTI2MS50aWYuanAyL2Z1bGwvZnVsbC8wL25hdGl2ZS5qcGciLCJwdWJsaWNfZG9tYWluIjp0cnVlLCJvYmplY3RfbnVtYmVyIjoiS0tTNTI2MSIsIm51bSI6IiJ9XQ==/KKS5261.jpg
```

Alternative (IIIF-native, resize on the fly, also confirmed 200):
```
https://iip.smk.dk/iiif/jp2/qz20sx771_kks5261.tif.jp2/full/1024,/0/default.jpg
```

## Verification log

- `curl -sI` on `image_native` URL → `HTTP/1.1 200 OK`, `Content-Type: image/jpeg`,
  `Content-Length: 24043853`, `Access-Control-Allow-Origin: *`.
- `curl -s` on `art/search` example URL → HTTP 200, valid JSON, `found: 39479`,
  `items[0].public_domain == true`, `items[0].has_image` implied by presence of `image_native`.
- `curl -sI` on IIIF `info.json` → HTTP 200, valid IIIF Image API 2.0 manifest with `sizes` array.
- Burst of 5 sequential unauthenticated requests → all 200, no throttling/key errors observed.

## Gotchas

1. **`filters` must be repeated, not concatenated** — see table above. This is the single
   biggest trap; the naive single-string form silently returns the wrong (larger, un-intersected)
   result set instead of erroring.
2. **`keys` is a required param** even for "give me everything" — use `keys=*`.
3. `image_hires` field exists in the schema but was `None` on the sampled item; `image_native`
   is the reliable full-res download link, not `image_hires`.
4. `image_native` URLs are single-use-looking base64-ish opaque tokens embedding the source IIIF
   path + object metadata — they are stable (not time-limited signed URLs) but don't try to
   hand-construct them; always take them verbatim from the API response.
5. IIIF server (`iip.smk.dk`) supports standard region/size/rotation/quality params if you want
   sizes other than native — `sizes` in `info.json` lists SMK's precomputed steps (156px up to
   2496px wide) but arbitrary `w,` / `w,h` sizes also work via `full/1024,/0/default.jpg` syntax.
6. No published rate limit was hit in testing; be a good citizen (the API is free, maintained by
   a small team — contact smkapi@smk.dk for anything at bulk-harvest scale).
7. `rights` is per-item — not every item with `public_domain:true` necessarily has an identical
   `rights` URL, but in the sample it was the CC Public Domain Mark 1.0 link.
8. `object_number` (e.g. `KKS5261`) is the human-facing ID; `id` (e.g. `1170000001_object`) is
   internal. Use `object_number` for the `/art?object_number=` single-item lookup.
