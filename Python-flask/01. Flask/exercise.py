from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/carousel')
def carousel():
    return render_template('carousel.html')

@app.route('/table')
def table():
    return render_template('table.html')


if __name__ == '__main__':
    app.run(debug=True)