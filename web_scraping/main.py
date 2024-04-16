import requests
from bs4 import BeautifulSoup

# Get html code of the website
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

# Parses the structured html code
# You can interact with html elements like you can with a developer tool (find elements by ID)
soup = BeautifulSoup(page.content, "html.parser")
# By ID
results = soup.find(id="ResultsContainer")
# print(results.prettify())

# By Class
job_elements = results.find_all("div", class_="card-content")
# for job_element in job_elements:
#     print(job_element, end="\n"*2)

# Filter specific element in job divs
# use .strip() to remove leading and trailing white spaces

# for job_element in job_elements:
#     title_element = job_element.find("h2", class_="title")
#     company_element = job_element.find("h3", class_="company")
#     location_element = job_element.find("p", class_="location")
#     print(title_element.text.strip())
#     print(company_element.text.strip())
#     print(location_element.text.strip())
#     print()

# Filter by matching string

# python_jobs = results.find_all("h2", string="Python")
# print(python_jobs)

# Filter by matching string with lambda function
# But this only returns the h2 element, not the whole job div => results in error
python_jobs = results.find_all("h2", string=lambda text: "python" in text.lower())
# for job_element in python_jobs:
#     title_element = job_element.find("h2", class_="title")
#     company_element = job_element.find("h3", class_="company")
#     location_element = job_element.find("p", class_="location")
#     print(title_element.text.strip())
#     print(company_element.text.strip())
#     print(location_element.text.strip())
#     print()

# Access parent element (3 generations up)
# We take this parent because it contains all the info we need
python_job_elements = [
    h2_element.parent.parent.parent for h2_element in python_jobs
]

# links
for job_element in python_job_elements:
    # -- snip --
    links = job_element.find_all("a")
    for link in links:
        link_url = link["href"]
        print(f"Apply here: {link_url}\n")