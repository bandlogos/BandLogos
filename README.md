Band Logos Source of Truth

What this project is

This project is a community maintained source of truth for artist identity artwork, with a primary focus on band and artist logos.

The goal is simple:
	•	Provide clean, high quality artist identity assets
	•	Keep them consistent, predictable, and reusable
	•	Make them easy to consume across different music players and media servers
	•	Avoid coupling the artwork to any single application

This repository is intentionally application agnostic. It references common media servers such as Plex, Plexamp, and Jellyfin as examples, but is not designed around the limitations or behaviors of any one platform.

This repository stores the artwork itself. It does not run services, host APIs, or require any always on infrastructure.

Why logos

Logos work well as artist identity artwork across modern music players and media servers.

They are especially effective in interfaces that emphasize clean layouts, strong contrast, and adaptive scaling, including applications like Plexamp, Plex, Jellyfin, and others.

This repository treats logos as the canonical identity asset and leaves application specific handling to external sync tooling.
# Band Logos — Source of Truth

This repository is a community-maintained source of truth for artist identity artwork, focused on band and artist logos.

## Goals

- Provide clean, high-quality artist identity assets
- Keep assets consistent, predictable, and reusable
- Make assets easy to consume across different music players and media servers
- Avoid coupling artwork to any single application

The repository stores artwork only; it does not run services or host APIs.

## Important Notices

**Not legal advice**: This repository does not provide legal advice. Consult an attorney for definitive guidance.

**Fan-Made Project / Not Official**: This is a fan-created, community-maintained project and is not affiliated with, endorsed by, or the official repository of any artist, label, or rights holder. Avoid wording or naming that implies official status.

**Permitted Use**: Assets are intended for personal, non-commercial use only. Redistribution, commercial use, or public hosting may increase legal risk.

**Takedown & DMCA**: We aim to honor verified takedown requests promptly. See [docs/LEGAL.md](docs/LEGAL.md) for the takedown procedure and required information for rights holders.

**Support Your Artists**: Music is created by talented people who deserve your support. If you enjoy an artist's work, please buy their albums, stream legally, attend shows, and help them continue making great music. This project exists to enhance your personal experience, not replace supporting the creators.

## Identifiers

Artists are identified using MusicBrainz Artist IDs (MBIDs). All artist directories are keyed by MBID, not by artist name.

## Finding MBIDs

Need the MusicBrainz Artist ID (MBID) for an artist? See `docs/MBID_LOOKUP.md` for step-by-step instructions (web UI, Picard, API/curl), and use the included helper `scripts/get_mbid.py` to search MusicBrainz from the command line.

Quick example (search for candidates):

```bash
python3 scripts/get_mbid.py --name "Artist Name"
```

Wiki-ready help is available in `docs/WIKI_CONTENT.md` if you want to paste pages into the repository wiki.

## Repository structure

```
artists/
  <musicbrainz-artist-id>/
    logo.png
    logo.svg      (optional)
    poster.png    (optional)
    fanart.png    (optional)
    metadata.yaml
```

Notes:

- `logo.png` is the required primary asset
- SVG files are optional source assets
- Poster and fanart are optional

## Design guidelines

- Visual clarity at small sizes
- Consistent framing and centering
- Minimal effects
- Predictable results across platforms

### Logo safe area

Logo content should fit within roughly 80% of the canvas to leave padding and avoid cropping in certain views.

### Stroke weight and detail

- Avoid extremely thin strokes
- Avoid fine internal details that disappear at small sizes
- Test legibility at ~128–256 pixels

### Color and contrast

- High contrast logos are preferred
- White or light logos on transparent backgrounds work well

## Alternates

Alternate versions are allowed (light/dark, historical). Naming examples:

- `logo-alt.png`
- `logo-dark.png`
- `logo-light.png`

Rules:

- One primary `logo.png` must exist
- Keep alternates to a reasonable number

## Validation and CI

Planned automated checks include:

- Directory structure and naming
- Valid MBID format
- Required files present
- Image dimensions and aspect ratio
- Transparency checks for logos

Non-automated checks include visual centering and artistic quality. Pull requests that fail automated checks will be asked to fix issues before merging.
	•	Avoid relying on background colors for legibility

Resources:

- Contributing guidelines: [CONTRIBUTING.md](CONTRIBUTING.md)
- Developer instructions: [docs/DEV.md](docs/DEV.md)
