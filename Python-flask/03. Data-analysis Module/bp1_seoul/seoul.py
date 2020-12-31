from flask import Blueprint, render_template, request, current_app
import pandas as pd
import folium, os, json
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager
mpl.rc('font', family='Malgun Gothic')
mpl.rc('axes', unicode_minus=False)
from utils.weather import cur_weather

seoul_bp = Blueprint('seoul_bp', __name__)

menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 1, 'co': 0, 'ca': 0, 'cr': 0, 'st': 0, 'wc': 0}
park_new = pd.read_csv('./static/data/park_info.csv')
dist_info = pd.read_csv('./static/data/dist_info.csv')
dist_info.set_index('구별', inplace=True)
crimes = pd.read_csv('./static/data/crime_in_Seoul.csv')
pol_cov = pd.read_csv('./static/data/pol_cov.csv')
crimes.set_index('구별', inplace=True)
geo_str = json.load(open('./static/data/02. skorea_municipalities_geo_simple.json', encoding='utf8'))


@seoul_bp.route('/park', methods=['GET', 'POST'])
def park():
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
        
        html_file = os.path.join(current_app.root_path, 'static/img/park.html')
        map.save(html_file)
        mtime = int(os.stat(html_file).st_mtime)
        return render_template(
            'seoul/park.html', 
            menu=menu, 
            weather=cur_weather(), 
            park_list=list(park_new['공원명'].values), 
            dist_list=set(park_new['구별'].values), 
            mtime=mtime
            )
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
            html_file = os.path.join(current_app.root_path, 'static/img/park_res.html')
            map.save(html_file)
            mtime = int(os.stat(html_file).st_mtime)
            return render_template(
                'seoul/park_res.html', 
                menu=menu, 
                weather=cur_weather(), 
                park_result=park_result, 
                mtime=mtime
                )
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
            html_file = os.path.join(current_app.root_path, 'static/img/park_res_dist.html')
            map.save(html_file)
            mtime = int(os.stat(html_file).st_mtime)
            return render_template(
                'seoul/park_res_dist.html', 
                menu=menu, 
                weather=cur_weather(), 
                dist_result=dist_result, 
                mtime=mtime
                )

@seoul_bp.route('/park_de/<option>')
def park_de(option):
    current_app.logger.warning("var error")
    option_dict = {'area':'공원면적합', 'count':'공원수', 'area_ratio':'공원면적비', 'per_person':'1인당공원면적'}
    column_index = option_dict[option]
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='Stamen Toner')
    map.choropleth(
        geo_data = geo_str, 
        data = dist_info[column_index], 
        columns = [dist_info.index, dist_info[column_index]], 
        fill_color = 'PuRd', 
        key_on = 'feature.id'
        )

    for i in park_new.index:
        folium.CircleMarker([park_new['위도'][i], park_new['경도'][i]], 
                        radius=int(park_new['면적'][i] / 2000000),
                        tooltip=f"{park_new['공원명'][i]}({int(park_new['면적'][i])}㎡)",
                        color='green', fill_color='green').add_to(map)
    html_file = os.path.join(current_app.root_path, 'static/img/park_de.html')
    map.save(html_file)
    mtime = int(os.stat(html_file).st_mtime)
    return render_template('seoul/park_de.html', menu=menu, weather=cur_weather(),
                            option=option, option_dict=option_dict, mtime=mtime)

@seoul_bp.route('/crime')
def crime():
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
    map.choropleth(
        geo_data= geo_str, 
        data= crimes['범죄'], 
        columns= [crimes.index, crimes['범죄']], 
        fill_color= 'PuRd', 
        key_on= 'feature.id'
        )

    for n in pol_cov.index:
        folium.CircleMarker(
            [pol_cov['lat'][n], pol_cov['lng'][n]], 
            radius=pol_cov['검거'][n] * 10, 
            color='#3186cc', 
            fill_color='#3186cc'
            ).add_to(map)

    html_file = os.path.join(current_app.root_path, 'static/img/crime.html')
    map.save(html_file)
    mtime = int(os.stat(html_file).st_mtime)
    return render_template('seoul/crime.html', menu=menu, weather=cur_weather(), mtime=mtime)

@seoul_bp.route('/crime_de/<option>')
def crime_de(option):
    current_app.logger.warning('var error')
    option_dict1 = {'violence': '폭력', 'rape': '강간', 'robbery': '강도', 'murder': '살인', 'theft': '절도'}
    option_dict2 = {
        'violence_arr': '폭력검거율', 
        'rape_arr': '강간검거율', 
        'robbery_arr': '강도검거율', 
        'murder_arr': '살인검거율', 
        'theft_arr': '절도검거율'}
    if option in list(option_dict1.keys()):
        column_index = option_dict1[option]
        map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
        map.choropleth(
            geo_data= geo_str, 
            data= crimes[column_index], 
            columns= [crimes.index, crimes[column_index]], 
            fill_color= 'PuRd', key_on= 'feature.id'
            )
    elif option in list(option_dict2.keys()):
        column_index = option_dict2[option]
        map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
        map.choropleth(
            geo_data= geo_str, 
            data= crimes[column_index], 
            columns= [crimes.index, crimes[column_index]], 
            fill_color= 'RdYlBu', key_on= 'feature.id'
            )
    
    html_file = os.path.join(current_app.root_path, 'static/img/crime_de.html')
    map.save(html_file)
    mtime = int(os.stat(html_file).st_mtime)
    return render_template(
        'seoul/crime_de.html', 
        menu=menu, 
        weather=cur_weather(), 
        option=option, 
        option_dict1=option_dict1, 
        option_dict2=option_dict2, 
        column_index=column_index, 
        mtime=mtime
        )

@seoul_bp.route('/cctv', methods=['GET', 'POST'])
def cctv():
    cctv = pd.read_csv('./static/data/CCTV_result.csv')
    cctv['cctv비율'] = cctv['소계'] / cctv['인구수'] * 100
    cctv.set_index('구별', inplace=True)
    if request.method == 'GET':
        map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='CartoDB Positron')
        map.choropleth(
            geo_data=geo_str, 
            data=cctv['소계'], 
            columns=[cctv.index, cctv['소계']], 
            fill_color='Blues', 
            key_on='feature.id'
            )
        
        html_file = os.path.join(current_app.root_path, 'static/img/cctv.html')
        map.save(html_file)
        mtime = int(os.stat(html_file).st_mtime)

        return render_template('seoul/cctv.html', menu=menu, weather=cur_weather(), mtime=mtime)
    else:
        kind = request.form['kind']
        cctv[kind].sort_values().plot(kind='barh', grid=True, figsize=(12, 10))
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=15)
        plt.grid(True)
        img_file = os.path.join(current_app.root_path, 'static/img/cctv.png')
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        return render_template('seoul/cctv_res.html', menu=menu, weather=cur_weather(), mtime=mtime, kind=kind)