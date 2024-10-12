import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
from thefuzz import fuzz


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
    return (artist_name, track_name)


def get_best_match(items, track):
    best_match = None
    best_ratio = 0
    for item in items:
        artist_name = item["artists"][0]["name"]
        track_name = item["name"]
        uri = item["uri"]
        track_result = f"{artist_name} - {track_name}"
        match_ratio = fuzz.partial_ratio(track, track_result)
        if match_ratio > best_ratio:
            best_match = track_result
            best_ratio = match_ratio
    print(track)
    print(best_match)
    print(best_ratio)
    print()
    return uri


sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

tracklist = "tracklists/brownswood-basement-gilles-peterson-44.txt"
with open(tracklist) as file:
    tracks = file.read().splitlines()

# DONE: increase search limit and choose result with highest fuzzy match
# TODO: fuzzy match artist and track name separately?
# TODO: only add to playlist if ratio above a certain threshold?

uris = []
for track in tracks:
    try:
        artist_name, track_name = parse_track(track)
    except ValueError as e:
        print(e)
        print()
        continue
    results = sp.search(
        q=f"{track_name} {artist_name}", type="track", limit=5, market="gb"
    )
    items = results["tracks"]["items"]
    uri = get_best_match(items, track)
    uris.append(uri)

print(uris)
