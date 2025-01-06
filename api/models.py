from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile

class AgentCreate(BaseModel):
    name: str
    role: str
    avatar: str
    expertise: List[str]
    personality: str

class AgentUpdate(AgentCreate):
    pass

class AgentResponse(AgentCreate):
    id: str
    has_knowledge_base: bool
    document_count: int

class Message(BaseModel):
    role: str
    content: str

class ConversationInput(BaseModel):
    messages: List[Message]
    goal: str