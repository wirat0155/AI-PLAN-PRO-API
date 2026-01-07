from pydantic import BaseModel
from typing import List

class TeamMember(BaseModel):
    role: str
    name: str

class PlanRequest(BaseModel):
    project_name: str
    description: str = None
    team_composition: List[TeamMember]
