import json
import os
from typing import List, Dict
from document_processor import AgentDocumentProcessor

class AgentStorage:
    def __init__(self, file_path: str = "agents.json"):
        """
        Initialize the AgentStorage with a file path for persistent storage.
        
        Args:
            file_path (str): Path to the JSON file for storing agent data
        """
        self.file_path = file_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create the storage file if it doesn't exist."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def get_all_agents(self) -> List[Dict]:
        """
        Retrieve all stored agents.
        
        Returns:
            List[Dict]: List of all agent configurations
        """
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def add_agent(self, agent: Dict) -> str:
        """
        Add a new agent to storage and process any associated documents.
        
        Args:
            agent (Dict): Agent configuration including optional documents
            
        Returns:
            str: ID of the created agent
        """
        agents = self.get_all_agents()
        agent['id'] = str(len(agents) + 1)
        
        # Handle document processing if documents are present
        if 'documents' in agent and agent['documents']:
            try:
                processor = AgentDocumentProcessor(
                    agent_id=agent['id'],
                    openai_api_key=os.getenv("OPENAI_API_KEY")
                )
                
                # Process each uploaded document
                for doc in agent['documents']:
                    success, message = processor.add_document(doc)
                    if not success:
                        print(f"Warning: {message}")
                
                # Store document references
                agent['has_knowledge_base'] = True
                agent['document_count'] = len(agent['documents'])
                
            except Exception as e:
                print(f"Error processing documents: {str(e)}")
                agent['has_knowledge_base'] = False
                agent['document_count'] = 0
        else:
            agent['has_knowledge_base'] = False
            agent['document_count'] = 0
        
        # Remove the actual document data before storing
        if 'documents' in agent:
            del agent['documents']
        
        agents.append(agent)
        with open(self.file_path, 'w') as f:
            json.dump(agents, f, indent=2)
        
        return agent['id']
    
    def update_agent(self, agent_id: str, updated_agent: Dict) -> bool:
        """
        Update an existing agent's configuration.
        
        Args:
            agent_id (str): ID of the agent to update
            updated_agent (Dict): New agent configuration
            
        Returns:
            bool: True if update was successful
        """
        agents = self.get_all_agents()
        for i, agent in enumerate(agents):
            if agent['id'] == agent_id:
                # Preserve knowledge base status
                updated_agent['has_knowledge_base'] = agent.get('has_knowledge_base', False)
                updated_agent['document_count'] = agent.get('document_count', 0)
                updated_agent['id'] = agent_id
                agents[i] = updated_agent
                
                with open(self.file_path, 'w') as f:
                    json.dump(agents, f, indent=2)
                return True
        return False
    
    def delete_agent(self, agent_id: str) -> bool:
        """
        Delete an agent and its associated knowledge base.
        
        Args:
            agent_id (str): ID of the agent to delete
            
        Returns:
            bool: True if deletion was successful
        """
        agents = self.get_all_agents()
        agents = [a for a in agents if a['id'] != agent_id]
        
        # Delete agent's knowledge base directory if it exists
        knowledge_base_path = f"agent_knowledge/{agent_id}"
        if os.path.exists(knowledge_base_path):
            try:
                import shutil
                shutil.rmtree(knowledge_base_path)
            except Exception as e:
                print(f"Warning: Could not delete knowledge base: {str(e)}")
        
        with open(self.file_path, 'w') as f:
            json.dump(agents, f, indent=2)
        
        return True
    
    def get_agent(self, agent_id: str) -> Dict:
        """
        Retrieve a specific agent's configuration.
        
        Args:
            agent_id (str): ID of the agent to retrieve
            
        Returns:
            Dict: Agent configuration or None if not found
        """
        agents = self.get_all_agents()
        for agent in agents:
            if agent['id'] == agent_id:
                return agent
        return None