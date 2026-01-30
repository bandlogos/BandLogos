## Contributing Guidelines

Thank you for contributing. The rules below help keep the repository consistent and easy to use.

If something is unclear, open an issue before submitting a pull request.

### Basic requirements

Every submission must:



### Repository structure

This repository stores assets organized by MusicBrainz Artist ID (MBID). Place files under the artist's MBID directory using the layout below:

```
artists/
	<musicbrainz-artist-id>/
		logo.png
		logo.svg      (optional)
		poster.png    (optional)
		fanart.png    (optional)
		metadata.yaml
```

- `logo.png` is required and should be the primary square logo asset.
- `logo.svg` is optional and recommended when available as a scalable source.
- `poster.png` and `fanart.png` are optional supplementary assets.
- Include `metadata.yaml` with `artist`, `mbid`, and `source` fields for provenance.
### Required asset

`logo.png` is required for every artist.

Recommended logo guidelines:

- Transparent background
- Flat design (no shadows or glow)
- No baked-in backgrounds
- Visually centered
- Square format
- Resolution: minimum 1024×1024, maximum 2048×2048

SVG source files are optional but encouraged.

### Optional assets

#### Poster

`poster.png` is optional for photo or illustration based artist images.

Guidelines:

- Square format
- Minimum 1024×1024, maximum 2048×2048
- Avoid heavy text overlays

#### Fanart

`fanart.png` is optional for wide background images.

Guidelines:

- Minimum 1920×1080, maximum 3840×2160
- Avoid logos or text overlays

### Alternate assets

Alternates may be included alongside the primary logo (for example light/dark variants).

Naming examples:

- `logo-alt.png`
- `logo-dark.png`
- `logo-light.png`

Rules:

- One primary `logo.png` must exist
- Alternates should follow the same resolution and format rules

### Metadata

Include a `metadata.yaml` file in each artist directory. Example:

```
artist: Metallica
mbid: 65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab
source: fanart
notes: Primary logo optimized for multiple platforms
```

If `mbid` is present in `metadata.yaml`, it should match the artist directory name.

### Review and CI

Automated checks should validate:

- Directory structure and file naming
- Valid MBID format (UUID)
- Required files are present (`logo.png`, `metadata.yaml`)
- Image dimensions and aspect ratio
- Presence of transparency for `logo.png`

Manual review focuses on:

- Visual centering
- Safe area and padding
- Overall artistic quality

Pull requests that fail automated checks should be updated before merging.

## How to make a PR

Follow these steps to contribute via a pull request (PR):

1. Fork the repository on GitHub and clone your fork locally:

```bash
git clone https://github.com/<your-username>/BandLogos.git
cd BandLogos
```

2. Create a feature branch with a clear name, e.g. `artist/<mbid>-add`:

```bash
git checkout -b artist/65f4f0c5-add
```

3. Add or update files under the correct MBID path:

```
artists/<MBID>/logo.png
artists/<MBID>/metadata.yaml
```

4. Run the validator locally before committing (see `docs/DEV.md`):

```bash
# basic run (no MusicBrainz checks)
python scripts/validate.py --only <MBID>

# with MusicBrainz checks (may perform network requests)
python scripts/validate.py --only <MBID> --check-mb
```

5. Commit, push the branch to your fork, and open a PR against `bandlogos/BandLogos:main`.

Include in the PR description:

- Artist name and MBID
- Repository path(s) changed (e.g., `artists/<MBID>/logo.png`)
- Source/origin of the asset and any attribution
- Any design notes or preview screenshots

6. Address CI failures and reviewer feedback; keep PRs small and focused.

Thank you — clear, small PRs speed review and merging.
