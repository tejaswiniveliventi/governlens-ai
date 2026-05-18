from models.structures import ImplicitSchemaBlueprint

class HipaasessmentEngine:
    def __init__(self):
        self.high_risk_anchors = ["ssn", "mrn", "patient_id", "medicaid_no", "tax_id", "social_security"]
        self.clinical_indicators = ["icd_code", "diagnosis", "prescription", "rxnorm", "clinical_notes"]

    def analyze_risk(self, blueprint: ImplicitSchemaBlueprint, env_context: str) -> ImplicitSchemaBlueprint:
        if env_context != "Healthcare/Clinical App":
            return blueprint
            
        identity_tables = set()
        for table in blueprint.tables:
            table_name_lower = table.table_name.lower()
            if "patient" in table_name_lower or "user" in table_name_lower or "member" in table_name_lower:
                identity_tables.add(table.table_name)
                
            for col in table.columns:
                if col.column_name.lower() in self.high_risk_anchors:
                    identity_tables.add(table.table_name)

        # Apply relational proximity evaluation logic
        for table in blueprint.tables:
            is_relationally_linked = table.table_name in identity_tables

            for col in table.columns:
                name_lbl = col.column_name.lower()
                
                if name_lbl in self.high_risk_anchors or any(c in name_lbl for c in self.clinical_indicators):
                    col.sensitivity_tier = "Highly Sensitive"
                    col.hipaa_rule_hit = "HIPAA Privacy Rule (§ 160.103) - Core Clinical PHI"
                    
                elif is_relationally_linked:
                    if name_lbl in ["status", "notes", "comments", "status_flag", "narrative_summary"]:
                        col.sensitivity_tier = "Moderately Sensitive"
                        col.hipaa_rule_hit = "HIPAA Safe Harbor - Contextual Proximity Elevation"
                        col.reasoning = "Escalated: Generic column field exists inside a dataset table linked directly to an identity anchor node."
                        
        return blueprint