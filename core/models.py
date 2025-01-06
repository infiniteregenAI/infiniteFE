from pydantic import BaseModel
from typing import List, Optional

class Agent(BaseModel):
    id: Optional[str] = None
    name: str
    role: str
    avatar: str
    expertise: List[str]
    personality: str
    has_knowledge_base: bool = False
    document_count: int = 0

class Document(BaseModel):
    content: str
    metadata: dict
