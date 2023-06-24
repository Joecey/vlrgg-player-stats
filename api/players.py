"""
Get details of player by either specifying team ID or brute forcing name search
TODO Also give option to list all players?
"""

import httpx 
from selectolax.parser import HTMLParser

# put data into class for post processing
from dataclasses import dataclass, asdict

@dataclass
class Player:
    index: int
    ign: str
    fullName: str
    country: str
    currentTeam: str
    twitter: str
    twitch: str

def get_html(player_id):
        url = "https://www.vlr.gg/player/{}".format(player_id)
        resp = httpx.get(url)
        return HTMLParser(resp.text)

def parse_player_id(html, id):
        new_player = Player(
            index = id,
            ign = remove_special(html.css_first("h1.wf-title").text()),
            fullName = html.css_first("h2.player-real-name").text(),
            country = remove_last(remove_esc_seq(html.css("div.ge-text-light")[0].text())).lower(),
            
            # for current team, get first left team from recent results
            currentTeam = remove_esc_seq(html.css_first("span.m-item-team-name").text()).lower(),
            twitter = html.css('a[style*="margin-top: 3px; display: block;"]')[0].text(),
            twitch = html.css('a[style*="margin-top: 3px; display: block;"]')[1].text()
        )
        
        # print(new_player)
        return(new_player)

# post processing to remove all special characters (if needed)
def remove_special(text):
    return ''.join(e for e in text if e.isalnum())

# remove special sequences
def remove_esc_seq(text):
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    return text.translate(translator)

# remove empty space after string (allows you to keep spaces in words)
def remove_last(text):
    final = text[:-1]
    return final

class GetPlayers:
    def get_player_by_id(player_id): 
        html = get_html(player_id)
        return(parse_player_id(html, player_id))
    
    def get_player_by_name(player_name):
        """
        Here, we can reiterate until we find the player name. Although,
        this will literally take forvere
        """
        return ("test")

# testing 
# html = get_html(9)  
# print(parse_player_id(html, 9))

    

    
        
