# AI Development Tutorial Collection

This repository contains a comprehensive collection of Python-based tutorials for getting started with AI development. While primarily focused on Azure OpenAI, it also includes tutorials for other AI platforms like Ollama and Model Context Protocol (MCP) implementations.

Each tutorial builds upon the previous ones, demonstrating progressively advanced concepts and techniques.

## Before You Start

Before diving into the tutorials, we strongly recommend reading these two foundational documents in order:

1. **`LLMs_explained.md`**: A comprehensive guide that explains how Large Language Models work, covering essential concepts like tokens, embeddings, and the transformer architecture. This will give you a solid understanding of the technology you'll be working with.

2. **`ai_solution_building_guide.md`**: A practical guide that covers key architectural patterns and best practices for building AI solutions, including:
   - Workflows vs. Agents: Understanding the trade-offs and when to use each approach
   - Fundamentals of Building Your Own Agent
   - Model Context Protocol (MCP)
   - Importance of Context engineering
   - Retrieval-Augmented Generation (RAG) techniques
   - Safety considerations for AI systems
   - Understanding Context window, Context rot and positional bias in LLMs
   - How AI Coding Assistants Work
   - AI Solutions: Where to Use and When Not To

These documents will provide you with the theoretical foundation and architectural understanding needed to make the most of the tutorials.

## Prerequisites

1. **Python 3**: Make sure Python 3 is installed on your system
2. **Virtual Environment**: Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Dependencies**: Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Configuration**: Copy `.env.dummy` to `.env` and fill in your Azure OpenAI credentials:
   ```bash
   cp .env.dummy .env
   ```

## Core Tutorial Files

| # | Tutorial Files | Purpose | Description |
|---|----------------|---------|-------------|
| 1 | `01_ask_question_get_ans_azure_api.py`<br>`01_ask_question_get_ans_azure_api.ipynb` | Ask a question and get an answer via Azure OpenAI library | Uses the Azure OpenAI Python library to demonstrate basic question-answer interactions. |
| 2 | `02_message_roles.py`<br>`02_message_roles.ipynb` | Understanding Message Roles and Input Formats | Explains the different ways to send input to Azure OpenAI models, and the various message roles (developer, user, assistant). |
| 3 | `03_conversational_chat.py`<br>`03_coversational_chat.ipynb` | Conversational Chat with Azure OpenAI | Builds upon single question-answer interactions to create a conversational chatbot. The AI maintains context throughout the conversation using message history. |
| 4 | `04_conversational_chat_with_token_limit_handling.py`<br>`04_coversational_chat_with_token_limit_handling.ipynb` | Conversational Chat with Token Limit Handling | Addresses the challenge of growing conversation history consuming more tokens. Implements smart token limit handling and conversation pruning mechanisms. |
| 5 | `05_server_side_conversation_management.py`<br>`05_server_side_conversation_management.ipynb` | Server-Side Conversation Management | Demonstrates how to manage conversations on the server side |
| 6 | `06_few_shot_prompting.py`<br>`06_few_shot_prompting.ipynb` | Few-Shot Prompting | Demonstrates few-shot prompting technique |
| 7 | `07_streaming_responses.py`<br>`07_streaming_responses.ipynb` | Streaming Responses | Learn how to provide immediate feedback to users as the AI generates responses. |
| 8 | `08_chatbot_for_document.py`<br>`08_chatbot_for_document.ipynb` | Chatbot for Document | Implements a chatbot that can answer questions by referencing a specific document |
| 9 | `09_structured_outputs.py`<br>`09_structured_outputs.ipynb` | Structured Outputs | Shows how to generate structured JSON outputs from AI models |
| 10 | `10_function_calling.py`<br>`10_function_calling.ipynb` | Function Calling | Demonstrates how to extend AI capabilities by allowing models to call external functions |
| 11 | `11_code_interpreter.py`<br>`11_code_interpreter.ipynb` | Code Interpreter | Direct LLMs to write python scripts to solve mathematical and statistical problems and accurately perform data analysis|

## Extended Platforms and Implementations

### Ollama Integration (`13_ollama/`)
Complete tutorial series for running AI models locally using Ollama:

| # | Tutorial Files | Purpose | Description |
|---|----------------|---------|-------------|
| 1 | `01_ask_question_get_ans_ollama.*` | Basic Ollama Usage | Getting started with Ollama for local AI model execution |
| 2 | `02_conversational_chat_ollama.*` | Conversational AI | Building chatbots with locally running Ollama models |
| 3 | `03_few_shot_prompting_ollama.*` | Advanced Prompting | Few-shot prompting techniques with Ollama |
| 4 | `04_thinking_model_ollama.*` | Advanced Reasoning | Using thinking/reasoning models with Ollama |
| 5 | `05_streaming_ollama.*` | Real-time Responses | Implementing streaming responses with Ollama |
| 6 | `06_thinking_levels_ollama.*` | Advanced Reasoning | Different levels of thinking and reasoning with Ollama models |
| 7 | `07_structured_outputs_ollama.*` | Structured Output | Generating structured JSON outputs with Ollama |
| 8 | `08_function_calling_ollama.*` | Function Calling | Implementing function calling capabilities with Ollama |
| 9 | `09_remote_ollama.*` | Remote Access | Connecting to and using remote Ollama instances |

### Model Context Protocol (`12_mcp/`)
Tutorials for implementing MCP servers and integrating with AI systems:

| # | Tutorial Files | Purpose | Description |
|---|----------------|---------|-------------|
| 1 | `01_local-mcp-server-fastmcp.py` | Local MCP Server | Creating a local MCP server using FastMCP library |
| 2 | `02_http-mcp-server-fastmcp.py` | HTTP MCP Server | Implementing an HTTP-based MCP server for remote access |
| 3 | `03_run_with_docker.md` | Docker Deployment | Guide for running MCP servers in Docker containers |

## Supporting Files

### Core Documentation
- **`LLMs_explained.md`**: Essential reading that provides a deep dive into how Large Language Models work, including:
  - Tokens and embeddings
  - Transformer architecture
  - Training and fine-tuning processes
  - Model behavior and limitations

- **`ai_solution_building_guide.md`**: Must-read guide for designing AI solutions, covering:
  - Workflows vs Agents: Deep dive into architecture patterns and hybrid approaches
  - Function calling, tools, and safety considerations
  - Context engineering and window management best practices
  - Code-RAG techniques for efficient codebase searching
  - Model Context Protocol (MCP) implementation and challenges
  - Guardrails and safety considerations for AI systems
  - Understanding context rot and positional bias in LLMs
  - Strategic approaches for AI coding assistants

### Project Files
- **`requirements.txt`**: Lists all Python dependencies needed for the tutorials
- **`.env.dummy`**: Template for environment variables configuration (rename to `.env` and fill with your credentials)
- **`.gitignore`**: Prevents sensitive files and local development artifacts from being committed
- **`test_document.txt`**: Sample document used in document-based chatbot tutorials
- **`dummy_build_data.json`**: Sample data file used in code interpreter examples
- **`images/`**: Folder containing diagrams and screenshots used in documentation
- **`13_ollama/`**: Complete tutorial series for using Ollama to run AI models locally
- **`12_mcp/`**: Tutorials and examples for implementing Model Context Protocol servers

## Additional Resources

### Foundational Knowledge
- **Understanding LLMs** (`LLMs_explained.md`): Master the fundamentals of how Large Language Models work, from tokenization to transformer architecture. This knowledge is crucial for making informed decisions about model selection and implementation.

### Architecture and Design Guidance
- **Building AI Solutions** (`ai_solution_building_guide.md`): Learn proven patterns and practices for creating reliable AI systems:
  - **Workflows vs. Agents**: Choose the right architecture for your use case
  - **Design Patterns**: Industry-tested patterns for building reliable AI systems
  - **Function Calling**: Extend AI capabilities through tool integration
  - **Context Engineering**: Master the art of providing the right context
  - **MCP Integration**: Implement standardized tool communication

### Platform-Specific Features
- **Azure OpenAI**: All core tutorials (01-10) demonstrate Azure OpenAI integration with proper authentication and configuration
- **Ollama**: Local AI development with privacy and control (13_ollama/ series)
- **Model Context Protocol**: Building extensible AI systems that can integrate with various tools and services (12_mcp/ series)

## Getting Help

Each tutorial file contains detailed comments explaining the concepts and implementation. The Jupyter notebook versions provide an interactive learning experience with explanations and outputs.

### Repository Structure
```
azure-open-ai/
├── Core Azure OpenAI Tutorials (01-11)
│   ├── 01_ask_question_get_ans_azure_api.*
│   ├── 02_message_roles.*
│   ├── 03_conversational_chat.*
│   ├── 04_conversational_chat_with_token_limit_handling.*
│   ├── 05_server_side_conversation_management.*
│   ├── 06_few_shot_prompting.*
│   ├── 07_streaming_responses.*
│   ├── 08_chatbot_for_document.*
│   ├── 09_structured_outputs.*
│   ├── 10_function_calling.*
│   └── 11_code_interpreter.*
├── 12_mcp/             # Model Context Protocol
│   ├── 01_local-mcp-server-fastmcp.py
│   ├── 02_http-mcp-server-fastmcp.py
│   ├── 03_run_with_docker.md
│   ├── Dockerfile
│   ├── README.md
│   ├── requirements.txt
│   └── screenshots/
├── 13_ollama/          # Local AI development with Ollama
│   ├── 01_ask_question_get_ans_ollama.*
│   ├── 02_conversational_chat_ollama.*
│   ├── 03_few_shot_prompting_ollama.*
│   ├── 04_thinking_model_ollama.*
│   ├── 05_streaming_ollama.*
│   ├── 06_thinking_levels_ollama.*
│   ├── 07_structured_outputs_ollama.*
│   ├── 08_function_calling_ollama.*
│   ├── 09_remote_ollama.*
│   ├── README.md
│   └── requirements.txt
├── images/             # Documentation assets and diagrams
├── ai_solution_building_guide.md  # Architecture and design guide
├── requirements.txt    # Main dependencies
├── test_document.txt   # Sample document for tutorials
├── dummy_build_data.json  # Sample data for examples
└── .env.dummy         # Configuration template
```
