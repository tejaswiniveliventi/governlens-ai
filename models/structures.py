from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict
import yaml

with open("config/governance_rules.yaml", "r") as f:
    rules_cfg = yaml.safe_load(f)
ALLOWED_TYPES = rules_cfg["extraction_rules"]["allowed_types"]

class ExtractedColumn(BaseModel):
    column_name: str = Field(description="The exact variable or property field string.")
    implied_type: str = Field(description="The matching technical data type context.")
    quote_from_source: str = Field(description="Verbatim text excerpt confirming this field's presence.")
    reasoning: str = Field(description="Deduction footprint tracking the extraction source location.")
    sensitivity_tier: str = Field(default="Low/Standard PII")
    hipaa_rule_hit: Optional[str] = Field(default=None)

    @field_validator('implied_type')
    @classmethod
    def enforce_type_bounds(cls, value: str) -> str:
        upper_val = value.upper()
        if upper_val not in ALLOWED_TYPES:
            return "UNSPECIFIED"
        return upper_val

class ExtractedTable(BaseModel):
    table_name: str = Field(description="Name of the logical database entity entity.")
    columns: List[ExtractedColumn] = Field(description="Array of associated attributes parsed.")

class ExtractionConfidenceMetrics(BaseModel):
    overall_confidence: float = Field(ge=0.0, le=1.0)
    schema_completeness: float = Field(ge=0.0, le=1.0)
    field_accuracy: float = Field(ge=0.0, le=1.0)
    compliance_basis: str

class ImplicitSchemaBlueprint(BaseModel):
    tables: List[ExtractedTable]
    metrics: ExtractionConfidenceMetrics