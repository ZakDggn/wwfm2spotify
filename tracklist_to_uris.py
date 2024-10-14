import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
from thefuzz import fuzz
import argparse


# Split track into artist and track name, and remove featuring artists
def parse_track(track):
    hyphen_count = track.count(" - ")
    if hyphen_count == 1:
        artist_name, track_name = track.split(" - ")
    elif hyphen_count == 0 and track.count(" -") == 1:
        artist_name, track_name = track.split(" -")
    elif hyphen_count == 0 and track.count("- ") == 1:
        artist_name, track_name = track.split("- ")
    else:
        raise ValueError(f"Couldn't parse track for artist and track name: {track}")
    for sub in [" feat. ", " ft. "]:
        artist_name = artist_name.split(sub)[0]
    return (artist_name, track_name)


# Find closest match in items and return its uri, or None if match not found
def get_uri(items, artist_name, track_name, threshold_ratio=80):
    best_ratio = 0
    best_artist_ratio = 0
    best_track_ratio = 0
    for item in items:
        artist_result = item["artists"][0]["name"]
        track_result = item["name"]
        uri = item["uri"]
        artist_ratio = fuzz.partial_ratio(artist_result.lower(), artist_name.lower())
        track_ratio = fuzz.partial_ratio(track_result.lower(), track_name.lower())
        match_ratio = (artist_ratio + track_ratio) / 2
        if match_ratio > best_ratio:
            best_ratio = match_ratio
            best_artist_ratio = artist_ratio
            best_track_ratio = track_ratio
    if best_artist_ratio > threshold_ratio and best_track_ratio > threshold_ratio:
        return uri


def tracklist_to_uris(path):
    with open(path) as file:
        tracks = file.read().splitlines()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    uris = []
    for track in tracks:
        try:
            artist_name, track_name = parse_track(track)
        except ValueError as e:
            print(e)
            continue
        results = sp.search(
            q=f"{artist_name.lower()} {track_name.lower()}",
            type="track",
            limit=10,
            market="gb",
        )
        items = results["tracks"]["items"]
        uri = get_uri(items, artist_name, track_name)
        if uri:
            uris.append(uri)
    return uris


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tracklist")
    args = parser.parse_args()
    tracklist = args.tracklist
    uris = tracklist_to_uris(tracklist)
    print(uris)
