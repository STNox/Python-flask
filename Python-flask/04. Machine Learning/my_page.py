from flask import Flask, render_template, request, session, escape
import pandas as pd
import os, folium, json, logging
from logging.config import dictConfig
import pandas_datareader as pdr
from utils.weather import cur_weather

from bp1_seoul.seoul import seoul_bp
from bp2_covid.covid import covid_bp
from bp3_cartogram.carto import carto_bp
from bp4_crawling.crawl import crawl_bp
from bp5_stock.stock import stock_bp
from bp6_wordcloud.cloud import cloud_bp
from bp7_classification.clsft import clsft_bp
from bp8_upperclass.upcls import upcls_bp
from bp9_regression.regre import regre_bp
from bp10_clustering.clust import clust_bp
from bp11_language.lang import lang_bp

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager
mpl.rc('font', family='Malgun Gothic')
mpl.rc('axes', unicode_minus=False)

app = Flask(__name__)
app.secret_key = '1q2w3e4r5t'

with open('./logging.json', 'r') as file:
    config = json.load(file)
dictConfig(config)
app.logger

app.register_blueprint(seoul_bp, url_prefix='/seoul')
app.register_blueprint(covid_bp, url_prefix='/covid')
app.register_blueprint(carto_bp, url_prefix='/carto')
app.register_blueprint(crawl_bp, url_prefix='/crawl')
app.register_blueprint(stock_bp, url_prefix='/stock')
app.register_blueprint(cloud_bp, url_prefix='/cloud')
app.register_blueprint(clsft_bp, url_prefix='/class')
app.register_blueprint(upcls_bp, url_prefix='/upcls')
app.register_blueprint(regre_bp, url_prefix='/regre')
app.register_blueprint(clust_bp, url_prefix='/clust')
app.register_blueprint(lang_bp, url_prefix='/lang')

''' def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        app.logger.debug("get new weather info")
        weather = cur_weather()
        session['weather'] = weather
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)
    return weather '''

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main')
def main():
    menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 0, 'co': 0, 'ca': 0, 'cr': 0, 'st': 0, 'wc': 0}
    return render_template('main.html', menu=menu, weather=cur_weather())

@app.route('/MaLe')
def MaLe():
    menu = {'ho': 0, 'da': 0, 'ml': 1, 'cf': 0, 'ac': 0, 're': 0, 'cl': 0}
    return render_template('MaLe.html', menu=menu, weather=cur_weather())

if __name__ == '__main__':
    app.run(debug=True)