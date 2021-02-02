from flask import Blueprint, render_template, request, current_app
import pandas as pd
import json, requests, os
from utils.weather import cur_weather
from urllib.parse import quote

lang_bp = Blueprint('lang_bp', __name__)

with open('./static/keys/naver_key.json') as nkey:
    json_str = nkey.read(100)
json_obj = json.loads(json_str)
naver_id = list(json_obj.keys())[0]
naver_secret = json_obj[naver_id]
trans_headers = {
    "X-NCP-APIGW-API-KEY-ID": naver_id,
    "X-NCP-APIGW-API-KEY": naver_secret
}
tts_headers = {
    "X-NCP-APIGW-API-KEY-ID": naver_id,
    "X-NCP-APIGW-API-KEY": naver_secret,
    "Content-Type": "application/x-www-form-urlencoded"
}
naver_url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
tts_url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
lang_for_naver = {
    'Korean': 'ko',
    'Chinese': 'zh-CN',
    'Japanese': 'ja',
    'English': 'en',
    'French': 'fr'
}

with open('./static/keys/kakaokey.txt') as kkey:
    kakao_key = kkey.read(100)
def kakao_url(text, src, dst):
    return f'https://dapi.kakao.com/v2/translation/translate?query={quote(text)}&src_lang={src}&target_lang={dst}'
lang_for_kakao = {
    'Korean': 'kr',
    'Chinese': 'cn',
    'Japanese': 'jp',
    'English': 'en',
    'French': 'fr'
}

menu = {'ho': 0, 'da': 0, 'ml': 1, 'cf': 0, 'ac': 0, 're': 0, 'cl': 0, 'la': 1}

@lang_bp.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'GET':
        return render_template('/language/trans.html', menu=menu, weather=cur_weather())
    else:
        text = request.form['text']
        lang = request.form['lang']
        val = {
            'source': 'ko',
            'target': lang_for_naver[lang],
            'text': text
        }
        naver_res = requests.post(naver_url, data=val, headers=trans_headers)
        rescode = naver_res.status_code
        if rescode == 200:
            naver_result = naver_res.json()
            naver_res_text = naver_result['message']['result']['translatedText']
        else:
            print("Error : " + naver_res.text)
        
        kakao_result = requests.get(kakao_url(text, 'kr', lang_for_kakao[lang]), headers={"Authorization": "KakaoAK " + kakao_key}).json()
        kakao_res = kakao_result['translated_text'][0]
        kakao_res_text = ''
        for element in kakao_res:
            kakao_res_text += (element + ' ')
        result = {'text': text, 'lang': lang, 'naver': naver_res_text, 'kakao': kakao_res_text}

        return render_template('/language/trans_res.html', menu=menu, weather=cur_weather(), result=result)

@lang_bp.route('/tts', methods=['GET', 'POST'])
def tts():
    if request.method == 'GET':
        return render_template('/language/tts.html', menu=menu, weather=cur_weather())
    else:
        text = request.form['text']
        speaker = request.form['speaker']
        speed = request.form['speed']
        pitch = request.form['pitch']
        emotion = request.form['emotion']
        val = {
            'speaker': speaker,
            'speed': speed,
            'pitch': pitch,
            'emotion': emotion,
            'text': text
        }
        response = requests.post(tts_url, data=val, headers=tts_headers)
        rescode = response.status_code
        audio_file = os.path.join(current_app.root_path, 'static/voice/tts.mp3')
        if(rescode == 200):
            print(rescode)
            with open(audio_file, 'wb') as f:
                f.write(response.content)
        else:
            print("Error : " + response.text)
        mtime = int(os.stat(audio_file).st_mtime)
        
        info = {'text': text, 'speaker': speaker, 'speed': speed, 'pitch': pitch, 'emotion': emotion}

        return render_template('/language/tts_res.html', menu=menu, weather=cur_weather(), info=info, mtime=mtime)