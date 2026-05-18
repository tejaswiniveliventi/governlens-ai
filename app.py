# app.py
import streamlit as st
import yaml
from core.database import get_supabase_client
from pipelines.git_adapter import GitRepositoryScanner
from pipelines.doc_adapter import DocumentUrlIngestor
from pipelines.extractor import TextExtractor
from pipelines.evaluator import HipaasessmentEngine
from pipelines.reporter import ReportStorageEngine


# Parse the externalized asset file
with open("config/presentation_markup.yaml", "r") as f:
    markup = yaml.safe_load(f)

st.set_page_config(page_title="GovernLens | Control Center", layout="wide")

# Inject the preserved multi-line CSS block straight into the view container
st.markdown(f'<style>{markup["ui_styles"]["custom_css"]}</style>', unsafe_allow_html=True)

st.title(markup["ui_branding"]["title"])
st.caption(markup["ui_branding"]["caption"])
st.markdown("---")

supabase = get_supabase_client()
tab_intake, tab_ledger = st.tabs(["📥 Ingestion Control Room", "📊 Compliance Evaluation Reports"])

# ==============================================================================
# TAB 1: DATA INGESTION ENGINE
# ==============================================================================
with tab_intake:
    st.markdown(markup["panels"]["intake_header"])
    if "intake_subheader" in markup["panels"]:
        st.caption(markup["panels"]["intake_subheader"])
        
    col_input, col_info = st.columns([3, 2])
    
    with col_input:
        env_context = st.selectbox(
            "Target Deployment Domain Environment Context:",
            ["Healthcare/Clinical App", "Internal HR/Operations", "General Marketing/B2C"]
        )
        
        # Dynamically pulls updated text variables from your decoupled presentation file
        st.markdown(markup["panels"].get("option_a_header", "#### Option A: Audit Codebase Infrastructure Repository"))
        git_url = st.text_input("Public Git Repository Endpoint URL (.sql or ORM definitions):", key="git_url_input")
        
        st.markdown(markup["panels"].get("option_b_header", "#### Option B: Audit Functional Requirements Documentation"))
        doc_url = st.text_input("Public Product Specification URI Link (Confluence / Wiki Portal):", key="doc_url_input")
        
        # Enforce reactive button locks directly via layout evaluations to prevent blank execution threads
        has_git = bool(git_url.strip())
        has_doc = bool(doc_url.strip())
        button_locked = not (has_git or has_doc)
        
        trigger_analysis = st.button(
            "🚀 Execute Comprehensive Analysis Pipeline", 
            disabled=button_locked, 
            use_container_width=True
        )

    with col_info:
        st.info(
            "👉 **Operational Router Parameters:**\n\n"
            "- **Git Only:** Executes an isolated codebase catalog structure parse.\n"
            "- **Doc Only:** Executes an isolated documentation text safety evaluation.\n"
            "- **Both Inputs:** Triggers a Contextual Intersection Scan. Pulls git layouts "
            "and evaluates changes strictly filtered against the functional spec parameters."
        )

    # Ingestion Processing Loop Execution
    if trigger_analysis:
        with st.spinner("Processing automated ingestion tracks and executing safety matrices..."):
            try:
                git_payload = ""
                doc_payload = ""
                
                if has_git:
                    git_payload = GitRepositoryScanner().extract_schema_files(git_url)
                if has_doc:
                    doc_payload = DocumentUrlIngestor().scrape_url_text(doc_url)
                
                # Assemble context string based on active logical track rules
                if has_git and has_doc:
                    payload_text = (
                        f"ANALYSIS MODE: Cross-reference Schema with Compliance Documentation\n\n"
                        f"SECTION 1: COMPLIANCE REQUIREMENTS (from documentation)\n{doc_payload}\n\n"
                        f"SECTION 2: IMPLEMENTED SCHEMA (from code)\n{git_payload}"
                    )
                    source_label = f"Intersection Scan: {git_url} + {doc_url}"
                elif has_git:
                    # FIX: Inject clear instruction mode blocks to prompt code-only overrides for the TextExtractor
                    payload_text = (
                        f"ANALYSIS MODE: Isolated Code Schema Extraction\n\n"
                        f"SECTION 1: IMPLEMENTED SCHEMA (from code)\n{git_payload}\n\n"
                        f"CRITICAL INSTRUCTION: Build a comprehensive database schema matrix mapping out "
                        f"every physical table and column declaration found in the source code file above."
                    )
                    source_label = f"Isolated Git Run: {git_url}"
                else:
                    payload_text = (
                        f"ANALYSIS MODE: Isolated Unstructured Specification Scan\n\n"
                        f"SECTION 1: COMPLIANCE REQUIREMENTS (from documentation)\n{doc_payload}"
                    )
                    source_label = f"Isolated Doc Run: {doc_url}"
                
                # Run the modular evaluation pipeline endpoints
                blueprint = TextExtractor().parse_text(payload_text)
                evaluated_blueprint = HipaasessmentEngine().analyze_risk(blueprint, env_context)
                
                plan_id = ReportStorageEngine().save_to_warehouse(evaluated_blueprint, env_context, source_label)
                st.success(f"Audit tracking records written under Reference Trace ID #{plan_id}. Navigate to the Reports tab to review.")
                
                
            except Exception as e:
                st.error(f"Ingestion Aborted: Execution pipeline fault occurred: {e}")

# ==============================================================================
# TAB 2: GOVERNANCE AUDIT LEDGER (The Report Sheet)
# ==============================================================================
with tab_ledger:
    # FIX: Swapped out direct dictionary index lookup for a clean fallback .get() method
    st.markdown(markup["panels"].get("ledger_header", "### 📊 Governance Compliance Ledger"))
    
    try:
        plans = supabase.table("design_plans").select("*").order("id", desc=True).execute().data
    except Exception:
        plans = []


    if plans:
        plan_options = [f"#{p['id']} - {p['project_name']} [{p['env_context']}]" for p in plans]
        selected_plan = st.selectbox("Choose Selected Schema Audit Trace to Display:", plan_options)
        target_plan_id = int(selected_plan.split(" ")[0].replace("#", ""))
        
        tables = supabase.table("mock_tables").select("*").eq("plan_id", target_plan_id).execute().data
        
        for table in tables:
            st.markdown(f"### 🗂️ Logical Entity Table: `{table['table_name']}`")
            columns = supabase.table("mock_columns").select("*").eq("table_id", table["id"]).execute().data
            
            for col in columns:
                tier = col["sensitivity_tier"]
                
                # Assign high-contrast status badge labels via html tags
                if "Highly" in tier:
                    badge = f'<span class="badge-crimson">🔴 HIGH RISK PHI</span>'
                elif "Moderately" in tier:
                    badge = f'<span class="badge-rust">🟡 CONTEXTUAL PHI</span>'
                else:
                    badge = f'<span class="badge-emerald">🟢 STANDARD PII</span>'
                
                with st.container():
                    c1, c2 = st.columns([2, 3])
                    with c1:
                        st.markdown(f"**Field Variable:** `{col['column_name']}`")
                        st.markdown(f"**Type Context:** `{col['implied_type']}`")
                        st.markdown(f"**Status Profile:** {badge}", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"**Trigger Rule:** {col['hipaa_rule_hit'] or 'N/A'}")
                        st.caption(f"**Evidence Quote:** *\"{col['quote_from_source'] or 'No matching snippet.'}\"*")
                    
                    # Descriptive human-in-the-loop action controls
                    a1, a2, _ = st.columns([2, 2, 3])
                    a1.button("🤝 Confirm Classification", key=f"ok_{col['id']}", use_container_width=True)
                    a2.button("⚡ Escalate for Legal Review", key=f"esc_{col['id']}", use_container_width=True)
                    st.markdown("---")
    else:
        st.info(markup["panels"]["empty_ledger"])