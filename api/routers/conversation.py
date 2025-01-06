from fastapi import APIRouter, HTTPException
from typing import List
from sse_starlette.sse import EventSourceResponse
from ..models import ConversationInput, Message
from core import ConversationManager, AgentManager, DocumentGenerator

router = APIRouter()
agent_manager = AgentManager()

@router.post("/conversation/{agent_id}/chat")
async def chat(agent_id: str, conversation: ConversationInput):
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    conv_manager = ConversationManager(agent)
    async def event_generator():
        response = conv_manager.get_response(conversation.messages)
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield {
                    "data": chunk.choices[0].delta.content
                }
    
    return EventSourceResponse(event_generator())

@router.post("/conversation/generate-document")
async def generate_document(conversation: ConversationInput):
    try:
        summary = DocumentGenerator.generate_summary(
            conversation.messages, 
            conversation.goal
        )
        doc_io = DocumentGenerator.create_document(
            summary, 
            conversation.goal, 
            conversation.messages
        )
        return doc_io
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))