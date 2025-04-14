import requests
from bs4 import BeautifulSoup
import json

class Player:
    def __init__(self, nick, flair, pin, fullBodyPin, userId, team, isGuest, isPresent, isBenched, isEligibleAsOwner, victories, clientType):
        self.nick = nick
        self.flair = flair
        self.pin = pin
        self.fullBodyPin = fullBodyPin
        self.userId = userId
        self.team = team
        self.isGuest = isGuest
        self.isPresent = isPresent
        self.isBenched = isBenched
        self.isEligibleAsOwner = isEligibleAsOwner
        self.victories = victories
        self.clientType = clientType
    
    def __str__(self):
        return f"Player {self.nick}: userId={self.userId}, team={self.team}, isGuest={self.isGuest}, isPresent={self.isPresent}, isBenched={self.isBenched}, isEligibleAsOwner={self.isEligibleAsOwner}, victories={self.victories}"
    
    def __repr__(self):
        return f"Player {self.nick}: flair={self.flair}, pin={self.pin}, fullBodyPin={self.fullBodyPin}, userId={self.userId}, team={self.team}, isGuest={self.isGuest}, isPresent={self.isPresent}, isBenched={self.isBenched}, isEligibleAsOwner={self.isEligibleAsOwner}, victories={self.victories}, clientType={self.clientType}"

    def get_nick(self):
        return self.nick
    
    def get_flair(self):
        return self.flair
    
    def get_pin(self):
        return self.pin
    
    def get_fullBodyPin(self):
        return self.fullBodyPin
    
    def get_userId(self):
        return self.userId
    
    def get_team(self):
        return self.team
    
    def get_isGuest(self):
        return self.isGuest
    
    def get_isPresent(self):
        return self.isPresent
    
    def get_isBenched(self):
        return self.isBenched
    
    def get_isEligibleAsOwner(self):
        return self.isEligibleAsOwner
    
    def get_victories(self):
        return self.victories

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

def convert_json_to_player(json_data):
    return Player(
        json_data['nick'],
        json_data['flair'],
        json_data['pin'],
        json_data['fullBodyPin'],
        json_data['userId'],
        json_data['team'],
        json_data['isGuest'],
        json_data['isPresent'],
        json_data['isBenched'],
        json_data['isEligibleAsOwner'],
        json_data['victories'],
        json_data['clientType']
    )

def get_party_owner(party_data):
    try:
        # Parse the JSON data to extract the party owner
        json_data = json.loads(party_data[0].string)
        # party owner in props -> pageProps -> party -> owner
        party_owner = json_data['props']['pageProps']['party']['owner']
        return convert_json_to_player(party_owner)
    except Exception as e:
        return None

print(get_party_owner(get_basic_party_data("https://www.geoguessr.com/join/J589D")))