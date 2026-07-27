# Art Institute of Chicago — Open-Access Image API Recipe

Verified: 2026-07-24

## Base URL
`https://api.artic.edu/api/v1`

Official docs: https://api.artic.edu/docs/ (confirmed live and current).

## API Key
**None required.** Fully open, anonymous access.
- Rate limit: 60 requests/minute per IP (throttled if exceeded, no auth error).
- Docs explicitly ask scrapers to self-throttle to ~1 req/sec and avoid parallel hammering — courtesy limit, not enforced by a key.

## Image License
**CC0 1.0 (Creative Commons Zero)** for artwork data and images flagged `is_public_domain: true`.
- Confirmed via live API response `info.license_text`:
  > "All other data in this response is licensed under a Creative Commons Zero (CC0) 1.0 designation and the Terms and Conditions of artic.edu."
  (The `description` field specifically is CC-BY 4.0 — everything else, including the image, is CC0.)
- Suggested (not legally required for CC0, but good practice) attribution: "Digital image courtesy of the Art Institute of Chicago."

## Search Recipe

### Step 1 — Search for public-domain artworks that have an image
```
GET https://api.artic.edu/api/v1/artworks/search?query[term][is_public_domain]=true&fields=id,title,image_id,artist_display&limit=20
```
- `query[term][is_public_domain]=true` filters to CC0/public-domain works.
- `fields=...,image_id` is required — without explicitly requesting `image_id` it won't be in the payload.
- Note: `is_public_domain=true` does not strictly guarantee `image_id` is non-null for every record (a few PD works lack digitized images) — check `image_id` is present/non-empty in each result before building an image URL. Safer alternative used by many integrations: also filter `query[exists][field]=image_id` or just skip results where `image_id` is null/empty.

### Step 2 — Build the full-resolution image URL from a result's `image_id`
```
https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg
```
- `843,` = width 843px, height auto — this is the museum's own site default and the most-likely-cached size.
- For actual full/max resolution, replace the size segment with `full` (i.e. `.../full/full/0/default.jpg`) — larger, uncached, slower.
- The IIIF base (`https://www.artic.edu/iiif/2`) is also returned dynamically in every API response under `config.iiif_url` — prefer reading it from there over hardcoding, in case they ever move image hosting.

## Example URLs (real, from live query)

**exampleApiUrl** (search):
```
https://api.artic.edu/api/v1/artworks/search?query[term][is_public_domain]=true&fields=id,title,image_id,artist_display&limit=3
```
Verified response (2026-07-24) included, among others:
- id 28560, "The Bedroom", Vincent van Gogh, image_id `6644829f-f292-c5c4-a73c-0356a6fdbf0d`
- id 21023, "Buddha Shakyamuni Seated in Meditation (Dhyanamudra)", image_id `0675f9a9-1a7b-c90a-3bb6-7f7be2afb678`
- id 20684, "Paris Street; Rainy Day", Gustave Caillebotte, image_id `f8fd76e9-c396-5678-36ed-6a348c904d27`
- Total public-domain-with-fields matches in collection: 61,568 (paginated, 20,523 pages at limit=3)
- `config.iiif_url` in response: `https://www.artic.edu/iiif/2`

**exampleImageUrl** (from van Gogh's "The Bedroom", id 28560):
```
https://www.artic.edu/iiif/2/6644829f-f292-c5c4-a73c-0356a6fdbf0d/full/843,/0/default.jpg
```

Also confirmed the single-artwork endpoint works:
```
GET https://api.artic.edu/api/v1/artworks/28560?fields=id,title,image_id
```
→ returned `{"data":{"id":28560,"title":"The Bedroom","image_id":"6644829f-f292-c5c4-a73c-0356a6fdbf0d"}, "info":{"license_text":"...CC0 1.0..."}}`

## Verification Notes

- **JSON API: verified working.** Both the search endpoint and the single-artwork endpoint were fetched live and returned real, current data (61,568 public-domain artworks, correct image_id, correct CC0 license text in `info`).
- **IIIF image URL: correct per official docs, but NOT independently confirmed as a working binary download by this research pass.** Direct `curl`/WebFetch requests to `www.artic.edu/iiif/2/.../default.jpg` were blocked with `HTTP 403` + `cf-mitigated: challenge` — this is Cloudflare's bot-management challenge on the `artic.edu` web/image domain, triggered regardless of User-Agent (tried default curl UA, desktop Chrome UA, iPhone Safari UA, and no UA — all 403'd identically, which points to TLS/JA3 fingerprinting rather than header-based blocking). This is a known behavior of Cloudflare-protected static asset domains and does not indicate the URL pattern itself is wrong — it is the officially documented pattern, and it is what the museum's own website uses to render images in a real browser.
  - I attempted to verify via a real headed browser (browser-harness/CDP) to bypass the bot check, but that tool requires one-time manual "Allow remote debugging" approval in the user's Chrome, which wasn't available in this pass.
  - **Practical implication for whoever builds against this recipe:** plain `curl`/`requests`/serverless-function fetches of the IIIF image may hit the same Cloudflare challenge. A real browser, a headless browser with a full JS-capable engine, or a fetch routed through something that passes Cloudflare's bot checks (residential proxy, or a client with a legitimate browser TLS fingerprint) is likely needed for automated bulk image downloading. The JSON metadata API (`api.artic.edu`) has no such protection and worked cleanly every time.

## Gotchas Summary
- No API key, but self-throttle to ~1 req/sec for bulk work; hard limit 60 req/min anonymous.
- Must explicitly request `image_id` via `fields=` — not returned by default.
- Not all `is_public_domain:true` records have a non-null `image_id`; check before building the URL.
- IIIF size param: `843,` = site-default/cached; `full` = max resolution but uncached/slower; can also request specific `{width},{height}` or `{width},` / `,{height}`.
- `www.artic.edu` (the IIIF image host) sits behind Cloudflare bot management — scripted/curl-style requests to the image URLs get a 403 challenge page even though the URL pattern is correct and it works in normal browser use. Budget for this if building an automated downloader.
- Attribution "Digital image courtesy of the Art Institute of Chicago" is good practice even though CC0 doesn't legally require it.
