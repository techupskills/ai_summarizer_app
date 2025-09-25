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

# AI Text Summarizer Workshop

## Overview
This repository contains a complete AI workshop for building and deploying a text summarization application. The workshop demonstrates key AI concepts through hands-on labs that progress from local development to cloud deployment.

## Workshop Structure

### 🎯 Learning Objectives
- Understand local vs. cloud AI model deployment
- Learn prompt engineering for summarization tasks
- Build interactive AI applications with Streamlit/Gradio
- Deploy applications to Hugging Face Spaces
- Compare different AI model architectures (Llama vs. BART)

### 📚 Key AI Concepts Demonstrated
- **Local LLM Integration**: Using Ollama with Llama 3.2
- **Cloud-based Inference**: Hugging Face Transformers with BART
- **Prompt Engineering**: Crafting effective summarization prompts
- **Text Processing**: Chunking strategies for long documents
- **Model Comparison**: Local vs. cloud trade-offs
- **UI/UX for AI**: Building user-friendly AI interfaces

## Files Included

### 🧪 Lab Materials
- `lab1_building_ai_summarizer.md` - Build local app with Ollama + Streamlit
- `lab2_deploying_to_huggingface.md` - Deploy to cloud with Hugging Face
- `lab3_enhanced_streamlit_interface.md` - Advanced Streamlit interface with file uploads, history, and analytics

### 💻 Code Examples
- `ai_summarizer_app.py` - Complete local version with Ollama integration
- `streamlit_enhanced.py` - Advanced Streamlit interface with file uploads, session history, and analytics
- `app_cloud.py` - Cloud-optimized version for Hugging Face Spaces  
- `gradio_version.py` - Alternative Gradio interface implementation
- `requirements.txt` - Python dependencies

### 🐳 DevContainer Setup
- `.devcontainer/devcontainer.json` - VS Code devcontainer configuration
- `.devcontainer/Dockerfile` - Custom container with Ollama and Python
- `.devcontainer/setup.sh` - Automated setup script for models and dependencies

### 📋 Prerequisites

#### For DevContainer (Recommended)
- **Requirements**: VS Code with Dev Containers extension OR GitHub Codespaces
- **Setup Time**: 3-5 minutes (automated)
- **Includes**: Everything pre-configured and ready to use

#### For Lab 1 (Local Development)
- **Environment**: Local Python 3.8+ (if not using devcontainer)
- **Tools**: 
  - Ollama installed and running
  - Python packages: `streamlit`, `requests`
- **Model**: Llama 3.2 (pulled via Ollama)
- **Time**: 8-10 minutes

#### For Lab 2 (Cloud Deployment)
- **Accounts**: Free Hugging Face account
- **Tools**: Git, web browser
- **Dependencies**: `transformers`, `torch`, `streamlit`
- **Time**: 8-10 minutes

#### For Lab 3 (Enhanced Interface)
- **Prerequisites**: Lab 1 completion
- **Additional Dependencies**: `python-docx`, `PyPDF2`
- **Features**: File uploads, session history, advanced analytics
- **Time**: 15-20 minutes

## Quick Start

### Option 1: GitHub Codespaces/DevContainer (Recommended)
**One-click setup with everything pre-configured!**

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/YOUR_USERNAME/ai-summarizer-workshop)

Or in VS Code with Dev Containers:
1. Open this repository in VS Code
2. Click "Reopen in Container" when prompted
3. Wait for setup to complete (3-5 minutes)
4. Start coding immediately!

The devcontainer includes:
- ✅ Ollama pre-installed and configured
- ✅ Llama 3.2 models pre-downloaded
- ✅ All Python dependencies installed
- ✅ VS Code extensions configured
- ✅ Port forwarding set up
- ✅ Sample files ready to use

### Option 2: Local Development with Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull Llama 3.2 model
ollama pull llama3.2:latest

# Install Python dependencies
pip install streamlit requests

# Run the local app
streamlit run ai_summarizer_app.py
```

### Option 3: Cloud Deployment to Hugging Face
```bash
# Create new Hugging Face Space (via web interface)
# Clone your space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
cd SPACE_NAME

# Copy cloud files
cp app_cloud.py .
cp requirements.txt .
cp README.md .

# Deploy
git add .
git commit -m "Deploy AI summarizer"
git push origin main
```

### Option 4: Enhanced Streamlit Interface
```bash
pip install streamlit requests python-docx PyPDF2
streamlit run streamlit_enhanced.py
```

### Option 5: Gradio Interface
```bash
pip install gradio transformers torch
python gradio_version.py
```

## Technical Architecture

### Local Version (Ollama + Llama 3.2)
- **Pros**: Privacy, customizable, no API limits
- **Cons**: Requires local resources, setup complexity
- **Best for**: Development, sensitive data, customization

### Cloud Version (Hugging Face + BART)
- **Pros**: Scalable, no setup, globally accessible
- **Cons**: API dependencies, potential costs, less privacy
- **Best for**: Production, sharing, collaboration

## Workshop Timeline

| Phase | Duration | Activity |
|-------|----------|----------|
| Setup | 5 min | Environment preparation |
| Lab 1 | 10 min | Build local AI app |
| Break | 5 min | Q&A and discussion |
| Lab 2 | 10 min | Deploy to cloud |
| Lab 3 | 20 min | Enhanced interface (optional) |
| Demo | 5 min | Test and share results |
| **Total** | **55 min** | Complete workshop (35 min core + 20 min advanced) |

## Troubleshooting

### Common Issues

#### Lab 1 (Local)
- **Ollama connection errors**: Ensure `ollama serve` is running
- **Model not found**: Run `ollama pull llama3.2:latest`
- **Port conflicts**: Check if port 11434 is available
- **Slow responses**: Try smaller models like `llama3.2:1b`

#### Lab 2 (Cloud)
- **Build failures**: Verify requirements.txt compatibility
- **Memory errors**: Use smaller models or optimize chunking
- **Deployment delays**: Allow 2-3 minutes for initial deployment
- **Runtime errors**: Check Hugging Face Space logs

## Extensions and Next Steps

### Advanced Features to Add
- **Multi-language support**: Integrate translation capabilities
- **Custom models**: Fine-tune on domain-specific data
- **Batch processing**: Handle multiple documents
- **API endpoints**: Create REST API for integration
- **Analytics**: Track usage and performance metrics

### Learning Extensions
- **RAG Implementation**: Combine with vector databases
- **Fine-tuning**: Custom model training workflows
- **Evaluation Metrics**: ROUGE, BLEU score integration
- **A/B Testing**: Compare different summarization approaches

## Resources

### Documentation
- [Ollama Documentation](https://ollama.ai/docs)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Gradio Documentation](https://gradio.app/docs/)

### Model Information
- [Llama 3.2 Model Card](https://ollama.ai/library/llama3.2)
- [BART-Large-CNN](https://huggingface.co/facebook/bart-large-cnn)

### Deployment Platforms
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)
- [Streamlit Community Cloud](https://streamlit.io/cloud)
- [Gradio on Hugging Face](https://huggingface.co/docs/hub/spaces-sdks-gradio)

## License
MIT License - Feel free to use and modify for educational purposes.

## Contributing
This is a workshop material. Suggestions for improvements welcome via issues or pull requests.

---
🚀 **Ready to build your first AI app?** 
- **Beginners**: Start with Lab 1 for the basic local app
- **Intermediate**: Continue to Lab 2 for cloud deployment  
- **Advanced**: Try Lab 3 for the enhanced interface with file uploads and analytics