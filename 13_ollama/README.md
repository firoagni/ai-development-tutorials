# Why Ollama?

Want to leverage local LLMs in your project? The simplest solution is Ollama - a powerful, open-source platform that allows you to run Large Language Models (LLMs) locally on your computer. It provides a straightforward way to download, run, and interact with various open-source models without requiring complex setup or cloud dependencies.

## Key Benefits

- **Local Execution**: Run models completely offline on your machine
- **Free and Open Source**: No usage costs or API fees
- **Easy Setup**: Simple installation and model management

## Installation

The installation process involves three simple steps:

1. **Install Ollama**
   - Visit [https://ollama.com/download](https://ollama.com/download) and follow instructions for your operating system

2. **Pull Your First Model**
   ```bash
   ollama pull llama3.2
   ```

3. **Start Using the Model**
   ```bash
   ollama run llama3.2
   ```

This will start an interactive chat session where you can begin conversing with the model.

## Using Ollama with Python

Ollama provides a Python client that mirrors OpenAI's API structure. Here's a basic example:

### Prerequisites

- [Ollama](https://ollama.com/download) should be installed and running
- Pull a model to use with the library: `ollama pull <model>` e.g. `ollama pull gemma3`
  - See [Ollama.com](https://ollama.com/search) for more information on the models available.

### Install

```sh
pip install ollama
```

## Usage

```python
from ollama import chat

response = = chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response.message.content)
```

## References
- [Ollama Python GitHub Repository](https://github.com/ollama/ollama-python)