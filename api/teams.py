"""
Get details of team by either specifying team ID or brute forcing name search
TODO Also give option to list all teams?
"""

import httpx 
from selectolax.parser import HTMLParser

# put data into class for post processing
from dataclasses import dataclass, asdict

@dataclass
class Team:
    name: str
    players: list
    
class GetTeams:
    def get_team_by_id(team_id):
        return {"Team": team_id}