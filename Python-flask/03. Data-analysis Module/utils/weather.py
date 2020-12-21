import requests
from urllib.parse import urlparse

def cur_weather():

    key_fd = open('weatherkey.txt', mode='r')
    openweather_key = key_fd.read(100)
    key_fd.close()
 
    lat = 37.5509655; lng = 126.849532 
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={openweather_key}&units=metric&lang=kr'
    result = requests.get(urlparse(url).geturl()).json()

    main = result['weather'][0]['main']
    desc = result['weather'][0]['description']
    icon = result['weather'][0]['icon']
    temp = result['main']['temp']
    temp_min = result['main']['temp_min']
    temp_max = result['main']['temp_max']
    temp = round(float(temp)+0.01, 1)
    icon_url = "http://openweathermap.org/img/wn/" + icon + ".png"

    return f'<span class="rounded-circle"><img src="{icon_url}", alt="날씨"></span><strong>{desc}</strong>, 기온: <strong>{temp}&deg;C</strong> (최저 {temp_min}&deg;C/최고 {temp_max}&deg;C)'