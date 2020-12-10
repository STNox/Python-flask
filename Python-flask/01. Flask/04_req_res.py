from flask import Flask, render_template, request
from flask import Response, make_response
app = Flask(__name__)

@app.route('/area')
def area():
    radius = request.args['radius']                # request.values['']도 가능
    pi = request.args.get('pi', '3.14')
    s = float(pi) * float(radius) * float(radius)
    return f'pi={pi}, radius={radius}, area={s}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('03.login.html')
    else:
        uid = request.form['uid']
        pwd = request.form['pwd']
        return f'uid={uid}, pwd={pwd}'

@app.route('/response')
def response_fn():
    custom_res = Response('Custom Response', 200, {'test': 'ttt'})
    return make_response(custom_res)

if __name__ == '__main__':
    app.run(debug=True)
