import nltk
from nltk.corpus import stopwords
sw_nltk = stopwords.words('english')

base_path = "../datasets/webscraper output data/"
raw_data_paths = [base_path + "arwen.txt", base_path + "bdva.txt", base_path + "dataeuropa.txt"]
ouput_base_path = "../datasets/preprocessed with stopwords data/"

def with_stopwords(data):
    words = [word for word in data.split() if word.lower() not in sw_nltk]
    new_data = " ".join(words)
    return new_data

def savePreprocessedData(data, name):
    with open(ouput_base_path + name, 'w') as file:
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
        savePreprocessedData(with_stopwords(data), "arwen_preprocessed.txt")
    # bdva
    with open(raw_data_paths[1], 'r') as file:
        data = file.read()
        savePreprocessedData(with_stopwords(data), "bdva_preprocessed.txt")
    # dataeuropa
    with open(raw_data_paths[2], 'r') as file:
        data = file.read()
        savePreprocessedData(with_stopwords(data), "dataeuropa_preprocessed.txt")

    print("Preprocessing done!")

preprocess()