Local developer instructions — running validation

This `DEV.md` contains instructions for running repository checks locally.

Quick start (macOS / Linux):

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies (either via `requirements.txt` or directly):

```bash
# if you keep requirements.txt
pip install -r requirements.txt

# or install just what you need
pip install Pillow PyYAML
```

3. Run the validator:

```bash
# basic run (no network checks)
python scripts/validate.py

# enable MusicBrainz checks (performs network requests)
python scripts/validate.py --check-mb
```

Notes:

- `--check-mb` contacts the MusicBrainz public API; avoid running it in tight loops to prevent rate limiting.
- The script will warn if `Pillow` or `PyYAML` are not installed and skip the related checks.
- Use the `local_dev/` folder for private notes and agent files; do not commit files from `local_dev/`.

Validating only changed artists
------------------------------

To avoid contacting the MusicBrainz API for the whole repository on every run, the validator supports limiting the check to a set of MBIDs.

- Validate a comma-separated list of MBIDs:

```bash
python3 scripts/validate.py --only 65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab,another-mbid
```

- Validate using a file with one MBID per line:

```bash
python3 scripts/validate.py --paths-file changed_mbids.txt --check-mb
```

CI guidance
-----------

The GitHub Actions workflow is updated to compute which `artists/<mbid>/` directories changed in the PR and pass those MBIDs to the validator. This keeps MusicBrainz requests scoped to only the changed artists.

If you need to run the same logic locally, create a file with changed MBIDs and use `--paths-file`.
