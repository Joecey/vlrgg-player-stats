"""
Get details of player by either specifying team ID or brute forcing name search
TODO Also give option to list all players?
"""

import httpx 
from selectolax.parser import HTMLParser

# put data into class for post processing
from dataclasses import dataclass, asdict

from api.helper import HelperFunctions as hl

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

#TODO add top 5 recent matches > maybe use matches url
#TODO add past teams
#TODO add 3 most recent news articles on player?
#TODO add total winnings

def parse_player_id(html, id):
        new_player = Player(
            index = id,
            ign = hl.remove_special(html.css_first("h1.wf-title").text()),
            fullName = html.css_first("h2.player-real-name").text(),
            country = hl.remove_last(hl.remove_esc_seq(html.css("div.ge-text-light")[0].text())).lower(),
            
            # for current team, get first left team from recent results
            currentTeam = hl.remove_esc_seq(html.css_first("span.m-item-team-name").text()).lower(),
            twitter = html.css('a[style*="margin-top: 3px; display: block;"]')[0].text(),
            twitch = html.css('a[style*="margin-top: 3px; display: block;"]')[1].text()
        )
        
        # print(new_player)
        return(new_player)

class GetPlayers:
    def get_player_by_id(player_id): 
        html = get_html(player_id)
        return(parse_player_id(html, player_id))

# testing 
# html = get_html(9)  
# print(parse_player_id(html, 9))

    

    
        
