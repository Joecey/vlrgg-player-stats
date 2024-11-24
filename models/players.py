'''
ORM Models used for database
'''

# class AgentInfo(BaseModel):
#     agentName: str
#     usage: int

# class PlayerInfo(BaseModel):
#     playerIGN: str
#     country: str
#     agentList: List[AgentInfo]
#     lastUpdated: Annotated[datetime, Body()]


from sqlalchemy import Column, Integer, String, ARRAY, DateTime

# call database.py file wiht Base
from database.database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key = True)    # this auto increments
    playerIGN = Column(String) # TODO: we should allow this to be indexable
    playerId = Column(Integer, unique=True) # TODO: we should allow this to be indexable
    country = Column(String)
    lastAgents = Column(ARRAY(String))
    lastAgentsUsageOrdered = Column(ARRAY(Integer))
    lastUpdated = Column(DateTime)
    
    