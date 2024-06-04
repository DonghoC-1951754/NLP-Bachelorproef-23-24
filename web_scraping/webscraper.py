import sys
import os
import requests
import validators
from bs4 import BeautifulSoup
import openpyxl
from urlextract import URLExtract
import langid
from urllib.parse import urlparse


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


"""
    Create a dataset from the excel file.
    
    Returns:
    list: A list of all rows in the excel file.
"""
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
    if '\n' in temp:
        temp = temp.strip()
    parsed_url = extractor.find_urls(temp)
    return parsed_url


"""
    Check whether a link is valid.

    Parameters:
    url (str): The url that is checked.
    domain (str): The domain of the webpage.
    
    Returns:
    bool: True if the link is valid, False otherwise.
"""
def is_valid_url(url, domain):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.pdf', '.pptx', '.xml', '.xmlx', '.docx', '.doc', '.ppt', '.pptx', '.xls', '.xlsx', '.csv', '.json', '.zip', '.rar', '.tar', '.gz', '.7z', '.bz2', '.xz', '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.webp', '.ico']
    if url is None or url == '#':
        return False
    if not any(url.startswith(scheme) for scheme in ['http://', 'https://']):
        # If the url does not start with http:// or https://
        if urlparse(url).netloc != domain:
            url = 'https://' + domain + url
    if validators.url(url):
        # Check for video extensions
        for ext in video_extensions:
            if urlparse(url).path.endswith(ext):
                return False
        return True
    return False


"""
    Find all links on a webpage

    Parameters:
    url (str): The url that is used to find all links on the webpage.
    domain (str): The domain of the webpage.

    Returns:
    list: A lists of all links on the webpage that are valid.
"""
def get_all_links(url, domain):
    try:
        # Attempt to send a GET request to the specified url
        page = requests.get(url, headers=headers)
    except Exception as e:
        print("\033[91m", url, "connection error\033[0m")
        return
    # Parse the HTML content of the page
    soup = BeautifulSoup(page.text, 'html.parser')
    all_a_tags = soup.find_all('a')
    links = []
    # Check whether the link is valid
    for link in all_a_tags:
        href = link.get('href')
        if is_valid_url(href, domain):
            if not any(href.startswith(scheme) for scheme in ['http://', 'https://']):
                if urlparse(href).netloc != domain:
                    href = 'https://' + domain + href
            links.append(href)
    return links


"""
    Scrape every webpage that is linked on the webpage and write the text to a file.

    Parameters:
    file (file): The file that is used to write the scraped text to.
    base_url (str): The url where the links are found.
    domain (str): The domain of the webpage.
    seen_links (list): A list of all links that have already been scraped.
"""
def scrape_all_links(file, base_url, domain, seen_links=[]):
    links = get_all_links(base_url, domain)
    if links is None:
        return
    for link in links:
        if link not in seen_links and urlparse(link).netloc == domain:
            seen_links.append(link)
            scrape_full_page(file, link)


"""
    Scrape the full content of a webpage and write the text to a file.
    Don't scrape if the webpage is not valid.

    Parameters:
    file (file): The file that is used to write the scraped text to.
    url (str): The url of the webpage.
"""
def scrape_full_page(file, url):
    try:
        page = requests.get(url, headers=headers)
    except Exception as e:
        # Connection error
        print("\033[91m", url, "connection error => not scraped\033[0m")
        return
    if page.status_code == 200:
        # Check if the language of the webpage is English
        language = langid.classify(page.text)[0]
        if language != 'en':
            print("\033[91m", url, "exists, but in", language, "=> not scraped", "\033[0m")
            return
        print("\033[92m", url, "exists => scraped\033[0m")
        # Parse the HTML content of the page
        soup = BeautifulSoup(page.content, "html.parser")
        tag = soup.body
        if tag is not None:
            # Remove all links from the text
            for a_tag in tag.find_all('a'):
                a_tag.extract()
            clean_text = tag.get_text()
            file.write(clean_text.encode('ascii', errors='ignore').decode('ascii'))
    else:
        print("\033[91m", url, "does not exist => not scraped\033[0m")

def main():
    dataset = create_dataset()
    for initiative in dataset:
        print(initiative[0].strip())
        file_path = "../datasets/webscraper output data/" + initiative[0].replace('\n', '').lower() + ".txt"
        with open(u"\\\\?\\" + os.path.abspath(file_path), "w") as file:
            file.write(initiative[4].encode('ascii', errors='ignore').decode('ascii') + "\n")
            initiative_link = get_link(initiative)
            if initiative_link == []:
                print("\033[91m", "No link found for", initiative[0], "\033[0m")
                continue
            # Scrape home page and all links on the home page
            scrape_full_page(file, initiative_link[0])
            scrape_all_links(file, initiative_link[0], urlparse(initiative_link[0]).netloc, initiative_link)
        print("")


if __name__ == "__main__":
    main()