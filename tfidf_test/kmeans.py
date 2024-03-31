import tfidf_test.tfidf as tfidf
from sklearn.cluster import KMeans

def kmeans_output(labels):
    doc_names = tfidf.doc_names_inorder()
    for doc_name in doc_names:
        print(doc_name, ": ", labels[doc_names.index(doc_name)])

def main():
    tfidf_matrix = tfidf.get_tfidf_matrix()
    kmeans_clustering = KMeans(n_clusters=2, init='k-means++', n_init='auto', max_iter=300, tol=0.0001, verbose=1, random_state=None, copy_x=True, algorithm='elkan').fit(tfidf_matrix)
    kmeans_output(kmeans_clustering.labels_)


if __name__ == "__main__":
    main()