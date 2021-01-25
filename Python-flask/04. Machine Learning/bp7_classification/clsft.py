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
        df = pd.read_csv('./static/data/pima_test.csv')
        scaler = MinMaxScaler()
        scaled_X = scaler.fit_transform(df.iloc[:, :-1])
        X = scaled_X[index, :].reshape(1, -1)
        label = df.iloc[index, -1]
        lr = joblib.load('./static/model/pima_lr.pkl')
        sv = joblib.load('./static/model/pima_sv.pkl')
        dt = joblib.load('./static/model/pima_dt.pkl')
        rf = joblib.load('./static/model/pima_rf.pkl')
        pred_lr = lr.predict(X)
        pred_sv = sv.predict(X)
        pred_dt = dt.predict(X)
        pred_rf = rf.predict(X)
        result = {'label': label, 'index': index, 'pred_lr': pred_lr[0], 'pred_sv': pred_sv[0], 'pred_dt': pred_dt[0], 'pred_rf': pred_rf[0]}

        return render_template('class/pima_res.html', menu=menu, weather=cur_weather(), dict=result)

@clsft_bp.route('/titanic', methods=['GET', 'POST'])
def titanic():
    if request.method == 'GET':
        return render_template('class/titanic.html', menu=menu, weather=cur_weather())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('./static/data/titanic_test.csv')
        X = df.iloc[index, :-1].values.reshape(1, -1)
        label = df.iloc[index, -1]
        lr = joblib.load('./static/model/titanic_lr.pkl')
        sv = joblib.load('./static/model/titanic_sv.pkl')
        dt = joblib.load('./static/model/titanic_dt.pkl')
        rf = joblib.load('./static/model/titanic_rf.pkl')
        pred_lr = lr.predict(X)
        pred_sv = sv.predict(X)
        pred_dt = dt.predict(X)
        pred_rf = rf.predict(X)
        result = {'label': label, 'index': index, 'pred_lr': pred_lr[0], 'pred_sv': pred_sv[0], 'pred_dt': pred_dt[0], 'pred_rf': pred_rf[0]}

        return render_template('class/titanic_res.html', menu=menu, weather=cur_weather(), dict=result)

@clsft_bp.route('/iris', methods=['GET', 'POST'])
def iris():
    if request.method == 'GET':
        return render_template('class/iris.html', menu=menu, weather=cur_weather())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('./static/data/iris_test.csv')
        X = df.iloc[index, :-1].values.reshape(1, -1)
        label = df.iloc[index, -1]
        dt = joblib.load('./static/model/iris_dt.pkl')
        rf = joblib.load('./static/model/iris_rf.pkl')
        kn = joblib.load('./static/model/iris_kn.pkl')
        pred_dt = dt.predict(X)
        pred_rf = rf.predict(X)
        pred_kn = kn.predict(X)
        result = {'label': label, 'index': index, 'pred_dt': pred_dt[0], 'pred_rf': pred_rf[0], 'pred_kn': pred_kn[0]}

        return render_template('class/iris_res.html', menu=menu, weather=cur_weather(), dict=result)

@clsft_bp.route('/wine', methods=['GET', 'POST'])
def wine():
    if request.method == 'GET':
        return render_template('class/wine.html', menu=menu, weather=cur_weather())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('./static/data/wine_test.csv')
        X = df.iloc[index, :-1].values.reshape(1, -1)
        label = df.iloc[index, -1]
        dt = joblib.load('./static/model/wine_dt.pkl')
        rf = joblib.load('./static/model/wine_rf.pkl')
        kn = joblib.load('./static/model/wine_kn.pkl')
        pred_dt = dt.predict(X)
        pred_rf = rf.predict(X)
        pred_kn = kn.predict(X)
        result = {'label': label, 'index': index, 'pred_dt': pred_dt[0], 'pred_rf': pred_rf[0], 'pred_kn': pred_kn[0]}

        return render_template('class/wine_res.html', menu=menu, weather=cur_weather(), dict=result)
