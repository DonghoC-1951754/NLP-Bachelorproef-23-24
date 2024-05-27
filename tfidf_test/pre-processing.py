from nltk.corpus import stopwords
sw_nltk = stopwords.words('english')
from nltk.stem import WordNetLemmatizer
import web_scraping.webscraper as ws
import os

base_path = "../datasets/webscraper output data/"
# raw_data_paths = [base_path + "arwen.txt", base_path + "bdva.txt", base_path + "dataeuropa.txt"]
output_stopwords_path = "../datasets/stopwords/"
output_lemmatized_path = "../datasets/lemmatization/"
output_puncs_nums_path = "../datasets/puncs_nums/"

lemmatizer = WordNetLemmatizer()

def save_lemmatized_data(data, name):
    with open(u"\\\\?\\" + os.path.abspath(output_lemmatized_path + name), 'w+') as file:
        file.write(data)
def lemmatize(data, name):
    words = [lemmatizer.lemmatize(word) for word in data.split()]
    # print("Lemmatized words: ", words)
    new_data = " ".join(words)
    save_lemmatized_data(new_data, name)
    return new_data

def stopwords(data, name):
    words = [word for word in data.split() if word.lower() not in sw_nltk]
    # print("Words without stopwords: ", words)
    new_data = " ".join(words)
    save_stopwords_data(new_data, name)
    return new_data

def save_stopwords_data(data, name):
    with open(u"\\\\?\\" + os.path.abspath(output_stopwords_path + name), 'w+') as file:
        file.write(data)

def remove_puncs_nums(data, name):
    for char in data:
        if not ((ord('a') <= ord(char) <= ord('z')) or (ord('A') <= ord(char) <= ord('Z')) or (ord(char) == ord(' '))):
            data = data.replace(char, "")
    save_punc_nums_data(data, name)
    return data

def save_punc_nums_data(data, name):
    with open(u"\\\\?\\" + os.path.abspath(output_puncs_nums_path + name), 'w+') as file:
        file.write(data)

def preprocess():
    # Automatically read all the raw data files
    # for path in raw_data_paths:
    #     with open(path, 'r') as file:
    #         data = file.read()
    dataset = ws.create_dataset()
    for initiative in dataset:
        initiative_name = initiative[0].replace('\n', '').lower()
        print(initiative_name)
        file_path = "../datasets/webscraper output data/" + initiative_name + '.txt'
        with open(u"\\\\?\\" + os.path.abspath(file_path), "r") as file:
            data = file.read()
            remove_puncs_nums(stopwords(lemmatize(data, initiative_name + "_lemmatized.txt"), initiative_name + "_stopwords.txt"), initiative_name + "_puncs_nums.txt")
    # Manually read the raw data files
    # arwen
    # with open(raw_data_paths[0], 'r') as file:
    #     data = file.read()
    #     remove_puncs_nums(stopwords(lemmatize(data, "arwen_lemmatized.txt"), "arwen_stopwords.txt"), "arwen_puncs_nums.txt")
    # # bdva
    # with open(raw_data_paths[1], 'r') as file:
    #     data = file.read()
    #     remove_puncs_nums(stopwords(lemmatize(data, "bdva_lemmatized.txt"), "bdva_stopwords.txt"), "bdva_puncs_nums.txt")
    # # dataeuropa
    # with open(raw_data_paths[2], 'r') as file:
    #     data = file.read()
    #     remove_puncs_nums(stopwords(lemmatize(data, "dataeuropa_lemmatized.txt"), "dataeuropa_stopwords.txt"), "dataeuropa_puncs_nums.txt")

    print("Preprocessing done!")

if __name__ == "__main__":
    preprocess()