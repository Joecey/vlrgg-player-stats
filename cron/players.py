'''
CRON job file to scrape players periodically and add their information to PostgresSQL database 
'''

import httpx 
from selectolax.parser import HTMLParser
from database.database import SessionLocal
from models import players
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def process_player_information():
    pass

def main():
    # connect to our session
    session = SessionLocal()
    
    print(f"Parsing players at time: {datetime.now()}")

    # testing adding to the players database - we require the type created in models
    player_test = players.Player(
        playerIGN="test", 
        playerId=150, 
        country="test", 
        lastAgents=["test"], 
        lastAgentsUsageOrdered=[1], 
        lastUpdated=datetime.now())
    
    player_test2 = players.Player(
        playerIGN="test", 
        playerId=40, 
        country="test", 
        lastAgents=["test"], 
        lastAgentsUsageOrdered=[1], 
        lastUpdated=datetime.now())
    
    
    # add player to be committed
    session.add_all([player_test, player_test2])
    
    # commit new player to database
    session.commit()
    
    
    pass
if __name__ == '__main__':
    main()
