import nltk
# nltk.download('wordnet')
# nltk.download('stopwords')
from nltk.corpus import stopwords
sw_nltk = stopwords.words('english')
from nltk.stem import WordNetLemmatizer

base_path = "../datasets/webscraper output data/"
raw_data_paths = [base_path + "arwen.txt", base_path + "bdva.txt", base_path + "dataeuropa.txt"]
ouput_stopwords_path = "../datasets/preprocessed with stopwords data/"
output_lemmatized_path = "../datasets/lemmatization/"

lemmatizer = WordNetLemmatizer()

def save_lemmatized_data(data, name):
    with open(output_lemmatized_path + name, 'w') as file:
        file.write(data)
def lemmatize(data):
    words = [lemmatizer.lemmatize(word) for word in data.split()]
    # print("Lemmatized words: ", words)
    new_data = " ".join(words)
    save_lemmatized_data(new_data, "arwen_lemmatized.txt")
    return new_data

def stopwords(data):
    words = [word for word in data.split() if word.lower() not in sw_nltk]
    # print("Words without stopwords: ", words)
    new_data = " ".join(words)
    save_stopwords_data(new_data, "arwen_preprocessed.txt")
    return new_data

def save_stopwords_data(data, name):
    with open(ouput_stopwords_path + name, 'w') as file:
        file.write(data)

def preprocess():
    # Automatically read all the raw data files
    # for path in raw_data_paths:
    #     with open(path, 'r') as file:
    #         data = file.read()

    # Manually read the raw data files
    # arwen
    with open(raw_data_paths[0], 'r') as file:
        data = file.read()
        stopwords(lemmatize(data))
    # bdva
    # with open(raw_data_paths[1], 'r') as file:
    #     data = file.read()
    #     savePreprocessedData(with_stopwords(data), "bdva_preprocessed.txt")
    # dataeuropa
    # with open(raw_data_paths[2], 'r') as file:
    #     data = file.read()
    #     savePreprocessedData(with_stopwords(data), "dataeuropa_preprocessed.txt")

    print("Preprocessing done!")

if __name__ == "__main__":
    preprocess()