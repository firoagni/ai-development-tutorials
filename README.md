# AI Development Tutorial Collection

This repository contains a comprehensive collection of Python-based tutorials for getting started with AI development. While primarily focused on Azure OpenAI, it also includes tutorials for other AI platforms like Ollama and Model Context Protocol (MCP) implementations.

Each tutorial builds upon the previous ones, demonstrating progressively advanced concepts and techniques.

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

| # | Tutorial Files | Category | Purpose | Description |
|---|----------------|----------|---------|-------------|
| 1 | `01_ask_question_get_ans_azure_api.py`<br>`01_ask_question_get_ans_azure_api.ipynb` | Basic API Interaction | Ask a question and get an answer via Azure OpenAI library | Uses the Azure OpenAI Python library to demonstrate basic question-answer interactions. |
| 2 | `02_message_roles.py`<br>`02_message_roles.ipynb` | API Understanding | Understanding Message Roles and Input Formats | Explains the different ways to send input to Azure OpenAI models, and the various message roles (developer, user, assistant). |
| 3 | `03_conversational_chat.py`<br>`03_coversational_chat.ipynb` | Conversational AI | Conversational Chat with Azure OpenAI | Builds upon single question-answer interactions to create a conversational chatbot. The AI maintains context throughout the conversation using message history. |
| 4 | `04_conversational_chat_with_token_limit_handling.py`<br>`04_coversational_chat_with_token_limit_handling.ipynb` | Conversational AI | Conversational Chat with Token Limit Handling | Addresses the challenge of growing conversation history consuming more tokens. Implements smart token limit handling and conversation pruning mechanisms. |
| 5 | `05_server_side_conversation_management.py`<br>`05_server_side_conversation_management.ipynb` | Conversational AI | Server-Side Conversation Management | Demonstrates how to manage conversations on the server side |

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

### Model Context Protocol (`14_mcp/`)
Tutorials for implementing MCP servers and integrating with AI systems:

| # | Tutorial Files | Purpose | Description |
|---|----------------|---------|-------------|
| 1 | `01_local-mcp-server-fastmcp.py` | Local MCP Server | Creating a local MCP server using FastMCP library |
| 2 | `02_http-mcp-server-fastmcp.py` | HTTP MCP Server | Implementing an HTTP-based MCP server for remote access |
| 3 | `03_run_with_docker.md` | Docker Deployment | Guide for running MCP servers in Docker containers |

## Supporting Files

- **`requirements.txt`**: Lists all Python dependencies needed for the tutorials
- **`.env.dummy`**: Template for environment variables configuration (rename to `.env` and fill with your credentials)
- **`.gitignore`**: Prevents sensitive files and local development artifacts from being committed
- **`test_document.txt`**: Sample document used in document-based chatbot tutorials
- **`dummy_build_data.json`**: Sample data file used in code interpreter examples
- **`ai_solution_building_guide.md`**: Comprehensive guide on building AI solutions, covering workflows vs. agents, design patterns, and best practices
- **`images/`**: Folder containing diagrams and screenshots used in documentation
- **`13_ollama/`**: Complete tutorial series for using Ollama to run AI models locally
- **`14_mcp/`**: Tutorials and examples for implementing Model Context Protocol servers

## Learning Path

For the best learning experience, follow this structured learning path:

| Step | Focus Area | Tutorial Files | Key Concepts | Prerequisites |
|------|------------|----------------|--------------|---------------|
| 1 | **Basic API Interaction** | Tutorial 1 | Azure OpenAI Python library, basic chat completions, API authentication | Python basics, Azure OpenAI basics |
| 2 | **Understanding Message Formats** | Tutorial 2 | Message roles | Step 1 completed |
| 3 | **Multi-Turn Conversations** | Tutorial 3 | Conversation history, context management, chatbot fundamentals | Step 2 completed |
| 4 | **Conversation Management** | Tutorial 4-5 | Token limits, conversation pruning, server-side management | Step 3 completed |
| 5 | **Advanced Prompting** | Tutorial 6-7 | Few-shot prompting, reproducible outputs, seed parameter | Step 3 completed |
| 6 | **Local AI with Ollama** | Tutorial 13 | Running models locally, Ollama setup, streaming, function calling | Step 2 completed |
| 7 | **Model Context Protocol** | Tutorial 14 | Creating MCP servers, exposing functions to AI systems, FastMCP usage | Step 2 completed |

## Additional Resources

### Architecture and Design Guidance
The `ai_solution_building_guide.md` provides comprehensive guidance on:
- **Workflows vs. Agents**: When to use structured workflows versus autonomous agents
- **Design Patterns**: Best practices for building reliable AI systems  
- **Function Calling**: How to extend AI capabilities with external tools
- **RAG (Retrieval Augmented Generation)**: Implementing document-based AI systems
- **Context Management**: Strategies for handling long conversations and large contexts

### Platform-Specific Features
- **Azure OpenAI**: All core tutorials (01-07) demonstrate Azure OpenAI integration with proper authentication and configuration
- **Ollama**: Local AI development with privacy and control (13_ollama/ series)
- **Model Context Protocol**: Building extensible AI systems that can integrate with various tools and services (14_mcp/ series)

## Getting Help

Each tutorial file contains detailed comments explaining the concepts and implementation. The Jupyter notebook versions provide an interactive learning experience with explanations and outputs.

### Repository Structure
```
azure-open-ai/
├── Core Azure OpenAI Tutorials (01-07)
├── 13_ollama/          # Local AI development
├── 14_mcp/             # Model Context Protocol
├── ai_solution_building_guide.md  # Architecture guide
├── images/             # Documentation assets  
├── requirements.txt    # Dependencies
└── .env.dummy         # Configuration template
```
