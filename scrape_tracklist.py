from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from pathlib import Path
import html
import argparse


def scrape_tracklist(url):
    filename = url.split("/")[-1] + ".txt"
    path = "tracklists/" + filename
    if Path(path).is_file():
        # raise SystemExit("Tracklist already scraped")
        print("Tracklist already scraped")
        return path

    req = Request(
        url=url,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    page = urlopen(req).read().decode("utf-8")
    soup = BeautifulSoup(page, "html.parser")

    tracklist = soup.find("div", class_="episode-tracklist filled")
    if tracklist is None or tracklist.text == "":
        print("Tracklist not found")
        return
    tracklist = tracklist.stripped_strings
    tracklist = filter(None, tracklist)
    tracklist = map(html.unescape, tracklist)
    tracklist = [track.replace("–", "-") for track in tracklist]
    tracklist = [track for track in tracklist if "-" in track]

    if len(tracklist) == 0:
        print("Tracklist is empty")
        return
    with open(path, "w") as file:
        file.writelines("\n".join(tracklist))
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    url = args.url
    path = scrape_tracklist(url)
    print(f"Tracklist saved to {path}")
