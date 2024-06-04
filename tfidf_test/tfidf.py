from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
import plotly.graph_objects as go
import numpy as np

# features met 2 woorden
# getallen in de dataset
# abstract uitleggen wat in tfidf vectorizer gebeurt

preprocessed_base_path = "../datasets/puncs_nums/"
documents = []

folder = Path(preprocessed_base_path)
vectorizer = TfidfVectorizer()

def doc_names_inorder():
    doc_names = []
    for file_path in folder.iterdir():
        if file_path.is_file():
            doc_names.append(file_path.name)
    return doc_names
def get_tfidf_matrix():
    for file_path in folder.iterdir():
        if file_path.is_file():
            with open(file_path, 'r') as file:
                data = file.read()
                documents.append(data)
    # Fit the vectorizer to the documents and transform the documents to TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Get the IDF scores
    idf_scores = vectorizer.idf_
    feature_names = vectorizer.get_feature_names_out()
    idf_dict = dict(zip(feature_names, idf_scores))
    word = 'arwen'
    idf_score = idf_dict.get(word, None)
    print(f"The IDF score for '{word}' is {idf_score}")

    # Get the TF-IDF values as a dense matrix
    dense_tfidf_matrix = tfidf_matrix.toarray()
    # Print the TF-IDF matrix
    print("TF-IDF Matrix:")
    print(dense_tfidf_matrix)
    return dense_tfidf_matrix

def test_tfidf():
    test_documents = [
        "car drive road",
        "truck drive highway",
        "train drive track",
        "plane fly sky",
    ]
    test_tfidf_matrix = vectorizer.fit_transform(test_documents).toarray()
    print(test_tfidf_matrix)
    print(vectorizer.idf_)
    fig = go.Figure(data=[go.Table(
        header=dict(values=vectorizer.get_feature_names_out()),
        cells=dict(values=np.ceil(test_tfidf_matrix.T * 1000) / 1000))
    ])
    fig.update_layout(width=700)
    fig.show()



if __name__ == "__main__":
    get_tfidf_matrix()
    # test_tfidf()
