import openai
from typing import List, Dict, Optional, Generator
from .models import Agent
from .document_processor import DocumentProcessor

class ConversationManager:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.doc_processor = DocumentProcessor(agent.id) if agent.has_knowledge_base else None
    
    def get_context(self, query: str) -> str:
        if not self.doc_processor:
            return ""
        try:
            docs = self.doc_processor.get_relevant_context(query)
            if docs:
                return "\n\nRelevant information from knowledge base:\n" + "\n".join(docs)
        except Exception:
            return ""
        return ""
    
    def get_response(self, messages: List[Dict[str, str]]) -> Generator:
        context = self.get_context(messages[-1]["content"]) if messages else ""
        system_message = self.agent.personality + context
        
        messages_with_context = [
            {"role": "system", "content": system_message}
        ] + messages
        
        return openai.chat.completions.create(
            model="gpt-4",
            messages=messages_with_context,
            temperature=0.9,
            max_tokens=800,
            stream=True
        )