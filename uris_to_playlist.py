import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint


def uris_to_playlist(track_uris):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public"))

    # get uri of current user
    results = sp.current_user()
    user_uri = results["uri"]
    # remove 'spotify:user:' from beginning of `user_uri`
    user_uri = user_uri.split(":")[-1]

    # check if playlist already exists
    playlist_name = "Gilles Peterson on Worldwide FM"
    results = sp.current_user_playlists()
    user_playlists = results["items"]
    for playlist in user_playlists:
        if playlist["name"] == playlist_name:
            playlist_uri = playlist["uri"]
            print("Found playlist")
            break
    else:  # create playlist if not found in user list
        results = sp.user_playlist_create(user_uri, playlist_name, public=True)
        playlist_uri = results["uri"]
        print("Created playlist")

    # add tracks to playlist
    results = sp.playlist_add_items(playlist_uri, track_uris)
    print("Added tracks to playlist")
