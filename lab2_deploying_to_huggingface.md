# Lab 2: Deploying AI Text Summarizer to Hugging Face Spaces

## Overview
Transform your local AI application into a publicly accessible web app by deploying it to Hugging Face Spaces. You'll learn how to adapt your Ollama-based app to use Hugging Face's cloud infrastructure.

## Prerequisites
- Completed Lab 1 (AI Text Summarizer)
- Hugging Face account (free at huggingface.co)
- Git installed
- Estimated time: 8-10 minutes

## Learning Objectives
- Adapt local AI apps for cloud deployment
- Use Hugging Face Transformers library
- Deploy applications to Hugging Face Spaces
- Handle cloud-based AI model inference

## Step-by-Step Instructions

### Step 1: Create Hugging Face Account and Space
1. Go to [huggingface.co](https://huggingface.co) and create a free account
2. Navigate to Spaces: [huggingface.co/spaces](https://huggingface.co/spaces)
3. Click "Create new Space"
4. Name: "ai-text-summarizer"
5. License: "MIT"
6. SDK: "Streamlit"
7. Hardware: "CPU basic" (free tier)
8. Click "Create Space"

### Step 2: Prepare Cloud-Compatible Application
Create a new `app_cloud.py` file adapted for Hugging Face:
```python
import streamlit as st
from transformers import pipeline
import torch

# Initialize the summarization pipeline
@st.cache_resource
def load_model():
    # Use a lightweight model suitable for free tier
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=0 if torch.cuda.is_available() else -1
    )

def create_summary(text: str, max_length: int = 150, min_length: int = 50):
    summarizer = load_model()
    
    # Handle long texts by chunking
    max_input_length = 1024
    if len(text.split()) > max_input_length:
        # Split into chunks
        words = text.split()
        chunks = [' '.join(words[i:i+max_input_length]) 
                 for i in range(0, len(words), max_input_length)]
        
        summaries = []
        for chunk in chunks:
            result = summarizer(chunk, 
                              max_length=max_length//len(chunks), 
                              min_length=min_length//len(chunks))
            summaries.append(result[0]['summary_text'])
        
        return ' '.join(summaries)
    else:
        result = summarizer(text, max_length=max_length, min_length=min_length)
        return result[0]['summary_text']
```

### Step 3: Create Requirements File
Create `requirements.txt`:
```
streamlit==1.28.0
transformers==4.35.0
torch==2.1.0
sentencepiece==0.1.99
```

### Step 4: Build the Streamlit Interface
Complete your `app_cloud.py`:
```python
def main():
    st.set_page_config(
        page_title="AI Text Summarizer",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AI Text Summarizer")
    st.markdown("Powered by Facebook BART-Large-CNN via Hugging Face")
    
    # Sidebar configuration
    st.sidebar.header("Settings")
    max_length = st.sidebar.slider("Max Summary Length", 50, 300, 150)
    min_length = st.sidebar.slider("Min Summary Length", 10, 100, 50)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Input Text")
        
        input_method = st.radio("Input Method:", ["Type Text", "Upload File"])
        
        text_input = ""
        if input_method == "Type Text":
            text_input = st.text_area(
                "Enter text to summarize:",
                height=300,
                placeholder="Paste your article, document, or text here..."
            )
        else:
            uploaded_file = st.file_uploader("Upload text file", type=['txt'])
            if uploaded_file:
                text_input = str(uploaded_file.read(), "utf-8")
                st.text_area("File content:", value=text_input[:500] + "...", height=150)
    
    with col2:
        st.subheader("📋 Summary")
        
        if st.button("Generate Summary", type="primary"):
            if not text_input.strip():
                st.warning("Please enter some text to summarize.")
            elif len(text_input.strip()) < 100:
                st.warning("Please enter at least 100 characters for meaningful summarization.")
            else:
                with st.spinner("Analyzing and summarizing..."):
                    try:
                        summary = create_summary(text_input, max_length, min_length)
                        
                        st.success("✅ Summary Generated!")
                        st.markdown("### Summary:")
                        st.info(summary)
                        
                        # Statistics
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Original Words", len(text_input.split()))
                        with col_b:
                            st.metric("Summary Words", len(summary.split()))
                        with col_c:
                            compression = len(summary.split()) / len(text_input.split()) * 100
                            st.metric("Compression Ratio", f"{compression:.1f}%")
                            
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
    
    # Footer with information
    st.markdown("---")
    st.markdown("🎯 **How it works:** This app uses Facebook's BART model fine-tuned on CNN/DailyMail dataset for abstractive summarization.")
    
if __name__ == "__main__":
    main()
```

### Step 5: Create README for Your Space
Create `README.md`:
```markdown
---
title: AI Text Summarizer
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.28.0
app_file: app_cloud.py
pinned: false
---

# AI Text Summarizer

An intelligent text summarization tool powered by Facebook's BART model.

## Features
- Abstractive text summarization
- Adjustable summary length
- File upload support
- Real-time processing

## Usage
1. Enter or upload your text
2. Adjust summary length settings
3. Click "Generate Summary"
4. View your concise summary with statistics
```

### Step 6: Set Up Local Git Repository
Initialize git and connect to your space:
```bash
git init
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/ai-text-summarizer
git add .
git commit -m "Initial commit: AI text summarizer with BART"
```

### Step 7: Deploy to Hugging Face Spaces
Push your code to deploy:
```bash
git push origin main
```

### Step 8: Configure Space Settings
1. Go to your Space on Hugging Face
2. Click "Settings" tab
3. Verify:
   - SDK: Streamlit
   - App file: `app_cloud.py`
   - Python version: 3.9
4. Save if any changes needed

### Step 9: Test Your Deployed App
1. Wait 2-3 minutes for build completion
2. Click on your Space URL
3. Test with sample texts:
   - News articles
   - Research abstracts
   - Long emails or documents

### Step 10: Monitor Performance
Check the logs section to monitor:
- Build status
- Runtime errors
- Performance metrics

### Step 11: Customize Your Space
Enhance your deployment:
```python
# Add custom CSS
st.markdown("""
<style>
.stApp > header {background-color: transparent;}
.stApp {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}
</style>
""", unsafe_allow_html=True)
```

### Step 12: Share and Iterate
1. Share your Space URL with others
2. Collect feedback through the community tab
3. Iterate based on user interactions
4. Consider upgrading to faster hardware if needed

## Key Differences from Local Version
- **Model**: Changed from Llama 3.2 (Ollama) to BART (Hugging Face)
- **Infrastructure**: Cloud-based vs. local processing
- **Scalability**: Handles multiple users simultaneously
- **Accessibility**: Public URL accessible worldwide

## Troubleshooting
- **Build Failures**: Check requirements.txt and Python compatibility
- **Memory Issues**: Use smaller models or optimize batch processing
- **Slow Performance**: Consider upgrading to paid hardware tiers
- **Import Errors**: Ensure all dependencies are in requirements.txt

## Next Steps
- **Custom Models**: Train domain-specific summarization models
- **Advanced Features**: Add keyword extraction, sentiment analysis
- **API Integration**: Create API endpoints for programmatic access
- **Analytics**: Add user interaction tracking

## Resources
- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Streamlit Components](https://docs.streamlit.io/)
- [BART Model Documentation](https://huggingface.co/facebook/bart-large-cnn)

Your AI text summarizer is now live and accessible to users worldwide! 🚀