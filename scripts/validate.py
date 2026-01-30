#!/usr/bin/env python3
"""Validation script for BandLogos repository.

Checks:
- artists/ directory presence
- MBID (UUID) format for artist directories
- presence of required files (logo.png, metadata.yaml)
- logo.png: square, dimensions within allowed range, and contains transparency
- metadata.yaml mbid matches directory name (if present)

Exit code 0 when all checks pass, non-zero otherwise.
"""
import sys
import os
import re
import argparse
import json
import time
from urllib import request, error

try:
    import yaml
except Exception:
    yaml = None

try:
    from PIL import Image
except Exception:
    Image = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTISTS_DIR = os.path.join(ROOT, 'artists')

UUID_RE = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')

MIN_LOGO = 1024
MAX_LOGO = 2048

errors = []


def is_uuid(s):
    return bool(UUID_RE.match(s))


def check_logo(path, artist):
    try:
        img = Image.open(path)
    except Exception as e:
        errors.append(f"{artist}: cannot open logo.png - {e}")
        return

    w, h = img.size
    if w != h:
        errors.append(f"{artist}: logo.png is not square ({w}x{h})")
    if w < MIN_LOGO or w > MAX_LOGO:
        errors.append(f"{artist}: logo.png width {w} outside allowed range {MIN_LOGO}-{MAX_LOGO}")

    # Check transparency: ensure image has alpha channel and at least one pixel with alpha < 255
    has_alpha = img.mode in ('LA', 'RGBA') or ('A' in img.getbands())
    if not has_alpha:
        errors.append(f"{artist}: logo.png has no alpha channel; logos should use a transparent background")
        return

    alpha = None
    try:
        alpha = img.split()[-1]
        extrema = alpha.getextrema()
        if extrema == (255, 255):
            errors.append(f"{artist}: logo.png appears fully opaque (no transparency)")
    except Exception:
        errors.append(f"{artist}: could not inspect alpha channel for transparency")


def check_metadata(path, artist_dir_name):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            data = yaml.safe_load(fh) or {}
    except Exception as e:
        errors.append(f"{artist_dir_name}: metadata.yaml cannot be read - {e}")
        return

    mbid = data.get('mbid')
    if mbid and mbid != artist_dir_name:
        errors.append(f"{artist_dir_name}: metadata.yaml mbid does not match directory name ({mbid} != {artist_dir_name})")


def main():
    parser = argparse.ArgumentParser(description='Validate BandLogos repository')
    parser.add_argument('--only', help='Comma-separated list of MBIDs to validate (limit run to these)')
    parser.add_argument('--paths-file', help='Path to a file containing MBIDs (one per line) to validate')
    parser.add_argument('--mb-cache-ttl', type=int, default=86400, help='Seconds to cache MusicBrainz results (default 86400)')
    parser.add_argument('--check-mb', action='store_true', help='Verify MBID exists in MusicBrainz')
    args = parser.parse_args()

    if yaml is None:
        print('Warning: PyYAML not installed. metadata.yaml checks will be limited.')
    if Image is None:
        print('Warning: Pillow not installed. image checks will be skipped.')
    if not os.path.isdir(ARTISTS_DIR):
        print('No artists/ directory found; skipping validation.')
        return 0

    # Determine MBIDs to validate (if --only or --paths-file provided)
    only_mbids = set()
    if args.only:
        for m in args.only.split(','):
            m = m.strip()
            if m:
                only_mbids.add(m)
    if args.paths_file:
        try:
            with open(args.paths_file, 'r', encoding='utf-8') as fh:
                for line in fh:
                    l = line.strip()
                    if l:
                        only_mbids.add(l)
        except Exception as e:
            errors.append(f"paths-file: cannot read file {args.paths_file} - {e}")

    # If only_mbids is provided, we'll validate only those entries. Ensure they exist or report missing.
    if only_mbids:
        for m in sorted(only_mbids):
            dirpath = os.path.join(ARTISTS_DIR, m)
            if not os.path.isdir(dirpath):
                errors.append(f"{m}: specified in --only/--paths-file but artist directory not found")

    infos = []

    # Load MB cache for --check-mb to reduce requests
    mb_cache = {}
    cache_path = os.path.join(ROOT, '.mb_cache.json')
    try:
        if os.path.isfile(cache_path):
            with open(cache_path, 'r', encoding='utf-8') as fh:
                mb_cache = json.load(fh) or {}
    except Exception:
        mb_cache = {}

    # Iterate over either the repository artist directories or the supplied --only list
    if only_mbids:
        names_iter = sorted(only_mbids)
    else:
        names_iter = [n for n in sorted(os.listdir(ARTISTS_DIR)) if os.path.isdir(os.path.join(ARTISTS_DIR, n))]

    for name in names_iter:
        dirpath = os.path.join(ARTISTS_DIR, name)
        if not os.path.isdir(dirpath):
            # already reported missing above when --only used; skip
            continue

        if not is_uuid(name):
            errors.append(f"{name}: directory name is not a valid MBID (UUID)")

        logo_path = os.path.join(dirpath, 'logo.png')
        metadata_path = os.path.join(dirpath, 'metadata.yaml')

        if not os.path.isfile(logo_path):
            errors.append(f"{name}: missing required file logo.png")
        else:
            if Image is not None:
                check_logo(logo_path, name)
            else:
                errors.append(f"{name}: Pillow not installed; cannot validate logo.png")

        if not os.path.isfile(metadata_path):
            errors.append(f"{name}: missing metadata.yaml")
        else:
            if yaml is not None:
                check_metadata(metadata_path, name)
            else:
                errors.append(f"{name}: PyYAML not installed; cannot validate metadata.yaml contents")

        # Optional remote MusicBrainz check
        if args.check_mb and is_uuid(name):
            mb_ok = False
            artist_name = None
            # Check cache first
            now = int(time.time())
            cached = mb_cache.get(name)
            if cached:
                try:
                    ts = int(cached.get('ts', 0))
                    if now - ts <= args.mb_cache_ttl:
                        mb_ok = bool(cached.get('ok'))
                        artist_name = cached.get('name')
                except Exception:
                    mb_ok = False

            if not mb_ok:
                url = f"https://musicbrainz.org/ws/2/artist/{name}?fmt=json"
                try:
                    with request.urlopen(url, timeout=10) as resp:
                        if resp.status == 200:
                            data = resp.read()
                            try:
                                j = json.loads(data)
                                if j.get('id') == name:
                                    mb_ok = True
                                    artist_name = j.get('name') or j.get('sort-name')
                            except Exception:
                                pass
                except error.HTTPError as e:
                    if e.code == 404:
                        mb_ok = False
                except Exception:
                    errors.append(f"{name}: could not contact MusicBrainz for MBID validation")

                # store in cache
                try:
                    mb_cache[name] = {'ts': int(time.time()), 'ok': bool(mb_ok), 'name': artist_name}
                except Exception:
                    pass

            if not mb_ok:
                errors.append(f"{name}: MBID not found on MusicBrainz or network error")
            else:
                if artist_name:
                    infos.append(f"{name}: MusicBrainz artist found: '{artist_name}'. Please confirm the artist for this MBID (type validation).")
                else:
                    infos.append(f"{name}: MusicBrainz artist found but name unavailable; please confirm manually.")

    if infos:
        print('\nManual checks / suggestions:')
        for i in infos:
            print('- ' + i)

    if errors:
        print('\nValidation failed with the following issues:')
        for e in errors:
            print('- ' + e)
        # Save cache before exiting
        try:
            with open(cache_path, 'w', encoding='utf-8') as fh:
                json.dump(mb_cache, fh)
        except Exception:
            pass
        return 2

    print('\nValidation passed: no issues found')
    try:
        with open(cache_path, 'w', encoding='utf-8') as fh:
            json.dump(mb_cache, fh)
    except Exception:
        pass
    return 0


if __name__ == '__main__':
    sys.exit(main())
