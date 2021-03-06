import os, cv2, json, urllib3, base64
import numpy as np
from bp12_deep_learning import etri
from PIL import Image, ImageDraw, ImageFont
from flask import Blueprint, render_template, request, current_app
from tensorflow.keras.applications.vgg16 import VGG16, decode_predictions
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.resnet50 import ResNet50

from utils.weather import cur_weather

deep_bp = Blueprint('deep_bp', __name__)

@deep_bp.route('/image', methods=['GET', 'POST'])
def deep_img():
    menu = {'ho': 0, 'da': 0, 'ml': 0, 'dl': 1, 'etimg': 0, 'img': 1, 'txt': 0}
    vgg16 = VGG16()
    vgg19 = VGG19()
    incpt = InceptionV3(input_shape=(299, 299, 3))
    resnet = ResNet50()
    if request.method == 'GET':
        return render_template('/deeplearning/deep_img.html', menu=menu, weather=cur_weather())
    else:
        image = request.files['image']
        img = os.path.join(current_app.root_path, 'static/img/') + 'class_img.jpg'
        image.save(img)
        img_vgg = np.array(Image.open(f'static/img/class_img.jpg').resize((224, 224)))
        img_incpt = cv2.imread(f'static/img/class_img.jpg', -1)
        img_res = img_incpt
        img_incpt = cv2.resize(img_incpt, (299, 299))
        img_res = cv2.cvtColor(img_res, cv2.COLOR_BGR2RGB)
        img_res = cv2.resize(img_res, (224, 224))
        model_list = [vgg16, vgg19, incpt, resnet]
        model_dict = {'vgg16': img_vgg, 'vgg19': img_vgg, 'incpt': img_incpt, 'resnet': img_res}
        result = []
        for i, model in enumerate(model_dict.keys()):
            if model != 'incpt':
                yhat = model_list[i].predict(model_dict[model].reshape(-1, 224, 224, 3))
                label = decode_predictions(yhat)
                label = label[0][0]
                pred = label[1]
            else:
                yhat = model_list[i].predict(img_incpt.reshape(-1, 299, 299, 3))
                label = decode_predictions(yhat)
                label = label[0][0]
                pred = label[1]
            result.append(pred)
        mtime = int(os.stat(img).st_mtime)

        return render_template('/deeplearning/deep_img_res.html', menu=menu, weather=cur_weather(), result=result, mtime=mtime)

@deep_bp.route('/etri_image', methods=['GET', 'POST'])
def etri_image():
    menu = {'ho': 0, 'da': 0, 'ml': 0, 'dl': 1, 'etimg': 1, 'img': 0, 'txt': 0}
    if request.method == 'GET':
        return render_template('/deeplearning/etri_img.html', menu=menu, weather=cur_weather())
    else:
        image = request.files['image']
        img = os.path.join(current_app.root_path, 'static/img/') + 'etri_img.jpg'
        image.save(img)
        object_img = etri.etri_img()
        mtime = int(os.stat(object_img).st_mtime)

        return render_template('/deeplearning/etri_img_res.html', menu=menu, weather=cur_weather(), mtime=mtime)