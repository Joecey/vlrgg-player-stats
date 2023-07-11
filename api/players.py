"""
Get details of player by either specifying team ID or brute forcing name search
TODO Also give option to list all players?
"""
import httpx 
from selectolax.parser import HTMLParser

# put data into class for post processing
from dataclasses import dataclass, asdict

from api.helper import HelperFunctions as hl

# Firebase setup
import pyrebase 
import os 

from dotenv import load_dotenv
load_dotenv()

config = {
    "apiKey": os.environ.get('API_KEY'),
    "authDomain": os.environ.get('AUTH_DOMAIN'),
    "databaseURL": os.environ.get('DATABASE_URL'),
    "storageBucket": os.environ.get('STORAGE_BUCKET'),

}
# setup config and login with client credentials
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
client = auth.sign_in_with_email_and_password(os.environ.get('CLIENT_EMAIL'), os.environ.get('CLIENT_PASSWORD'))
db = firebase.database()

@dataclass
class Player:
    index: int
    ign: str
    fullName: str
    country: str
    currentTeam: str
    twitter: str
    twitch: str
    
class PlayerViaName:
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
    
def parse_player_name(ign : str):
    # first check firebase storage for previously saved players
    # doing this means request will be processed faster
    cloud_players = db.child("players").get()
    if (ign.lower()) in cloud_players.val():
        print("Player found in Firebase...")
        url_substring = db.child("players").child(ign.lower()).get().val()
        return url_substring

    # get all players from stats page (this may take some time)
    else:
        print("player not found in local storage. adding to firebase - this may take some time...")
        player_stats_url = "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all"
        resp = httpx.get(player_stats_url, timeout=None)
        raw_html = HTMLParser(resp.text)
        
        # find all players from raw html
        # ! NOTE: This includes only players with more than 200 rounds played
        all_players = raw_html.css("td.mod-player")
        
        for i in range(len(all_players)):
            current_player = all_players[i]
            a_div = current_player.css_first('a')
            
            # get player name
            div_layer = a_div.css_first('div.text-of')
            player_name = div_layer.text().lower()
            
            if ign.lower() == player_name:
                print("Player found!")
                
                # Add to Firebase for faster future reference
                data = {player_name: a_div.attributes['href']}
                db.child("players").update(data, client.get('idToken'))
                return data
        
        return "Player not found."

class GetPlayers:
    def get_player_by_id(player_id): 
        html = get_html(player_id)
        return(parse_player_id(html, player_id))
    
    def get_player_by_name(player_name):
        # stats page with all time players with over 200 rounds played
        
        return(parse_player_name(player_name))


    

    
        
