from core.database import get_supabase_client
from models.structures import ImplicitSchemaBlueprint

class ReportStorageEngine:
    def __init__(self):
        self.supabase = get_supabase_client()

    def save_to_warehouse(self, blueprint: ImplicitSchemaBlueprint, env: str, label: str) -> int:
        # Commit parent execution design block metrics tracking parameter variables
        plan_res = self.supabase.table("design_plans").insert({
            "project_name": "GovernLens Auto Audit Run",
            "env_context": env,
            "raw_text_chunk": label,
            "source_text": label
        }).execute()
        
        plan_id = plan_res.data[0]["id"]
        
        for table in blueprint.tables:
            table_res = self.supabase.table("mock_tables").insert({
                "plan_id": plan_id,
                "table_name": table.table_name,
                "deduced_context": f"Parsed logical architecture context block."
            }).execute()
            
            table_id = table_res.data[0]["id"]
            
            for col in table.columns:
                self.supabase.table("mock_columns").insert({
                    "table_id": table_id,
                    "column_name": col.column_name,
                    "implied_type": col.implied_type,
                    "sensitivity_tier": col.sensitivity_tier,
                    "hipaa_rule_hit": col.hipaa_rule_hit,
                    "quote_from_source": col.quote_from_source,
                    "reasoning": col.reasoning
                }).execute()
                
        return plan_id