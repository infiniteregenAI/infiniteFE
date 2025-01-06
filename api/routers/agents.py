from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
from ..models import AgentCreate, AgentUpdate, AgentResponse
from core import AgentManager, Agent

router = APIRouter()
agent_manager = AgentManager()

@router.post("/agents/", response_model=AgentResponse)
async def create_agent(
    agent: AgentCreate = Form(...),
    documents: List[UploadFile] = File(None)
):
    try:
        agent_obj = Agent(**agent.dict())
        doc_contents = []
        if documents:
            doc_contents = [await doc.read() for doc in documents]
        return agent_manager.create_agent(agent_obj, doc_contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/agents/", response_model=List[AgentResponse])
async def get_all_agents():
    return agent_manager.get_all_agents()

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent: AgentUpdate,
    documents: List[UploadFile] = File(None)
):
    try:
        agent_obj = Agent(**agent.dict())
        doc_contents = []
        if documents:
            doc_contents = [await doc.read() for doc in documents]
        updated = agent_manager.update_agent(agent_id, agent_obj)
        if not updated:
            raise HTTPException(status_code=404, detail="Agent not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    if not agent_manager.delete_agent(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted"}