from typing import List, Optional
import json
import os
from .models import Agent
from .document_processor import DocumentProcessor

class AgentManager:
    def __init__(self, storage_path: str = "agents.json"):
        """
            This constructor initializes the agent manager.
            
            Args :
                storage_path (str) : The path to the agents storage file.
                
            Returns :
                None
        """
        self.storage_path = storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """
            This method ensures that the storage file exists.
            
            Returns :
                None
        """
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump([], f)
    
    def create_agent(self, agent: Agent, documents: List[bytes] = None) -> Agent:
        """
            This method creates a new agent.
            
            Args :
                agent (Agent) : The agent details.
                documents (List[bytes]) : List of documents to be added to the agent's knowledge base.
                
            Returns :
                Agent : The created agent details.
        """
        agents = self.get_all_agents()
        agents = [agent.model_dump() for agent in agents]
        agent.id = str(len(agents) + 1)
        
        if documents:
            processor = DocumentProcessor(agent.id)
            for idx ,doc in enumerate(documents):
                processor.add_document(content = doc , filename= f"{agent.id}_document_{idx}.txt")
            agent.has_knowledge_base = True
            agent.document_count = len(documents)
        
        agents.append(agent.model_dump())
        with open(self.storage_path, 'w') as f:
            json.dump(agents, f, indent=2)
        
        return agent
    
    def get_all_agents(self) -> List[Agent]:
        """
            This method returns all agents.
            
            Returns :
                List[Agent] : List of all agents.
        """
        with open(self.storage_path, 'r') as f:
            agents = json.load(f)
        return [Agent(**agent) for agent in agents]
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """
            This method returns an agent by id.
            
            Args :
                agent_id (str) : The id of the agent.
                
            Returns :
                Agent : The agent details.
        """
        agents = self.get_all_agents()
        for agent in agents:
            if agent.id == agent_id:
                return agent
        return None
    
    def update_agent(self, agent_id: str, agent: Agent) -> Optional[Agent]:
        """
            This method updates an agent by id.
            
            Args :
                agent_id (str) : The id of the agent.
                agent (Agent) : The updated agent details.
                
            Returns :
                Agent : The updated agent details.
        """
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
        """
            This method deletes an agent by id.
            
            Args :
                agent_id (str) : The id of the agent.
                
            Returns :
                bool : The result of the operation.
        """
        agents = self.get_all_agents()
        agents = [a for a in agents if a.id != agent_id]
        
        knowledge_base_path = f"agent_knowledge/{agent_id}"
        if os.path.exists(knowledge_base_path):
            import shutil
            shutil.rmtree(knowledge_base_path)
        
        with open(self.storage_path, 'w') as f:
            json.dump([a.dict() for a in agents], f, indent=2)
        return True