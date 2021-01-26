from flask import Blueprint, render_template, request, current_app
import pandas as pd
import numpy as np
import joblib, os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from utils.weather import cur_weather
from utils.scatter import get_scatter

regre_bp = Blueprint('regre_bp', __name__)

menu = {'ho': 0, 'da': 0, 'ml': 1, 'cf': 0, 'ac': 0, 're': 1, 'cl': 0}

@regre_bp.route('/iris', methods=['GET', 'POST'])
def iris():
    if request.method == 'GET':
        return render_template('/regression/iris.html', menu=menu, weather=cur_weather())
    else:
        feature_dict = {
            'sl': 'sepal length (cm)',
            'sw': 'sepal width (cm)',
            'pl': 'petal length (cm)',
            'pw': 'petal width (cm)'
        }
        index = int(request.form['index'])
        feature = request.form['feature']
        ft_name = feature_dict[feature]
        del feature_dict[feature]
        df = pd.read_csv('./static/data/iris_test.csv')
        X = df.iloc[index, :]
        lr = joblib.load(f'./static/model/iris_{feature}_lr.pkl')
        weight = lr.coef_
        bias = lr.intercept_
        pred = round(weight[0] * X[list(feature_dict.values())[0]] + weight[1] * X[list(feature_dict.values())[1]] + weight[2] * X[list(feature_dict.values())[2]] + weight[3] * X['target'] + bias, 2)
        # np.dot 활용
        return render_template(
            '/regression/iris_res.html', 
            menu=menu, weather=cur_weather(), 
            pred=pred, index=index, feature=feature, 
            X=X, ft_name=ft_name
        )

@regre_bp.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    df = pd.read_csv('./static/data/diabetes_test.csv')
    feature_list = df.columns.tolist()[:-1]
    if request.method == 'GET':
        return render_template('/regression/diabetes.html', menu=menu, weather=cur_weather(), list=feature_list)
    else:
        index = int(request.form['index'])
        feature = request.form['feature']
        X = df.loc[index, feature]
        label = df.iloc[index, -1]
        lr = joblib.load(f'./static/model/diabetes_{feature}_lr.pkl')
        weight = lr.coef_
        bias = lr.intercept_
        mtime = get_scatter(df[feature], df.iloc[:, -1], weight, bias)
        pred = round((X * weight + bias)[0], 2)

        return render_template(
            '/regression/diabetes_res.html', 
            menu=menu, weather=cur_weather(), 
            pred=pred, index=index, feature=feature,
            list=feature_list, label=label, mtime=mtime
        )

@regre_bp.route('/boston', methods=['GET', 'POST'])
def boston():
    df = pd.read_csv('./static/data/boston_test.csv')
    columns = df.columns.tolist()[:-1]
    if request.method == 'GET':
        return render_template('/regression/boston.html', menu=menu, weather=cur_weather(), columns=columns)
    else:
        index = int(request.form['index'])
        feature = request.form.getlist('feature')
        fts = ', '.join(str(ft) for ft in feature)
        feature_dict = dict(zip(columns, [0] * len(columns)))
        for f in feature:
            feature_dict.update({f: 1})
        temp = np.array(list(feature_dict.values()))
        X = df.iloc[index, :-1].values
        temp_X = temp * X
        label = df.iloc[index, -1]
        lr = joblib.load('./static/model/boston_lr.pkl')
        weight, bias = lr.coef_, lr.intercept_
        pred = round(np.dot(temp_X, weight) + bias, 2)
        result = {'index': index, 'label': label, 'feature': fts, 'pred': pred}

        return render_template('/regression/boston_res.html', menu=menu, weather=cur_weather(), dict=result)