import requests
from bs4 import BeautifulSoup

file_path = "../datasets/webscraper output data/dataeuropa.txt"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
URL = "https://dataeuropa.gitlab.io/data-provider-manual/"

# No clear structure on id's or classes

page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

# find the article tag
main_tag = soup.find("article")

# remove the div tag with class name 'admonition information'
div_to_remove = main_tag.find("div", class_='admonition information')
div_to_remove.decompose()

# remove the third ul tag which does not contain any useful information
ul_tags = main_tag.find_all('ul')
ul_tags[2].decompose()

# find all p, ol, ul tags
descriptions = main_tag.find_all(["p", "ol", "ul"])

# write to file
with open(file_path, "w") as file:
    for description in descriptions:
        parsed_text = description.get_text().strip()
        file.write(parsed_text + "\n")
print("Done!")
