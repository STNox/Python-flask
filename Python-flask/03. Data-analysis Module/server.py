from flask import Flask, render_template
from weather import cur_weather
from bp1_seoul.seoul import seoul_bp
#from bp2_covid.covid import covid_bp
#from bp3_cartogram.carto import carto_bp
#from bp4_crawling.crawl import crawl_bp
from bp5_stock.simple import simple_bp
from bp5_stock.stock import stock_bp
#from bp6_wordcloud.cloud import cloud_bp

app = Flask(__name__)
app.register_blueprint(simple_bp, url_prefix='/simple')
app.register_blueprint(stock_bp, url_prefix='/stock')
app.register_blueprint(seoul_bp, url_prefix='/seoul')


@app.route('/')
def index():
    return 'Index Page'

@app.route('/main')
def main():
    menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 0, 'co': 0, 'ca': 0, 'cr': 0, 'st': 0, 'wc': 0}
    return render_template('main.html', menu=menu, weather=cur_weather())

if __name__ == '__main__':
    app.run(debug=True)