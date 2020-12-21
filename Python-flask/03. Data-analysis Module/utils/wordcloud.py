from wordcloud import WordCloud, STOPWORDS
import nltk, re
from konlpy.tag import Okt; okt = Okt()
import numpy as np
from flask import request
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager
mpl.rc('font', family='Malgun Gothic')
mpl.rc('axes', unicode_minus=False)


def eng_cloud(text, mask, stop_words, img_file):
    stopwords = set(STOPWORDS)
    for sw in stop_words:
        stopwords.add(sw)
    
    if mask == None: 
        wc = WordCloud(background_color='black', width=800, height=800, max_words=1000, stopwords=stopwords, margin=10, random_state=1)
    else:
        mask = np.array(Image.open(mask))
        wc = WordCloud(background_color='white', width=800, height=800, max_words=1000, mask=mask, stopwords=stopwords, margin=10, random_state=1)
    wc = wc.generate(text)
    plt.figure(figsize=(8, 8), dpi=100)
    plt.imshow(wc, interpolation='nearest', aspect='equal')
    plt.axis('off')
    plt.savefig(img_file)
    
def kor_cloud(text, mask, stop_words, img_file):
    tokens = okt.nouns(text)
    new_text = []
    for token in tokens:
        text = re.sub('[a-zA-Z0-9]', '', token)
        new_text.append(text)
    new_text = [each_word for each_word in new_text if each_word not in stop_words]
    kor_text = nltk.Text(new_text,  name='한글 텍스트')
    data = kor_text.vocab().most_common(300)

    if mask == None:
        wc = WordCloud(font_path='c:/Windows/Fonts/malgun.ttf', width=800, height=800, max_words=1000, relative_scaling=0.2, background_color='black').generate_from_frequencies(dict(data))
    else:
        mask = np.array(Image.open(mask))
        wc = WordCloud(font_path='c:/Windows/Fonts/malgun.ttf', width=800, height=800, mask=mask, max_words=1000, relative_scaling=0.2, background_color='white').generate_from_frequencies(dict(data))
    plt.figure(figsize=(8, 8), dpi=100)
    ax = plt.axes([0, 0, 1, 1])
    plt.imshow(wc, interpolation='nearest', aspect='equal')
    plt.axis('off')
    plt.savefig(img_file)