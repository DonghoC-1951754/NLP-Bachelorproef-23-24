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

def get_link(initiative):
    extractor = URLExtract()
    temp = initiative[3]
    if initiative[0].strip() == "BelRAI":
        return ["https://www.belrai.org/nl"]
    if '\n' in temp:
        temp = temp.strip()
    parsed_url = extractor.find_urls(temp)
    return parsed_url


def scrape_all_links(file, url):
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')


def scrape_full_page(file, url):
    try:
        page = requests.get(url, headers=headers)
    except Exception as e:
        print("\033[91m", url, "connection error\033[0m")
        return
    if page.status_code == 200:
        print("\033[92m", url, "exists\033[0m")
        soup = BeautifulSoup(page.content, "html.parser")
        # filtered_texts = [node.get_text() for node in soup.body.children if not isinstance(node, str) or not node.name == 'a']
        tag = soup.body
        for a_tag in tag.find_all('a'):
            a_tag.extract()
        # clean_text = ''
        # for string in tag.strings:
        #     clean_text += string.strip()
        clean_text = tag.get_text()
        # clean_text = ''.join(filtered_texts)
        file.write(clean_text.encode('ascii', errors='ignore').decode('ascii'))
    else:
        print("\033[91m", url, "does not exist\033[0m")
        # print(url, " does not exist")

def main():
    dataset = create_dataset()

    for initiative in dataset:
        print(initiative[0].strip())
        if initiative[0] == "DHU (Digital Health Uptake) and DHU Radar":
            sys.exit(0)
        file_path = "../datasets/webscraper output data/" + initiative[0].replace('\n', '').lower() + ".txt"
        with open(file_path, "w") as file:
            file.write(initiative[4].encode('ascii', errors='ignore').decode('ascii') + "\n")
            initiative_link = get_link(initiative)
            # initiative_link = get_link(initiative[3])
            # Home page
            scrape_full_page(file, initiative_link[0])
            # All links
            scrape_all_links(file, initiative_link[0])
            # About page
            scrape_full_page(file, initiative_link[0] + "about")
            if initiative_link[0] == "https://www.darwin-eu.org/":
                scrape_full_page(file, initiative_link[0] + "index.php/about/who-is-involved")
                scrape_full_page(file, initiative_link[0] + "index.php/about/ehds")
            if initiative_link[0] == "https://data.europa.eu/en":
                scrape_full_page(file, "https://dataeuropa.gitlab.io/data-provider-manual/")
                scrape_full_page(file, "https://dataeuropa.gitlab.io/data-provider-manual/publications-education/")
        print("")


if __name__ == "__main__":
    main()