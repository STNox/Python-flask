from flask import Blueprint, render_template, request, current_app, redirect, url_for
import pandas as pd
import folium, os, json
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager
mpl.rc('font', family='Malgun Gothic')
mpl.rc('axes', unicode_minus=False)
from datetime import datetime
from utils.weather import cur_weather
import utils.covid_util as cu 
import DB.db_module as dm

covid_bp = Blueprint('covid_bp', __name__)

menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 0, 'co': 1, 'ca': 0, 'cr': 0, 'st': 0, 'wc': 0}

@covid_bp.route('/national_status')
def national_status():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    rows = dm.get_status(date)

    return render_template('covid/status.html', menu=menu, weather=cur_weather(), rows=rows, date=date)

@covid_bp.route('/update_status/<date>')
def update_status(date):
    rows = dm.get_status(date)
    if len(rows) == 0:
        cu.add_status(date)
    
    return redirect(url_for('covid_bp.national_status')+f'?date={date}')

@covid_bp.route('/age_gender')
def age_gender():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    rows = dm.get_age_gender(date)

    return render_template('covid/age_gender.html', menu=menu, weather=cur_weather(), rows=rows, date=date)

@covid_bp.route('/update_age_gender/<date>')
def update_age_gender(date):
    rows = dm.get_age_gender(date)
    if len(rows) == 0:
        cu.add_age_gender(date)

    return redirect(url_for('covid_bp.age_gender')+f'?date={date}')
    
@covid_bp.route('/abroad')
def abroad():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    rows = dm.get_abroad(date)

    return render_template('covid/abroad.html', menu=menu, weather=cur_weather(), rows=rows, date=date)

@covid_bp.route('/update_abroad/<date>')
def update_abroad(date):
    rows = dm.get_abroad(date)
    if len(rows) == 0:
        cu.add_abroad(date)
    
    return redirect(url_for('covid_bp.abroad')+f'?date={date}')

@covid_bp.route('/visual', methods=['GET', 'POST'])
def visual():
    if request.method == 'GET':
        rows, cols = dm.get_national_status()
        df = pd.DataFrame.from_records(data=rows, columns=cols)
        df.date = pd.to_datetime(df.date)
        df.plot(x='date', y='inc_decs', figsize=(20, 10))
        plt.xlabel('')
        plt.xticks(fontsize=20)
        plt.ylabel('신규 확진자(명)', fontsize=20)
        plt.yticks(fontsize=20)
        plt.grid(True)
        plt.legend().set_visible(False)
        img_file = os.path.join(current_app.root_path, 'static/img/cov_national.png')
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)
        regions = ['세종', '대전', '대구', '광주', '울산', '부산', '제주']

        return render_template('covid/visual.html', menu=menu, weather=cur_weather(), mtime=mtime, regions=regions)
    else:    
        dist = request.form['district']
        if dist == '수도권':
            rows, cols = dm.get_capital_area()
        elif dist =='광역시':
            rows, cols = dm.get_metropol()
        
        df = pd.DataFrame.from_records(data=rows, columns=cols)
        fig = df.plot(figsize=(12, 5))
        img_file = os.path.join(current_app.root_path, 'static/img/cov_metropol.png')
        fig.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)
        
        return render_template('covid/visual_res.html', menu=menu, weather=cur_weather(), mtime=mtime)
