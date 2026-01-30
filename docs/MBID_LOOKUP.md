## Finding a MusicBrainz Artist ID (MBID)

This document explains simple ways contributors and users can find an artist's MusicBrainz Artist ID (MBID). You do not need to host a website — these steps use MusicBrainz's public site and APIs or local tools.

## What is an MBID?

An MBID is a MusicBrainz identifier for an artist. It is a UUID (for example: `65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab`). In this project each artist folder must be named with the exact MBID.

## 1) MusicBrainz web interface (recommended)

1. Open https://musicbrainz.org
2. Enter the artist name in the search box and press Enter.
3. From the results, click the artist entry that matches the performer you mean.
4. The MBID appears in the URL for the artist page: `https://musicbrainz.org/artist/<MBID>`

Example: the artist page `https://musicbrainz.org/artist/65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab` has MBID `65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab`.

## 2) MusicBrainz Picard (desktop app)

- Install Picard: https://picard.musicbrainz.org/
- Search for an artist and open the artist page inside Picard — the MBID is visible in the metadata and in the artist URL.

## 3) Quick curl / API search (command line)

You can query the MusicBrainz search API. Replace `ARTIST+NAME` with the artist you want (URL-encoded).

```bash
curl -s "https://musicbrainz.org/ws/2/artist?query=artist:ARTIST+NAME&fmt=json&limit=5" \
  -H "User-Agent: BandLogos/1.0 (https://github.com/bandlogos/BandLogos)"
```

Inspect the returned JSON for `id` fields — those are MBIDs.

## 4) `scripts/get_mbid.py` helper (included)

We include a small helper script `scripts/get_mbid.py` that queries MusicBrainz and prints matching artists and MBIDs. Use it like:

```bash
python3 scripts/get_mbid.py --name "Metallica"
```

This is a convenience for contributors; it depends on network access to MusicBrainz.

## MBID format rules

- Must be a UUID (hex digits with dashes) exactly as MusicBrainz shows it.
- Example valid MBID: `65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab`

## Verification tips

- Confirm artist name, disambiguation (year or location), and country when multiple results exist.
- If in doubt, link to the MusicBrainz artist page in `metadata.yaml`'s `source` or `notes` field.

## What to include in `metadata.yaml`

Include the `mbid` field matching the directory name and optionally the `artist` name and a `source` URL. Example:

```yaml
artist: Metallica
mbid: 65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab
source: https://musicbrainz.org/artist/65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab
notes: Primary logo optimized for multiple platforms
```

## Troubleshooting

- If no exact MBID exists for the modern artist name, check for common alternate names, collaborations, or a group vs solo-artist record.
- If you accidentally use the wrong MBID, our validator will warn that the MBID does not match the directory or that MusicBrainz lookup did not find a match (when `--check-mb` is enabled).

---

If you'd like, I can also add a GitHub Actions step that generates a simple `mbid-help` page using this content and commits it to a `gh-pages` branch, but that's optional.
