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
st.markdown(markup["ui_styles"]["custom_css"], unsafe_allow_html=True)
st.title(markup["ui_branding"]["title"])
st.caption(markup["ui_branding"]["caption"])
st.markdown("---")

supabase = get_supabase_client()

# Establish the minimalist two-tab operational division
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
        
        # Reactive state evaluation: break form deadlocks by evaluating variables live
        has_git = bool(git_url.strip())
        has_doc = bool(doc_url.strip())
        
        # The primary analysis button unlocks dynamically when valid entry parameters exist
        trigger_analysis = st.button(
            "🚀 Execute Comprehensive Analysis Pipeline", 
            use_container_width=True,
            disabled=not (has_git or has_doc)
        )

    with col_info:
        st.markdown("#### ⚙️ Ingestion Capabilities")
        st.info(
            "GovernLens dynamically routes inputs based on the properties configured:\n\n"
            "- Populating the Git Pipeline pulls remote schema DDL blueprints down into volatile memory caches for structural checks.\n"
            "- Populating the Documentation Pipeline scrapes remote web trees, routing unstructured functional plans directly into semantic parsing layers.\n\n"
            "Select your target parameter context vectors, supply an execution pathway, and boot the analyzer."
        )

    # Ingestion Processing & Context Routing Loop
    if trigger_analysis:
        with st.spinner("Processing ingestion feeds and calculating risk vectors..."):
            try:
                extractor = TextExtractor()
                evaluator = HipaasessmentEngine()
                storage = ReportStorageEngine()
                
                payload_text = ""
                source_label = "Manual Target Trigger"
                
                # Permutation 1: Isolated Code Scan
                if has_git and not has_doc:
                    scanner = GitRepositoryScanner()
                    # Inject explicit execution tags to override strict cross-reference prompt constraints
                    payload_text = f"ANALYSIS MODE: Isolated Code Schema Extraction\n"
                    payload_text += scanner.extract_schema_files(git_url)
                    source_label = f"Isolated Git Run: {git_url}"
                
                # Permutation 2: Isolated Requirements Spec Scan
                elif has_doc and not has_git:
                    ingestor = DocumentUrlIngestor()
                    payload_text = f"ANALYSIS MODE: Isolated Requirement Specification Scan\n"
                    payload_text += ingestor.scrape_url_text(doc_url)
                    source_label = f"Isolated Doc Run: {doc_url}"
                
                # Permutation 3: Intersection Contextual Scan
                elif has_git and has_doc:
                    scanner = GitRepositoryScanner()
                    ingestor = DocumentUrlIngestor()
                    payload_text = f"ANALYSIS MODE: Blended Cross-Reference Intersection Scan\n"
                    payload_text += f"COMPLIANCE BOUNDARIES:\n{ingestor.scrape_url_text(doc_url)}\n\n"
                    payload_text += f"TARGET ARCHITECTURE BLUEPRINT:\n{scanner.extract_schema_files(git_url)}"
                    source_label = f"Intersection Audit: {git_url} + {doc_url}"
                
                # Execute pipeline validation sequence
                raw_blueprint = extractor.parse_text(payload_text)
                evaluated_blueprint = evaluator.analyze_risk(raw_blueprint, env_context)
                plan_id = storage.save_to_warehouse(evaluated_blueprint, env_context, source_label)