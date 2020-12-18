from flask import Blueprint, render_template, request, current_app
import pandas as pd
import os, time, urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.request import urlopen
from utils import wordcloud as wc
from utils.weather import cur_weather

cloud_bp = Blueprint('cloud_bp', __name__)

menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 0, 'co': 0, 'ca': 0, 'cr': 0, 'st': 0, 'wc': 1}

@cloud_bp.route('/create_wc', methods=['GET', 'POST'])
def cloud():
    if request.method == 'GET':
        return render_template('wordcloud/create_wc.html', menu=menu, weather=cur_weather())
    else:
        lang = request.form['lang']
        txt = request.files['txt']
        txt_filename = os.path.join(current_app.root_path, 'static/upload/') + txt.filename
        txt.save(txt_filename)
        current_app.logger.info(f'{txt_filename} is saved.')
        if request.files['mask']:
            mask = request.files['mask']
            mask_filename = os.path.join(current_app.root_path, 'static/upload/') + mask.filename
            mask.save(mask_filename)
        else:
            mask_filename = None
        stopwds = request.form['stopwords'].split() if request.form['stopwords'] else []

        text = open(txt_filename).read()
    
        img_file = os.path.join(current_app.root_path, 'static/img/wordcloud.png')
        if lang == 'en':
            wc.eng_cloud(text, mask_filename, stopwds, img_file)
        else:
            wc.kor_cloud(text, mask_filename, stopwds, img_file)
        mtime = int(os.stat(img_file).st_mtime)
        return render_template('wordcloud/wc_result.html', menu=menu, weather=cur_weather(), mtime=mtime)

@cloud_bp.route('/hot_keyword')
def hottie():
    driver = webdriver.Chrome(r'G:\\Workspace\\Data-analysis\\Data-analysis\\chromedriver.exe')
    events = ['kbaseball', 'wbaseball', 'kfootball', 'wfootball', 'basketball', 'volleyball', 'golf', 'general']
    first_url = 'https://sports.news.naver.com/kbaseball/news/index.nhn?isphoto=N'
    driver.get(first_url)
    time.sleep(1)
    pagi = driver.find_elements_by_css_selector('.paginate')
    base_url = 'https://sports.news.naver.com/'
    for i in len(pagi) + 1:
        page_url = f'&page={i+1}'
        for event in events:
            event_url = f'{event}/news/index.nhn?isphoto=N'
            url = base_url + event_url + page_url
            driver.get(url)
            time.sleep(1)
            news_list = driver.find_elements_by_css_selector('.news_list.text')
            titles = ''
            for news in news_list:
                titles += news.find_element_by_class_name('title').text
    text = open('./static/data/title.txt', 'w')
    text.write(titles)
    text.close()


            
        