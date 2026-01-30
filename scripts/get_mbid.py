#!/usr/bin/env python3
"""Simple MusicBrainz artist search helper.

Usage:
  python3 scripts/get_mbid.py --name "Metallica"

This prints candidate artists with MBIDs and brief metadata.
"""
import argparse
import json
import urllib.parse
from urllib import request, error


def search_artist(name, limit=10):
    q = urllib.parse.quote_plus(name)
    url = f"https://musicbrainz.org/ws/2/artist?query=artist:{q}&fmt=json&limit={limit}"
    req = request.Request(url, headers={
        'User-Agent': 'BandLogos/1.0 (https://github.com/bandlogos/BandLogos)'
    })
    try:
        with request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            j = json.loads(data)
            return j.get('artists', [])
    except error.HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}")
    except Exception as e:
        print(f"Error contacting MusicBrainz: {e}")
    return []


def pretty_print(artists):
    if not artists:
        print('No results')
        return
    for a in artists:
        mbid = a.get('id')
        name = a.get('name')
        dis = a.get('disambiguation', '')
        country = a.get('country', '')
        life = a.get('life-span', {}) or {}
        begin = life.get('begin', '')
        end = life.get('end', '')
        print('MBID:', mbid)
        print('  Name:       ', name)
        if dis:
            print('  Disambiguation:', dis)
        if country:
            print('  Country:    ', country)
        if begin or end:
            print('  Life-span:  ', f"{begin} - {end}")
        print('  URL:        ', f"https://musicbrainz.org/artist/{mbid}")
        print('')


def main():
    parser = argparse.ArgumentParser(description='Search MusicBrainz for artist MBIDs')
    parser.add_argument('--name', required=True, help='Artist name to search for')
    parser.add_argument('--limit', type=int, default=10, help='Max results to return')
    args = parser.parse_args()

    artists = search_artist(args.name, limit=args.limit)
    pretty_print(artists)


if __name__ == '__main__':
    main()
