from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile

class AgentCreate(BaseModel):
    name: str
    role: str
    avatar: str
    expertise: List[str]
    personality: str
    documents: Optional[List[UploadFile]] = None

    class Config:
        arbitrary_types_allowed = True

class AgentUpdate(AgentCreate):
    pass

class AgentResponse(AgentCreate):
    id: str
    has_knowledge_base: bool
    document_count: int

class AgentsMessage(BaseModel):
    agent_id: str
    content: str

class Message(BaseModel):
    role: str
    content: str

class ConversationInput(BaseModel):
    messages: List[AgentsMessage]
    goal: str

class GenerateDocumentInput(BaseModel):
    messages: List[Message]
    goal: str

class GenerateSummaryRequest(BaseModel):
    messages: List[Message]

class CreateDocumentRequest(BaseModel):
    summary: str
    goal: str
    messages: List[Message]

class GetRelevantContextRequest(BaseModel):
    query: str
    k: Optional[int] = 3