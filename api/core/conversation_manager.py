from typing import List, Dict, AsyncGenerator
from .models import AgentModel
from .document_processor import DocumentProcessor
from .config import settings
from swarm import Swarm, Agent
import os

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
client = Swarm()

class ConversationManager:
    def __init__(self, agent: AgentModel):
        """
            This constructor initializes the conversation manager.
            
            Args :
                agent (Agent) : The agent details.
                
            Returns :
                None
        """
        
        self.agent_personality = agent.personality
        
        self.agent = Agent(
            name=agent.name,
            model="gpt-4o-mini",
            instructions=agent.personality
        )
        self.doc_processor = DocumentProcessor(agent.id) if agent.has_knowledge_base else None
    
    def get_context(self, query: str) -> str:
        """
            This method gets the context from the knowledge base.
            
            Args :
                query (str) : The query.
                
            Returns :
                str : The context.
        """
        if not self.doc_processor:
            return ""
        try:
            docs = self.doc_processor.get_relevant_context(query)
            if docs:
                return "\n\nRelevant information from knowledge base:\n" + "\n".join(docs)
        except Exception:
            return ""
        return ""
    
    async def get_response(self, messages: List[Dict[str, str]]) -> AsyncGenerator:
        """ 
            This method gets the response from the agent.
            
            Args :
                messages (List[Dict[str, str]]) : The conversation messages.
                
            Returns :
                Generator : The response messages.
        """
        context = self.get_context(messages[-1]["content"]) if messages else ""
        system_message = f"Personality : {self.agent_personality} \n\n Context : {context}"
        
        messages_with_context = [
            {"role": "system", "content": system_message}
        ] + messages
        
        response =  client.run(
            agent=self.agent,
            messages=messages_with_context,
            stream=True
        )
        
        for chunk in response:
            if "content" in chunk:
                yield(chunk["content"])