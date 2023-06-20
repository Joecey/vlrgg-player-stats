# main FastAPI app
from typing import Union
from api.players import GetPlayers

from fastapi import FastAPI

app = FastAPI(
    title="vlr.gg player API",
    description="An Unofficial REST API for player information from [vlr.gg](https://www.vlr.gg/). "
    "Inspired by the other unofficial API by [Rehkloos](https://github.com/Rehkloos) ",
    version="1.0.0",
    
    # set the docs url to be the root URL 
    docs_url="/",
    redoc_url=None,
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/player/{player_name}")
def read_item(player_name: str):
    return {"item_name": player_name}

@app.get("/playerID/{player_id}")
def read_item(player_id: int):
    player_obj = GetPlayers.get_player_by_id(player_id)
    return player_obj
    