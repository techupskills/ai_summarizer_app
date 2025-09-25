import requests
import json
import streamlit as st
from typing import Optional


class OllamaClient:
    """Simple client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, model: str, prompt: str, stream: bool = False) -> Optional[str]:
        """Generate text using Ollama model"""
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
                return self._handle_stream(response)
            else:
                result = response.json()
                return result.get("response", "")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to Ollama: {e}")
            return None
    
    def _handle_stream(self, response):
        """Handle streamed response from Ollama"""
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_response = json.loads(line)
                    if "response" in json_response:
                        full_response += json_response["response"]
                except json.JSONDecodeError:
                    continue
        return full_response


def create_summary_prompt(text: str, summary_type: str = "general") -> str:
    """Create a structured prompt for text summarization"""
    
    prompts = {
        "general": f"""Please provide a concise summary of the following text. Focus on the main points and key information:

Text to summarize:
{text}

Summary:""",
        
        "bullet_points": f"""Please summarize the following text as bullet points, highlighting the most important information:

Text to summarize:
{text}

Key Points:
•""",
        
        "executive": f"""Please provide an executive summary of the following text, focusing on key insights and actionable information:

Text to summarize:
{text}

Executive Summary:"""
    }
    
    return prompts.get(summary_type, prompts["general"])


def main():
    st.set_page_config(
        page_title="AI Text Summarizer",
        page_icon="📝",
        layout="wide"
    )
    
    st.title("🤖 AI Text Summarizer")
    st.markdown("Powered by Llama 3.2 via Ollama")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    model_name = st.sidebar.selectbox(
        "Select Model",
        ["llama3.2:latest", "llama3.2:1b", "llama3.2:3b"],
        index=0
    )
    
    summary_type = st.sidebar.selectbox(
        "Summary Style",
        ["general", "bullet_points", "executive"],
        index=0
    )
    
    # Initialize Ollama client
    ollama = OllamaClient()
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Input Text")
        
        # Text input options
        input_method = st.radio(
            "Choose input method:",
            ["Type/Paste Text", "Upload File"]
        )
        
        text_to_summarize = ""
        
        if input_method == "Type/Paste Text":
            text_to_summarize = st.text_area(
                "Enter text to summarize:",
                height=300,
                placeholder="Paste your text here..."
            )
        
        else:  # Upload File
            uploaded_file = st.file_uploader(
                "Upload a text file",
                type=['txt', 'md']
            )
            
            if uploaded_file is not None:
                text_to_summarize = str(uploaded_file.read(), "utf-8")
                st.text_area("File content:", value=text_to_summarize, height=200)
    
    with col2:
        st.subheader("📋 Summary")
        
        if st.button("Generate Summary", type="primary"):
            if not text_to_summarize.strip():
                st.warning("Please enter some text to summarize.")
            else:
                with st.spinner("Generating summary..."):
                    # Create the prompt
                    prompt = create_summary_prompt(text_to_summarize, summary_type)
                    
                    # Generate summary
                    summary = ollama.generate(model_name, prompt)
                    
                    if summary:
                        st.success("Summary generated successfully!")
                        st.markdown("### Summary:")
                        st.write(summary)
                        
                        # Display statistics
                        st.markdown("### Statistics:")
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            st.metric("Original Length", f"{len(text_to_summarize)} chars")
                        
                        with col_b:
                            st.metric("Summary Length", f"{len(summary)} chars")
                        
                        with col_c:
                            compression_ratio = len(summary) / len(text_to_summarize) * 100
                            st.metric("Compression", f"{compression_ratio:.1f}%")
                    
                    else:
                        st.error("Failed to generate summary. Please check your Ollama connection.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "💡 **Tip:** Make sure Ollama is running locally with `ollama serve` and the selected model is pulled with `ollama pull llama3.2`"
    )


if __name__ == "__main__":
    main()