from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import requests
import pandas as pd

def bugs_chart():
    url = 'https://music.bugs.co.kr/'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    chart = soup.find('div', {'class': 'trackChart'})
    tbody = chart.find('tbody')
    trs = tbody.find_all('tr')
    chart_list = []
    for tr in trs:
        th = tr.find('th')
        th_a = th.find('a', {'class': 'thumbnail'})
        thumbn = th_a.find('img').attrs['src']
        resize = thumbn.find('60/')
        thumbn = thumbn.replace(thumbn[resize:resize+3], '140/')
        p_t = th.find('p')
        title = p_t.find('a').string
        p_a = tr.find('p', {'class': 'artist'})
        artist = p_a.find('a').string

        chart_list.append([thumbn, title, artist])
    return chart_list

def melon_chart():
    url = 'https://www.melon.com/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get(url, headers=header)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    chart = soup.find('div', {'class': 'list_wrap typeRealtime'})
    lis = chart.find_all('li', {'class': 'rank_item'})
    chart_list = []
    for li in lis:
        rank = li.find('div', {'class': 'rank_cntt'})
        thumbn = rank.find('img').attrs['src']
        resize = thumbn.find('48/o')
        thumbn = thumbn.replace(thumbn[resize:resize+3], '140/')
        rank_info = li.find('div', {'class': 'rank_info'})
        song_info = rank_info.find('p', {'class': 'song'})
        ellipsis = rank_info.find('div', {'class': 'ellipsis'})
        arti_nm = ellipsis.find('span')
        title = song_info.find('a').string
        artists = arti_nm.find_all('a')
        if len(artists) <= 1:
            artist = artists[0].string
        else:
            artist = ''
            for a in artists:
                artist += a.string + ' '
        
        chart_list.append([thumbn, title, artist])
    return chart_list

def genie_chart():
    url = 'https://www.genie.co.kr/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get(url, headers=header)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    chart = soup.find('table', {'class': 'list-wrap'})
    tbody = chart.find('tbody')
    trs = tbody.find_all('tr')
    chart_list = []
    for tr in trs:
        info = tr.find('td', {'class': 'info'})
        thumbn = info.find('img').attrs['src']
        title = info.find('a', {'class': 'title'}).string
        artist = info.find('a', {'class': 'artist'}).string

        chart_list.append([thumbn, title, artist])
    return chart_list

def movies():
    url = 'http://www.cgv.co.kr/movies/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get(url, headers=header)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    chart_sec = soup.find('div', {'class': 'sect-movie-chart'})
    lis = chart_sec.find_all('li')
    imgs, titles, scores, dates, kinds = [], [], [], [], []
    for li in lis:
        span = li.find('span', {'class': 'thumb-image'})
        imgs.append(span.find('img').attrs['src'])
        box = li.find('div', {'class': 'box-contents'})
        titles.append(box.find('strong', {'class': 'title'}).string)
        scores.append(box.find('span', {'class': 'percent'}).string)
        release_date = box.find('span', {'class': 'txt-info'})
        dates.append(release_date.find('strong').string)
        kinds.append(release_date.find('span').string)

    return imgs, titles, scores, dates, kinds
