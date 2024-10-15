from pathlib import Path
from scrape_tracklist import scrape_tracklist
from tracklist_to_uris import tracklist_to_uris
from uris_to_playlist import uris_to_playlist

with open("urls.txt") as file:
    urls = file.read().splitlines()

completed_path = Path("completed_urls.txt")
completed_urls = []
if completed_path.is_file():
    with open(completed_path) as file:
        completed_urls = file.read().splitlines()

for url in urls[:3]:
    print(url)
    if url in completed_urls:
        print("Tracks already added to playlist")
        continue
    path = scrape_tracklist(url)
    if path is None:
        continue
    uris = tracklist_to_uris(path)
    uris_to_playlist(uris)
    with open(completed_path, "a") as file:
        file.write(url + "\n")
