from flask import Flask, render_template, request
import os
app = Flask(__name__)

@app.route('/')
def index():
    img_file = os.path.join(app.root_path, 'static/img/hanguel.png')
    mtime = int(os.stat(img_file).st_mtime)                         # 파일 이름 변경 즉각 적용
    return render_template('05.index.html', mtime=mtime)

if __name__ == '__main__':
    app.run(debug=True)