from scrape_tracklist import scrape_tracklist
from tracklist_to_uris import tracklist_to_uris
from uris_to_playlist import uris_to_playlist

url = "https://worldwidefm.net/episode/gilles-peterson-brownswood-basement-26-10-2017-2"
with open("completed_urls.txt") as file:
    lines = file.read().splitlines()
    if url in lines:
        raise SystemExit("Tracks already added to playlist")

path = scrape_tracklist(url)
uris = tracklist_to_uris(path)
uris_to_playlist(uris)

with open("completed_urls.txt", "a") as file:
    file.write(url)
