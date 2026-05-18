import os
from dotenv import load_dotenv

# Force system to discover the environment properties from disk
load_dotenv()

class AppSettings:
    """Enterprise-grade Environment Registry for GovernLens Core Services."""
    def __init__(self):
        # API Access Token Keys
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
        
        # Supabase Infrastructure Credentials
        self.SUPABASE_URL = os.getenv("SUPABASE_URL", "")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
        
        # Fallback validation to flag missing infrastructure keys early
        if not self.GEMINI_API_KEY:
            print("⚠️ WARNING: GEMINI_API_KEY environment property is not configured.")
        if not self.SUPABASE_URL or not self.SUPABASE_KEY:
            print("⚠️ WARNING: Supabase cloud connection configurations are missing.")

# Global instantiation contract exported out to the application packages
settings = AppSettings()