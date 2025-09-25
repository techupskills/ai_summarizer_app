import streamlit as st
from transformers import pipeline
import torch

# Initialize the summarization pipeline
@st.cache_resource
def load_model():
    """Load and cache the summarization model"""
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=0 if torch.cuda.is_available() else -1
    )

def create_summary(text: str, max_length: int = 150, min_length: int = 50):
    """Generate summary using BART model with chunking for long texts"""
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

def main():
    st.set_page_config(
        page_title="AI Text Summarizer",
        page_icon="🤖",
        layout="wide"
    )
    
    # Custom CSS for better appearance
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>🤖 AI Text Summarizer</h1><p>Powered by Facebook BART-Large-CNN via Hugging Face</p></div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Settings")
    max_length = st.sidebar.slider("Max Summary Length (words)", 50, 300, 150, step=10)
    min_length = st.sidebar.slider("Min Summary Length (words)", 10, 100, 50, step=5)
    
    # Ensure min_length is less than max_length
    if min_length >= max_length:
        st.sidebar.error("Min length must be less than max length!")
        min_length = max_length - 10
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Input Text")
        
        input_method = st.radio("Choose input method:", ["Type Text", "Upload File"])
        
        text_input = ""
        if input_method == "Type Text":
            text_input = st.text_area(
                "Enter text to summarize:",
                height=300,
                placeholder="Paste your article, document, or text here...\n\nExample: News articles, research papers, long emails, meeting notes, etc."
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload a text file", 
                type=['txt', 'md'],
                help="Upload a .txt or .md file containing the text you want to summarize"
            )
            if uploaded_file:
                text_input = str(uploaded_file.read(), "utf-8")
                st.text_area("File content preview:", value=text_input[:500] + "...", height=150)
    
    with col2:
        st.subheader("📋 Summary")
        
        if st.button("🚀 Generate Summary", type="primary"):
            if not text_input.strip():
                st.warning("⚠️ Please enter some text to summarize.")
            elif len(text_input.strip()) < 100:
                st.warning("⚠️ Please enter at least 100 characters for meaningful summarization.")
            else:
                with st.spinner("🔄 Analyzing and summarizing your text..."):
                    try:
                        summary = create_summary(text_input, max_length, min_length)
                        
                        st.success("✅ Summary Generated Successfully!")
                        
                        # Display summary in an info box
                        st.markdown("### 📝 Your Summary:")
                        st.info(summary)
                        
                        # Copy to clipboard button
                        st.code(summary, language=None)
                        
                        # Statistics
                        st.markdown("### 📊 Statistics:")
                        col_a, col_b, col_c = st.columns(3)
                        
                        original_words = len(text_input.split())
                        summary_words = len(summary.split())
                        compression_ratio = (summary_words / original_words) * 100
                        
                        with col_a:
                            st.metric("📄 Original Words", f"{original_words:,}")
                        with col_b:
                            st.metric("📋 Summary Words", f"{summary_words:,}")
                        with col_c:
                            st.metric("🎯 Compression Ratio", f"{compression_ratio:.1f}%")
                            
                    except Exception as e:
                        st.error(f"❌ Error generating summary: {str(e)}")
                        st.info("💡 Try with shorter text or check your internet connection.")
    
    # Sample texts section
    st.markdown("---")
    with st.expander("📚 Try Sample Texts"):
        sample_text = st.selectbox(
            "Choose a sample text:",
            [
                "Technology News Article",
                "Scientific Abstract",
                "Business Report"
            ]
        )
        
        sample_texts = {
            "Technology News Article": """
            Artificial intelligence has reached a new milestone with the development of large language models that can understand and generate human-like text. These models, trained on vast amounts of data, have shown remarkable capabilities in various tasks including translation, summarization, and creative writing. Companies are now integrating these AI systems into their products and services, revolutionizing how we interact with technology. However, concerns about bias, accuracy, and ethical use remain significant challenges that researchers and developers are actively addressing. The rapid advancement in AI technology promises to transform industries from healthcare to education, but it also raises important questions about the future of work and human-AI collaboration.
            """,
            "Scientific Abstract": """
            Climate change represents one of the most pressing challenges of our time, with global temperatures rising at an unprecedented rate due to human activities. Recent studies have shown that carbon dioxide levels in the atmosphere have reached their highest point in over 3 million years, leading to significant changes in weather patterns, sea levels, and ecosystem dynamics. The impacts are already visible through more frequent extreme weather events, melting polar ice caps, and shifts in agricultural productivity. To address this crisis, scientists emphasize the urgent need for comprehensive mitigation strategies including renewable energy adoption, carbon capture technologies, and international cooperation. The window for limiting global warming to 1.5°C above pre-industrial levels is rapidly closing, requiring immediate and sustained action from governments, businesses, and individuals worldwide.
            """,
            "Business Report": """
            The quarterly financial results show strong performance across all major business segments, with revenue increasing by 15% compared to the same period last year. The technology division led growth with a 22% increase, driven by strong demand for cloud services and artificial intelligence solutions. Operating margins improved to 18.5%, reflecting successful cost optimization initiatives and operational efficiency gains. International markets contributed 45% of total revenue, with particularly strong performance in Asia-Pacific regions. Looking ahead, the company expects continued growth momentum, supported by new product launches and expanding market opportunities. However, challenges include supply chain constraints, inflationary pressures, and increased competition in key markets. Management remains confident in the long-term strategy and expects to achieve full-year targets despite near-term headwinds.
            """
        }
        
        if st.button("📋 Use This Sample"):
            st.rerun()
    
    # Footer with information
    st.markdown("---")
    st.markdown("""
    ### 🎯 How It Works
    This app uses **Facebook's BART** (Bidirectional and Auto-Regressive Transformers) model, 
    fine-tuned on CNN/DailyMail dataset for abstractive summarization. Unlike extractive 
    summarization that selects existing sentences, BART generates new sentences that capture 
    the essence of the original text.
    
    ### 💡 Tips for Best Results
    - Use well-structured text (articles, reports, documents)
    - Minimum 100 characters for meaningful summaries
    - Longer texts may be automatically chunked for processing
    - Adjust summary length based on your needs
    """)

if __name__ == "__main__":
    main()