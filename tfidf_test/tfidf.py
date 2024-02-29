from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path

preprocessed_base_path = "../datasets/preprocessed with stopwords data/"
documents = []

folder = Path(preprocessed_base_path)
vectorizer = TfidfVectorizer()

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

# Get feature names (words)
feature_names = vectorizer.get_feature_names_out()

# Print feature names
print("\nFeature Names:")
print(feature_names)