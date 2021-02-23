from flask import current_app
import matplotlib.pyplot as plt
import numpy as np
import os

def get_scatter(x, y, weight, bias):
    plt.figure()
    plt.scatter(x, y, label='train')
    plt.plot([np.min(x), np.max(x)], [np.min(x) * weight + bias, np.max(x) * weight + bias], 'r', lw=3)
    plt.grid()
    img_file = os.path.join(current_app.root_path, 'static/img/diabetes.png')
    plt.savefig(img_file)
    mtime = int(os.stat(img_file).st_mtime)

    return mtime