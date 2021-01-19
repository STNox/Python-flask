from flask import Blueprint, render_template, request, current_app
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler
from utils.weather import cur_weather

clsft_bp = Blueprint('clsft_bp', __name__)

menu = {'ho': 0, 'da': 0, 'ml': 1, 'cf': 1, 'ac': 0, 're': 0, 'cl': 0}

@clsft_bp.route('/cancer', methods=['GET', 'POST'])
def cancer():
    if request.method == 'GET':
        return render_template('class/cancer.html', menu=menu, weather=cur_weather())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('./static/data/cancer_test.csv')
        scaler = MinMaxScaler()
        scaled_X = scaler.fit_transform(df.iloc[:, :-1])
        X_test = scaled_X[index, :].reshape(1, -1)
        X_test_dtc = df.iloc[index, :-1].values.reshape(1, -1)
        label = df.iloc[index, -1]
        lr = joblib.load('./static/model/cancer_lr.pkl')
        dt = joblib.load('./static/model/cancer_dt.pkl')
        sv = joblib.load('./static/model/cancer_sv.pkl')
        pred_lr = lr.predict(X_test)
        pred_dt = dt.predict(X_test_dtc)
        pred_sv = sv.predict(X_test)
        result = {'label': label, 'index': index, 'pred_lr': pred_lr[0], 'pred_dt': pred_dt[0], 'pred_sv': pred_sv[0]}

        return render_template('class/cancer_res.html', menu=menu, weather=cur_weather(), result=result)

@clsft_bp.route('/pima', methods=['GET', 'POST'])
def pima():
    if request.method == 'GET':
        return render_template('class/pima.html', menu=menu, weather=cur_weather())
    else:
        index = int(request.form['index'])