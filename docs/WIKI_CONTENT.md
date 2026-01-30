# Wiki Content (copy into GitHub wiki)

Below are ready-to-paste pages for the BandLogos GitHub wiki.

---

## Home

BandLogos — community-maintained source of artist identity artwork. This wiki contains help pages for contributors and users: how to find MBIDs, contribution guidelines, and integration tips.

Links:
- How to find an MBID — copy from the `How to find an MBID` page
- Contribution guidelines — copy from `CONTRIBUTING.md`

---

## How to find an MBID

Use the MusicBrainz website to search for your artist. The MBID is a UUID visible in the artist page URL: `https://musicbrainz.org/artist/<MBID>`.

Quick methods:
- MusicBrainz web UI: search then open the artist page.
- Use the included helper `scripts/get_mbid.py --name "Artist Name"` to see candidates and MBIDs.
- Use MusicBrainz Picard or the MusicBrainz API (see docs/MBID_LOOKUP.md in repository).

Format: MBIDs are UUIDs (hex characters with dashes). Example: `65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab`.

---

## Using BandLogos

1. Find the MBID for an artist.
2. Create a directory under `artists/<mbid>/`.
3. Add `logo.png` and `metadata.yaml` (include `artist`, `mbid`, `source`).
4. Run `scripts/validate.py --only <mbid>` locally to verify.

---

## FAQ

Q: What if multiple artists have the same name?
A: Use disambiguation details (year, country) and verify via the MusicBrainz page.
