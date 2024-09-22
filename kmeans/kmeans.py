from sklearn.cluster import KMeans

import matplotlib.pyplot as plt


from sklearn.metrics import confusion_matrix,  roc_curve, auc 
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

import numpy as np

from load_image import load_images

CLUSTERS = 11

def plot_and_save(x, y, labels,title):
    plt.figure()
    plt.scatter(x, y,c=labels, cmap='viridis')
    plt.title(title)
    plt.savefig(title+".png")
    plt.clf()

le = LabelEncoder()
num_images = 100
X, y = load_images("./spark22",num_images)
y = le.fit_transform(y)


dim_reduction= { #"tsne_3d" : TSNE(n_components=3), 
                 "tsne_2d" : TSNE(n_components=2), 
                 #"pca_3d"  : PCA(n_components=2),
                 "pca_2d"  : PCA(n_components=3) }

reduced = { d: dim_reduction[d].fit_transform(X) for d in dim_reduction.keys() }

k = KMeans(n_clusters=CLUSTERS)
k.fit(X)
labels = k.labels_ 
for m, r in reduced.items():
    plot_and_save(r[:,0], r[:,1], labels=labels, title=m+"_kmeans")
    plot_and_save(r[:,0], r[:,1], labels=y, title=m+"_class")
