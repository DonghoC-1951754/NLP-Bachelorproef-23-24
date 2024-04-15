import sys

import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import openpyxl
from urlextract import URLExtract


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def create_dataset():
    workbook = openpyxl.load_workbook('../datasets/raw_dataset/initiatives_oversight.xlsx')
    sheet = workbook.active
    dataset = []
    for row in sheet.iter_rows(values_only=True):
        dataset.append(row)
    return dataset[1:68]

def get_link(initiative_link):
    extractor = URLExtract()
    temp = initiative_link
    if (""):
        return "https://www.belrai.org/nl"
    if '\n' in initiative_link:
        temp = initiative_link.strip()
    parsed_url = extractor.find_urls(temp)
    return parsed_url

# def scrape_home_page(file, url):
#     try:
#         page = requests.get(url, headers=headers)
#     except Exception as e:
#         print("\033[91m", url, "connection error\033[0m")
#     if page.status_code == 200:
#         soup = BeautifulSoup(page.content, "html.parser")
#         print("\033[92m", url, "exists\033[0m")
#         tag = soup.body
#         clean_text = ''
#         for string in tag.strings:
#             clean_text += string.strip()
#         file.write(clean_text + "\n")
#     else:
#         print("\033[91m", url, "does not exist\033[0m")
#         return


def scrape_full_page(file, url):
    try:
        page = requests.get(url, headers=headers)
    except Exception as e:
        print("\033[91m", url, "connection error\033[0m")
        return
    if page.status_code == 200:
        print("\033[92m", url, "exists\033[0m")
        soup = BeautifulSoup(page.content, "html.parser")
        tag = soup.body
        clean_text = ''
        for string in tag.strings:
            clean_text += string.strip()
        file.write(clean_text)
    else:
        print("\033[91m", url, "does not exist\033[0m")
        # print(url, " does not exist")

def main():
    dataset = create_dataset()

    for initiative in dataset:
        print(initiative[0].strip())
        if initiative[0] == "data.europa.eu":
            sys.exit(0)
        file_path = "../datasets/webscraper output data/" + initiative[0].replace('\n', '').lower() + ".txt"
        with open(file_path, "w") as file:
            file.write(initiative[4].encode('ascii', errors='ignore').decode('ascii') + "\n")
            initiative_link = get_link(initiative[3])
            scrape_full_page(file, initiative_link[0])
            scrape_full_page(file, initiative_link[0] + "about")
            if initiative_link[0] == "https://www.darwin-eu.org/":
                scrape_full_page(file, initiative_link[0] + "index.php/about/who-is-involved")
                scrape_full_page(file, initiative_link[0] + "index.php/about/ehds")
        print("")


if __name__ == "__main__":
    main()