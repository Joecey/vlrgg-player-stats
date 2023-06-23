# main FastAPI app
from api.players import GetPlayers

from fastapi import FastAPI, status, Response

app = FastAPI(
    title="vlr.gg player API",
    description="An Unofficial REST API for player information from [vlr.gg](https://www.vlr.gg/). "
    "Inspired by the other unofficial API by [axsddlr](https://github.com/axsddlr/vlrggapi) ",
    version="1.0.0",
    
    # set the docs url to be the root URL 
    docs_url="/",
    redoc_url=None,
)

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"Service running": True }

"""
Give option to search by player name or by player ID
Also, async to allow for multipler users to use the api (i think that's how that works)
"""


# @app.get("/player/{player_name}")
# async def read_item(player_name: str):
#     return {"item_name": player_name}


@app.get("/playerID/{player_id}", status_code=status.HTTP_200_OK)
async def read_item(player_id: int, response: Response):
    try:
        player_obj = GetPlayers.get_player_by_id(player_id)
        return player_obj
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Not a valid player ID"
    