# Public-Domain Art Sourcing Cheat-Sheet

Consolidated from 8 verified museum-API recipes (2026-07-24). For an agent sourcing hi-res public-domain artwork for blog heroes, decks, social cards, essay figures.

## Quick-pick table (ranked: fastest/most reliable first)

| Rank | Museum | Keyless? | License | How to get a hi-res PD image (one line) | Best for |
|---|---|---|---|---|---|
| 1 | **Met (Metropolitan Museum)** | Yes, no key | CC0 (per-object flag) | `GET /search?q=X&hasImages=true&isPublicDomain=true` → `/objects/{id}` → read `primaryImage` (static JPEG, no IIIF hop) | Broadest single source — Western painting, Asian art, Egyptian antiquities, American art |
| 2 | **Cleveland Museum of Art** | Yes, no key | CC0 | `GET /api/artworks/?cc0=1&has_image=1` → read `images.print.url` (3400px JPEG) or `images.full.url` (archival TIFF) — no hop | Broad European/American painting + Asian art; archival-res TIFFs available |
| 3 | **SMK (National Gallery of Denmark)** | Yes, no key | Public Domain Mark (functionally CC0) | `GET /art/search?keys=*&filters=[public_domain:true]&filters=[has_image:true]` (repeat `filters=`, don't concatenate!) → read `image_native` directly | Danish/Nordic + European painting, decorative arts |
| 4 | **Rijksmuseum** | Yes, no key | CC0/PD (mostly), check per-object | `GET /search/collection?type=painting&imageAvailable=true` → walk object → VisualItem → DigitalObject → `access_point[0].id` is the ready IIIF URL (3 sequential GETs) | Dutch/Flemish masters, prints, decorative arts |
| 5 | **NGA (National Gallery of Art, DC)** | Yes, no key | CC0 (dataset); per-image `openaccess` flag gates rights | Download `published_images.csv` from GitHub, filter `openaccess=1`, then `GET https://api.nga.gov/iiif/{uuid}/full/full/0/default.jpg` | American + European painting/sculpture; best for bulk/offline querying (no live search API) |
| 6 | **Art Institute of Chicago** | Yes, no key | CC0 | `GET /artworks/search?query[term][is_public_domain]=true&fields=...,image_id` → build `https://www.artic.edu/iiif/2/{image_id}/full/full/0/default.jpg` — **but** the image host (`www.artic.edu`) 403s scripted/curl fetches (Cloudflare bot challenge); JSON metadata API is fine, image download needs a real/headless browser | Impressionism, European + American painting, Buddhist/Asian art |
| 7 | **Getty** | Yes, no key | CC0 (dataset); images "mostly" CC0 but per-image rights block inconsistently populated — verify before trusting | No keyword search exists — use SPARQL (`?obj crm:P138i_has_representation ?img`) which returns a ready-to-use IIIF image URL directly in the same query | European painting, photography, antiquities, decorative arts |
| 8 | **Smithsonian** | **No** — needs `api_key` (free instant signup, or shared `DEMO_KEY` at 30 req/hr) | CC0 | `GET /search?q=X AND online_media_type:Images&api_key=KEY` → `media[].content` (IDS deliveryService URL); check `media[].usage.access=="CC0"` per-image | Extremely broad: American art (SAAM), portraiture (NPG), Asian art (Freer\|Sackler), design (Cooper Hewitt), natural history/specimens |

## The 2-3 best keyless APIs to reach for FIRST

1. **The Met Collection API** — single JSON call, no IIIF/linked-data hop, `primaryImage` field is a directly-downloadable full-res JPEG, CC0 is a simple boolean flag, 80 req/sec, huge and diverse collection. Best all-around default.
2. **Cleveland Museum of Art Open Access API** — same one-hop simplicity as the Met, plus it's the only one of the 8 offering an archival-resolution TIFF tier (`images.full`) alongside a 3400px print JPEG, no rate limit trouble observed.
3. **SMK (Denmark) Art API** — also one-hop (`image_native` ready in the search result, no chain), broad European painting/decorative holdings. Caveat: the `filters=` param MUST be repeated (one bracket each), not concatenated into one string, or the AND silently fails.

Honorable mention: if the ask is specifically Dutch/Flemish masters or decorative arts, Rijksmuseum is worth the extra 2 hops. If it's European antiquities/photography and a keyword isn't essential, Getty's SPARQL trick returns an image URL in one query.

## Attribution / licensing notes

- **True CC0 (no legal attribution required, safe to treat as public domain outright):** Met, Cleveland, Art Institute of Chicago, NGA (dataset-level; images gated by per-image `openaccess` flag), Smithsonian.
- **"Public Domain Mark" / open-access-but-not-technically-CC0 (functionally free to use, museum requests but does not require a credit line):** Rijksmuseum (mixed — some items are CC BY and DO require attribution, always check the object's own rights block), SMK (Public Domain Mark 1.0 — functionally equivalent to CC0 for reuse, credit "SMK" requested).
- **Mixed/needs per-image verification — do not blanket-trust the collection-level CC0 claim:** Getty (dataset is CC0 but per-image `VisualItem.subject_to` rights block is inconsistently populated on older records — cross-check the object's public page, which flags true Open Content items with a "Download" button, before using an image commercially), NGA (per-image `openaccess=0` rows are NOT open — resolution-capped and rights-restricted), Smithsonian (record-level `metadata_usage.access` and per-media `media.usage.access` can theoretically diverge — check the media-level flag, not just the record flag).
- **Good practice everywhere even when not legally required:** a short credit line ("Digital image courtesy of [Museum]") costs nothing and avoids ambiguity, especially for mixed-license collections (Rijksmuseum, Getty) where a CC BY item could slip through a broad query.
- **Practical rule for the agent:** when a museum's API exposes a rights/license field, filter AND spot-check it per image before shipping — never assume "the collection is open access" implies "this specific image is." The 3 collections where this bites hardest are Getty, Rijksmuseum, and NGA/Smithsonian's per-image flags.

## Gaps — major keyless/near-keyless PD art sources the 8 museums miss

None of the 8 notes covered these; an agent building a general-purpose "find me a public-domain artwork" tool should know about them:

- **Wikimedia Commons API** — `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=<term>&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata` (fully keyless). Aggregates PD/CC-licensed images from dozens of museums already normalized into one schema; `extmetadata.LicenseShortName` gives the license per file. Best single fallback when a specific museum's own API comes up empty — search `Category:Paintings_by_...` or a direct `File:` page via `Special:FilePath/{filename}` for the raw image bytes.
- **Europeana API** — `https://api.europeana.eu/record/v2/search.json?wskey=<KEY>&query=<term>` — aggregates 50M+ items from thousands of European cultural institutions in one schema; **requires a free API key** (instant self-serve signup, not fully keyless like the others).
- **Harvard Art Museums API** — `https://api.harvardartmuseums.org/object?apikey=<KEY>&q=<term>` — **requires a free key** (instant signup). Strong for teaching-collection-style Western art and object photography.
- **Yale (LUX / Yale Center for British Art)** — `https://lux.collections.yale.edu/api/search/...` (Linked Art model, similar shape to Getty's) — keyless, aggregates Yale University Art Gallery + Yale Center for British Art + Beinecke; strong British art and rare books.
- **Paris Musées (Paris city museums collections)** — open-data portal at `https://www.parismuseescollections.paris.fr/en/collections` with a CC0 bulk dataset also mirrored on Paris's open-data platform (`opendata.paris.fr`) — keyless, French painting/decorative arts, explicit CC0.
- **NYPL Digital Collections API** — `https://api.repository.library.nyc/...` — **requires a free key** (instant signup via `api.repository.library.nyc/register`). Huge trove of digitized public-domain prints, maps, photographs, illustrations (not "museum paintings" but excellent for editorial/essay figures).
- **Wellcome Collection API** — `https://api.wellcomecollection.org/catalogue/v2/works?query=<term>` — keyless, no key needed. CC0/PD medical, historical, and scientific imagery — a good niche source for essay figures on health/science topics that the 8 art museums won't have.
- **Internet Archive** — `https://archive.org/advancedsearch.php?q=<term>&fl[]=identifier&output=json` — keyless. Not a museum but a deep well of PD book illustrations, historical photographs, and scanned ephemera; useful when the need is "old illustration/engraving" rather than "fine-art painting."
- **DPLA (Digital Public Library of America)** — `https://api.dp.la/v2/items?q=<term>&api_key=<KEY>` — **requires a free key**. Aggregates US libraries/archives/museums (including several of the 8 above) into one federated search — useful as a cross-collection fallback once a key is obtained.

**Practical recommendation for the agent:** try Met → Cleveland → SMK first (keyless, one-hop). If nothing fits the brief, fall back to Wikimedia Commons (keyless aggregator across everything). If the visual need is more "historical illustration/engraving" than "museum painting," go straight to Internet Archive or Wikimedia Commons instead of the fine-art APIs.
