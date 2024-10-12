from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from pathlib import Path
import html

url = "https://worldwidefm.net/episode/brownswood-basement-gilles-peterson-44"
filename = url.split("/")[-1] + ".txt"
path = "tracklists/" + filename
if Path(path).is_file():
    print("Tracklist already scraped")
    exit()

req = Request(
    url=url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    },
)
page = urlopen(req).read().decode("utf-8")
soup = BeautifulSoup(page, "html.parser")

tracklist = soup.find_all("div", class_="episode-tracklist filled")[0]
tracklist = tracklist.find_all("p")[0]
tracklist = str(tracklist)
start = tracklist.find("<p>") + len("<p>")
end = tracklist.find("</p>")
tracklist = tracklist[start:end]
tracklist = tracklist.split("<br/>")
tracklist = list(filter(None, tracklist))
tracklist = list(map(html.unescape, tracklist))
# remove lines with <strong>/in session/in conversation
tracklist = [track for track in tracklist if "-" in track]

with open(path, "w") as file:
    file.writelines("\n".join(tracklist))

print(f"Tracklist saved to {path}")
