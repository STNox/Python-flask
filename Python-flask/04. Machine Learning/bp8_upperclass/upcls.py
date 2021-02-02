from flask import Blueprint, render_template, request, current_app
import pandas as pd
import joblib, os
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_digits
from utils.weather import cur_weather

upcls_bp = Blueprint('upcls_bp', __name__)

menu = {'ho': 0, 'da': 0, 'ml': 1, 'cf': 0, 'ac': 1, 're': 0, 'cl': 0, 'la': 0}
scaler = MinMaxScaler()
digits = load_digits()

@upcls_bp.route('/mnist', methods=['GET', 'POST'])
def mnist():
    if request.method == 'GET':
        return render_template('/upperclass/mnist.html', menu=menu, weather=cur_weather())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('./static/data/digits_test.csv')
        img_index = df.iloc[index:index+5, 0].values
        scaled_df = scaler.fit_transform(df.drop(columns=['index', 'target'], axis=1))
        X_data = scaled_df[index:index+5, :]
        label = df.iloc[index:index+5, -1].values
        lr = joblib.load('./static/model/digits_lr.pkl')
        sv = joblib.load('./static/model/digits_sv.pkl')
        rf = joblib.load('./static/model/digits_rf.pkl')
        pred_lr = lr.predict(X_data)
        pred_sv = sv.predict(X_data)
        pred_rf = rf.predict(X_data)
        result_dict = {'index': img_index, 'label': label, 'pred_lr': pred_lr, 'pred_sv': pred_sv, 'pred_rf': pred_rf}

        for i, j in enumerate(img_index):
            num = str(i+1)
            plt.figure(figsize=(2, 2))
            plt.xticks([]); plt.yticks([])
            img_file = os.path.join(current_app.root_path, f'static/img/digits{num}.png')
            plt.imshow(digits.images[j], cmap=plt.cm.binary, interpolation='nearest')
            plt.savefig(img_file)
            mtime = int(os.stat(img_file).st_mtime)
        
        return render_template('/upperclass/mnist_res.html', menu=menu, weather=cur_weather(), dict=result_dict, mtime=mtime)

@upcls_bp.route('/20news', methods=['GET', 'POST'])
def newsgroups():
    if request.method == 'GET':
        return render_template('/upperclass/20news.html', menu=menu, weather=cur_weather())
    else:
        index = int(request.form['index'])

@upcls_bp.route('/IMDB', methods=['GET', 'POST'])
def imdb():
    if request.method == 'GET':
        return render_template('/upperclass/imdb.html', menu=menu, weather=cur_weather())
    else:
        select = request.form['select']
        df = pd.read_csv('./static/data/imdb_test.csv')
        cvlr = joblib.load('./static/model/imdb_cvlr.pkl')
        tvlr = joblib.load('./static/model/imdb_tvlr.pkl')
        if select == 'text':
            review = request.form['review']
        else:
            index = int(request.form['index'] or '0')
            review = df.loc[index, 'review']
        pred_cvlr = cvlr.predict([review])
        pred_tvlr = tvlr.predict([review])
        p_c = '긍정' if pred_cvlr == 1 else '부정'
        p_t = '긍정' if pred_tvlr == 1 else '부정'

        return render_template('/upperclass/imdb_res.html', menu=menu, weather=cur_weather(), p_c=p_c, p_t=p_t, review=review)

@upcls_bp.route('/NaverMovie', methods=['GET', 'POST'])
def naver():
    if request.method == 'GET':
        return render_template('/upperclass/naver.html', menu=menu, weather=cur_weather())
    else:
        select = request.form['select']
        df = pd.read_csv('./static/data/NaverMovie/test.tsv', sep='\t')
        cvlr = joblib.load('./static/model/nm_cl.pkl')
        cvnb = joblib.load('./static/model/nm_cn.pkl')
        tvlr = joblib.load('./static/model/nm_tl.pkl')
        tvnb = joblib.load('./static/model/nm_tn.pkl')
        if select == 'text':
            review = request.form['review']
        else:
            index = int(request.form['index'] or '0')
            review = df.loc[index, 'document']
        pred_cvlr = cvlr.predict([review])
        pred_cvnb = cvnb.predict([review])
        pred_tvlr = tvlr.predict([review])
        pred_tvnb = cvnb.predict([review])
        p_cl = '긍정' if pred_cvlr == 1 else '부정'
        p_cn = '긍정' if pred_cvnb == 1 else '부정'
        p_tl = '긍정' if pred_tvlr == 1 else '부정'
        p_tn = '긍정' if pred_tvnb == 1 else '부정'
        result = {'review': review, 'p_cl': p_cl, 'p_cn': p_cn, 'p_tl': p_tl, 'p_tn': p_tn}
        
        return render_template('/upperclass/naver_res.html', menu=menu, weather=cur_weather(), result=result)