import tfidf_test.tfidf as tfidf
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import numpy as np

CLUSTER_AMOUNT = 5

def kmeans_output(labels, feature_names, centroids):
    doc_names = tfidf.doc_names_inorder()
    for doc_name in doc_names:
        print(doc_name, ": ", labels[doc_names.index(doc_name)])
    top_words_per_cluster_list = create_top_words(feature_names, centroids)
    doc_names_per_cluster_list = doc_names_per_cluster(labels, doc_names)
    visualize(top_words_per_cluster_list, doc_names_per_cluster_list)

def main():
    tfidf_matrix = tfidf.get_tfidf_matrix()
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

# def create_top_words(labels, tfidf_matrix, feature_names):
#     top_words_per_cluster = []
#     for cluster in range(CLUSTER_AMOUNT):
#         cluster_indices = np.where(labels == cluster)[0]
#         top_word_indices = []
#         top_word_scores = []
#         for cluster_index in cluster_indices:
#             top_word_index_list = np.argsort(tfidf_matrix[cluster_index])[::-1]
#             for i in range(3):
#                 top_word_indices.append(top_word_index_list[i])
#                 top_word_scores.append(tfidf_matrix[cluster_index][top_word_index_list[i]])
#         sorted_indices = np.argsort(top_word_scores)[::-1]
#         seen = []
#         top_words = []
#         for sorted_index in sorted_indices:
#             if top_word_indices[sorted_index] not in seen:
#                 seen.append(top_word_indices[sorted_index])
#                 top_words.append(feature_names[top_word_indices[sorted_index]])
#                 # print("Cluster ", cluster, " top word: ", feature_names[top_word_indices[sorted_index]])
#             if len(seen) == 3:
#                 top_words_per_cluster.append(top_words)
#                 break
#     return top_words_per_cluster

def visualize(top_words_per_cluster, doc_names_per_cluster):
    fig = go.Figure(data=[go.Table(header=dict(values=top_words_per_cluster), cells=dict(values=doc_names_per_cluster))])
    fig.show()


if __name__ == "__main__":
    main()