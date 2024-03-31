from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path

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
    # Get the TF-IDF values as a dense matrix
    dense_tfidf_matrix = tfidf_matrix.toarray()
    # Print the TF-IDF matrix
    print("TF-IDF Matrix:")
    print(dense_tfidf_matrix)
    return dense_tfidf_matrix


#
# # Get feature names (words)
# feature_names = vectorizer.get_feature_names_out()
#
# # Print feature names
# print("\nFeature Names:")
# print(feature_names)