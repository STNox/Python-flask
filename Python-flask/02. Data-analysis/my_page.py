from flask import Flask, render_template, request, session, escape
from datetime import timedelta, datetime
from fbprophet import Prophet
import pandas as pd
import os, folium, json
import pandas_datareader as pdr
from weather import cur_weather
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager
mpl.rc('font', family='Malgun Gothic')
mpl.rc('axes', unicode_minus=False)
app = Flask(__name__)
app.secret_key = '1q2w3e4r5t'
kospi_dict = {}; kosdaq_dict = {}

def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        app.logger.debug("get new weather info")
        weather = cur_weather()
        session['weather'] = weather
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)
    return weather

@app.before_first_request
def before_first_request():
    kospi = pd.read_csv('./static/data/kospi_code.csv', dtype={'종목코드': str})
    for i in kospi.index:
        kospi_dict[kospi['종목코드'][i]] = kospi['기업명'][i]
    kosdaq = pd.read_csv('./static/data/kosdaq_code.csv', dtype={'종목코드': str})
    for i in kosdaq.index:
        kosdaq_dict[kosdaq['종목코드'][i]] = kosdaq['기업명'][i]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main')
def main():
    menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 0, 'co': 0, 'ca': 0, 'cr': 0, 'st': 0, 'wc': 0}
    return render_template('main.html', menu=menu, weather=get_weather_main())

@app.route('/seoul/park', methods=['GET', 'POST'])
def park():
    menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 1, 'co': 0, 'ca': 0, 'cr': 0, 'st': 0, 'wc': 0}
    park_new = pd.read_csv('./static/data/park_info.csv')
    if request.method == 'GET':
        map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
        for i in park_new.index:
            if park_new['공원크기'][i] == '대':
                folium.CircleMarker(
                    location=[park_new['위도'][i], park_new['경도'][i]],
                    radius=20,
                    color='blue', fill_color='blue',
                    tooltip=f"{park_new['공원명'][i]}({int(park_new['면적'][i])}㎡)"
                    ).add_to(map)
            elif park_new['공원크기'][i] == '중':
                folium.CircleMarker(
                    location=[park_new['위도'][i], park_new['경도'][i]],
                    radius=10,
                    color='blue', fill_color='blue',
                    tooltip=f"{park_new['공원명'][i]}({int(park_new['면적'][i])}㎡)"
                    ).add_to(map)
            else:
                folium.CircleMarker(
                    location=[park_new['위도'][i], park_new['경도'][i]],
                    radius=5,
                    color='blue', fill_color='blue',
                    tooltip=f"{park_new['공원명'][i]}({int(park_new['면적'][i])}㎡)"
                    ).add_to(map)
        
        html_file = os.path.join(app.root_path, 'static/img/park.html')
        map.save(html_file)
        mtime = int(os.stat(html_file).st_mtime)
        return render_template('park.html', menu=menu, weather=get_weather_main(), park_list=list(park_new['공원명'].values), dist_list=set(park_new['구별'].values), mtime=mtime)
    else:
        distinct = request.form['distinct']
        if distinct == 'name':
            park_name = request.form['name']
            df = park_new[park_new['공원명'] == park_name].reset_index()
            park_result = {'name': park_name, 'addr': df['주소'][0], 'area': df['면적'][0], 'desc': df['공원개요'][0]}
            map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
            for i in park_new.index:
                if park_new['공원크기'][i] == '대':
                    folium.CircleMarker(
                        location=[park_new['위도'][i], park_new['경도'][i]],
                        radius=20,
                        color='blue', fill_color='blue',
                        tooltip=f"{park_new['공원명'][i]}({int(park_new['면적'][i])}㎡)"
                        ).add_to(map)
                elif park_new['공원크기'][i] == '중':
                    folium.CircleMarker(
                        location=[park_new['위도'][i], park_new['경도'][i]],
                        radius=10,
                        color='blue', fill_color='blue',
                        tooltip=f"{park_new['공원명'][i]}({int(park_new['면적'][i])}㎡)"
                        ).add_to(map)
                else:
                    folium.CircleMarker(
                        location=[park_new['위도'][i], park_new['경도'][i]],
                        radius=5,
                        color='blue', fill_color='blue',
                        tooltip=f"{park_new['공원명'][i]}({int(park_new['면적'][i])}㎡)"
                        ).add_to(map)
            if df['공원크기'][0] == '대':
                folium.CircleMarker(
                    [df['위도'][0], df['경도'][0]], radius=20,
                    tooltip=f"{df['공원명'][0]}({int(df['면적'][0])}㎡)",
                    color='crimson', fill_color='crimson').add_to(map)
            elif df['공원크기'][0] == '중':
                folium.CircleMarker(
                    [df['위도'][0], df['경도'][0]], radius=10,
                    tooltip=f"{df['공원명'][0]}({int(df['면적'][0])}㎡)",
                    color='crimson', fill_color='crimson').add_to(map)
            else:
                folium.CircleMarker(
                    [df['위도'][0], df['경도'][0]], radius=5,
                    tooltip=f"{df['공원명'][0]}({int(df['면적'][0])}㎡)",
                    color='crimson', fill_color='crimson').add_to(map)
            html_file = os.path.join(app.root_path, 'static/img/park_res.html')
            map.save(html_file)
            mtime = int(os.stat(html_file).st_mtime)
            return render_template('park_res.html', menu=menu, weather=get_weather_main(), park_result=park_result, mtime=mtime)
        else:
            dist_name = request.form['dist']
            dist_info = pd.read_csv('./static/data/dist_info.csv')
            df = dist_info[dist_info['구별'] == dist_name].reset_index()
            df2 = park_new[park_new['구별'] == dist_name].reset_index()
            dist_result = {
                'dist': dist_name, 
                'area': round(float(df['공원면적합'][0]) * 1000000, 2), 
                'count': df['공원수'][0],
                'area_ratio': round(float(df['공원면적비'][0]), 2),
                'app': round(float(df['1인당공원면적'][0]) * 1000000, 2),
                'area_mean': round(float(dist_info['공원면적합'].mean()) * 1000000, 2),
                'count_mean': round(float(dist_info['공원수'].mean()), 2),
                'ar_mean': round(float(dist_info['공원면적비'].mean()), 2),
                'app_mean': round(float(dist_info['1인당공원면적'].mean()) * 1000000, 2)}
            map = folium.Map(location=[df['위도'][0], df['경도'][0]], zoom_start=13)
            for i in df2.index:
                if df2['공원크기'][i] == '대':
                    folium.CircleMarker(
                        location=[df2['위도'][i], df2['경도'][i]],
                        radius=20,
                        color='blue', fill_color='blue',
                        tooltip=f"{df2['공원명'][i]}({int(df2['면적'][i])}㎡)"
                        ).add_to(map)
                elif df2['공원크기'][i] == '중':
                    folium.CircleMarker(
                        location=[df2['위도'][i], df2['경도'][i]],
                        radius=10,
                        color='blue', fill_color='blue',
                        tooltip=f"{df2['공원명'][i]}({int(df2['면적'][i])}㎡)"
                        ).add_to(map)
                else:
                    folium.CircleMarker(
                        location=[df2['위도'][i], df2['경도'][i]],
                        radius=5,
                        color='blue', fill_color='blue',
                        tooltip=f"{df2['공원명'][i]}({int(df2['면적'][i])}㎡)"
                        ).add_to(map)
            html_file = os.path.join(app.root_path, 'static/img/park_res_dist.html')
            map.save(html_file)
            mtime = int(os.stat(html_file).st_mtime)
            return render_template('park_res_dist.html', menu=menu, weather=get_weather_main(), dist_result=dist_result, mtime=mtime)

@app.route('/seoul/park_de/<option>')
def park_de(option):
    menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 1, 'co': 0, 'ca': 0, 'cr': 0, 'st': 0, 'wc': 0}
    park_new = pd.read_csv('./static/data/park_info.csv')
    dist_info = pd.read_csv('./static/data/dist_info.csv')
    dist_info.set_index('구별', inplace=True)
    geo_str = json.load(open('./static/data/02. skorea_municipalities_geo_simple.json', encoding='utf8'))
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='Stamen Toner')
    if option == 'area':
        map.choropleth(geo_data = geo_str,
                       data = dist_info['공원면적합'],
                       columns = [dist_info.index, dist_info['공원면적합']],
                       fill_color = 'PuRd',
                       key_on = 'feature.id')
    elif option == 'count':
        map.choropleth(geo_data = geo_str,
                       data = dist_info['공원수'],
                       columns = [dist_info.index, dist_info['공원수']],
                       fill_color = 'PuRd',
                       key_on = 'feature.id')
    elif option == 'area_ratio':
        map.choropleth(geo_data = geo_str,
                       data = dist_info['공원면적비'],
                       columns = [dist_info.index, dist_info['공원면적비']],
                       fill_color = 'PuRd',
                       key_on = 'feature.id')
    elif option == 'per_person':
        map.choropleth(geo_data = geo_str,
                       data = dist_info['1인당공원면적'],
                       columns = [dist_info.index, dist_info['1인당공원면적']],
                       fill_color = 'PuRd',
                       key_on = 'feature.id')

    for i in park_new.index:
        folium.CircleMarker([park_new['위도'][i], park_new['경도'][i]], 
                        radius=int(park_new['면적'][i] / 2000000),
                        tooltip=f"{park_new['공원명'][i]}({int(park_new['면적'][i])}㎡)",
                        color='green', fill_color='green').add_to(map)
    html_file = os.path.join(app.root_path, 'static/img/park_de.html')
    map.save(html_file)
    mtime = int(os.stat(html_file).st_mtime)
    option_dict = {'area':'공원면적', 'count':'공원수', 'area_ratio':'공원면적 비율', 'per_person':'인당 공원면적'}
    return render_template('park_de.html', menu=menu, weather=get_weather_main(),
                            option=option, option_dict=option_dict, mtime=mtime)

@app.route('/stock', methods=['GET', 'POST'])
def stock():
    menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 0, 'co': 0, 'ca': 0, 'cr': 0, 'st': 1, 'wc': 0}
    if request.method == 'GET':
        return render_template('stock.html', menu=menu, weather=get_weather_main(), kospi=kospi_dict, kosdaq=kosdaq_dict)
    else:
        market = request.form['market']
        if market == 'KS':
            code = request.form['kospi_code']
            comp_name = kospi_dict[code]
            code += '.KS'
        else:
            code = request.form['kosdaq_code']
            comp_name = kosdaq_dict[code]
            code += '.KQ'
        learn_period = int(request.form['learn'])
        pred_period = int(request.form['pred'])
        today = datetime.now()
        start_learn = today - timedelta(days=learn_period * 365)
        end_learn = today - timedelta(days=1)

        stock_data = pdr.DataReader(code, data_source='yahoo', start=start_learn, end=end_learn)
        df = pd.DataFrame({'ds': stock_data.index, 'y': stock_data.Close})
        df.reset_index(inplace=True)
        del df['Date']

        model = Prophet(daily_seasonality=True)
        model.fit(df)
        future = model.make_future_dataframe(periods=pred_period)
        forecast = model.predict(future)
        
        fig = model.plot(forecast);
        img_file = os.path.join(app.root_path, 'static/img/stock.png')
        fig.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)  

        return render_template('stock_res.html', menu=menu, weather=get_weather_main(), mtime=mtime, comp_name=comp_name)


if __name__ == '__main__':
    app.run(debug=True)