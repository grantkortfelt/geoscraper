import requests
from bs4 import BeautifulSoup
from itertools import product
import string
import threading

lock = threading.Lock()
file_path = 'found.txt'

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


def url_generator(pid):
    base_url = "https://www.geoguessr.com/join/"
    characters = string.ascii_uppercase + string.digits
    for combo in product(characters, repeat=4):
        code = pid + ''.join(combo)
        url = base_url + code
        if check_page_not_found(url):
            if code[4] == "A": # this is just to make the terminal scrollable, otherwise it's a mess
                print(f"[Thread {pid}]: {code} was not found")
        else:
            print(f"[Thread {pid}]: -----{code} was found-----")
            with lock:
                with open(file_path, 'a') as f:
                    f.write(f"{url}\n")

threads = []

for character in string.ascii_uppercase + string.digits:
    t = threading.Thread(target=url_generator, args=(character,), name=character)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
