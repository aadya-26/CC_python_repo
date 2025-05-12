import streamlit as st
import time
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import plotly.express as px
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide"
)

# Custom CSS for a minimalist look
st.markdown("""
<style>
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .summary-container {
        border-radius: 5px;
        padding: 20px;
        background-color: #f8f9fa;
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #2E4053;
    }
    .stProgress .st-eb {
        background-color: #4CAF50;
    }
    .stat-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.title("AI Text Summarizer")
st.markdown("Generate summaries using state-of-the-art AI models")

# Initialize session state variables
if 'model_cache' not in st.session_state:
    st.session_state.model_cache = {}
if 'results' not in st.session_state:
    st.session_state.results = None
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# Define the models - simplified to just 2
MODELS = {
    "facebook/bart-base": {
        "name": "BART",
        "description": "A classic summarization baseline from Facebook AI",
        "max_length": 1024,
        "color": "#1877F2"  # Facebook blue
    },
    "google/pegasus-xsum": {
        "name": "Pegasus",
        "description": "A strong abstractive summarizer fine-tuned on XSum dataset",
        "max_length": 512,
        "color": "#4285F4"  # Google blue
    }
}

# Main layout with sidebar
col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("⚙️ Model Settings")
    
    # Model selection - simplified options
    selected_model = st.radio(
        "Choose a model:",
        options=list(MODELS.keys()),
        format_func=lambda x: MODELS[x]["name"],
        horizontal=True
    )
    
    # Simple parameters
    max_new_tokens = st.slider("Summary Length", 50, 300, 150)
    num_beams = st.slider("Quality (Beam Size)", 1, 8, 4)
    
    # Model info
    st.markdown("---")
    st.markdown(f"**{MODELS[selected_model]['name']}**")
    st.markdown(f"_{MODELS[selected_model]['description']}_")

with col1:
    input_text = st.text_area(
        "Enter text to summarize:",
        height=200,
        placeholder="Paste your article, report, or essay here... (minimum 100 characters)"
    )

    # Generate button
    generate_button = st.button(
        "Generate Summary", 
        disabled=not (input_text and len(input_text) > 100)
    )

    # Display a minimum text length message
    if input_text and len(input_text) <= 100:
        st.info("Please enter at least 100 characters for better results.")

# Function to load models (with caching)
@st.cache_resource
def load_model(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    return model, tokenizer

# Function to generate summary
def generate_summary(model_id, text):
    # Get model and tokenizer
    start_time = time.time()
    
    if model_id not in st.session_state.model_cache:
        with st.spinner(f"Loading {MODELS[model_id]['name']} model..."):
            model, tokenizer = load_model(model_id)
            st.session_state.model_cache[model_id] = (model, tokenizer)
    else:
        model, tokenizer = st.session_state.model_cache[model_id]
    
    loading_time = time.time() - start_time
    
    # Generate summary
    inference_start = time.time()
    
    # Truncate input if needed
    max_length = MODELS[model_id]["max_length"]
    inputs = tokenizer(text, max_length=max_length, truncation=True, return_tensors="pt")
    
    # Generate with parameters
    with torch.no_grad():
        output = model.generate(
            inputs.input_ids,
            max_new_tokens=max_new_tokens,
            num_beams=num_beams,
            early_stopping=True
        )
    
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    inference_time = time.time() - inference_start
    
    # Calculate compression ratio
    input_tokens = len(tokenizer.encode(text))
    output_tokens = len(tokenizer.encode(summary))
    compression_ratio = (input_tokens - output_tokens) / input_tokens * 100
    
    return {
        "summary": summary,
        "loading_time": loading_time,
        "inference_time": inference_time,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "compression_ratio": compression_ratio
    }

# Process when button is clicked
if generate_button:
    if len(input_text) <= 100:
        st.error("Text is too short. Please enter at least 100 characters for meaningful summarization.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Processing status
        progress_bar.progress(0.2)
        status_text.text(f"Processing with {MODELS[selected_model]['name']}...")
        
        try:
            result = generate_summary(selected_model, input_text)
            st.session_state.results = {selected_model: result}
            st.session_state.show_results = True
            st.session_state.input_text = input_text
        except Exception as e:
            st.error(f"Error processing: {str(e)}")
        
        # Complete the progress
        progress_bar.progress(1.0)
        status_text.text("Summary generated successfully!")
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()

# Display results
if st.session_state.show_results and st.session_state.results:
    st.markdown("---")
    st.subheader("📊 Summary Results")
    
    model_id = list(st.session_state.results.keys())[0]
    result = st.session_state.results[model_id]
    
    # Display summary
    st.markdown("<div class='summary-container'>", unsafe_allow_html=True)
    st.markdown("### Summary")
    st.markdown(result["summary"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display metrics in a nice layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.metric("Processing Time", f"{result['inference_time']:.2f}s")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.metric("Compression", f"{result['compression_ratio']:.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.metric("Output Length", f"{result['output_tokens']} tokens")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Add visualization
    st.markdown("### Text Comparison")
    
    # Create bar chart for token comparison
    comparison_data = pd.DataFrame({
        "Type": ["Original Text", "Summary"],
        "Tokens": [result["input_tokens"], result["output_tokens"]]
    })
    
    fig = px.bar(
        comparison_data,
        x="Type",
        y="Tokens",
        title="Original vs Summary Length",
        color="Type",
        color_discrete_sequence=[MODELS[model_id]["color"], "#45a049"]
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and Hugging Face Transformers")