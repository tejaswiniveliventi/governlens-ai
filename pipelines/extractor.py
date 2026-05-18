from google import genai
from google.genai import types
from models.structures import ImplicitSchemaBlueprint
from core.config import settings

class TextExtractor:
    def __init__(self):
        # Initializes the client with native GenAI bindings
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def parse_text(self, context_payload: str) -> ImplicitSchemaBlueprint:
        prompt = f"""
        You are an elite Data Architecture and HIPAA Compliance Auditor.
        Analyze the provided telemetry text payload. This may include code schemas, 
        unstructured requirements documentation, or both in an intersection layout.
        
        Extract all implied logical database entities, attribute tables, and data fields.
        If both a specifications document and a Git codebase layout are provided, map out 
        the data architecture components mentioned in the code specifically through the lens 
        of the compliance constraints stated in the documentation text.
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, context_payload],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ImplicitSchemaBlueprint,
                temperature=0.1
            ),
        )
        # Parse output directly back into your verified Pydantic schema validation contract
        return ImplicitSchemaBlueprint.model_validate_json(response.text)