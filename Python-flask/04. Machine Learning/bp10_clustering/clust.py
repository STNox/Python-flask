from flask import Blueprint, render_template, request, current_app
import pandas as pd
import joblib, os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from utils.weather import cur_weather

clust_bp = Blueprint('clust_bp', __name__)

menu = {'ho': 0, 'da': 0, 'ml': 1, 'cf': 0, 'ac': 0, 're': 0, 'cl': 1, 'la': 0}

@clust_bp.route('/clust', methods=['GET', 'POST'])
def clust():
    if request.method == 'GET':
        return render_template('/clustering/clust.html', menu=menu, weather=cur_weather())
    else:
        file = request.files['file']
        n = int(request.form['n'])
        filename = os.path.join(current_app.root_path, 'static/upload/') + file.filename
        file.save(filename)
        current_app.logger.info(f'{filename} is saved.')

        df = pd.read_csv(filename)
        df2 = df.iloc[:, :-1]
        scaler = StandardScaler()
        pca = PCA(n_components=2)
        df_scaled = scaler.fit_transform(df2)
        df_pca = pca.fit_transform(df_scaled)
        kmeans = KMeans(n_clusters=n, init='k-means++', max_iter=300, random_state=2021)
        kmeans.fit(df2)
        df['cluster'] = kmeans.labels_
        df['pca_x'] = df_pca[:, 0]
        df['pca_y'] = df_pca[:, 1]

        plt.figure()
        for i in df.target.unique():
            x_axis_data = df[df.target == i]['pca_x']
            y_axis_data = df[df.target == i]['pca_y']
            plt.scatter(x_axis_data, y_axis_data)
        
        plt.xlabel('PCA 1'); plt.ylabel('PCA 2')
        plt.title('Original Dataset Visualization by 2 PCA Components')
        img_file = os.path.join(current_app.root_path, 'static/img/original_data.png')
        plt.savefig(img_file)
        
        plt.figure()
        for i in range(n):
            x_axis_data = df[df.cluster == i]['pca_x']
            y_axis_data = df[df.cluster == i]['pca_y']
            plt.scatter(x_axis_data, y_axis_data)

        plt.xlabel('PCA 1'); plt.ylabel('PCA 2')
        plt.title(f'{n} Clusters Visualization by 2 PCA Components')
        img_file = os.path.join(current_app.root_path, 'static/img/cluster.png')
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        return render_template('/clustering/clust_res.html', menu=menu, weather=cur_weather(), mtime=mtime, n_cluster=n)
