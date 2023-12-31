"""
MIT License

Copyright (c) 2023 Joe Linogao

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# main FastAPI app
from api.players import GetPlayers
from api.teams import GetTeams
from fastapi import FastAPI, status, Response, Request

# Limit the amount of requests using slowapi so vercel doesn't blow up
# also saw thi in axsddlr's solution, so i decided to use it too
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import os

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="vlr.gg player API",
    description="An Unofficial REST API for player information from [vlr.gg](https://www.vlr.gg/). "
    "Inspired by the other unofficial API by [axsddlr](https://github.com/axsddlr/vlrggapi) ",
    version="1.0.0",
    
    # set the docs url to be the root URL 
    docs_url='/',
    redoc_url=None,
)

# set limit rate for API
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
limiter_amount = "200/minute"

@app.get("/health", status_code=status.HTTP_200_OK)
def service_health():
    return {"Service running": True}

"""
Give option to search by player name or by player ID
Also, async to allow for multipler users to use the api (i think that's how that works)
"""

@app.get("/teamID/{team_id}", status_code=status.HTTP_200_OK)
@limiter.limit(limiter_amount)
async def get_team_info_by_id(team_id: int, response: Response, request: Request):
    try:
        player_obj = GetTeams.get_team_by_id(team_id)
        return player_obj
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Not a valid team ID"


@app.get("/playerID/{player_id}", status_code=status.HTTP_200_OK)
@limiter.limit(limiter_amount)
async def get_player_info_by_id(player_id: int, response: Response, request: Request):
    try:
        player_obj = GetPlayers.get_player_by_id(player_id)
        return player_obj
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Not a valid player ID"
    
@app.get("/playerName/{player_name}", status_code=status.HTTP_200_OK)
@limiter.limit(limiter_amount)
async def get_player_info_by_name(player_name: str, response: Response, request: Request):
    try:
        player_obj = GetPlayers.get_player_by_name(player_name)
        return player_obj
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Not a valid player name"
    