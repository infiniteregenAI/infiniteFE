from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
from api.models import  AgentUpdate, AgentResponse
from ..core.agent_manager import AgentManager
from ..core.models import AgentModel
import traceback

router = APIRouter()
agent_manager = AgentManager()

@router.post("/agents/", response_model=AgentResponse)
async def create_agent(
    name: str = Form(...),
    role: str = Form(...),
    avatar: str = Form(...),
    expertise: List[str] = Form(...),
    personality: str = Form(...),
    documents: List[UploadFile] = File(None)
):
    """
        This api endpoint is used to create a new agent.
        It expects a form data with the following fields:
        
        Args :
            agent (AgentCreate) : The agent details.
            documents (List[UploadFile]) : List of documents to be added to the agent's knowledge base.
            
        Returns :
            AgentResponse : The created agent details.
    """
    try:
        agent = {
            "name": name,
            "role": role,
            "avatar": avatar,
            "expertise": expertise[0].split(','),
            "personality": personality,
        }
        agent_obj = AgentModel(**agent)
        doc_contents = []
        if documents:
            doc_contents = [await doc.read() for doc in documents]
        return agent_manager.create_agent(agent_obj, doc_contents)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/agents/", response_model=List[AgentResponse])
async def get_all_agents():
    """
        This api endpoint is used to get all agents.
        
        Returns :
            List[AgentResponse] : List of all agents.
    """
    return agent_manager.get_all_agents()

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """
        This api endpoint is used to get an agent by id.
        
        Args :
            agent_id (str) : The id of the agent.
            
        Returns :
            AgentResponse : The agent details.
    """
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
    """
        This api endpoint is used to update an agent by id.
        
        Args :
            agent_id (str) : The id of the agent.
            agent (AgentUpdate) : The updated agent details.
            documents (List[UploadFile]) : List of documents to be added to the agent's knowledge base.
            
        Returns :
            AgentResponse : The updated agent details.
    """
    try:
        agent_obj = AgentModel(**agent.dict())
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
    """
        This api endpoint is used to delete an agent by id.
        
        Args :
            agent_id (str) : The id of the agent.
            
        Returns :
            dict : The response message.
    """
    if not agent_manager.delete_agent(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted"}