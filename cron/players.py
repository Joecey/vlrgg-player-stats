'''
CRON job file to scrape players periodically and add their information to PostgresSQL database 
'''

import httpx 
from selectolax.parser import HTMLParser
