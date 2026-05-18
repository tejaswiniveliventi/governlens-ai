
# core/database.py
from supabase import create_client, Client
from core.config import settings

def get_supabase_client() -> Client:
    """Instantiates a clean thread-safe client lifecycle instance."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("Critical System Error: Missing SUPABASE_URL or SUPABASE_KEY configurations.")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def init_db():
    """
    With Supabase Client UI paradigms, your tables are constructed visually 
    via the online Table Editor. 
    
    Ensure you create these tables in public schema via Supabase Dashboard UI:
    1. 'design_plans' -> Columns: id (int8), project_name (text), env_context (text), source_text (text)
    2. 'mock_tables'  -> Columns: id (int8), plan_id (int8, FK references design_plans), table_name (text), data_purpose (text)
    3. 'mock_columns' -> Columns: id (int8), table_id (int8, FK references mock_tables), column_name (text), implied_type (text), contextual_clues (text), sensitivity_tier (text), hipaa_rule_hit (text), quote_from_source (text)
    4. 'mock_relationships' -> Columns: id (int8), plan_id (int8, FK references design_plans), source_table (text), target_table (text)
    """
    pass