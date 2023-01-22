import requests
import json
import os
from bs4 import BeautifulSoup
import pandas as pd

def get_musics(pages=1, musictype="featured"):
    musics = []
    url = "https://mrtehran.com/browse/{}/page-{}"
    page = requests.get(url.format(musictype,1))
    soup = BeautifulSoup(page.content, 'html.parser')
    page_numbers = soup.find_all(
        'li', attrs={'class': 'page-item'})
    if len(page_numbers)>0:
        pages = int(page_numbers[-1].text)
    else:
        pages = 1
    print("music_type=>",music_type," pages=>", pages)
    for page_number in range(1, (pages+1)):

        page = requests.get(url.format(musictype,page_number))
        soup = BeautifulSoup(page.content, 'html.parser')

        featured = soup.find_all(
            'div', attrs={'data-song': True})
        for item in featured:
            musics.append({
                'artist': item.get('data-artist'),
                'title': item.get('data-title'),
                'cover': item.get('data-thumb').replace('_thumb', ''),
                'cover_thumb': item.get('data-thumb'),
                'data_url':item.get("data-url"),
                'data_id':item.get('data-id'),
                'mp3': item.get('data-song')
            })

    return musics
if not os.path.exists("./result/"):
    os.mkdir("./result")

all_cats = ["featured","latest","popular", "podcasts", "travel"]
for music_type in all_cats:
    pd.DataFrame(get_musics(1,music_type)).drop_duplicates().to_csv("./result/"+music_type +".csv")