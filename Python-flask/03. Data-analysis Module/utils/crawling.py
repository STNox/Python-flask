from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import pandas as pd

def bugs_new():
    url = 'https://music.bugs.co.kr/'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    na_place = soup.find(attrs={'id': 'newalbum_place'})
    lis = na_place.find_all('li')
    new_album = []
    for li in lis:
        thumbn = li.find('img').attrs['src']
        caption = li.find('figcaption')
        title = caption.find('a', {'class': 'albumTitle'}).string
        artist_info = caption.find('p', {'class': 'artist'})
        artist = artist_info.find('a').string

        new_album.append([thumbn, title, artist])
    return new_album

def bugs_chart():
    url = 'https://music.bugs.co.kr/'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    chart = soup.find('div', {'class': 'trackChart'})
    trs = chart.find_all('tr')
    chart_list = []
    for tr in trs:
        th = tr.find('th')
        thumbn = th.find('img').attrs['src']
        p_t = th.find('p')
        title = p_t.find('a').string
        p_a = tr.find('p', {'class': 'artist'})
        artist = p_a.find('a').string

        chart_list.append([thumbn, title, artist])
    return chart_list

def melon_chart():
    url = 'https://www.melon.com/'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    chart = soup.find('div', {'class': 'list_wrap'})
    lis = chart.find_all('li')
    chart_list = []
    for li in lis:
        thumb = li.find('div', {'class': 'thumb'})
        thumbn = thumb.find('img').attrs['src']
        rank_info = li.find('div', {'class': 'rank_info'})
        song_info = rank_info.find('p', {'class': 'song'})
        ellipsis = rank_info.find('div', {'class': 'ellipsis'})
        title = song_info.find('a').string
        artists = ellipsis.find_all('a')
        if len(artists) == 1:
            artist = artists[0].string
        else:
            artist = ''
            for a in artists:
                artist += a.string
        
        chart_list.append([thumbn, title, artist])
    return chart_list

def genie_chart():
    url = 'https://www.genie.co.kr/'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    chart = soup.find('div', {'class': 'music-list-wrap'})
    trs = chart.find_all('tr')
    chart_list = []
    for tr in trs:
        info = tr.find('td', {'class': 'info'})
        thumbn = info.find('img').attrs['src']
        title = info.find('a', {'class': 'title'}).string
        artist = info.find('a', {'class': 'artist'}).string

        chart_list.append([thumbn, title, artist])
    return chart_list