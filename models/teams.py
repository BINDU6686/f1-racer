from pydantic import BaseModel, PrivateAttr
import uuid

class Teams(BaseModel):
    id: str = PrivateAttr(default_factory=lambda:str(uuid.uuid4))
    team_name: str
    year_founded:int 
    total_pole_position:int
    total_race_wins: int
    total_constructor_titles:int
    finishing_position_in_previous_season: int
    created_by: str
    
    