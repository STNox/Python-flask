from flask import Blueprint, render_template, request, current_app
import pandas as pd
import os
from utils import drawkorea
from utils.weather import cur_weather

carto_bp = Blueprint('carto_bp', __name__)

menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 0, 'co': 0, 'ca': 1, 'cr': 0, 'st': 0, 'wc': 0}

@carto_bp.route('/pop_crisis/<option>')
def pop_cri(option):
    pop_cri = pd.read_csv('./static/data/pop_cri.csv')
    pop_cri['소멸위기지역'] = [1 if con else 0 for con in pop_cri['소멸위기지역']]
    columns = {'crisis_area': '소멸위기지역', 'crisis_ratio': '소멸비율'}
    carto_colors = {'crisis_area': 'Reds', 'crisis_ratio': 'PuBu'}
    img_file = os.path.join(current_app.root_path, 'static/img/pop_cri.png')
    drawkorea.drawKorea(columns[option], pop_cri, carto_colors[option], img_file)
    mtime = int(os.stat(img_file).st_mtime)
    return render_template('cartogram/pop_cri.html', menu=menu, weather=cur_weather(), mtime=mtime, option=option, columns=columns)

@carto_bp.route('/coffee', methods=['GET', 'POST'])
def coffee():
    if request.method == 'GET':
        return render_template('cartogram/coffee.html', menu=menu, weather=cur_weather())
    else:
        carto = request.form['carto_list']
        f = request.files['csv']
        filename = os.path.join(current_app.root_path, 'static/upload/') + f.filename
        f.save(filename)
        current_app.logger.info(f'{filename} is saved.')

        cafe_count = pd.read_csv(filename).set_index('Unnamed: 0')
        carto_colors = {'스타벅스 매장수': 'Greens', '이디야 매장수': 'Blues', '커피빈 매장수': 'YlOrBr', '빽다방 매장수': 'Oranges', '커피지수': 'copper_r'}
        img_file = os.path.join(current_app.root_path, 'static/img/coffee.png')
        drawkorea.drawKorea(carto, cafe_count, carto_colors[carto], img_file)
        mtime = int(os.stat(img_file).st_mtime)

        df = cafe_count.sort_values(by=carto, ascending=False)[['ID', carto]].reset_index()
        top10 = {}
        for i in range(10):
            top10[df['ID'][i]] = round(df[carto][i], 2)
        return render_template('cartogram/coffee_res.html', menu=menu, weather=cur_weather(), carto=carto, mtime=mtime, top10=top10)


