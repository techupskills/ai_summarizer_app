#!/bin/bash

# AI Summarizer Workshop - Development Container Setup Script
echo "🚀 Setting up AI Summarizer Workshop environment..."

# Wait for Ollama service to be ready
echo "⏳ Waiting for Ollama service to start..."
max_attempts=30
attempt=0

while ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; do
    if [ $attempt -ge $max_attempts ]; then
        echo "❌ Ollama service failed to start after $max_attempts attempts"
        exit 1
    fi
    echo "   Attempt $((attempt + 1))/$max_attempts - waiting for Ollama..."
    sleep 2
    ((attempt++))
done

echo "✅ Ollama service is running!"

# Pull required models
echo "📦 Downloading AI models (this may take a few minutes)..."

# Pull Llama 3.2 models (starting with smallest for faster setup)
echo "   Pulling llama3.2:1b (small, fast model)..."
if ollama pull llama3.2:1b; then
    echo "   ✅ llama3.2:1b downloaded successfully"
else
    echo "   ⚠️  Failed to download llama3.2:1b, but continuing..."
fi

echo "   Pulling llama3.2:latest (default model)..."
if ollama pull llama3.2:latest; then
    echo "   ✅ llama3.2:latest downloaded successfully"
else
    echo "   ⚠️  Failed to download llama3.2:latest"
fi

# Optionally pull the 3b model (commented out to save time and space)
# echo "   Pulling llama3.2:3b (medium model)..."
# if ollama pull llama3.2:3b; then
#     echo "   ✅ llama3.2:3b downloaded successfully"
# else
#     echo "   ⚠️  Failed to download llama3.2:3b, but continuing..."
# fi

# Verify models are available
echo "📋 Verifying installed models..."
ollama list

# Create sample data directory if it doesn't exist
mkdir -p samples

# Create a sample text file for testing
cat > samples/sample_article.txt << 'EOF'
# Sample Article: The Future of AI in Education

Artificial intelligence is revolutionizing the educational landscape in unprecedented ways. From personalized learning algorithms that adapt to individual student needs to automated grading systems that provide instant feedback, AI technologies are reshaping how we teach and learn.

## Key Applications

**Personalized Learning**: AI-powered platforms can analyze student performance data to create customized learning paths, ensuring that each student progresses at their optimal pace.

**Intelligent Tutoring Systems**: Virtual tutors powered by natural language processing can provide 24/7 support to students, answering questions and providing explanations in real-time.

**Administrative Efficiency**: AI streamlines administrative tasks such as scheduling, resource allocation, and student assessment, freeing up educators to focus on teaching.

## Challenges and Considerations

While the potential benefits are significant, the integration of AI in education also presents challenges. Privacy concerns regarding student data, the digital divide between different socioeconomic groups, and the need for teacher training on new technologies are all important considerations.

## Looking Forward

As AI technology continues to evolve, we can expect to see even more innovative applications in education. The key will be finding the right balance between technological advancement and human interaction, ensuring that AI enhances rather than replaces the fundamental human elements of education.
EOF

echo "📝 Created sample article for testing"

# Install additional Python packages that might be useful
echo "🐍 Installing additional Python packages..."
pip install --quiet \
    streamlit-option-menu \
    plotly \
    pandas \
    numpy \
    matplotlib \
    seaborn

# Create a quick test script
cat > test_setup.py << 'EOF'
#!/usr/bin/env python3
"""Quick test script to verify the setup"""

import sys
import requests
import streamlit as st

def test_ollama_connection():
    """Test if Ollama is accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama is running with {len(models)} models available")
            for model in models:
                print(f"   - {model['name']}")
            return True
        else:
            print("❌ Ollama is not responding correctly")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to Ollama: {e}")
        return False

def test_python_packages():
    """Test if required packages are installed"""
    required_packages = [
        'streamlit', 'requests', 'transformers', 'torch', 
        'docx', 'PyPDF2', 'gradio'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'docx':
                __import__('docx')
            elif package == 'PyPDF2':
                __import__('PyPDF2')
            else:
                __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    return len(missing_packages) == 0

if __name__ == "__main__":
    print("🧪 Testing AI Summarizer Workshop setup...\n")
    
    print("Testing Python packages:")
    packages_ok = test_python_packages()
    
    print("\nTesting Ollama connection:")
    ollama_ok = test_ollama_connection()
    
    if packages_ok and ollama_ok:
        print("\n🎉 Setup is complete! All tests passed.")
        print("\n🚀 You can now run:")
        print("   streamlit run ai_summarizer_app.py")
        print("   streamlit run streamlit_enhanced.py --server.port 8502")
        print("   python gradio_version.py")
    else:
        print("\n⚠️  Some issues were found. Please check the logs above.")
        sys.exit(1)
EOF

chmod +x test_setup.py

# Run the test
echo "🧪 Running setup verification..."
python test_setup.py

# Create VS Code workspace settings
mkdir -p .vscode
cat > .vscode/settings.json << 'EOF'
{
    "python.defaultInterpreterPath": "/usr/local/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "terminal.integrated.defaultProfile.linux": "bash",
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,
    "terminal.integrated.env.linux": {
        "OLLAMA_HOST": "0.0.0.0:11434"
    }
}
EOF

# Create launch configuration for debugging
cat > .vscode/launch.json << 'EOF'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Basic Streamlit App",
            "type": "python",
            "request": "launch",
            "program": "/usr/local/bin/streamlit",
            "args": ["run", "ai_summarizer_app.py", "--server.port", "8501"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Run Enhanced Streamlit App",
            "type": "python",
            "request": "launch",
            "program": "/usr/local/bin/streamlit",
            "args": ["run", "streamlit_enhanced.py", "--server.port", "8502"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Run Gradio App",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/gradio_version.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
EOF

echo ""
echo "🎉 AI Summarizer Workshop setup complete!"
echo ""
echo "📖 Available applications:"
echo "   • Basic Streamlit App:    streamlit run ai_summarizer_app.py"
echo "   • Enhanced Streamlit App: streamlit run streamlit_enhanced.py --server.port 8502"
echo "   • Gradio Interface:       python gradio_version.py"
echo ""
echo "🔗 Ports forwarded:"
echo "   • 8501 - Basic Streamlit App"
echo "   • 8502 - Enhanced Streamlit App"  
echo "   • 7860 - Gradio Interface"
echo "   • 11434 - Ollama API (internal)"
echo ""
echo "💡 Tip: Use Ctrl+Shift+P in VS Code and search for 'Ports' to see forwarded URLs"
echo "🚀 Ready to start the workshop!"