import requests
from bs4 import BeautifulSoup
import json

def get_basic_party_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the party members json at <script id="__NEXT_DATA__" type="application/json">
        # with open('page.html', 'w', encoding='utf8') as f:
        #     f.write(soup.prettify())
        party_data = soup.find_all('script', id='__NEXT_DATA__')
        # with open('party.json', 'w', encoding='utf8') as f:
        #     f.write(party_data[0].string)
        return party_data
    except requests.exceptions.RequestException as e:
        return []

def get_party_owner(party_data):
    try:
        # Parse the JSON data to extract the party owner
        json_data = json.loads(party_data[0].string)
        # party owner in props -> pageProps -> party -> owner
        party_owner = json_data['props']['pageProps']['party']['owner']
        return party_owner
    except Exception as e:
        return None