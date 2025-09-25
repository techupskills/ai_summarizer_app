# Workshop Prerequisites and Setup Guide

## Pre-Workshop Checklist

### Required Accounts (Free)
- [ ] **GitHub Account** - For accessing GitHub Codespaces
- [ ] **Hugging Face Account** - For deploying to Spaces (Lab 2)
- [ ] **Basic Python Knowledge** - Variables, functions, imports

### Environment Options

#### Option 1: GitHub Codespace (Recommended)
**Pros**: Pre-configured, cloud-based, no local setup
**Cons**: Limited free hours per month

**Setup Steps:**
1. Create or access existing GitHub repository
2. Click "Code" → "Codespaces" → "Create codespace"
3. Wait for environment to initialize (2-3 minutes)
4. Terminal and VS Code interface ready to use

#### Option 2: Local Development
**Pros**: Full control, no time limits, offline capability
**Cons**: Setup complexity, resource requirements

**Requirements:**
- Python 3.8 or higher
- 4GB+ available RAM
- 2GB+ free disk space
- Stable internet connection

## Software Installation

### Essential Tools

#### 1. Python and Pip
```bash
# Check Python version (should be 3.8+)
python --version
python3 --version

# Check pip installation
pip --version
pip3 --version
```

#### 2. Ollama (For Lab 1)
```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Windows (PowerShell)
# Download from: https://ollama.ai/download/windows

# Verify installation
ollama --version
```

#### 3. Git
```bash
# Check if Git is installed
git --version

# If not installed:
# Linux: sudo apt-get install git
# macOS: git (will prompt to install Xcode tools)
# Windows: Download from git-scm.com
```

### Python Packages

#### For Lab 1 (Local Development)
```bash
pip install streamlit==1.28.0 requests==2.31.0
```

#### For Lab 2 (Cloud Deployment)
```bash
pip install transformers==4.35.0 torch==2.1.0 streamlit==1.28.0
```

#### Optional: Gradio Alternative
```bash
pip install gradio==4.0.0
```

## Pre-Workshop Setup Tasks

### 1. Test Ollama Installation (Lab 1 Prep)
```bash
# Start Ollama service
ollama serve

# In another terminal, pull the model (this may take 5-10 minutes)
ollama pull llama3.2:latest

# Test the model
ollama run llama3.2:latest "Hello, how are you?"

# Expected: Llama should respond with a greeting
```

### 2. Verify Python Environment
```bash
# Create test script
echo "import streamlit as st; print('Streamlit version:', st.__version__)" > test_streamlit.py

# Run test
python test_streamlit.py

# Expected output: Streamlit version: 1.28.0
```

### 3. Test Streamlit
```bash
# Create minimal app
echo "import streamlit as st; st.write('Hello, Streamlit!')" > hello_app.py

# Run app
streamlit run hello_app.py

# Expected: Browser opens showing "Hello, Streamlit!"
```

### 4. Hugging Face Account Setup (Lab 2 Prep)
1. Go to [huggingface.co](https://huggingface.co)
2. Click "Sign Up" and create free account
3. Verify email address
4. Navigate to [huggingface.co/spaces](https://huggingface.co/spaces)
5. Familiarize yourself with the Spaces interface

## Troubleshooting Common Issues

### Ollama Issues
```bash
# Issue: "ollama: command not found"
# Solution: Restart terminal or add to PATH
export PATH=$PATH:/usr/local/bin

# Issue: "connection refused"
# Solution: Ensure ollama serve is running
ps aux | grep ollama

# Issue: Model download fails
# Solution: Check internet connection and try again
ollama pull llama3.2:latest --verbose
```

### Python/Pip Issues
```bash
# Issue: "pip: command not found"
# Solution: Use python -m pip instead
python -m pip install streamlit

# Issue: Permission denied
# Solution: Use user installation
pip install --user streamlit

# Issue: Version conflicts
# Solution: Create virtual environment
python -m venv workshop_env
source workshop_env/bin/activate  # Linux/macOS
# workshop_env\Scripts\activate     # Windows
```

### Streamlit Issues
```bash
# Issue: "ModuleNotFoundError: No module named 'streamlit'"
# Solution: Install in correct Python environment
which python
pip show streamlit

# Issue: Port already in use
# Solution: Use different port
streamlit run app.py --server.port 8502

# Issue: Browser doesn't open automatically
# Solution: Manually navigate to displayed URL
```

## Performance Optimization

### For Limited Resources
```bash
# Use smaller Llama model for Lab 1
ollama pull llama3.2:1b

# Reduce Streamlit memory usage
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=50
```

### For GitHub Codespaces
```bash
# Monitor resource usage
htop

# Free up space if needed
ollama rm unused_model
docker system prune -f
```

## Workshop Day Checklist

### 30 Minutes Before Workshop
- [ ] Test internet connection stability
- [ ] Verify Ollama is running: `ollama serve`
- [ ] Confirm Llama 3.2 is available: `ollama list`
- [ ] Test Streamlit: `streamlit hello`
- [ ] Log into Hugging Face account
- [ ] Close unnecessary applications to free resources

### 5 Minutes Before Workshop
- [ ] Open terminal/command prompt
- [ ] Navigate to workshop directory
- [ ] Have Hugging Face login page ready
- [ ] Clear browser cache if needed
- [ ] Ensure stable internet connection

## Emergency Fallback Options

### If Ollama Fails (Lab 1)
- Use cloud-based Llama via Hugging Face API
- Skip to Lab 2 with cloud implementation
- Pair with someone who has working setup

### If Hugging Face Spaces Fails (Lab 2)
- Deploy to Streamlit Community Cloud instead
- Run locally and share screenshots
- Use pre-deployed demo version

### If Internet Connection Issues
- Work on local versions only
- Use offline model if available
- Focus on code understanding vs. live deployment

## Support Resources

### During Workshop
- **Instructor**: Primary support for workshop content
- **Documentation**: Keep official docs bookmarked
- **Peer Support**: Work with nearby participants
- **Chat/Forum**: Workshop-specific communication channel

### Post-Workshop
- **GitHub Repository**: All code examples and solutions
- **Discord/Slack**: Community support channels
- **Office Hours**: Scheduled follow-up sessions
- **Documentation**: Comprehensive guides and troubleshooting

---

## Quick Reference Commands

```bash
# Essential commands for workshop
ollama serve                              # Start Ollama
ollama pull llama3.2:latest             # Download model
streamlit run app.py                     # Run Streamlit app
git add . && git commit -m "message"     # Git commit
git push origin main                     # Deploy to HF Spaces
```

**Ready for the workshop? ✅**

All prerequisites complete! You're ready to build your first AI application.