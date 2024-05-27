from scipy.spatial.distance import cdist
import tfidf_test.tfidf as tfidf
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt

CLUSTER_AMOUNT = 10

def kmeans_output(labels, feature_names, centroids):
    doc_names = tfidf.doc_names_inorder()
    for doc_name in doc_names:
        print(doc_name, ": ", labels[doc_names.index(doc_name)])
    top_words_per_cluster_list = create_top_words(feature_names, centroids)
    doc_names_per_cluster_list = doc_names_per_cluster(labels, doc_names)
    visualize(top_words_per_cluster_list, doc_names_per_cluster_list)

def main():
    tfidf_matrix = tfidf.get_tfidf_matrix()
    # elbow_method(tfidf_matrix)
    kmeans_clustering = KMeans(n_clusters=CLUSTER_AMOUNT, init='k-means++', n_init='auto', max_iter=300, tol=0.0001, verbose=1, random_state=None, copy_x=True, algorithm='lloyd').fit(tfidf_matrix)
    kmeans_output(kmeans_clustering.labels_, tfidf.vectorizer.get_feature_names_out(), kmeans_clustering.cluster_centers_)

def doc_names_per_cluster(labels, doc_names):
    doc_per_cluster_list = []
    for cluster in range(CLUSTER_AMOUNT):
        cluster_indices = np.where(labels == cluster)[0]
        temp = []
        for cluster_index in cluster_indices:
            temp.append(doc_names[cluster_index].replace('_puncs_nums.txt', ''))
        doc_per_cluster_list.append(temp)
    return doc_per_cluster_list

def create_top_words(feature_names, centroids):
    top_words_per_cluster = []
    for centroid in centroids:
        sorted_indices = np.argsort(centroid)[::-1]
        top3_indices = sorted_indices[:3]
        top3_words = []
        for top3_index in top3_indices:
            top3_words.append((feature_names[top3_index], " " + str(round(centroid[top3_index], 3))))
        top_words_per_cluster.append(top3_words)
    return top_words_per_cluster


def elbow_method(tfidf_matrix):
    distortions = []
    inertias = []
    mapping1 = {}
    mapping2 = {}
    K = range(1, len(tfidf_matrix))
    print("Elbow method: ")
    # from 1 to K
    # for each iteration k try 10 times and take average
    for k in K:
        print("K: ", k)
        iter_distortions = []
        iter_inertias = []
        for i in range(10):
            kmeans_clustering = KMeans(n_clusters=k, init='k-means++', n_init='auto', max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True, algorithm='lloyd').fit(tfidf_matrix)
            iter_distortions.append(sum(np.min(cdist(tfidf_matrix, kmeans_clustering.cluster_centers_, 'euclidean'), axis=1))/tfidf_matrix.shape[0])
            iter_inertias.append(kmeans_clustering.inertia_)
        print("Distortions: ", iter_distortions)
        print("Inertias: ", iter_inertias)
        distortions.append(np.mean(iter_distortions))
        inertias.append(np.mean(iter_inertias))

    plt.plot(K, distortions, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method using Distortion')
    plt.show()

    plt.plot(K, inertias, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Inertia')
    plt.title('The Elbow Method using Inertia')
    plt.show()


def visualize(top_words_per_cluster, doc_names_per_cluster):
    fig = go.Figure(data=[go.Table(header=dict(values=top_words_per_cluster), cells=dict(values=doc_names_per_cluster))])
    fig.show()


if __name__ == "__main__":
    main()