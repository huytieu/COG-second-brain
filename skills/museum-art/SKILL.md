---
name: museum-art
description: Source authentic, high-res PUBLIC-DOMAIN artwork from museum open-access APIs (Met, Cleveland, SMK, Rijksmuseum, NGA, Art Institute of Chicago, Getty, Smithsonian) instead of AI-generated or generic-stock imagery. The default move whenever a visual needs an aesthetic, credible image (blog heroes, decks, social cards, essay/spec figures). Verified keyless recipes + licensing rules inside.
---

# museum-art: Public-Domain Artwork for Visuals

> Standing rule (adopted 2026-07-24, from Eric Li's post on museum open-access): **whenever a visual needs a real image with aesthetic weight, source public-domain museum artwork first** - over AI-generated imagery and over generic stock. Curated, historically significant art reads as credible and sophisticated; AI-gen reads as slop. This stacks with, and reinforces, the `no-ai-slop` skill and your house image style. It does NOT replace the generative `editorial-illustrations` skill (that owns claim-driven diagrams/figures) or your house chart style - use museum art for photographic/hero/decorative/mood imagery, generative figures for data and concept diagrams.

## When to reach for this
- Blog post hero images, section breaks, mood imagery (the blog-publish image step).
- Deck/slide backgrounds and section dividers, social cards, essay figures, spec cover art.
- Any time the instinct is "generate an image" for something decorative or evocative. Stop and pull a real painting instead.
- NOT for: product screenshots, UI mockups, data charts, logos, or claim-driven explanatory diagrams (those are editorial-illustrations / real captures).

## Decision: which source
1. **Met -> Cleveland -> SMK first.** All keyless, one JSON hop, CC0/PD, broad collections. Fastest path to a hi-res image.
2. **Need Dutch/Flemish masters or decorative arts?** Rijksmuseum (keyless, 3 hops).
3. **Need European antiquities/photography and keyword isn't essential?** Getty (keyless, SPARQL).
4. **Nothing fits, or you want a cross-museum search?** Wikimedia Commons API (keyless aggregator, normalized license metadata) is the best general fallback.
5. **"Historical illustration/engraving/old photo" rather than fine-art painting?** Go straight to Internet Archive or Wikimedia Commons.
6. **Science/health/medical essay figure?** Wellcome Collection (keyless, CC0/PD).

## How to fetch in THIS environment
- Use **WebFetch** to hit the JSON search endpoint, then WebFetch/download the returned image URL. These APIs are server-side reachable; no browser needed.
- **Exception - Art Institute of Chicago images:** the JSON API (`api.artic.edu`) is fine, but the image host `www.artic.edu/iiif/...` 403s scripted/curl fetches via a Cloudflare bot challenge. Use the JSON metadata from AIC, but download the actual image through a real/headless browser (browser-harness) or prefer a different museum for the image bytes.
- Always **filter for public domain in the query AND spot-check the per-image license flag** before shipping (see Licensing).

## Freshness over caching (mandatory)
**Fetch fresh per need. Do NOT build a reusable local pool of downloaded images to draw from.** A small cached set gets reused everywhere and becomes the new "same stock photo on every post" - sameness is a form of slop, and the variety of a huge open collection is the entire point. Fetching is keyless and sub-second, so there is no cost reason to cache pixels.
- **Cache recipes/metadata, not images** - that is what this skill's `references/` already are.
- **Commit an image only into the specific artifact that uses it** (a post's `assets/`, a deck's media) once chosen - for provenance and offline builds. That is an artifact asset, never a shared library other artifacts pull from.
- Each new visual = a fresh query. Vary the search terms and the source museum so consecutive posts do not converge on the same few crowd-pleasers.

## Verified keyless recipes (2026-07-24, all live-tested)

### 1. The Met - best all-around default
- Base: `https://collectionapi.metmuseum.org/public/collection/v1/` - no key, 80 req/s, CC0 where `isPublicDomain:true`.
- Search: `GET /search?q=<term>&hasImages=true&isPublicDomain=true` -> `{total, objectIDs[]}`
- Object: `GET /objects/{id}` -> read `primaryImage` (full-res JPEG, static, no IIIF hop) or `primaryImageSmall` (web-large).
- Example: `https://collectionapi.metmuseum.org/public/collection/v1/search?q=sunflowers&hasImages=true&isPublicDomain=true`

### 2. Cleveland Museum of Art - only one with archival TIFF
- Base: `https://openaccess-api.clevelandart.org/api/artworks/` - no key, CC0.
- Search: `GET /api/artworks/?cc0=1&has_image=1&limit=10` (add `&q=monet`, `&skip=10`).
- Image fields on each result: `images.web.url` (900px), `images.print.url` (3400px JPEG), `images.full.url` (archival TIFF). Directly downloadable from `openaccess-cdn.clevelandart.org`.
- Confirm `share_license_status == "CC0"` per result.

### 3. SMK (Denmark) - one-hop, broad European/Nordic
- Base: `https://api.smk.dk/api/v1` - no key. License: Public Domain Mark 1.0 (functionally CC0).
- Search: `GET /art/search?keys=*&filters=[public_domain:true]&filters=[has_image:true]`
- Read `image_native` directly from each result (no chain).
- **Gotcha (verified):** pass `filters` as a **repeated** query param, one `[field:value]` bracket each. Concatenating `filters=[public_domain:true][has_image:true]` returns 200 but silently ignores the second condition.

### 4. Rijksmuseum - Dutch/Flemish masters (keyless, 3 hops)
- Base: `https://data.rijksmuseum.nl/search/collection` (Linked Art, no key).
- `GET /search/collection?type=painting&imageAvailable=true` -> walk object -> VisualItem -> DigitalObject -> `access_point[0].id` is a ready IIIF URL.
- Mixed license: mostly CC0/PD but some CC BY 4.0 - **check the per-object rights block** (a CC BY item requires attribution).

### 5. NGA (Washington) - bulk/offline, no live search
- CSV: `https://raw.githubusercontent.com/NationalGalleryOfArt/opendata/main/data/published_images.csv` - filter `openaccess=1`.
- Image (IIIF): `https://api.nga.gov/iiif/{uuid}/full/full/0/default.jpg`
- **Per-image `openaccess=0` rows are NOT open** (resolution-capped, rights-restricted). Only `openaccess=1` is free.

### 6. Art Institute of Chicago - Impressionism/European (image host caveat)
- JSON: `GET https://api.artic.edu/api/v1/artworks/search?query[term][is_public_domain]=true&fields=id,title,image_id` - no key, CC0.
- Image: build `https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg` - **but Cloudflare 403s scripted fetches**; download via browser or use another museum for bytes.

### 7. Getty - European painting/photography/antiquities (SPARQL)
- Base: `https://data.getty.edu/museum/collection/` - no key. No keyword search; use SPARQL with `?obj crm:P138i_has_representation ?img` which returns a ready IIIF image URL in the same query.
- Dataset is CC0; **per-image rights inconsistently populated** - cross-check the object's public getty.edu page (a "Download" button flags true Open Content) before commercial use.

## Key-gated + aggregator sources (know these too)
- **Smithsonian** (needs free `api.data.gov` key; `DEMO_KEY` works at 30 req/hr): `GET https://api.si.edu/openaccess/api/v1.0/search?q=<term> AND online_media_type:Images&api_key=KEY`; CC0; check `media[].usage.access=="CC0"` per image. Extremely broad (SAAM, NPG portraits, Freer/Sackler Asian, Cooper Hewitt design).
- **Wikimedia Commons** (keyless, best aggregator fallback): `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=<term>&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata`; license per file in `extmetadata.LicenseShortName`; raw bytes via `Special:FilePath/{filename}`.
- **Wellcome Collection** (keyless): `https://api.wellcomecollection.org/catalogue/v2/works?query=<term>`; CC0/PD medical/scientific/historical imagery.
- **Internet Archive** (keyless): `https://archive.org/advancedsearch.php?q=<term>&fl[]=identifier&output=json`; PD book illustrations, engravings, historical photos, ephemera.
- **Europeana** (free key): `https://api.europeana.eu/record/v2/search.json?wskey=<KEY>&query=<term>`; 50M+ items across European institutions.
- **Harvard Art Museums** (free key): `https://api.harvardartmuseums.org/object?apikey=<KEY>&q=<term>`.
- **Yale LUX** (keyless, Linked Art like Getty): `https://lux.collections.yale.edu/api/search/...`; strong British art + rare books.
- **Paris Musees** (keyless, explicit CC0): `parismuseescollections.paris.fr` / `opendata.paris.fr`; French painting/decorative arts.
- **NYPL Digital Collections** (free key): `https://api.repository.library.nyc/...`; PD prints, maps, photos, illustrations.
- **DPLA** (free key): `https://api.dp.la/v2/items?q=<term>&api_key=<KEY>`; federated US collections.

## Licensing rules (apply before shipping any image)
- **True CC0 (no attribution required):** Met, Cleveland, Art Institute of Chicago, Smithsonian, NGA (dataset-level; image gated by per-image `openaccess=1`).
- **Public Domain Mark / open-but-not-CC0 (free to use, credit requested not required):** SMK, and the PD subset of Rijksmuseum.
- **Verify per-image, do NOT blanket-trust collection-level "open access":** Getty, Rijksmuseum (CC BY items require attribution), NGA and Smithsonian per-image flags.
- **Rule:** when the API exposes a rights/license field, filter on it in the query AND spot-check it on the chosen image. Never assume "the collection is open access" implies "this specific image is."
- **Good practice everywhere:** a one-line credit ("Digital image courtesy of [Museum]") costs nothing and covers mixed-license collections. When masking/compositing per house style, keep the credit.

## Relationship to other skills
- Stacks with **no-ai-slop** and the house image style: real museum art is the anti-slop default for evocative imagery.
- Complements **editorial-illustrations** (generative claim-driven diagrams) and **dataviz** (charts) - those own explanatory graphics; this owns photographic/artwork/mood imagery.
- Feeds **blog-publish**, **social-media-kit**, **weekly-ai-slide**, deck and essay work at their image-sourcing step.

## References (full per-museum recipes, verified)
`references/_synthesis.md` (cheat-sheet) + one file per museum (`met.md`, `cleveland.md`, `smk.md`, `rijksmuseum.md`, `nga.md`, `artic.md`, `getty.md`, `smithsonian.md`) with live-tested example URLs, field maps, and gotchas.
