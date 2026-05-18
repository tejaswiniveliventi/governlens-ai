import os
import yaml
from core.database import get_supabase_client
from models.structures import ImplicitSchemaBlueprint

class ReportStorageEngine:
    def __init__(self):
        self.supabase = get_supabase_client()

    def save_to_warehouse(self, blueprint: ImplicitSchemaBlueprint, env_context: str, source_label: str) -> int:
        """Commits extracted architectural schemas to Supabase storage cleanly."""
        
        # Unify payload elements to satisfy both historical and updated database constraints
        plan_payload = {
            "project_name": "GovernLens Auto Audit Run",
            "env_context": env_context,
            "source_text": source_label,       # -- Satisfies the older strict NOT-NULL column constraint
            "raw_text_chunk": source_label      #-- Maps to your newly modified tracking structure
        }
        
        # Execute the primary plan registration trace
        plan_res = self.supabase.table("design_plans").insert(plan_payload).execute()
        plan_id = plan_res.data[0]["id"]

        # Safely iterate through logical entities and unpack structural children
        for table in blueprint.tables:
            table_payload = {
                "plan_id": plan_id,
                "table_name": table.table_name
            }
            table_res = self.supabase.table("mock_tables").insert(table_payload).execute()
            table_id = table_res.data[0]["id"]

            for col in table.columns:
                column_payload = {
                    "table_id": table_id,
                    "column_name": col.column_name,
                    "implied_type": col.implied_type,
                    "sensitivity_tier": col.sensitivity_tier,
                    "hipaa_rule_hit": col.hipaa_rule_hit,
                    "reasoning": col.reasoning,
                    "quote_from_source": col.quote_from_source
                }
                self.supabase.table("mock_columns").insert(column_payload).execute()

        return plan_id