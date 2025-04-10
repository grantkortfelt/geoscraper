import requests
from bs4 import BeautifulSoup
from itertools import product
import string

def check_page_not_found(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        error_heading = soup.find('h1', class_='_error_heading__K1wbX')
        if error_heading and error_heading.text.strip() == "Page not found":
            return True
        return False
    except requests.exceptions.RequestException as e:
        return True


def url_generator():
    base_url = "https://www.geoguessr.com/join/"
    characters = string.ascii_uppercase + string.digits
    for combination in product(characters, repeat=5):
        url = base_url + ''.join(combination)
        yield url

for url in url_generator():
    party_code = url[-5:]
    if check_page_not_found(url):
        if party_code[4] == "A":
            print(f"{party_code} was not found")
    else:
        print(f"-----{party_code} was found-----")
        with open('found.txt', 'a') as f:
            f.write(f"{url}\n")
