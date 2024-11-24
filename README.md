# Unofficial vlr.gg REST Api
Side project I am working on to learn more about FastAPI. This project allows users to get player data based on the 
[vlr.gg](https://www.vlr.gg/) website

## How to run 
Run using uvicorn server in development mode
`uvicorn main:app --host 0.0.0.0 --port 80 --reload`

Run cron scripts from root using `python -m cron.players`