import httpx 
from selectolax.parser import HTMLParser

# put data into class for post processing
from dataclasses import dataclass, asdict

@dataclass
class Player:
    index: int
    ign: str
    fullName: str

def get_html(player_id):
    url = "https://www.vlr.gg/player/{}".format(player_id)
    resp = httpx.get(url)
    return HTMLParser(resp.text)

# post processing to remove all special characters (if needed)
def remove_special(text):
    return ''.join(e for e in text if e.isalnum())

def parse_player(html, id):
    new_player = Player(
        index = id,
        ign = remove_special(html.css_first("h1.wf-title").text()),
        fullName = html.css_first("h2.player-real-name").text()
    )
    
    print(new_player)

def main(): 
    for i in range (1,10):
        player_id = i
        html = get_html(player_id)
        parse_player(html, player_id)
    

if __name__ == '__main__':
    main()