import unittest
from core.database import get_supabase_client
from core.config import settings

class TestGovernLensDatabaseSchema(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Initialize connection parameters using the verified SDK framework client."""
        cls.supabase = get_supabase_client()

    def test_verify_cloud_connection(self):
        """Verify that a secure cloud session can be established."""
        try:
            # Query a limit-bounded sample to verify authentication lane status
            response = self.supabase.table("design_plans").select("id").limit(1).execute()
            self.assertIsNotNone(response.data, "Database connection failed to return a valid array track.")
        except Exception as e:
            self.fail(f"Database Access Rejected: Check RLS policies or .env keys. Error: {e}")

    def test_validate_design_plans_table(self):
        """Validate the structural column assets of the 'design_plans' table."""
        try:
            response = self.supabase.table("design_plans").select("*").limit(1).execute()
            if response.data:
                record = response.data[0]
                # Reconciled validation mapping past database tracking faults
                self.assertIn("env_context", record, "Missing critical column asset: 'env_context'")
                self.assertIn("source_text", record, "Missing critical column asset: 'source_text'")
                self.assertIn("raw_text_chunk", record, "Missing critical column asset: 'raw_text_chunk'")
        except Exception as e:
            self.fail(f"Failed to query design_plans structural parameters: {e}")

    def test_validate_mock_columns_table(self):
        """Validate that the 'mock_columns' attributes match Pydantic properties."""
        try:
            response = self.supabase.table("mock_columns").select("*").limit(1).execute()
            if response.data:
                record = response.data[0]
                expected_fields = [
                    "table_id", 
                    "column_name", 
                    "implied_type", 
                    "sensitivity_tier", 
                    "hipaa_rule_hit", 
                    "reasoning", 
                    "quote_from_source"
                ]
                for field in expected_fields:
                    self.assertIn(field, record, f"Schema Contract Violation: Column '{field}' missing from DB.")
        except Exception as e:
            self.fail(f"Failed to query mock_columns structural parameters: {e}")

    def test_verify_table_relationships(self):
        """Ensure relational dependency tracking tables are active in the public catalog."""
        try:
            response = self.supabase.table("mock_tables").select("*").limit(1).execute()
            self.assertIsNotNone(response.data, "Table 'mock_tables' failed validation request.")
        except Exception as e:
            self.fail(f"Relational Verification Failed: {e}")

if __name__ == "__main__":
    unittest.main()