from pydantic import BaseModel
from typing import List, Optional

# Request Models
class CreateAgentRequest(BaseModel):
    name: str
    role: str
    tools: List[str]
    description: str
    instructions: List[str]
    urls: Optional[List[str]] = []

class CreateTeamRequest(BaseModel):
    name: str
    agent_names: List[str]
    instructions: List[str]

# Response Models
class AgentResponse(BaseModel):
    id: str 
    name: str
    role: str
    tools: List[str]
    description: str
    instructions: List[str]
    urls: List[str]
    markdown: bool
    show_tool_calls: bool
    add_datetime_to_instructions: bool

class TeamResponse(BaseModel):
    id: str
    name: str
    agents: List[AgentResponse]
    instructions: List[str]
    markdown: bool
    show_tool_calls: bool

class CreateTeamResponse(BaseModel):
    message: str
    team: TeamResponse

class CreateAgentResponse(BaseModel):
    message: str
    agent: AgentResponse