from flask import Blueprint, render_template, request, current_app
import pandas as pd
import folium, os, json
from datetime import datetime
from utils.weather import cur_weather
import DB.covid_db as cov
import DB.db_module as dm

covid_bp = Blueprint('covid_bp', __name__)

menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 0, 'co': 1, 'ca': 0, 'cr': 0, 'st': 0, 'wc': 0}

@covid_bp.route('/national_status')
def national_status():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    rows = dm.get_status(date)

    return render_template('covid/status.html', menu=menu, weather=cur_weather(), rows=rows, date=date)

# DB 채워 넣고 화면에 띄우기
# covid_1.db 쓸 것