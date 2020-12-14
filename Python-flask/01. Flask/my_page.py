from flask import Flask, render_template, request, session, escape
from datetime import timedelta, datetime
from fbprophet import Prophet
import pandas as pd
import os
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