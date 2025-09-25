# DevContainer Setup for AI Summarizer Workshop

This directory contains the development container configuration for the AI Summarizer Workshop, providing a complete, pre-configured environment that works with GitHub Codespaces and VS Code Dev Containers.

## 🚀 Quick Start

### Option 1: GitHub Codespaces
1. Click the "Open in GitHub Codespaces" button in the main README
2. Wait for the container to build and setup to complete (3-5 minutes)
3. All tools, models, and dependencies will be ready automatically

### Option 2: VS Code Dev Containers
1. Install the "Dev Containers" extension in VS Code
2. Open this repository in VS Code
3. Press `Ctrl+Shift+P` and select "Dev Containers: Reopen in Container"
4. Wait for setup to complete

## 📦 What's Included

### Pre-installed Software
- **Ollama**: Local LLM server pre-configured
- **Python 3.11**: Latest Python with pip
- **AI Models**: Llama 3.2 variants pre-downloaded
- **Development Tools**: Git, curl, wget, build tools

### Python Packages
- **Core**: streamlit, requests, transformers, torch
- **File Processing**: python-docx, PyPDF2
- **UI Frameworks**: gradio
- **Development**: jupyter, matplotlib, pandas, numpy

### VS Code Extensions
- Python development tools
- Jupyter notebook support
- YAML and JSON editors
- Auto-formatting and linting

## 🔧 Configuration Details

### Port Forwarding
- **8501**: Basic Streamlit app (`ai_summarizer_app.py`)
- **8502**: Enhanced Streamlit app (`streamlit_enhanced.py`)
- **7860**: Gradio interface (`gradio_version.py`)
- **11434**: Ollama API (internal)

### Environment Variables
- `OLLAMA_HOST=0.0.0.0:11434`
- `STREAMLIT_SERVER_PORT=8501`
- `STREAMLIT_SERVER_ADDRESS=0.0.0.0`

### Volume Mounts
- `ollama-data`: Persistent storage for Ollama models and data

## 🏗️ Build Process

### Container Build Steps
1. **Base Image**: Ubuntu 22.04 with development tools
2. **Python Setup**: Python 3.11 installation and configuration
3. **Ollama Installation**: Download and configure Ollama
4. **Dependencies**: Install all Python packages from requirements.txt
5. **Configuration**: Set up environment and permissions

### Post-Creation Setup
The `setup.sh` script automatically:
- Waits for Ollama service to start
- Downloads Llama 3.2 models (1b and latest versions)
- Verifies all installations
- Creates sample files for testing
- Configures VS Code workspace settings

## 🧪 Testing Your Setup

After the container starts, you can verify everything works:

```bash
# Test the setup
python test_setup.py

# Start the basic app
streamlit run ai_summarizer_app.py

# Start the enhanced app (different port)
streamlit run streamlit_enhanced.py --server.port 8502

# Start the Gradio interface
python gradio_version.py
```

## 🔍 Troubleshooting

### Container Won't Start
- Ensure Docker is running
- Check available disk space (need ~4GB for full setup)
- Try rebuilding the container: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"

### Ollama Not Responding
- The setup script waits up to 60 seconds for Ollama to start
- Check if Ollama is running: `curl http://localhost:11434/api/tags`
- Manually restart: `ollama serve &`

### Models Not Downloaded
- Large models take time to download
- Check available models: `ollama list`
- Manually download: `ollama pull llama3.2:latest`

### Port Forwarding Issues
- VS Code should automatically forward ports
- Check the "Ports" tab in the terminal panel
- Manually add ports if needed: `Ctrl+Shift+P` → "Ports: Focus on Ports View"

## 📝 Files Explained

### `devcontainer.json`
Main configuration file defining:
- Base container image and build settings
- Port forwarding configuration
- VS Code extensions and settings
- Environment variables
- Startup commands

### `Dockerfile`
Custom container image with:
- Ubuntu 22.04 base system
- Python 3.11 and development tools
- Ollama installation
- All required Python packages
- Proper user permissions and directory setup

### `setup.sh`
Post-creation script that:
- Waits for Ollama service
- Downloads AI models
- Creates sample files
- Configures VS Code settings
- Verifies installation

## 🚀 Advanced Usage

### Adding New Models
```bash
# In the container terminal
ollama pull <model-name>
ollama list  # verify
```

### Installing Additional Packages
```bash
pip install <package-name>
# Add to requirements.txt for persistence
```

### Customizing VS Code
Edit `.vscode/settings.json` or use the VS Code settings UI

## 💡 Tips

1. **First Startup**: Allow 3-5 minutes for complete setup
2. **Model Storage**: Models persist between container sessions
3. **Port Access**: Use the "Ports" tab to access forwarded applications
4. **Resource Usage**: The container needs ~2GB RAM and 4GB disk space
5. **Internet Required**: For initial model downloads

## 🆘 Support

If you encounter issues:
1. Check the terminal output for error messages
2. Try rebuilding the container
3. Ensure you have enough disk space and memory
4. Check that ports aren't blocked by firewalls

The devcontainer provides a consistent, reproducible environment for the AI Summarizer Workshop, eliminating setup complexity and ensuring all participants have the same tools and configurations.