# pipelines/doc_adapter.py
import requests
from bs4 import BeautifulSoup
from google import genai
from core.config import settings

class DocumentUrlIngestor:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def scrape_url_text(self, url: str) -> str:
        """Scrapes web docs or wiki portals, stripping markup text headers."""
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Target structural text sections while dropping scripts, styling, or cookies
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
                
            return soup.get_text(separator="\n", strip=True)
        except Exception as e:
            raise ValueError(f"Document URL extraction failure: {e}")

    def query_semantic_search(self, doc_text: str, user_query: str) -> str:
        """Acts as a virtual RAG/Semantic block using text context vectors inside Gemini."""
        system_instruction = (
            "You are a compliance document retriever. Your role is to find and quote evidence, "
            "not to synthesize or infer.\n\n"
            "RULES:\n"
            "1. For every claim, provide the exact text quotation from the documentation.\n"
            "2. If a policy is mentioned but details are missing, say 'Policy mentioned but details not provided.'\n"
            "3. Never combine statements from different sections to create new compliance rules.\n"
            "4. Use these confidence levels:\n"
            "   - EXPLICIT: Direct quote matching the query\n"
            "   - IMPLIED: Reasonable inference from stated policy\n"
            "   - NOT_FOUND: Policy not mentioned in documentation\n"
            "5. Always prefer explicit quotes over implied interpretation."
        )
        
        prompt = f"DOCUMENTATION CONTEXT:\n{doc_text}\n\nUSER DISCOVERY QUERY:\n{user_query}"
        
        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config={"system_instruction": system_instruction, "temperature": 0.2}
        )
        return response.text