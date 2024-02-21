import requests
from bs4 import BeautifulSoup

file_path = "../datasets/webscraper output data/arwen.txt"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
URL = "https://arwen.eu/how-it-works/"

# No clear structure on id's or classes

page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

main_tag = soup.find("main")
descriptions = main_tag.find_all("p")

with open(file_path, "w") as file:
    for description in descriptions:
        parsed_text = description.get_text(strip=True)
        file.write(parsed_text + "\n")
print("Done!")
