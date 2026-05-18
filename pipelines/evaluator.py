import yaml
from models.structures import ImplicitSchemaBlueprint

class HipaasessmentEngine:
    def __init__(self):
        with open("config/governance_rules.yaml", "r") as f:
            self.matrix = yaml.safe_load(f)["evaluator_matrices"]

    def analyze_risk(self, blueprint: ImplicitSchemaBlueprint, env_context: str) -> ImplicitSchemaBlueprint:
        if env_context != "Healthcare/Clinical App":
            return blueprint

        # Resolve primary relational anchor mapping targets
        linked_identity_tables = set()
        for table in blueprint.tables:
            t_name = table.table_name.lower()
            if any(anchor in t_name for anchor in self.matrix["identity_anchors"]):
                linked_identity_tables.add(table.table_name)

        # Execute relational context proximity checks
        for table in blueprint.tables:
            is_anchored = table.table_name in linked_identity_tables
            
            for col in table.columns:
                c_name = col.column_name.lower()
                
                # Baseline high risk structural rules
                if any(match in c_name for match in ["ssn", "mrn", "patient_id", "medicaid"]):
                    col.sensitivity_tier = "Highly Sensitive"
                    col.hipaa_rule_hit = "HIPAA Safe Harbor Identifier"
                    continue
                    
                # Skip known operational non-PHI tracking metrics
                if any(safe in c_name for safe in self.matrix["safe_generic_fields"]):
                    col.sensitivity_tier = "Low/Standard PII"
                    continue
                
                # Relational elevation logic
                if is_anchored or any(pat in c_name for pat in self.matrix["sensitive_context_patterns"]):
                    col.sensitivity_tier = "Moderately Sensitive"
                    col.hipaa_rule_hit = "PHI Context Linkage Rule"
                    col.reasoning += " [Escalated via Relational Proximity Layer]"

        return blueprint