import requests
from bs4 import BeautifulSoup

# No clear structure on id's or classes

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

URL = "https://arwen.eu/how-it-works/"
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

main_tag = soup.find("main")
descriptions = main_tag.find_all("p")

for description in descriptions:
    print(description.text.strip())
