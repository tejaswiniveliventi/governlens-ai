from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedColumn(BaseModel):
    # Enforcing explicit naming conventions matching database properties
    column_name: str = Field(description="The exact alphanumeric name of the structural database column or attribute attribute field.")
    implied_type: str = Field(description="The determined technical data type context e.g., VARCHAR, INT, TIMESTAMP, TEXT.")
    sensitivity_tier: str = Field(description="Must default strictly to one choice: 'Highly Sensitive', 'Moderately Sensitive', or 'Low/Standard PII'.")
    hipaa_rule_hit: Optional[str] = Field(None, description="The explicit HIPAA Safe Harbor or Privacy Rule mapping violation context triggered.")
    reasoning: str = Field(description="Detailed compliance justification explaining how the field exposure or relational status was computed.")
    quote_from_source: Optional[str] = Field(None, description="Literal snippet quote isolated from the ingestion document text payload justifying the tier.")

class ExtractedTable(BaseModel):
    table_name: str = Field(description="The verified alphanumeric name of the logical database table asset.")
    columns: List[ExtractedColumn] = Field(description="The array grouping of all structural child attributes identified inside the entity schema.")

class ImplicitSchemaBlueprint(BaseModel):
    tables: List[ExtractedTable] = Field(description="The parent collection array hosting all structural metadata tables resolved by the pipeline.")