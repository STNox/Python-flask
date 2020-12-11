from flask import Flask, render_template, request, session
from datetime import timedelta
from weather import cur_weather
app = Flask(__name__)
app.secret_key = '1q2w3e4r5t'

def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        app.logger.info("get new weather info")
        weather = cur_weather()
        session['weather'] = weather
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)
    return weather

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/board')
def board():
    menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 0, 'co': 0, 'ca': 0, 'cr': 0, 'st': 0, 'wc': 0}
    return render_template('main.html', menu=menu, weather=get_weather_main())

if __name__ == '__main__':
    app.run(debug=True)