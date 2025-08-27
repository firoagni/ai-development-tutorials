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
## Tutorial Files

| # | Tutorial Files | Category | Purpose | Description |
|---|----------------|----------|---------|-------------|
| 1 | `01_ask_question_get_ans_ollama.py`<br>`01_ask_question_get_ans_ollama.ipynb` | Basic Integration | Basic Question Answering | Demonstrates how to interact with Ollama for basic question-answering using locally running models |
| 2 | `02_conversational_chat_ollama.py`<br>`02_conversational_chat_ollama.ipynb` | Chat | Conversational Chat | Shows how to create multi-turn conversations using locally running Ollama models |
| 3 | `03_few_shot_prompting_ollama.py`<br>`03_few_shot_prompting_ollama.ipynb` | Advanced Prompting | Few-Shot Prompting | Implements few-shot prompting techniques with locally running models |
| 4 | `04_thinking_model_ollama.py`<br>`04_thinking_model_ollama.ipynb` | Advanced Reasoning | Thinking Model | Demonstrates how to implement thinking patterns and reasoning with Ollama models |
| 5 | `05_streaming_ollama.py`<br>`05_streaming_ollama.ipynb` | Real-time Processing | Streaming | Shows how to implement streaming responses with Ollama for real-time output |
| 6 | `06_thinking_levels_ollama.py`<br>`06_thinking_levels_ollama.ipynb` | Advanced Reasoning | Multi-level Thinking | Explores different levels of thinking and reasoning capabilities with Ollama models |
| 7 | `07_structured_outputs_ollama.py`<br>`07_structured_outputs_ollama.ipynb` | Output Control | Structured Outputs | Demonstrates how to get structured JSON outputs from Ollama models |
| 8 | `08_function_calling_ollama.py`<br>`08_function_calling_ollama.ipynb` | Integration | Function Calling | Shows how to implement function calling capabilities with local models |
| 9 | `09_remote_ollama.py`<br>`09_remote_ollama.ipynb` | Remote Access | Remote Integration | Demonstrates how to connect to and use remote Ollama instances |

## References
- [Ollama Python GitHub Repository](https://github.com/ollama/ollama-python)