from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def main():
    url = "/index.php/buh"
    domain = "darwin"
    if not any(url.startswith(scheme) for scheme in ['http://', 'https://']):
        if urlparse(url).netloc != domain:
            url = 'https://' + domain + url
    print(url)

    # page = requests.get("https://amdex.eu/", headers=headers)
    # soup = BeautifulSoup(page.content, "html.parser")

if __name__ == "__main__":
    main()