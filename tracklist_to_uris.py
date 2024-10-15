import spotipy
from spotipy.oauth2 import SpotifyOAuth
from thefuzz import fuzz
import argparse
import re


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


def get_closest_artist(artist_results, artist_name):
    closest_artist = ""
    closest_ratio = 0
    for artist in artist_results:
        name = artist["name"]
        ratio = fuzz.partial_ratio(name, artist_name)
        if ratio > closest_ratio:
            closest_artist = name
            closest_ratio = ratio
    return closest_artist


# Find closest match in items and return its uri, or None if match not found
def get_uri(items, artist_name, track_name, threshold_ratio=80):
    best_ratio = 0
    best_artist_ratio = 0
    best_track_ratio = 0
    best_uri = None
    for item in items:
        artist_result = get_closest_artist(item["artists"], artist_name)
        track_result = item["name"]
        uri = item["uri"]
        artist_ratio = fuzz.partial_ratio(artist_result.lower(), artist_name.lower())
        track_ratio = fuzz.partial_ratio(track_result.lower(), track_name.lower())
        match_ratio = (artist_ratio + track_ratio) / 2
        if match_ratio > best_ratio:
            best_ratio = match_ratio
            best_artist_ratio = artist_ratio
            best_track_ratio = track_ratio
            best_uri = uri
    if best_artist_ratio >= threshold_ratio and best_track_ratio >= threshold_ratio:
        return best_uri


def get_search_results(sp, artist_name, track_name):
    results = sp.search(
        q=f"{artist_name.lower()} {track_name.lower()}",
        type="track",
        limit=10,
        market="gb",
    )
    return results["tracks"]["items"]


def tracklist_to_uris(path):
    with open(path) as file:
        tracks = file.read().splitlines()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    uris = []
    for track in tracks:
        try:
            artist_name, track_name = parse_track(track)
        except ValueError as e:
            with open("track_parse_errors.txt", "a") as file:
                file.write(str(e) + "\n")
            print(e)
            continue
        items = get_search_results(sp, artist_name, track_name)
        uri = get_uri(items, artist_name, track_name)
        if uri is None:
            # remove '&'
            pattern = " ?& ?"
            artist_name = re.sub(pattern, " ", artist_name)
            track_name = re.sub(pattern, " ", track_name)
            # remove text inside brackets, text after 'with' and 'and's
            patterns = [r"\(.*?\)|\[.*?\]", "with.*", " and "]
            for pattern in patterns:
                artist_name = re.sub(pattern, "", artist_name).strip()
                track_name = re.sub(pattern, "", track_name).strip()
            items = get_search_results(sp, artist_name, track_name)
            uri = get_uri(items, artist_name, track_name)
        if uri is None:
            # swap artist and track
            uri = get_uri(items, track_name, artist_name)
        if uri:
            uris.append(uri)
        else:
            with open("tracks_not_found.txt", "a") as file:
                file.write(track + "\n")
    return uris


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tracklist")
    args = parser.parse_args()
    tracklist = args.tracklist
    uris = tracklist_to_uris(tracklist)
    print(uris)
