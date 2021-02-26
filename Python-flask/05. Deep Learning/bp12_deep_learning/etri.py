from PIL import Image, ImageDraw, ImageFont
import json, base64, os, urllib3
import matplotlib.pyplot as plt

def etri_img():
    with open('./etri_ai_key.txt') as key:
        eai_key = key.read(100)
    
    openApiURL = 'http://aiopen.etri.re.kr:8000/ObjectDetect'
    image_file = './static/img/etri_img.jpg'
    _, image_type = os.path.splitext(image_file)
    image_type = 'jpg' if image_type == '.jfif' else image_type[1:]
    
    with open(image_file, 'rb') as file:
        image_contents = base64.b64encode(file.read()).decode('utf8')

    request_json = {
        'request_id': 'reserved field',
        'access_key': eai_key,
        'argument': {
            'file': image_contents,
            'type': image_type
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        'POST',
        openApiURL,
        headers={'Content-Type': 'application/json; charset=UTF-8'},
        body=json.dumps(request_json)
    )
    result = json.loads(response.data)
    obj_list = result['return_object']['data']

    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)
    for obj in obj_list:
        name = obj['class']
        x = int(obj['x'])
        y = int(obj['y'])
        w = int(obj['width'])
        h = int(obj['height'])
        draw.text((x, y-30), name, font=ImageFont.truetype('malgun.ttf', 20), fill=(255, 0, 0))
        draw.rectangle(((x, y), (x+w, y+h)), outline=(255, 0, 0), width=3)
    
    image.save('./static/img/object.' + image_type)
    return f"./static/img/object.{image_type}"