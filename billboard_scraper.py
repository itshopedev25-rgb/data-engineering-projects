import requests
from bs4 import BeautifulSoup
import csv

def scrape_billboard():

    url = "https://www.billboard.com/charts/hot-100/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # More specific selector
    songs = soup.find_all("h3", id="title-of-a-story")

    # Filter out non-song titles
    real_songs = [
        song.get_text(strip=True) for song in songs
        if song.get_text(strip=True) not in [
            "Gains in Weekly Performance",
            "Additional Awards",
            "Songwriter(s)",
            "Producer(s)",
            "Imprint/Label"
        ]
    ]

    print(f"Found {len(real_songs)} actual songs\n")

    with open('billboard_charts.csv', 'w',
              newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Position', 'Title'])

        for i, title in enumerate(real_songs):
            print(f"#{i+1} {title}")
            writer.writerow([i+1, title])

    print("\nSaved to billboard_charts.csv!")

scrape_billboard()