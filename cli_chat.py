import os
import json
from typing import Dict, Any
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import dotenv
from chroma_config import get_chroma_client  # Add this import

dotenv.load_dotenv()

class PersonalityBot:
    def __init__(
        self,
        openai_api_key: str,
        personality_path: str = "personality.json",
        collection_name: str = "pdf_embeddings",
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7
    ):
        self.openai_api_key = openai_api_key
        self.personality = self._load_personality(personality_path)
        
        # Initialize ChromaDB with unified configuration
        self.chroma_client = get_chroma_client()
        
        # Get collection
        try:
            self.collection = self.chroma_client.get_collection(name=collection_name)
            self.all_docs = self.collection.get()
        except Exception as e:
            print(f"Error accessing collection: {str(e)}")
            raise
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name=model_name,
            temperature=temperature
        )
        
        # Setup conversation memory
        self.memory = ConversationBufferMemory(
            return_messages=True,
            ai_prefix=self.personality["name"]
        )
        
        # Create system message with personality
        system_template = self._create_system_template()
        
        # Setup chat prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # Initialize conversation chain
        self.conversation = ConversationChain(
            memory=self.memory,
            prompt=self.prompt,
            llm=self.llm
        )

    def _load_personality(self, personality_path: str) -> Dict[str, Any]:
        """Load personality from JSON file."""
        try:
            with open(personality_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading personality file: {str(e)}")
            return {"name": "Assistant", "bio": "", "skills": []}

    def _create_system_template(self) -> str:
        """Create system template using personality information."""
        return f"""You are {self.personality['name']}.

Background:
{self.personality['bio']}

Your skills include: {', '.join(self.personality['skills'])}

When responding to questions:
1. First check if the question requires information from the knowledge base
2. If yes, search the relevant information from the database
3. Provide responses that align with your personality and expertise
4. If you use information from the knowledge base, cite the source
5. If you don't find relevant information, use your general knowledge but stay in character

Remember to maintain a consistent personality throughout the conversation."""

    def _search_knowledge_base(self, query: str, n_results: int = 3):
        """Search the pre-loaded knowledge base documents."""
        try:
            # Use pre-loaded documents instead of generating new embeddings
            if not hasattr(self, 'all_docs') or not self.all_docs['documents']:
                return None
                
            # For now, return the first n_results documents
            # This is a simple approach - you might want to implement more sophisticated
            # search based on your needs
            return {
                'documents': [self.all_docs['documents'][:n_results]],
                'metadatas': [self.all_docs['metadatas'][:n_results]]
            }
            
        except Exception as e:
            print(f"Error searching knowledge base: {str(e)}")
            return None

    def process_message(self, message: str) -> str:
        """
        Process a message and return a response.
        
        Args:
            message (str): User's message
            
        Returns:
            str: Bot's response
        """
        # Search knowledge base
        search_results = self._search_knowledge_base(message)
        
        # Prepare context with search results if available
        context = ""
        if search_results and search_results['documents'][0]:
            context = "\nRelevant information from knowledge base:\n"
            for i, (doc, metadata) in enumerate(zip(search_results['documents'][0], search_results['metadatas'][0])):
                context += f"\nFrom {metadata['source']}:\n{doc}\n"
        
        # Combine user message with context
        full_message = f"{message}\n{context}" if context else message
        
        # Get response using conversation chain
        response = self.conversation.predict(input=full_message)
        
        return response
    
    def process_message_stream(self, message: str):
        """
        Process a message and yield response chunks for streaming.
        
        Args:
            message (str): User's message
                
        Yields:
            str: Chunks of the bot's response
        """
        # Search knowledge base
        search_results = self._search_knowledge_base(message)
        
        # Prepare context with search results if available
        context = ""
        if search_results and search_results['documents'][0]:
            context = "\nRelevant information from knowledge base:\n"
            for i, (doc, metadata) in enumerate(zip(search_results['documents'][0], search_results['metadatas'][0])):
                context += f"\nFrom {metadata['source']}:\n{doc}\n"
        
        # Combine user message with context
        full_message = f"{message}\n{context}" if context else message
        
        # Get streaming response using conversation chain
        response = self.llm.stream(self.prompt.format_messages(
            history=self.memory.load_memory_variables({})["history"],
            input=full_message
        ))
        
        # Process the streaming response
        for chunk in response:
            if chunk.content:
                yield chunk.content
                
        # Update memory after streaming is complete
        self.memory.save_context(
            {"input": full_message},
            {"output": "".join(chunk.content for chunk in response)}
        )

# Example usage
if __name__ == "__main__":
    # Get API key from environment variable
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
    
    # Initialize bot
    bot = PersonalityBot(
        openai_api_key=OPENAI_API_KEY,
        personality_path="personality.json",
        collection_name="pdf_embeddings"
    )
    
    # Interactive chat loop
    print(f"Chat with {bot.personality['name']}! (type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            break
            
        response = bot.process_message(user_input)
        print(f"\n{bot.personality['name']}: {response}\n")