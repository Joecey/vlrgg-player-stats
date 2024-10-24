"""
Get details of team by either specifying team ID or brute forcing name search
TODO Also give option to list all teams?
"""

import httpx 
from selectolax.parser import HTMLParser

# put data into class for post processing
from dataclasses import dataclass, asdict, field

from api.helper import HelperFunctions as hl

@dataclass
class Team:
    index: int 
    name: str 
    roster: list 
    country: str 
    region: str 
    currentRank: str
    rating: str
    earnings: str
    

def get_html(team_id):
        url = "https://www.vlr.gg/team/{}".format(team_id)
        resp = httpx.get(url)
        return HTMLParser(resp.text)

def create_roster_list(object_scrape):
    new_roster = []
    for i in range(len(object_scrape)):
        new_roster.append(hl.remove_esc_seq(object_scrape[i].text()))
        
    return new_roster

def check_if_exists(html, query):
    check = html.css_first(query, default='not-found')
    # print(check)
    if check == 'not-found':
        return 'n/a'
    else:
        final = hl.remove_esc_seq(html.css_first(query).text())
        return final
        
        
def parse_team_id(html, team_id):
    new_team = Team(
        index = team_id,
        name = html.css_first("h1.wf-title").text(), 
        roster = [create_roster_list(html.css("div.team-roster-item-name-alias"))],
        country = hl.remove_esc_seq(html.css_first("div.team-header-country").text()), 
        region = check_if_exists(html, "div.rating-txt"), 
        currentRank = check_if_exists(html, "div.rank-num"), 
        rating = check_if_exists(html, "div.rating-num"),
        earnings = check_if_exists(html, 'span[style*="font-size: 22px; font-weight: 500;"]')
    )
    
    return new_team

class GetTeams:
    #TODO related news
    #TODO most recent matches
    #TODO socials if required 
    
    def get_team_by_id(team_id):
        html = get_html(team_id)
        # print(html.css_first("div.rating-txt", default="not-found").text())
        return(parse_team_id(html, team_id))