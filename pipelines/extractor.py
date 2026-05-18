import yaml
import json
from google import genai
from google.genai import types
from core.config import settings
from models.structures import ImplicitSchemaBlueprint

class TextExtractor:
    def __init__(self):
        with open("config/governance_rules.yaml", "r") as f:
            self.rules = yaml.safe_load(f)
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def parse_text(self, context_payload: str) -> ImplicitSchemaBlueprint:
        instruction = self.rules["prompts"]["extractor_instruction"]
        model_name = self.rules["system_settings"]["model_target"]
        temp = self.rules["system_settings"]["temperature"]
        
        response = self.client.models.generate_content(
            model=model_name,
            contents=f"PAYLOAD TO SCAPE:\n{context_payload}",
            config=types.GenerateContentConfig(
                system_instruction=instruction,
                temperature=temp,
                response_mime_type="application/json",
                response_schema=ImplicitSchemaBlueprint,
            ),
        )
        
        # Enforce validation structure contract via dynamic json payload handling
        validated_data = json.loads(response.text)
        return ImplicitSchemaBlueprint(**validated_data)