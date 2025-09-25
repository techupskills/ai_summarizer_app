# Lab 1: Building an AI Text Summarizer with Streamlit and Ollama

## Overview
In this lab, you'll create a complete AI-powered text summarization application using Llama 3.2 running locally through Ollama, with a user-friendly Streamlit interface.

## Prerequisites
- GitHub Codespace (or local development environment)
- Basic Python knowledge
- Ollama installed and running
- Estimated time: 8-10 minutes

## Learning Objectives
- Understand how to integrate local LLMs with web applications
- Learn prompt engineering for summarization tasks
- Build interactive AI applications with Streamlit
- Implement different summarization styles

## Step-by-Step Instructions

### Step 1: Set Up Your Environment
Create a new directory and navigate to it:
```bash
mkdir ai-summarizer
cd ai-summarizer
```

### Step 2: Install Required Dependencies
Create and install from requirements:
```bash
pip install streamlit requests
```

### Step 3: Start Ollama Service
In your codespace terminal, start Ollama:
```bash
ollama serve
```
Keep this terminal running throughout the lab.

### Step 4: Pull the Llama 3.2 Model
In a new terminal, download the model:
```bash
ollama pull llama3.2:latest
```
This may take 2-3 minutes depending on your connection.

### Step 5: Create the Core Application File
Create `app.py` and add the OllamaClient class:
```python
import requests
import json
import streamlit as st
from typing import Optional

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, model: str, prompt: str) -> Optional[str]:
        url = f"{self.base_url}/api/generate"
        payload = {"model": model, "prompt": prompt, "stream": False}
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to Ollama: {e}")
            return None
```

### Step 6: Add Prompt Engineering Function
Add the summarization prompt creator:
```python
def create_summary_prompt(text: str, summary_type: str = "general") -> str:
    prompts = {
        "general": f"""Please provide a concise summary of the following text:

Text: {text}

Summary:""",
        
        "bullet_points": f"""Summarize as bullet points:

Text: {text}

Key Points:
•""",
        
        "executive": f"""Provide an executive summary:

Text: {text}

Executive Summary:"""
    }
    return prompts.get(summary_type, prompts["general"])
```

### Step 7: Create the Streamlit Interface
Add the main application interface:
```python
def main():
    st.set_page_config(page_title="AI Text Summarizer", page_icon="📝")
    st.title("🤖 AI Text Summarizer")
    st.markdown("Powered by Llama 3.2 via Ollama")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    model_name = st.sidebar.selectbox("Model", ["llama3.2:latest"])
    summary_type = st.sidebar.selectbox(
        "Summary Style", 
        ["general", "bullet_points", "executive"]
    )
```

### Step 8: Add Input and Output Sections
Create the main interface with columns:
```python
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Input Text")
        text_to_summarize = st.text_area(
            "Enter text to summarize:",
            height=300,
            placeholder="Paste your text here..."
        )
    
    with col2:
        st.subheader("📋 Summary")
        
        if st.button("Generate Summary", type="primary"):
            if text_to_summarize.strip():
                with st.spinner("Generating summary..."):
                    ollama = OllamaClient()
                    prompt = create_summary_prompt(text_to_summarize, summary_type)
                    summary = ollama.generate(model_name, prompt)
                    
                    if summary:
                        st.success("Summary generated!")
                        st.write(summary)
```

### Step 9: Add Statistics and File Upload
Enhance with metrics and file upload capability:
```python
                        # Add statistics
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Original", f"{len(text_to_summarize)} chars")
                        with col_b:
                            compression = len(summary)/len(text_to_summarize)*100
                            st.metric("Compression", f"{compression:.1f}%")
```

### Step 10: Run Your Application
Complete the main function and run:
```python
if __name__ == "__main__":
    main()
```

Start your app:
```bash
streamlit run app.py
```

### Step 11: Test Different Summary Types
1. Paste a news article or document
2. Try different summary styles from the sidebar
3. Upload a text file to test file processing
4. Observe the compression ratios

### Step 12: Customize and Experiment
Try modifying the prompts in `create_summary_prompt()` to create:
- Technical summaries
- Creative summaries
- Question-based summaries

## Key Concepts Demonstrated
- **Local LLM Integration**: Using Ollama for private, local AI processing
- **Prompt Engineering**: Crafting effective prompts for different output styles
- **Interactive UI**: Building user-friendly interfaces with Streamlit
- **Error Handling**: Managing API connections and user input validation
- **Streaming vs. Non-streaming**: Understanding different response patterns

## Troubleshooting
- **Connection Error**: Ensure `ollama serve` is running
- **Model Not Found**: Run `ollama pull llama3.2:latest`
- **Port Issues**: Check if port 11434 is available
- **Slow Response**: Try smaller models like `llama3.2:1b`

## Next Steps
Your AI summarizer is ready! In Lab 2, you'll deploy this application to Hugging Face Spaces to share it with the world.

## Files Created
- `app.py` - Main application file
- Requirements for Streamlit and requests packages