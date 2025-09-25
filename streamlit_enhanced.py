import requests
import json
import streamlit as st
from typing import Optional, List, Dict
import time
from datetime import datetime
import io
import docx
import PyPDF2


class OllamaClient:
    """Enhanced client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, model: str, prompt: str, stream: bool = False) -> Optional[str]:
        """Generate text using Ollama model with streaming support"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            if stream:
                return self._handle_stream_ui(response)
            else:
                result = response.json()
                return result.get("response", "")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to Ollama: {e}")
            return None
    
    def _handle_stream_ui(self, response):
        """Handle streamed response with UI updates"""
        full_response = ""
        response_placeholder = st.empty()
        
        for line in response.iter_lines():
            if line:
                try:
                    json_response = json.loads(line)
                    if "response" in json_response:
                        chunk = json_response["response"]
                        full_response += chunk
                        response_placeholder.markdown(f"**Generating:** {full_response}▊")
                except json.JSONDecodeError:
                    continue
        
        response_placeholder.empty()
        return full_response
    
    def list_models(self) -> List[str]:
        """Get available models from Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        except:
            return ["llama3.2:latest", "llama3.2:1b", "llama3.2:3b"]


def create_advanced_prompt(text: str, summary_type: str, custom_instructions: str = "") -> str:
    """Create advanced prompts with custom instructions"""
    
    base_prompts = {
        "general": f"""Provide a comprehensive yet concise summary of the following text. Focus on the main ideas, key arguments, and important details:

Text to summarize:
{text}

{custom_instructions}

Summary:""",
        
        "bullet_points": f"""Create a structured bullet-point summary of the following text. Organize information hierarchically with main points and sub-points:

Text to summarize:
{text}

{custom_instructions}

Key Points:
•""",
        
        "executive": f"""Create an executive summary suitable for business leaders. Focus on key insights, actionable information, and strategic implications:

Text to summarize:
{text}

{custom_instructions}

Executive Summary:""",
        
        "academic": f"""Create an academic-style summary that highlights the main thesis, methodology (if applicable), key findings, and conclusions:

Text to summarize:
{text}

{custom_instructions}

Academic Summary:""",
        
        "timeline": f"""Extract and organize the chronological events or processes mentioned in the text:

Text to summarize:
{text}

{custom_instructions}

Timeline Summary:""",
        
        "questions": f"""Generate a summary in the form of key questions and answers based on the content:

Text to summarize:
{text}

{custom_instructions}

Q&A Summary:"""
    }
    
    return base_prompts.get(summary_type, base_prompts["general"])


def extract_text_from_file(uploaded_file) -> str:
    """Extract text from various file formats"""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_extension == 'txt':
            return str(uploaded_file.read(), "utf-8")
        
        elif file_extension == 'pdf':
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        
        elif file_extension in ['docx', 'doc']:
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        else:
            return str(uploaded_file.read(), "utf-8")
    
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return ""


def save_summary_session(text: str, summary: str, model: str, summary_type: str) -> None:
    """Save summary session to browser session state"""
    if 'summary_history' not in st.session_state:
        st.session_state.summary_history = []
    
    session_data = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'original_text': text[:200] + "..." if len(text) > 200 else text,
        'summary': summary,
        'model': model,
        'type': summary_type,
        'original_length': len(text),
        'summary_length': len(summary)
    }
    
    st.session_state.summary_history.insert(0, session_data)
    # Keep only last 10 sessions
    st.session_state.summary_history = st.session_state.summary_history[:10]


def display_summary_history():
    """Display previous summaries"""
    if 'summary_history' in st.session_state and st.session_state.summary_history:
        st.subheader("📚 Recent Summaries")
        
        for i, session in enumerate(st.session_state.summary_history):
            with st.expander(f"Summary {i+1} - {session['timestamp']} ({session['type']})"):
                st.write(f"**Model:** {session['model']}")
                st.write(f"**Original:** {session['original_length']} chars | **Summary:** {session['summary_length']} chars")
                st.write("**Summary:**")
                st.write(session['summary'])


def main():
    st.set_page_config(
        page_title="Enhanced AI Text Summarizer",
        page_icon="🚀",
        layout="wide"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>🚀 Enhanced AI Text Summarizer</h1><p>Advanced text summarization with multiple models and formats</p></div>', unsafe_allow_html=True)
    
    # Initialize Ollama client
    ollama = OllamaClient()
    
    # Sidebar configuration
    st.sidebar.header("🔧 Configuration")
    
    # Model selection with dynamic loading
    available_models = ollama.list_models()
    model_name = st.sidebar.selectbox(
        "🤖 Select Model",
        available_models,
        index=0
    )
    
    # Enhanced summary types
    summary_type = st.sidebar.selectbox(
        "📋 Summary Style",
        ["general", "bullet_points", "executive", "academic", "timeline", "questions"],
        index=0
    )
    
    # Advanced options
    st.sidebar.subheader("🎛️ Advanced Options")
    
    enable_streaming = st.sidebar.checkbox("Enable Streaming", value=False)
    
    custom_instructions = st.sidebar.text_area(
        "Custom Instructions (Optional)",
        placeholder="e.g., Focus on technical aspects, Include statistics, Emphasize main arguments...",
        height=100
    )
    
    # Word limit slider
    word_limit = st.sidebar.slider(
        "Approximate Word Limit",
        min_value=50,
        max_value=500,
        value=150,
        step=25
    )
    
    if word_limit:
        custom_instructions += f"\n\nPlease keep the summary to approximately {word_limit} words."
    
    # Main interface with tabs
    tab1, tab2, tab3 = st.tabs(["📝 Summarizer", "📚 History", "ℹ️ About"])
    
    with tab1:
        # Main interface
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📄 Input")
            
            # Text input options
            input_method = st.radio(
                "Choose input method:",
                ["Type/Paste Text", "Upload File", "Sample Text"]
            )
            
            text_to_summarize = ""
            
            if input_method == "Type/Paste Text":
                text_to_summarize = st.text_area(
                    "Enter text to summarize:",
                    height=300,
                    placeholder="Paste your article, document, or any text here..."
                )
            
            elif input_method == "Upload File":
                uploaded_file = st.file_uploader(
                    "Upload a file",
                    type=['txt', 'md', 'pdf', 'docx'],
                    help="Supported formats: TXT, MD, PDF, DOCX"
                )
                
                if uploaded_file is not None:
                    with st.spinner("Extracting text from file..."):
                        text_to_summarize = extract_text_from_file(uploaded_file)
                    
                    if text_to_summarize:
                        st.success(f"✅ Extracted {len(text_to_summarize)} characters")
                        with st.expander("Preview extracted text"):
                            st.text_area("File content:", value=text_to_summarize[:1000] + "...", height=150)
            
            else:  # Sample Text
                samples = {
                    "Technology Article": """Artificial intelligence has transformed from a futuristic concept to an integral part of our daily lives. Machine learning algorithms now power everything from recommendation systems on streaming platforms to autonomous vehicles navigating city streets. The rapid advancement in natural language processing has enabled AI assistants to understand and respond to human queries with unprecedented accuracy. However, this technological revolution raises important questions about privacy, job displacement, and the ethical implications of algorithmic decision-making. As we stand at the threshold of artificial general intelligence, society must carefully balance innovation with responsibility to ensure AI benefits humanity as a whole.""",
                    
                    "Business Report": """The third quarter financial results demonstrate exceptional performance across all business units, with total revenue reaching $2.8 billion, representing a 24% increase year-over-year. The cloud services division emerged as the primary growth driver, contributing 42% of total revenue with a remarkable 35% growth rate. International markets showed particularly strong momentum, accounting for 38% of revenue and growing at 28%. Operating margins expanded to 22.1%, reflecting successful cost optimization initiatives and economies of scale. Customer acquisition metrics remained robust with a 15% increase in enterprise clients and a customer retention rate of 94%. The company's strategic investments in artificial intelligence and cybersecurity solutions are positioning it well for continued market leadership.""",
                    
                    "Scientific Study": """Recent research in cognitive neuroscience has revealed fascinating insights into the brain's plasticity and its ability to reorganize throughout life. Using advanced neuroimaging techniques, scientists have observed how learning new skills creates new neural pathways while strengthening existing connections. The study followed 200 participants over 18 months as they learned musical instruments, finding significant structural changes in areas responsible for motor control, auditory processing, and memory formation. Remarkably, these neuroplastic changes were observed across all age groups, challenging previous assumptions about critical learning periods. The findings have profound implications for rehabilitation medicine, educational strategies, and our understanding of lifelong learning potential."""
                }
                
                selected_sample = st.selectbox("Choose a sample:", list(samples.keys()))
                if selected_sample:
                    text_to_summarize = samples[selected_sample]
                    st.text_area("Sample text:", value=text_to_summarize, height=200)
        
        with col2:
            st.subheader("📋 Summary")
            
            if st.button("🚀 Generate Summary", type="primary", use_container_width=True):
                if not text_to_summarize.strip():
                    st.warning("⚠️ Please enter some text to summarize.")
                else:
                    start_time = time.time()
                    
                    with st.spinner("🤖 AI is analyzing your text..."):
                        # Create the prompt
                        prompt = create_advanced_prompt(text_to_summarize, summary_type, custom_instructions)
                        
                        # Generate summary
                        summary = ollama.generate(model_name, prompt, stream=enable_streaming)
                        
                        if summary:
                            end_time = time.time()
                            processing_time = end_time - start_time
                            
                            st.success("✅ Summary generated successfully!")
                            
                            # Display summary with nice formatting
                            st.markdown("### 📝 Generated Summary:")
                            st.markdown(f"""
                            <div style="background-color: #f8f9fa; padding: 1rem; border-left: 4px solid #667eea; margin: 1rem 0;">
                                {summary}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Enhanced statistics
                            st.markdown("### 📊 Analysis")
                            
                            col_a, col_b, col_c, col_d = st.columns(4)
                            
                            with col_a:
                                st.metric("Original Length", f"{len(text_to_summarize):,} chars")
                            
                            with col_b:
                                st.metric("Summary Length", f"{len(summary):,} chars")
                            
                            with col_c:
                                compression_ratio = (len(summary) / len(text_to_summarize)) * 100
                                st.metric("Compression", f"{compression_ratio:.1f}%")
                            
                            with col_d:
                                st.metric("Processing Time", f"{processing_time:.1f}s")
                            
                            # Word count analysis
                            original_words = len(text_to_summarize.split())
                            summary_words = len(summary.split())
                            
                            st.markdown("### 📈 Detailed Metrics")
                            col_x, col_y = st.columns(2)
                            
                            with col_x:
                                st.info(f"**Original:** {original_words:,} words")
                            
                            with col_y:
                                st.info(f"**Summary:** {summary_words:,} words")
                            
                            # Save to session
                            save_summary_session(text_to_summarize, summary, model_name, summary_type)
                            
                            # Download option
                            summary_download = f"""# Summary ({summary_type.title()})
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Model: {model_name}

## Original Text ({len(text_to_summarize):,} characters)
{text_to_summarize}

## Summary ({len(summary):,} characters)
{summary}

## Statistics
- Compression Ratio: {compression_ratio:.1f}%
- Processing Time: {processing_time:.1f}s
- Word Count: {original_words:,} → {summary_words:,}
"""
                            
                            st.download_button(
                                label="📥 Download Summary",
                                data=summary_download,
                                file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown"
                            )
                        
                        else:
                            st.error("❌ Failed to generate summary. Please check your Ollama connection.")
    
    with tab2:
        display_summary_history()
        
        if st.button("🗑️ Clear History"):
            st.session_state.summary_history = []
            st.rerun()
    
    with tab3:
        st.markdown("""
        ## 🚀 Enhanced AI Text Summarizer
        
        This advanced version includes:
        
        ### 🎯 Features
        - **Multiple Summary Types**: General, bullet points, executive, academic, timeline, and Q&A formats
        - **File Upload Support**: TXT, PDF, DOCX, and Markdown files
        - **Custom Instructions**: Add specific requirements for your summaries
        - **Streaming Support**: Watch summaries generate in real-time
        - **Session History**: Keep track of recent summaries
        - **Advanced Analytics**: Detailed metrics and statistics
        - **Export Function**: Download summaries as Markdown files
        
        ### 🤖 Models Supported
        - Llama 3.2 (latest, 1b, 3b variants)
        - Any model available in your local Ollama installation
        
        ### 💡 Tips for Best Results
        1. **Choose the right summary type** for your content
        2. **Add custom instructions** for specific requirements
        3. **Adjust word limits** based on your needs
        4. **Use streaming** for longer texts to see progress
        5. **Upload files directly** instead of copy-pasting large documents
        
        ### 🔧 Technical Details
        - Built with Streamlit and Python
        - Uses Ollama for local AI processing
        - Supports multiple file formats
        - Responsive design with custom CSS
        - Session state management for history
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>💡 <strong>Pro Tip:</strong> Ensure Ollama is running with <code>ollama serve</code> and your desired model is pulled with <code>ollama pull [model-name]</code></p>
        <p>🔒 <strong>Privacy:</strong> All processing happens locally on your machine</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()