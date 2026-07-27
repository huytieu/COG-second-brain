# The Metropolitan Museum of Art — Open Access Image Recipe

Status: **VERIFIED** (both the search endpoint and the resulting image URL were fetched live and returned real data / HTTP 200).

## Base URL
`https://collectionapi.metmuseum.org/public/collection/v1/`

Docs: https://metmuseum.github.io/ (official, GitHub Pages)
Initiative overview: https://www.metmuseum.org/hubs/open-access
Repo: https://github.com/metmuseum/openaccess

## API key
**None required.** The docs state explicitly: "At this time, we do not require API users to register or obtain an API key to use the service."
Rate limit: **80 requests/second** (documented; be polite and add a small delay/backoff for bulk jobs anyway). Contact for questions: `openaccess@metmuseum.org`.

## License
**CC0 (Creative Commons Zero)** for objects flagged `isPublicDomain: true` — The Met has waived all copyright and related/neighboring rights on this subset of the dataset (both the metadata and the associated images). No attribution is legally required, though crediting "The Metropolitan Museum of Art" is good practice / house style.

Caveat: not every object in the collection is CC0 — only ones where `isPublicDomain` is `true`. Objects where it's `false` still have metadata returned by the API but the image (if any) is NOT open-licensed for reuse — always check the flag per-object, don't assume every API result is free to use.

## Endpoints used in this recipe

| Endpoint | Purpose |
|---|---|
| `GET /search?...` | Search for object IDs matching filters (query term, `hasImages`, `isPublicDomain`, department, date range, etc.) |
| `GET /objects/{objectID}` | Full record for one object: title, artist, `isPublicDomain`, `primaryImage`, `primaryImageSmall`, rights fields |
| `GET /departments` | List of department IDs/names, for scoping search |

Confirmed search params (from live docs): `q`, `isHighlight`, `title`, `tags`, `departmentId`, `isOnView`, `artistOrCulture`, `medium`, `hasImages`, `geoLocation`, `dateBegin` + `dateEnd` (must be given together). **`isPublicDomain` is also a live, working param** even though it isn't prominently listed in every doc rendering — confirmed by direct test below.

## Step-by-step recipe

1. **Search** for public-domain artworks with images:
   ```
   GET https://collectionapi.metmuseum.org/public/collection/v1/search?q=<term>&hasImages=true&isPublicDomain=true
   ```
   Response: `{"total": N, "objectIDs": [id1, id2, ...]}`. If `objectIDs` is null, no matches — try a broader `q` or drop a filter.

2. **Fetch one object's full record:**
   ```
   GET https://collectionapi.metmuseum.org/public/collection/v1/objects/{objectID}
   ```
   Check `isPublicDomain === true` before reuse (belt-and-suspenders even though the search already filtered on it — the object may have been re-flagged since indexing).

3. **Grab the image URL directly from the object JSON** — no extra IIIF/image-service call needed:
   - `primaryImage` — full original resolution JPEG (can be very large, several MB, up to ~8MB+ observed).
   - `primaryImageSmall` — "web-large" size, smaller JPEG, good default for web use.
   - `additionalImages` — array of extra full-res image URLs if the object has more than one photographed view.

   No IIIF Image API / sizing-parameter syntax is involved — Met just serves static JPEGs at fixed pre-rendered sizes (`original`, `web-large` in the URL path), not a dynamic IIIF resizer.

## Example URLs (live-tested)

**Search:**
```
https://collectionapi.metmuseum.org/public/collection/v1/search?q=sunflowers&hasImages=true&isPublicDomain=true
```
Verified live: returned `"total": 40` and a real `objectIDs` array (e.g. 544320, 310453, 200668, 437261, 824771, 36225, ... 436535 among later results is a different van Gogh but 436535 below was pulled independently for the full example).

**Object record:**
```
https://collectionapi.metmuseum.org/public/collection/v1/objects/436535
```
Verified live via curl — returns real JSON:
- `objectID`: 436535
- `title`: "Wheat Field with Cypresses"
- `artistDisplayName`: Vincent van Gogh
- `department`: European Paintings
- `isPublicDomain`: `true`
- `primaryImage`: `https://images.metmuseum.org/CRDImages/ep/original/DP-42549-001.jpg`
- `primaryImageSmall`: `https://images.metmuseum.org/CRDImages/ep/web-large/DP-42549-001.jpg`

**Full-res image URL (verified):**
```
https://images.metmuseum.org/CRDImages/ep/original/DP-42549-001.jpg
```
`curl -sI` on this URL returned `HTTP/2 200`, `content-type: image/jpeg`, `content-length: 8291194` (~8.3MB) — confirmed real, downloadable, full-resolution JPEG.

## Gotchas

- **Rate limit 80 req/sec** per the docs — fine for interactive/scripted use, but throttle bulk crawls (e.g. iterate all `/objects`) to be a good citizen; the server is fronted by Imperva/Incapsula (visible in response headers) which may rate-limit/challenge aggressive traffic beyond the documented cap.
- **No CORS problem** — `access-control-allow-origin: *` is set on the image CDN (`images.metmuseum.org`), so these URLs are directly usable from browser JS (e.g. `<img>` tags, canvas/fetch) without a proxy.
- **`objects` bulk listing endpoint** (`/objects?metadataDate=...&departmentIds=...`) returns *all* object IDs for the filter, not just public-domain/has-image ones — you still need to check `isPublicDomain` + `primaryImage` (non-empty) per object, or better, use `/search?hasImages=true&isPublicDomain=true` up front to pre-filter.
- **`primaryImage` can be empty string** even for public-domain objects that haven't been photographed — always check `primaryImage !== ""` (or non-null) before using.
- **No IIIF sizing params** — unlike some museum APIs (e.g. Smithsonian, some Europeana sources), the Met does not expose a dynamic image resize API. You get exactly two fixed sizes baked into the URL (`original`, `web-large`) plus optional `additionalImages`. If you need a specific pixel size, resize client-side after download.
- **Attribution not legally required (CC0)** but recommended: "Image courtesy of The Metropolitan Museum of Art" / link back to the object's page (`https://www.metmuseum.org/art/collection/search/{objectID}`).
- **`rightsAndReproduction` field is often blank** even on legitimate public-domain records — don't treat an empty rights field as a red flag; `isPublicDomain: true` is the authoritative signal.
