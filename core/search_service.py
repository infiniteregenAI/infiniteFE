from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from typing import Optional, List, Dict, Tuple
from datetime import datetime
import re
import json
from pydantic import BaseModel
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from functools import lru_cache

class SearchResult(BaseModel):
    """Model for structured search results."""
    title: Optional[str]
    snippet: str
    source: Optional[str]
    relevance_score: float

class EnhancedSearchService:
    """
    Enhanced search service with multiple fallback mechanisms and error handling.
    """
    
    def __init__(self, max_retries: int = 3, max_workers: int = 3, cache_size: int = 100):
        """
        Initialize the search service.
        
        Args:
            max_retries: Maximum number of retry attempts for failed searches
            max_workers: Maximum number of concurrent search workers
            cache_size: Size of the LRU cache for search results
        """
        self.max_retries = max_retries
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.cache_size = cache_size
        self.initialize_search_wrappers()
        
    def initialize_search_wrappers(self):
        """Initialize search wrappers with fallback mechanisms."""
        try:
            # Primary search wrapper with API backend
            self.primary_wrapper = DuckDuckGoSearchRun(
                api_wrapper=DuckDuckGoSearchAPIWrapper(backend="api")
            )
            
            self.backup_wrappers = [
                self._create_custom_search_wrapper(),
                DuckDuckGoSearchRun(
                    api_wrapper=DuckDuckGoSearchAPIWrapper(backend="html")
                )
            ]
        except Exception as e:
            print(f"Initialization error: {str(e)}")
            # Ensure we always have at least one working search method
            self.primary_wrapper = self._create_custom_search_wrapper()
            self.backup_wrappers = []

    def _create_custom_search_wrapper(self):
        """Create a custom search wrapper using direct HTML parsing."""
        class CustomSearchWrapper:
            @retry(
                stop=stop_after_attempt(3),
                wait=wait_exponential(multiplier=1, min=4, max=10)
            )
            def run(self, query: str) -> str:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    }
                    
                    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        results = []
                        
                        # Extract search results
                        for result in soup.select('.result__body'):
                            title_elem = result.select_one('.result__title')
                            snippet_elem = result.select_one('.result__snippet')
                            
                            title = title_elem.get_text(strip=True) if title_elem else "No Title"
                            snippet = snippet_elem.get_text(strip=True) if snippet_elem else "No Snippet"
                            
                            if snippet:
                                results.append(f"{title}\n{snippet}")
                        
                        if results:
                            return '\n\n'.join(results[:5])  # Return top 5 results
                        else:
                            print("No results found in the parsed HTML.")
                            return ""
                    else:
                        print(f"HTTP request failed with status code {response.status_code}.")
                        return ""
                except requests.exceptions.RequestException as req_err:
                    print(f"Request error: {req_err}")
                    return ""
                except Exception as e:
                    print(f"Custom search error: {str(e)}")
                    return ""
        
        return CustomSearchWrapper()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((requests.RequestException, ConnectionError))
    )
    async def _execute_single_search(self, query: str, search_wrapper) -> Optional[str]:
        """
        Execute a single search attempt with enhanced error handling.
        
        Args:
            query: Search query string
            search_wrapper: Search wrapper instance to use
            
        Returns:
            Optional[str]: Search results or None if search failed
        """
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                search_wrapper.run,
                query
            )
            
            # Validate result
            if result and isinstance(result, str) and len(result.strip()) > 0:
                return result
            return None
            
        except Exception as e:
            print(f"Search attempt failed: {str(e)}")
            return None

    async def _parallel_search(self, query: str) -> List[str]:
        """
        Execute parallel searches with fallback mechanisms.
        
        Args:
            query: Search query string
            
        Returns:
            List[str]: List of search results
        """
        all_wrappers = [self.primary_wrapper] + self.backup_wrappers
        search_tasks = []
        
        for wrapper in all_wrappers:
            task = asyncio.create_task(self._execute_single_search(query, wrapper))
            search_tasks.append(task)
        
        results = []
        timeout = 30  # 30 second timeout
        
        try:
            done, pending = await asyncio.wait(
                search_tasks,
                timeout=timeout,
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Process completed tasks
            for task in done:
                try:
                    result = await task
                    if result:
                        results.append(result)
                        # Cancel remaining tasks if we have a good result
                        if len(results) >= 1:
                            for p in pending:
                                p.cancel()
                            break
                except Exception as e:
                    print(f"Task processing error: {str(e)}")
            
            # Cancel any remaining tasks
            for task in pending:
                task.cancel()
                
        except asyncio.TimeoutError:
            print("Search timeout occurred")
            # Cancel all tasks on timeout
            for task in search_tasks:
                task.cancel()
        
        return results

    @lru_cache(maxsize=100)
    def _calculate_relevance(self, text: str, query: str) -> float:
        """
        Calculate relevance score based on keyword matching and text quality.
        
        Args:
            text: Text to analyze
            query: Search query
            
        Returns:
            float: Relevance score between 0 and 1
        """
        query_terms = set(query.lower().split())
        text_lower = text.lower()
        
        # Calculate keyword match ratio
        matched_terms = sum(1 for term in query_terms if term in text_lower)
        keyword_score = matched_terms / len(query_terms) if query_terms else 0
        
        # Calculate text quality score
        avg_sentence_length = len(text.split()) / (len(text.split('.')) + 1)
        quality_score = min(1.0, avg_sentence_length / 20)  # Normalize to 0-1
        
        # Combined score with weights
        return (0.7 * keyword_score) + (0.3 * quality_score)

    def _parse_search_result(self, raw_result: str) -> List[SearchResult]:
        """
        Parse and structure raw search results.
        
        Args:
            raw_result: Raw search result string
            
        Returns:
            List[SearchResult]: List of structured search results
        """
        results = []
        segments = raw_result.split('\n\n')
        
        for segment in segments:
            if segment.strip():
                results.append(SearchResult(
                    title=None,
                    snippet=segment.strip(),
                    source=None,
                    relevance_score=0.0
                ))
        
        return results

    def should_search(self, query: str) -> bool:
        """
        Determine if a query requires internet search.
        
        Args:
            query: Query string to analyze
            
        Returns:
            bool: True if search is needed, False otherwise
        """
        patterns = {
            'time': r'\b(current|latest|recent|today|now)\b',
            'year': r'\b\d{4}\b',
            'date': r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',
            'questions': r'\b(what|who|where|when|why|how)\b',
            'definition': r'\b(define|meaning of|definition)\b',
            'comparison': r'\b(versus|vs|compared to|difference between)\b',
            'news': r'\b(news|headline|announcement)\b',
            'facts': r'\b(fact|statistic|data|research|study)\b',
            'events': r'\b(event|conference|release|launch)\b'
        }
        
        query_lower = query.lower()
        return any(bool(re.search(pattern, query_lower)) for pattern in patterns.values())

    async def search_internet(self, query: str, max_results: int = 3) -> Optional[str]:
        """
        Perform enhanced internet search with fallback mechanisms.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            Optional[str]: Formatted search results or None if search failed
        """
        try:
            # Execute parallel searches
            raw_results = await self._parallel_search(query)
            
            if not raw_results:
                # Fallback to simple search if all parallel searches fail
                try:
                    result = await self._execute_single_search(query, self._create_custom_search_wrapper())
                    if result:
                        raw_results = [result]
                except Exception as e:
                    print(f"Fallback search error: {str(e)}")
                    return None
            
            if not raw_results:
                return None
                
            # Process results
            all_results = []
            seen_snippets = set()
            
            for raw_result in raw_results:
                parsed_results = self._parse_search_result(raw_result)
                for result in parsed_results:
                    # Deduplication
                    normalized_snippet = ' '.join(result.snippet.lower().split())
                    if normalized_snippet not in seen_snippets:
                        result.relevance_score = self._calculate_relevance(result.snippet, query)
                        all_results.append(result)
                        seen_snippets.add(normalized_snippet)
            
            # Sort and limit results
            sorted_results = sorted(
                all_results,
                key=lambda x: x.relevance_score,
                reverse=True
            )[:max_results]
            
            # Format results
            if sorted_results:
                formatted_results = []
                for idx, result in enumerate(sorted_results, 1):
                    formatted_results.append(
                        f"{idx}. {result.snippet.strip()} "
                        f"(Relevance: {result.relevance_score:.2f})"
                    )
                return "\nRelevant search results:\n" + "\n\n".join(formatted_results)
            
            return None
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return None

    def get_research_summary(self, query: str, search_results: List[SearchResult]) -> str:
        """
        Generate a research summary from search results.
        
        Args:
            query: Original search query
            search_results: List of search results
        
        Returns:
            str: Formatted research summary
        """
        if not search_results:
            return f"No relevant results were found for your query: {query}"
        
        summary_lines = [
            f"Research summary for query: '{query}':",
            "-" * 50
        ]
        
        for idx, result in enumerate(search_results, 1):
            title = result.title if result.title else "No title available"
            source = result.source if result.source else "Unknown source"
            snippet = result.snippet.strip() if result.snippet else "No content available"
            relevance = f"{result.relevance_score:.2f}"
            
            summary_lines.append(
                f"{idx}. {title}\n   Snippet: {snippet}\n   Source: {source}\n   Relevance: {relevance}\n"
            )
        
        return "\n".join(summary_lines)

    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text using sentence analysis."""
        sentences = text.split('.')
        key_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                importance_score = self._calculate_sentence_importance(sentence)
                if importance_score > 0.5:
                    key_points.append(sentence)
        
        return key_points

    def _calculate_sentence_importance(self, sentence: str) -> float:
        """Calculate sentence importance based on various factors."""
        importance_keywords = {
            'significant', 'important', 'key', 'main', 'primary',
            'essential', 'crucial', 'fundamental', 'major', 'critical'
        }
        
        words = sentence.lower().split()
        
        # Calculate metrics
        keyword_score = sum(1 for word in words if word in importance_keywords) / len(words)
        length_score = min(1.0, len(words) / 20)
        
        return (0.6 * keyword_score) + (0.4 * length_score)

    def _identify_topic(self, text: str) -> str:
        """Identify the topic of a piece of text."""
        topics = {
            'Definition': ['is', 'means', 'refers to', 'defined as'],
            'Process': ['how', 'steps', 'procedure', 'method'],
            'Comparison': ['versus', 'compared to', 'different from'],
            'Statistics': ['percent', 'number', 'rate', 'statistics'],
            'Historical': ['history', 'originally', 'previously', 'past'],
            'Current': ['current', 'now', 'present', 'recent']
        }
        
        text_lower = text.lower()
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
                
        return "General Information"
