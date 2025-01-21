import openai
import asyncio
from typing import List, Dict, AsyncGenerator, Tuple
from .models import Agent
from .document_processor import DocumentProcessor
from .search_service import EnhancedSearchService

class ConversationManager:
    def __init__(self, agent: Agent):
        """Initialize the conversation manager with enhanced search capabilities."""
        self.agent = agent
        self.doc_processor = DocumentProcessor(agent.id) if agent.has_knowledge_base else None
        self.search_service = EnhancedSearchService()
    
    async def get_context_with_sources(self, query: str) -> Tuple[str, Dict[str, List[str]]]:
        """Get enhanced context and track sources for validation."""
        context = []
        sources = {
            "knowledge_base": [],
            "internet": []
        }
        
        # Get context from knowledge base if available
        if self.doc_processor:
            try:
                # Assuming get_relevant_context returns (docs, sources)
                kb_result = self.doc_processor.get_relevant_context(query)
                if isinstance(kb_result, tuple) and len(kb_result) == 2:
                    docs, doc_sources = kb_result
                    if docs:
                        context.append("Relevant information from knowledge base:\n" + "\n".join(docs))
                        sources["knowledge_base"].extend(doc_sources)
                else:
                    # Handle case where get_relevant_context doesn't return sources
                    docs = kb_result
                    if docs:
                        context.append("Relevant information from knowledge base:\n" + "\n".join(docs))
            except Exception as e:
                print(f"Error retrieving knowledge base context: {str(e)}")
        
        # Check if internet search would be beneficial
        if self.search_service.should_search(query):
            try:
                # Handle the case where search_internet returns only results
                search_result = await self.search_service.search_internet(query)
                if isinstance(search_result, tuple) and len(search_result) == 2:
                    search_results, search_sources = search_result
                else:
                    # If only results are returned, use the results URL as the source
                    search_results = search_result
                    search_sources = []  # Empty list if no sources available
                
                if search_results:
                    context.append(search_results)
                    sources["internet"].extend(search_sources)
            except Exception as e:
                print(f"Error performing internet search: {str(e)}")
        
        return "\n\n".join(context) if context else "", sources

    async def validate_against_sources(self, output: str, sources: Dict[str, List[str]]) -> Tuple[bool, str]:
        """Validate output against original sources."""
        validation_errors = []
        
        # Validate against knowledge base sources
        if sources["knowledge_base"]:
            for source in sources["knowledge_base"]:
                try:
                    # Get original content from knowledge base
                    original_content = self.doc_processor.get_document_content(source)
                    if not self.check_consistency(output, original_content):
                        validation_errors.append(f"Inconsistency found with knowledge base source: {source}")
                except Exception as e:
                    validation_errors.append(f"Error validating against knowledge base: {str(e)}")

        # Validate against internet sources
        if sources["internet"]:
            for source in sources["internet"]:
                try:
                    # Fetch and verify against original source
                    original_content = await self.search_service.fetch_source_content(source)
                    if not self.check_consistency(output, original_content):
                        validation_errors.append(f"Inconsistency found with internet source: {source}")
                except Exception as e:
                    validation_errors.append(f"Error validating against internet source: {str(e)}")

        return len(validation_errors) == 0, "\n".join(validation_errors)

    def check_consistency(self, output: str, source_content: str) -> bool:
        """Check if the output is consistent with the source content."""
        # Extract key facts and claims from output
        key_facts = self.extract_key_facts(output)
        
        # Compare each fact against source content
        for fact in key_facts:
            if not self.verify_fact(fact, source_content):
                return False
        return True

    def extract_key_facts(self, text: str) -> List[str]:
        """Extract key facts and claims from text."""
        # Simple sentence splitting for now
        sentences = text.split('.')
        return [s.strip() for s in sentences if s.strip()]

    def verify_fact(self, fact: str, source_content: str) -> bool:
        """Verify if a fact is supported by the source content."""
        return fact.lower() in source_content.lower()

    async def get_response(self, messages: List[Dict[str, str]]) -> AsyncGenerator:
        """Get enhanced response with thorough source validation."""
        while True:
            try:
                # Get context and track sources
                context, sources = await self.get_context_with_sources(messages[-1]["content"])
                
                system_message = (
                    f"Personality: {self.agent.personality}\n\n"
                    f"Expertise: {', '.join(self.agent.expertise)}\n\n"
                    f"Role: {self.agent.role}\n\n"
                    "Instructions:\n"
                    "1. Base your response strictly on provided sources\n"
                    "2. Cite specific sources for each claim\n"
                    "3. Maintain factual accuracy\n"
                    "4. Express uncertainty when information is not directly supported\n"
                )
                
                if context:
                    system_message += f"\nContext:\n{context}\n\n"
                
                messages_with_context = [
                    {"role": "system", "content": system_message}
                ] + messages
                
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages_with_context,
                    temperature=0.7,
                    max_tokens=800,
                    stream=True
                )
                
                full_output = ""
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        partial_output = chunk.choices[0].delta.content
                        full_output += partial_output
                        yield partial_output

                # Validate output against original sources
                is_valid, validation_errors = await self.validate_against_sources(full_output, sources)
                
                if not is_valid:
                    self.log_debug_info("Validation Failed", validation_errors)
                    # Regenerate response with error feedback
                    messages[-1]["content"] += f"\n\nPlease correct the following errors:\n{validation_errors}"
                    continue
                
                # Log successful validation
                self.log_debug_info("Validation", "Response successfully validated against sources")
                break

            except Exception as e:
                self.log_debug_info("Error", str(e))
                yield f"I apologize, but I encountered an error: {str(e)}"
                break

    def log_debug_info(self, step: str, info: str):
        """Log detailed debug information for monitoring."""
        print(f"[DEBUG] Step: {step} - Info: {info}")
