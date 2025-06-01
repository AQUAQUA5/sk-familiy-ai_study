from urllib.parse import urlparse, urlencode, quote
import requests
from bs4 import BeautifulSoup
import re
import os
import pathlib

p = re.compile("playSong\(\'([0-9]+)\',([0-9]+)\)")


def my_request(url, method='get'):
    head = {'user-agent'
            : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'}
    if method == "get":
        return requests.get(url, headers=head)


def search_id(title):
    host = "https://www.melon.com/search/total/index.htm?"
    payload = {
        'searchGnbYn': ['Y'],
        'kkoSpl': ['Y'],
        'mwkLogType': ['T']
    }
    payload['q'] = [title]

    # url 주소 생성 
    url = host + urlencode(payload, doseq=True)

    # return url 
    r = my_request(url)
    text = BeautifulSoup(r.text).find("div", class_="tb_list d_song_list songTypeOne").find_all("tr")[1].find("button",
                                                                                                              "btn_icon play")[
        'onclick']

    return p.findall(text)[0][-1]


def save_lyrics(songid, path='lyrics'):
    url = f"https://www.melon.com/song/detail.htm?songId={songid}"
    r = requests.get(url)
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'}

    r = requests.get(url, headers=head)
    bs = BeautifulSoup(r.text)
    lyrics = BeautifulSoup(str(bs.find("div", id="d_video_summary")).replace("<br/>", "\n")).text

    # if not os.path.isdir(f"./lyrics/{path}"):
    #     os.mkdir(f"./lyrics/{path}")
    # else:
    #     pass
    pathlib.Path(f"./lyrics/{path}").mkdir(parents=True, exist_ok=True)

    title = bs.find("div", class_="song_name").text.replace("곡명", "").strip()
    artist = bs.find("div", class_="artist").text.strip()
    f = open(f"./lyrics/{path}/{artist}-{title}.txt", 'w', encoding='utf-8')
    f.write(lyrics.strip())
    f.close()
