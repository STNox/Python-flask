from flask import Blueprint, render_template, request, current_app, redirect, url_for
import pandas as pd
from utils.weather import cur_weather
from utils import crawling as cr

crawl_bp = Blueprint('crawl_bp', __name__)

menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 0, 'co': 0, 'ca': 0, 'cr': 1, 'st': 0, 'wc': 0}

@crawl_bp.route('/chart')
def m_chart():
    bugs = cr.bugs_chart()
    melon = cr.melon_chart()
    genie = cr.genie_chart()

    return render_template('crawl/chart.html', menu=menu, weather=cur_weather(), bugs=bugs, melon=melon, genie=genie)
