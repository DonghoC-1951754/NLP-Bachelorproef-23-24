import requests
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def main():
    URL = "https://amdex.eu/"
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    main_tag = soup.find("body")
    descriptions = main_tag.find_all("p")
    clean_text = ''
    with open("./test.txt", "w") as file:
        for description in descriptions:
            clean_text += description.get_text(separator=' ').strip()
        file.write(clean_text + "\n")
    print("Done!")

    # page = requests.get("https://amdex.eu/", headers=headers)
    # soup = BeautifulSoup(page.content, "html.parser")

if __name__ == "__main__":
    main()