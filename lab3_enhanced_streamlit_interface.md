# Lab 3: Building an Enhanced Streamlit Interface with Advanced Features

## Overview
In this lab, you'll create a sophisticated AI text summarizer with advanced features including multiple file format support, custom instructions, streaming responses, session history, and enhanced analytics.

## Prerequisites
- Completion of Lab 1 (Basic AI Summarizer)
- GitHub Codespace or local development environment
- Ollama installed and running
- Basic Python knowledge
- Estimated time: 15-20 minutes

## Learning Objectives
- Build advanced Streamlit interfaces with custom CSS and components
- Implement file upload and text extraction from multiple formats
- Create session management and history tracking
- Design responsive layouts with tabs and columns
- Add real-time streaming capabilities
- Implement download functionality for results

## Step-by-Step Instructions

### Step 1: Install Additional Dependencies
Update your requirements to include new packages for file processing:
```bash
pip install streamlit requests python-docx PyPDF2
```

### Step 2: Create the Enhanced Application
Create `streamlit_enhanced.py` with the advanced OllamaClient:

```python
import requests
import json
import streamlit as st
from typing import Optional, List
import time
from datetime import datetime
import io
import docx
import PyPDF2

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, model: str, prompt: str, stream: bool = False) -> Optional[str]:
        # Enhanced generation with streaming support
        url = f"{self.base_url}/api/generate"
        payload = {"model": model, "prompt": prompt, "stream": stream}
        
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
```

### Step 3: Add Advanced Prompt Engineering
Create sophisticated prompts for different summary types:

```python
def create_advanced_prompt(text: str, summary_type: str, custom_instructions: str = "") -> str:
    base_prompts = {
        "general": f"""Provide a comprehensive yet concise summary of the following text:

Text: {text}
{custom_instructions}

Summary:""",
        
        "academic": f"""Create an academic-style summary highlighting thesis, methodology, and conclusions:

Text: {text}
{custom_instructions}

Academic Summary:""",
        
        "timeline": f"""Extract chronological events or processes from the text:

Text: {text}
{custom_instructions}

Timeline Summary:""",
        
        "questions": f"""Generate key questions and answers based on the content:

Text: {text}
{custom_instructions}

Q&A Summary:"""
    }
    return base_prompts.get(summary_type, base_prompts["general"])
```

### Step 4: Implement File Processing
Add support for multiple file formats:

```python
def extract_text_from_file(uploaded_file) -> str:
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
```

### Step 5: Add Session History Management
Implement session tracking for summary history:

```python
def save_summary_session(text: str, summary: str, model: str, summary_type: str):
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
    st.session_state.summary_history = st.session_state.summary_history[:10]

def display_summary_history():
    if 'summary_history' in st.session_state and st.session_state.summary_history:
        st.subheader("📚 Recent Summaries")
        
        for i, session in enumerate(st.session_state.summary_history):
            with st.expander(f"Summary {i+1} - {session['timestamp']} ({session['type']})"):
                st.write(f"**Model:** {session['model']}")
                st.write(f"**Stats:** {session['original_length']} → {session['summary_length']} chars")
                st.write("**Summary:**")
                st.write(session['summary'])
```

### Step 6: Create Enhanced UI with Custom CSS
Add professional styling and layout:

```python
def main():
    st.set_page_config(
        page_title="Enhanced AI Text Summarizer",
        page_icon="🚀",
        layout="wide"
    )
    
    # Custom CSS for styling
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
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>🚀 Enhanced AI Text Summarizer</h1><p>Advanced text summarization with multiple models and formats</p></div>', unsafe_allow_html=True)
```

### Step 7: Implement Tabbed Interface
Create organized sections with tabs:

```python
    # Main interface with tabs
    tab1, tab2, tab3 = st.tabs(["📝 Summarizer", "📚 History", "ℹ️ About"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📄 Input")
            
            input_method = st.radio(
                "Choose input method:",
                ["Type/Paste Text", "Upload File", "Sample Text"]
            )
```

### Step 8: Add Advanced Configuration Options
Implement sophisticated controls:

```python
    # Sidebar configuration
    st.sidebar.header("🔧 Configuration")
    
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
        placeholder="e.g., Focus on technical aspects, Include statistics...",
        height=100
    )
    
    word_limit = st.sidebar.slider(
        "Approximate Word Limit",
        min_value=50,
        max_value=500,
        value=150,
        step=25
    )
```

### Step 9: Implement Enhanced Analytics
Add comprehensive metrics and statistics:

```python
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
```

### Step 10: Add Download Functionality
Enable users to download their summaries:

```python
    summary_download = f"""# Summary ({summary_type.title()})
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Model: {model_name}

## Summary
{summary}

## Statistics
- Compression Ratio: {compression_ratio:.1f}%
- Processing Time: {processing_time:.1f}s
"""
    
    st.download_button(
        label="📥 Download Summary",
        data=summary_download,
        file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )
```

### Step 11: Run and Test Your Enhanced Application
Start your enhanced app:
```bash
streamlit run streamlit_enhanced.py
```

### Step 12: Test All Features
1. **Text Input**: Try all three input methods (paste, upload, sample)
2. **File Upload**: Test with PDF, DOCX, and TXT files
3. **Summary Types**: Experiment with all six summary styles
4. **Custom Instructions**: Add specific requirements
5. **Streaming**: Enable streaming for real-time generation
6. **History**: Check the history tab for previous summaries
7. **Download**: Export summaries as Markdown files

### Step 13: Customization Challenges
Try these enhancements:
- Add more file format support (CSV, JSON)
- Create custom summary templates
- Implement summary comparison features
- Add text preprocessing options
- Create batch processing capabilities

## Key Features Implemented

### 🎯 Advanced Features
- **Multiple Summary Types**: 6 different summarization styles
- **File Upload Support**: TXT, PDF, DOCX, and Markdown files
- **Custom Instructions**: Personalized summarization requirements
- **Streaming Support**: Real-time generation display
- **Session History**: Track and review previous summaries
- **Enhanced Analytics**: Detailed metrics and statistics
- **Export Function**: Download summaries as Markdown files

### 🎨 UI/UX Enhancements
- Custom CSS styling with gradients
- Responsive layout with tabs and columns
- Professional metrics display
- Interactive file preview
- Progress indicators and loading states

### 🔧 Technical Improvements
- Robust file processing with error handling
- Session state management
- Dynamic model loading
- Performance timing
- Memory-efficient text processing

## Troubleshooting

### Common Issues
- **File Upload Errors**: Check file format and size limits
- **PDF Extraction Issues**: Some PDFs may have complex layouts
- **Memory Issues**: Large files may cause performance problems
- **Streaming Not Working**: Ensure Ollama supports streaming for your model

### Performance Tips
- Use smaller models (llama3.2:1b) for faster processing
- Enable streaming for long texts
- Clear history regularly to save memory
- Optimize custom instructions for better results

## Next Steps
Your enhanced AI summarizer is complete! Consider these additional improvements:
- Add user authentication for personalized history
- Implement cloud storage for summaries
- Create API endpoints for programmatic access
- Add collaborative features for team use

## Files Created
- `streamlit_enhanced.py` - Enhanced application with advanced features
- Updated requirements for additional dependencies

This enhanced version provides a professional-grade text summarization tool with enterprise-level features while maintaining ease of use.