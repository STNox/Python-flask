from flask import Blueprint, render_template, request, current_app
import pandas as pd
import joblib, os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from utils.weather import cur_weather

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