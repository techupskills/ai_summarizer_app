import gradio as gr
from transformers import pipeline
import torch

# Initialize the summarization pipeline
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=0 if torch.cuda.is_available() else -1
)

def summarize_text(text, max_length=150, min_length=50):
    """Generate summary using BART model"""
    if not text.strip():
        return "Please enter some text to summarize."
    
    if len(text.strip()) < 100:
        return "Please enter at least 100 characters for meaningful summarization."
    
    try:
        # Handle long texts by chunking
        max_input_length = 1024
        if len(text.split()) > max_input_length:
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
            
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def get_statistics(original_text, summary_text):
    """Calculate text statistics"""
    if not summary_text or summary_text.startswith("Error") or summary_text.startswith("Please"):
        return "", "", ""
    
    original_words = len(original_text.split())
    summary_words = len(summary_text.split())
    compression_ratio = (summary_words / original_words) * 100
    
    return f"{original_words:,}", f"{summary_words:,}", f"{compression_ratio:.1f}%"

# Sample texts for demonstration
sample_texts = {
    "Technology News": """
    Artificial intelligence has reached a new milestone with the development of large language models that can understand and generate human-like text. These models, trained on vast amounts of data, have shown remarkable capabilities in various tasks including translation, summarization, and creative writing. Companies are now integrating these AI systems into their products and services, revolutionizing how we interact with technology. However, concerns about bias, accuracy, and ethical use remain significant challenges that researchers and developers are actively addressing.
    """,
    "Climate Science": """
    Climate change represents one of the most pressing challenges of our time, with global temperatures rising at an unprecedented rate due to human activities. Recent studies have shown that carbon dioxide levels in the atmosphere have reached their highest point in over 3 million years, leading to significant changes in weather patterns, sea levels, and ecosystem dynamics. The impacts are already visible through more frequent extreme weather events, melting polar ice caps, and shifts in agricultural productivity. To address this crisis, scientists emphasize the urgent need for comprehensive mitigation strategies including renewable energy adoption, carbon capture technologies, and international cooperation.
    """,
    "Business Report": """
    The quarterly financial results show strong performance across all major business segments, with revenue increasing by 15% compared to the same period last year. The technology division led growth with a 22% increase, driven by strong demand for cloud services and artificial intelligence solutions. Operating margins improved to 18.5%, reflecting successful cost optimization initiatives and operational efficiency gains. International markets contributed 45% of total revenue, with particularly strong performance in Asia-Pacific regions. Looking ahead, the company expects continued growth momentum, supported by new product launches and expanding market opportunities.
    """
}

def load_sample(sample_name):
    """Load a sample text"""
    return sample_texts.get(sample_name, "")

# Create Gradio interface
with gr.Blocks(title="AI Text Summarizer", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🤖 AI Text Summarizer
    **Powered by Facebook BART-Large-CNN via Hugging Face**
    
    Generate concise, intelligent summaries of your text using state-of-the-art AI.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📄 Input Text")
            
            # Sample text selector
            sample_dropdown = gr.Dropdown(
                choices=list(sample_texts.keys()),
                label="Try a sample text (optional)",
                value=None
            )
            
            text_input = gr.Textbox(
                label="Enter your text here",
                placeholder="Paste your article, document, or any text you want to summarize...",
                lines=12,
                max_lines=15
            )
            
            # Settings
            with gr.Row():
                max_length_slider = gr.Slider(
                    minimum=50,
                    maximum=300,
                    value=150,
                    step=10,
                    label="Max Summary Length"
                )
                min_length_slider = gr.Slider(
                    minimum=10,
                    maximum=100,
                    value=50,
                    step=5,
                    label="Min Summary Length"
                )
            
            summarize_btn = gr.Button("🚀 Generate Summary", variant="primary", size="lg")
            
        with gr.Column(scale=1):
            gr.Markdown("### 📋 Summary Output")
            
            summary_output = gr.Textbox(
                label="Generated Summary",
                lines=8,
                max_lines=12,
                interactive=False
            )
            
            gr.Markdown("### 📊 Statistics")
            with gr.Row():
                original_words = gr.Textbox(label="Original Words", interactive=False)
                summary_words = gr.Textbox(label="Summary Words", interactive=False)
                compression_ratio = gr.Textbox(label="Compression Ratio", interactive=False)
    
    # Event handlers
    def process_summary(text, max_len, min_len):
        summary = summarize_text(text, max_len, min_len)
        orig_words, summ_words, comp_ratio = get_statistics(text, summary)
        return summary, orig_words, summ_words, comp_ratio
    
    # Load sample text
    sample_dropdown.change(
        fn=load_sample,
        inputs=[sample_dropdown],
        outputs=[text_input]
    )
    
    # Generate summary
    summarize_btn.click(
        fn=process_summary,
        inputs=[text_input, max_length_slider, min_length_slider],
        outputs=[summary_output, original_words, summary_words, compression_ratio]
    )
    
    gr.Markdown("""
    ### 🎯 How It Works
    This app uses **Facebook's BART** (Bidirectional and Auto-Regressive Transformers) model, 
    fine-tuned on CNN/DailyMail dataset for abstractive summarization.
    
    ### 💡 Tips for Best Results
    - Use well-structured text (articles, reports, documents)
    - Minimum 100 characters for meaningful summaries
    - Longer texts are automatically chunked for processing
    - Adjust summary length based on your needs
    """)

if __name__ == "__main__":
    demo.launch()