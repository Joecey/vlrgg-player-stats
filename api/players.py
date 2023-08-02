"""
Get details of player by either specifying team ID or brute forcing name search
TODO Also give option to list all players?
"""
import httpx 
from selectolax.parser import HTMLParser

# put data into class for post processing
from dataclasses import dataclass, asdict
from pocketbase import PocketBase

from api.helper import HelperFunctions as hl

# pocketbase setup
import os 

# dotenv for testing locally only
from dotenv import load_dotenv
load_dotenv()
pb_url = os.environ.get('PB_DOMAIN')
#! email isn't getting pulled into os.getenv
admin_email = os.environ.get('EMAIL')
admin_pass = os.environ.get('PASSWORD')

pb_client = PocketBase(pb_url)
admin_data = pb_client.admins.auth_with_password(admin_email , admin_pass)

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
    
def check_if_exists(html, query):
    check = html.css_first(query, default='not-found')
    # print(check)
    if check == 'not-found':
        return 'n/a'
    else:
        final = hl.remove_esc_seq(html.css_first(query).text())
        return final
        

#TODO add top 5 recent matches > maybe use matches url
#TODO add past teams
#TODO add 3 most recent news articles on player?
#TODO add total winnings

def parse_player_id(html, id):
        new_player = Player(
            index = id,
            ign = hl.remove_special(html.css_first("h1.wf-title").text()),
            fullName = html.css_first("h2.player-real-name").text(),
            country = hl.remove_last(check_if_exists(html, "div.ge-text-light")).lower(),
            
            # for current team, get first left team from recent results
            currentTeam = check_if_exists(html, "span.m-item-team-name").lower(),
            
            #! these two require separate check function
            twitter = html.css('a[style*="margin-top: 3px; display: block;"]')[0].text(),
            twitch = html.css('a[style*="margin-top: 3px; display: block;"]')[1].text()
        )
        # print(new_player)
        return(new_player)
    
def parse_player_name(ign : str):
    # first check firebase storage for previously saved players
    # doing this means request will be processed faster
    
    try:
        record = pb_client.collection('players').get_first_list_item('ign="{}"'.format(ign))
        print('player in database')
        # print(record.ign)
        url_substring = record.url_end
        url = "https://www.vlr.gg{}".format(url_substring)
        resp = httpx.get(url, timeout=None)
        raw_html = HTMLParser(resp.text)
        return(parse_player_id(raw_html, url_substring.split('/')[2]))
        

    # get all players from stats page (this may take some time)
    except:
        print("player not found in local storage. adding to database - this may take some time...")
        # ! NOTE: This includes only players with more than 200 rounds played
        # player_stats_url = "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=all"
        
        #! in vercel hobby plan, timeout max out after 5 seconds > might need upgrade?
        #! or just have a giant databse in pocketbase already
        player_stats_url = "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=90d"
        resp = httpx.get(player_stats_url, timeout=None)
        raw_html = HTMLParser(resp.text)
        # find all players from raw html

        all_players = raw_html.css("td.mod-player")
        
        for i in range(len(all_players)):
            current_player = all_players[i]
            a_div = current_player.css_first('a')
            
            # get player name
            div_layer = a_div.css_first('div.text-of')
            player_name = div_layer.text().lower()
            
            if ign.lower() == player_name:
                print("Player found!")
            
            
                data = {player_name: a_div.attributes['href']}

                # upload to database here
                pb_data = {
                    "ign":player_name,
                    "url_end":data[player_name]
                    }
                
                record = pb_client.collection('players').create(pb_data)
                
                # data represents player name and substring url e.g /player/9/tenz
                url = "https://www.vlr.gg{}".format(data[player_name])
                # print(url)
                resp = httpx.get(url)
                player_url = HTMLParser(resp.text)
                return(parse_player_id(player_url, data[player_name].split('/')[2]))
        
        return "Player not found."

class GetPlayers:
    def get_player_by_id(player_id): 
        html = get_html(player_id)
        return(parse_player_id(html, player_id))
    
    def get_player_by_name(player_name):
        # stats page with all time players with over 200 rounds played
        
        return(parse_player_name(player_name))


    

    
        
