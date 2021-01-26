from flask import Blueprint, render_template, request, current_app
import pandas as pd
import joblib, os
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_digits
from utils.weather import cur_weather

upcls_bp = Blueprint('upcls_bp', __name__)

menu = {'ho': 0, 'da': 0, 'ml': 1, 'cf': 0, 'ac': 1, 're': 0, 'cl': 0}
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

