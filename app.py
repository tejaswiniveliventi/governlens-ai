import streamlit as st
import yaml
import os
from core.database import get_supabase_client
from pipelines.git_adapter import GitRepositoryScanner
from pipelines.doc_adapter import DocumentUrlIngestor
from pipelines.extractor import TextExtractor
from pipelines.evaluator import HipaasessmentEngine
from pipelines.reporter import ReportStorageEngine

# ----------------------------------------------------------------------
# 1. INITIALIZATION & LAYOUT DECLARATIVE LOADERS
# ----------------------------------------------------------------------
def load_presentation_markup():
    markup_path = os.path.join("config", "presentation_markup.yaml")
    with open(markup_path, "r") as f:
        return yaml.safe_load(f)

ui_config = load_presentation_markup()

st.set_page_config(
    page_title=ui_config["ui"]["page_title"], 
    layout=ui_config["ui"]["layout"]
)

# Apply global CSS stylesheet tokens and enlarged tab header parameters
st.markdown(ui_config["ui"]["styling"]["css_theme"], unsafe_allow_html=True)
st.markdown(ui_config["ui"]["styling"]["font_sizes"]["tab_header_css"], unsafe_allow_html=True)

# Instantiate Cloud SDK Operations
supabase = get_supabase_client()
extractor = TextExtractor()
evaluator = HipaasessmentEngine()
storage = ReportStorageEngine()

st.title(ui_config["ui"]["labels"]["section_title"])
st.caption(ui_config["ui"]["labels"]["section_subtitle"])
st.markdown("---")

# Dynamically name tab categories from decoupled presentation configuration
tab_intake, tab_ledger = st.tabs([
    ui_config["ui"]["tabs"]["input_header"],
    ui_config["ui"]["tabs"]["report_header"]
])

# ======================================================================
# TAB 1: DATA INGESTION ASSURANCE (CONDITIONAL LOGIC CONTROLLER)
# ======================================================================
with tab_intake:
    st.markdown(f"### {ui_config['ui']['labels']['input_header_sub']}")
    
    col_input, col_info = st.columns([3, 2])
    
    with col_input:
        env_context = st.selectbox(
            ui_config["ui"]["labels"].get("dropdown_context_label", "Deployment Environment Context:"),
            ui_config["ui"]["dropdowns"]["environments"]
        )
        
        # Reactive UI fields mapping parameters continuously to runtime states
        git_url = st.text_input(
            ui_config["ui"]["labels"]["repo_input"],
            placeholder=ui_config["ui"]["placeholders"]["repo_ph"],
            key="governlens_git_url_field"
        ).strip()
        
        doc_url = st.text_input(
            ui_config["ui"]["labels"]["doc_input"],
            placeholder=ui_config["ui"]["placeholders"]["doc_ph"],
            key="governlens_doc_url_field"
        ).strip()
        
        # Operational Logic Gate Matrix
        has_git = bool(git_url)
        has_doc = bool(doc_url)
        inputs_valid = has_git or has_doc
        
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        trigger_analysis = st.button(
            ui_config["ui"]["labels"]["action_button"],
            disabled=not inputs_valid,
            use_container_width=True
        )
        
        if not inputs_valid:
            st.warning(ui_config["ui"]["labels"]["empty_inputs_warning"])
            
    with col_info:
        st.markdown(f"#### {ui_config['ui']['labels'].get('strategy_header', '⚙️ In-Memory Token Routing')}")
        if not inputs_valid:
            st.info(ui_config["ui"]["strategy_alerts"]["idle"])
        else:
            if has_git and has_doc:
                st.info(ui_config["ui"]["strategy_alerts"]["intersection"])
            elif has_git:
                st.info(ui_config["ui"]["strategy_alerts"]["git_only"])
            elif has_doc:
                st.info(ui_config["ui"]["strategy_alerts"]["doc_only"])

    # Processing Loop Strategy execution track
    if trigger_analysis and inputs_valid:
        with st.spinner(ui_config["ui"]["labels"].get("spinner_text", "Processing compliance layers...")):
            try:
                payload_text = ""
                source_label = ""
                
                # Clone-free token-filtered intersection mapping routing
                if has_git and has_doc:
                    scanner = GitRepositoryScanner()
                    ingestor = DocumentUrlIngestor()
                    
                    git_schemas = scanner.extract_schema_files(git_url)
                    doc_text = ingestor.scrape_url_text(doc_url)
                    
                    payload_text = f"CONTEXT DOCUMENTATION:\n{doc_text}\n\nTARGET BLUEPRINT TO EVALUATE:\n{git_schemas}"
                    source_label = f"Intersection Scan: {git_url} + {doc_url}"
                    
                elif has_git:
                    scanner = GitRepositoryScanner()
                    payload_text = scanner.extract_schema_files(git_url)
                    source_label = f"In-Memory Git API Scan: {git_url}"
                    
                elif has_doc:
                    ingestor = DocumentUrlIngestor()
                    payload_text = ingestor.scrape_url_text(doc_url)
                    source_label = f"Isolated Spec URL Scan: {doc_url}"
                
                # Execute Modular Pipeline Layers
                raw_blueprint = extractor.parse_text(payload_text)
                evaluated_blueprint = evaluator.analyze_risk(raw_blueprint, env_context)
                plan_id = storage.save_to_warehouse(evaluated_blueprint, env_context, source_label)
                
                st.success(f"{ui_config['ui']['labels'].get('success_msg', 'Scan verified and committed under Reference ID')} #{plan_id}.")
                st.balloons()
                
            except Exception as e:
                st.error(f"Ingestion Aborted: Execution pipeline fault occurred: {e}")

# ======================================================================
# TAB 2: GOVERNANCE AUDIT REPORT LEDGER (THE TELEMETRY CARD PANEL)
# ======================================================================
with tab_ledger:
    st.markdown(f"### {ui_config['ui']['labels'].get('ledger_title', '📋 System Evaluation Reports')}")
    st.caption(ui_config["ui"]["labels"].get("ledger_subtitle", "Audit structural assets and verify evidence metrics."))
    
    try:
        plans_response = supabase.table("design_plans").select("*").order("id", desc=True).execute()
        plans = plans_response.data
    except Exception as e:
        st.error(f"Database Connection Interrupted: {e}")
        plans = []
        
    if plans:
        plan_options = [f"#{p['id']} - {p['project_name']} [{p['env_context']}]" for p in plans]
        selected_plan = st.selectbox(ui_config["ui"]["labels"].get("selector_label", "Select Architecture Audit Run:"), plan_options)
        target_plan_id = int(selected_plan.split(" ")[0].replace("#", ""))
        
        tables_response = supabase.table("mock_tables").select("*").eq("plan_id", target_plan_id).execute()
        
        for table in tables_response.data:
            st.markdown("---")
            st.markdown(f"### 🗂️ {ui_config['ui']['labels'].get('entity_label', 'Logical Database Entity:')} `{table['table_name']}`")
            
            columns_response = supabase.table("mock_columns").select("*").eq("table_id", table['id']).execute()
            
            for col in columns_response.data:
                tier = col['sensitivity_tier']
                
                # Extract visual high-contrast layouts from styling parameters configurations
                if "Highly" in tier:
                    tier_html = ui_config["ui"]["styling"]["badges"]["high"]
                elif "Moderately" in tier:
                    tier_html = ui_config["ui"]["styling"]["badges"]["medium"]
                else:
                    tier_html = ui_config["ui"]["styling"]["badges"]["low"]
                
                with st.container():
                    col_meta, col_justification = st.columns([2, 3])
                    
                    with col_meta:
                        st.markdown(f"**Field Name:** `{col['column_name']}`")
                        st.markdown(f"**Implied Type:** `{col['implied_type']}`")
                        st.markdown(f"**Status Profile:** {tier_html}", unsafe_allow_html=True)
                        
                    with col_justification:
                        st.markdown(f"**Regulatory Trigger:** {col['hipaa_rule_hit'] if col['hipaa_rule_hit'] else 'N/A'}")
                        st.markdown(f"**Document Text Evidence Snippet:**")
                        st.caption(f"\"{col['quote_from_source'] if col['quote_from_source'] else 'No direct risk text isolated'}\"")
                    
                    col_action1, col_action2, _ = st.columns([2, 2, 3])
                    with col_action1:
                        st.button(
                            f"🤝 Confirm Assessment [{col['column_name']}]",
                            key=f"approve_{col['id']}",
                            use_container_width=True
                        )
                    with col_action2:
                        st.button(
                            f"⚡ Escalate to Legal",
                            key=f"escalate_{col['id']}",
                            use_container_width=True
                        )
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    else:
        st.info(ui_config["ui"]["labels"].get("empty_ledger_msg", "No active scans logged in your cloud warehouse database tables yet."))