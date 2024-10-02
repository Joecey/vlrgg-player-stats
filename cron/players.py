'''
CRON job file to scrape players periodically and add their information to PostgresSQL database 
'''

import httpx 
from selectolax.parser import HTMLParser
from database.database import SessionLocal, engine
from models import players
from datetime import datetime

players.Base.metadata.create_all(bind=engine)

# initialise database 
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"An issue occurred connecting to database: {e}")
    finally:
        db.close()


def process_player_information():
    pass

def main():
    print(f"Parsing players at time: {datetime.now()}")
    
    pass
if __name__ == '__main__':
    main()
