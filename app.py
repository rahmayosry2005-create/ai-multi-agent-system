import streamlit as st
from main import app, validate_input, validate_output

# Page Configuration
st.set_page_config(
    page_title="Multi-Agent Coding System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Dark Theme CSS with High Contrast Text
st.markdown("""
    <style>
    /* Global App Background */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* Headers & Subheaders */
    .main-header {
        font-size: 2.25rem;
        color: #38bdf8;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    
    /* Sidebar Fixes for High Visibility */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #f3f4f6 !important;
    }
    
    /* Input Fields & Selectboxes Styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #1f2937 !important;
        color: #f3f4f6 !important;
        border-color: #374151 !important;
    }
    
    /* Labels visibility */
    label {
        color: #e5e7eb !important;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    
    /* Cards for Results */
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #111827;
        border: 1px solid #1f2937;
        margin-bottom: 1rem;
        color: #f3f4f6;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=70)
    st.markdown("### ⚙️ Pipeline Config")
    max_iters = st.slider("Max Iterations (Retry Cap)", min_value=1, max_value=5, value=3)
    
    st.markdown("---")
    st.markdown("### 👥 Team Architecture")
    st.markdown("- **PM Agent**: Specs & Criteria")
    st.markdown("- **Coder Agent**: LlamaIndex & Code Execution")
    st.markdown("- **Reviewer Agent**: Validation & Feedback")
    
    st.markdown("---")
    st.markdown("### 🛡️ Guardrails")
    st.markdown("- Input Guard (Prompt Injection)")
    st.markdown("- Output Guard (AST Syntax Check)")

# Main Content Area
st.markdown('<p class="main-header">🤖 Multi-Agent Software Development Team</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transforming single-line prompts into production-grade Python code through collaborative AI agents.</p>', unsafe_allow_html=True)

# Preset task examples for quick demo
preset_tasks = [
    "Write a Python function to check if a word is a palindrome.",
    "Write a Python function to calculate the Fibonacci sequence up to n terms.",
    "Write a Python class for a basic bank account with deposit and withdraw methods."
]

selected_preset = st.selectbox("💡 Choose a quick demo task:", ["-- Custom Task --"] + preset_tasks)

if selected_preset != "-- Custom Task --":
    default_task = selected_preset
else:
    default_task = "Write a Python function to check if a word is a palindrome."

user_task = st.text_area("Enter your coding task:", value=default_task, height=90)

col1, col2 = st.columns([1, 4])
with col1:
    run_button = st.button("🚀 Run Pipeline")

if run_button:
    if not user_task.strip():
        st.warning("Please enter a valid task.")
    else:
        # 1. Input Guardrail
        with st.status("🔍 Executing Security & Guardrail Checks...", expanded=True) as status:
            st.write("Running Input Guardrail (Checking for prompt injection / unsafe requests)...")
            is_safe, input_msg = validate_input(user_task)
            
            if not is_safe:
                status.update(label="Input Guardrail Blocked!", state="error", expanded=True)
                st.error(f"❌ [Blocked]: {input_msg}")
                st.stop()
            else:
                st.write("✅ Input Guardrail Passed: Request is safe.")
                
                # 2. Workflow Execution
                st.write("🤖 Agents collaborating: PM Agent ➔ Coder Agent ➔ Reviewer Agent...")
                initial_state = {
                    "task": user_task,
                    "code": "",
                    "review_feedback": "",
                    "current_iteration": 0,
                    "max_iterations": max_iters,
                    "messages": []
                }
                final_state = app.invoke(initial_state)
                status.update(label="Workflow Executed Successfully!", state="complete", expanded=False)
        
        final_code = final_state.get("code", "")
        final_feedback = final_state.get("review_feedback", "")
        
        # Clean up list/dict if returned
        if isinstance(final_code, list) and len(final_code) > 0:
            if isinstance(final_code[0], dict) and "text" in final_code[0]:
                final_code = final_code[0]["text"]
        elif not isinstance(final_code, str):
            final_code = str(final_code)

        # 3. Output Guardrail
        is_valid_out, output_msg = validate_output(final_code)
        if not is_valid_out:
            st.warning(f"⚠️ [Output Guardrail Warning]: {output_msg}")
        
        # Results Section
        st.markdown("### 📊 Execution Results")
        
        tab1, tab2 = st.tabs(["💻 Final Generated Code", "📋 Reviewer Feedback & Iterations"])
        
        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.code(final_code, language="python")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(final_feedback)
            st.markdown('</div>', unsafe_allow_html=True)