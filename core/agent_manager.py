from typing import List, Dict, Optional
import json
import os
from .models import Agent
from .document_processor import DocumentProcessor

class AgentManager:
    def __init__(self, storage_path: str = "agents.json"):
        self.storage_path = storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump([], f)
    
    def create_agent(self, agent: Agent, documents: List[bytes] = None) -> Agent:
        agents = self.get_all_agents()
        agent.id = str(len(agents) + 1)
        
        if documents:
            processor = DocumentProcessor(agent.id)
            for doc in documents:
                processor.add_document(doc)
            agent.has_knowledge_base = True
            agent.document_count = len(documents)
        
        agents.append(agent.dict())
        with open(self.storage_path, 'w') as f:
            json.dump(agents, f, indent=2)
        
        return agent
    
    def get_all_agents(self) -> List[Agent]:
        with open(self.storage_path, 'r') as f:
            agents = json.load(f)
        return [Agent(**agent) for agent in agents]
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        agents = self.get_all_agents()
        for agent in agents:
            if agent.id == agent_id:
                return agent
        return None
    
    def update_agent(self, agent_id: str, agent: Agent) -> Optional[Agent]:
        agents = self.get_all_agents()
        for i, existing_agent in enumerate(agents):
            if existing_agent.id == agent_id:
                agent.id = agent_id
                agents[i] = agent.dict()
                with open(self.storage_path, 'w') as f:
                    json.dump([a.dict() for a in agents], f, indent=2)
                return agent
        return None
    
    def delete_agent(self, agent_id: str) -> bool:
        agents = self.get_all_agents()
        agents = [a for a in agents if a.id != agent_id]
        
        knowledge_base_path = f"agent_knowledge/{agent_id}"
        if os.path.exists(knowledge_base_path):
            import shutil
            shutil.rmtree(knowledge_base_path)
        
        with open(self.storage_path, 'w') as f:
            json.dump([a.dict() for a in agents], f, indent=2)
        return True