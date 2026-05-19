import streamlit as st
import yaml
from core.database import get_supabase_client
from pipelines.git_adapter import GitRepositoryScanner
from pipelines.doc_adapter import DocumentUrlIngestor
from pipelines.extractor import TextExtractor
from pipelines.evaluator import HipaasessmentEngine
from pipelines.reporter import ReportStorageEngine

# Load styling and content from decoupled presentation configuration setup
with open("config/presentation_markup.yaml", "r") as f:
    markup = yaml.safe_load(f)

st.set_page_config(page_title="GovernLens | Control Center", layout="wide")

# Injection of custom theme CSS to override default styling mechanics gracefully
st.markdown(f'<style>{markup["ui_styles"]["custom_css"]}</style>', unsafe_allow_html=True)
st.title(markup["ui_branding"]["title"])
st.caption(markup["ui_branding"]["caption"])
st.markdown("---")

supabase = get_supabase_client()

# Establish the minimalist two-tab operational division with custom typography sizing
tab_intake, tab_ledger = st.tabs([
    "📥 Schema & Documentation Intake", 
    "📊 Governance Compliance Ledger"
])

# ==============================================================================
# TAB 1: INTEGRATED DATA INGESTION ENGINE
# ==============================================================================
with tab_intake:
    st.markdown("### 🔌 Automated Architecture Ingestion")
    st.caption("Feed active development channels into the compliance validation engine.")
    
    col_input, col_info = st.columns([3, 2])
    
    with col_input:
        env_context = st.selectbox(
            "Target Deployment Domain Environment Context:",
            ["Healthcare/Clinical App", "Internal HR/Operations", "General Marketing/B2C"]
        )
        
        st.markdown("#### Route A: Audit Codebase Infrastructure Repository")
        git_url = st.text_input(
            "Public Git Repository Endpoint URL (.sql or ORM definitions):",
            placeholder="https://github.com/organization/target-repository"
        )
        
        st.markdown("#### Route B: Audit Functional Requirements Documentation")
        doc_url = st.text_input(
            "Public Product Specification URI Link (Confluence / Wiki Portal):",
            placeholder="https://example.com/specifications/intake-feature"
        )
        
        # Reactive state evaluation: break form deadlocks by checking strings natively
        has_git = bool(git_url.strip())
        has_doc = bool(doc_url.strip())
        
        # The button remains locked if both fields are empty to prevent blank executions
        trigger_analysis = st.button(
            "🚀 Execute Comprehensive Analysis Pipeline", 
            use_container_width=True,
            disabled=not (has_git or has_doc)
        )

    with col_info:
        st.markdown(markup["panels"].get("intake_info_header", "#### ⚙️ Ingestion Capabilities"))
        st.info(
            "GovernLens dynamically routes inputs based on the properties configured:\n\n"
            "- Populating the Git Pipeline pulls remote schema DDL blueprints down into volatile memory caches for structural checks.\n"
            "- Populating the Documentation Pipeline scrapes remote web trees, routing unstructured functional plans directly into semantic parsing layers.\n\n"
            "Select your target parameter context vectors, supply an execution pathway, and boot the analyzer."
        )

    # Integrated processing and multi-source context routing loop
    if trigger_analysis:
        with st.spinner("Processing ingestion feeds and calculating risk vectors..."):
            try:
                extractor = TextExtractor()
                evaluator = HipaasessmentEngine()
                storage = ReportStorageEngine()
                
                payload_text = ""
                source_label = "Manual Target Trigger"
                
                # Permutation 1: Isolated Code Scan (Overriding constraints via explicit tag)
                if has_git and not has_doc:
                    scanner = GitRepositoryScanner()
                    payload_text = f"ANALYSIS MODE: Isolated Code Schema Extraction\n"
                    payload_text += scanner.extract_schema_files(git_url)
                    source_label = f"Isolated Git Run: {git_url}"
                
                # Permutation 2: Isolated Requirements Document Scan
                elif has_doc and not has_git:
                    ingestor = DocumentUrlIngestor()
                    payload_text = f"ANALYSIS MODE: Isolated Requirement Specification Scan\n"
                    payload_text += ingestor.scrape_url_text(doc_url)
                    source_label = f"Isolated Doc Run: {doc_url}"
                
                # Permutation 3: Combined Contextual Intersection Scan
                elif has_git and has_doc:
                    scanner = GitRepositoryScanner()
                    ingestor = DocumentUrlIngestor()
                    payload_text = f"ANALYSIS MODE: Blended Cross-Reference Intersection Scan\n"
                    payload_text += f"COMPLIANCE BOUNDARIES:\n{ingestor.scrape_url_text(doc_url)}\n\n"
                    payload_text += f"TARGET ARCHITECTURE BLUEPRINT:\n{scanner.extract_schema_files(git_url)}"
                    source_label = f"Intersection Audit: {git_url} + {doc_url}"
                
                # Run the backend execution steps sequentially 
                raw_blueprint = extractor.parse_text(payload_text)
                evaluated_blueprint = evaluator.analyze_risk(raw_blueprint, env_context)
                plan_id = storage.save_to_warehouse(evaluated_blueprint, env_context, source_label)
                
                st.success(
                    f"Audit mapping successful! Plan records securely written to database warehouse under Reference ID #{plan_id}. "
                    f"Navigate to the 'Governance Compliance Ledger' tab to review the generated sheets."
                )
                
            except Exception as e:
                st.error(f"Ingestion Aborted: Execution pipeline fault occurred: {e}")

# ==============================================================================
# TAB 2: GOVERNANCE AUDIT LEDGER (The Report Sheet View)
# ==============================================================================
with tab_ledger:
    st.markdown("### 📋 System Evaluation Reports")
    st.caption(markup["panels"].get("ledger_header", "Audit structural assets, verify textual context evidence, and sign off on data classifications."))
    
    try:
        plans = supabase.table("design_plans").select("*").order("id", desc=True).execute().data
    except Exception as e:
        st.error(f"Database Connection Interrupted: {e}")
        plans = []
        
    if plans:
        # Map ledger configuration options cleanly into a historical drop list
        plan_options = [f"#{p['id']} - {p['project_name']} [{p['env_context']}]" for p in plans]
        selected_plan = st.selectbox("Choose Selected Schema Audit Trace to Display:", plan_options)
        target_plan_id = int(selected_plan.split(" ")[0].replace("#", ""))
        
        # Pull child entities associated with the selected audit block
        tables_response = supabase.table("mock_tables").select("*").eq("plan_id", target_plan_id).execute()
        
        for table in tables_response.data:
            st.markdown("---")
            st.markdown(f"### 🗂️ Logical Database Entity: `{table['table_name']}`")
            st.markdown(f"**Deduced Structural Objective Context:** {table.get('deduced_context', 'No table context summary mapped.')}")
            
            columns_response = supabase.table("mock_columns").select("*").eq("table_id", table['id']).execute()
            
            # Draw individual visual column asset fields inside dedicated layout boxes
            for col in columns_response.data:
                tier = col['sensitivity_tier']
                
                if "Highly" in tier or "High" in tier:
                    tier_html = f'<span class="badge-red">🔴 HIGH COMPLIANCE RISK</span>'
                elif "Moderately" in tier or "Moderate" in tier:
                    tier_html = f'<span class="badge-orange">🟡 MODERATE CONTEXTUAL RISK</span>'
                else:
                    tier_html = f'<span class="badge-green">🟢 LOW / OPERATIONALLY SAFE</span>'
                
                with st.container():
                    col_meta, col_justification = st.columns([2, 3])
                    
                    with col_meta:
                        st.markdown(f"**Field Name:** `{col['column_name']}`")
                        st.markdown(f"**Implied Type:** `{col['implied_type']}`")
                        st.markdown(f"**Status Profile:** {tier_html}", unsafe_allow_html=True)
                    
                    with col_justification:
                        st.markdown(f"**Regulatory Trigger:** *{col['hipaa_rule_hit'] if col['hipaa_rule_hit'] else 'N/A'}*")
                        st.markdown("**Document Text Evidence Snippet:**")
                        evidence_quote = col['quote_from_source'] if col['quote_from_source'] else 'No direct risk text isolated'
                        st.caption(f'"{evidence_quote}"')
                
                # Human-In-The-Loop management triggers
                col_action1, col_action2, _ = st.columns([2, 2, 3])
                with col_action1:
                    st.button(
                        f"🤝 Confirm & Approve {col['column_name']}",
                        key=f"approve_{col['id']}",
                        use_container_width=True
                    )
                with col_action2:
                    st.button(
                        f"⚡ Escalate to Legal",
                        key=f"escalate_{col['id']}",
                        use_container_width=True
                    )
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("No active architecture scans logged in your remote cloud tables yet.")