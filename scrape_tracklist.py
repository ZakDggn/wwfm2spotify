from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from pathlib import Path
import html
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url")
args = parser.parse_args()

url = args.url
filename = url.split("/")[-1] + ".txt"
path = "tracklists/" + filename
if Path(path).is_file():
    raise SystemExit("Tracklist already scraped")

req = Request(
    url=url,
    headers={"User-Agent": "Mozilla/5.0"},
)
page = urlopen(req).read().decode("utf-8")
soup = BeautifulSoup(page, "html.parser")

tracklist = soup.find("div", class_="episode-tracklist filled")
div = tracklist.div
if div.p:
    tracklist = div.p.stripped_strings
else:
    tracklist = div.stripped_strings
tracklist = filter(None, tracklist)
tracklist = map(html.unescape, tracklist)
tracklist = [track for track in tracklist if "-" in track]

with open(path, "w") as file:
    file.writelines("\n".join(tracklist))

print(f"Tracklist saved to {path}")
