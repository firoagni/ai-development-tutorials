# AI Development Tutorial Collection

This repository contains a comprehensive collection of Python-based tutorials for getting started with AI development. While primarily focused on Azure OpenAI, it also includes tutorials for other AI platforms like Ollama. 

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
4. **Environment Configuration**: Copy `.env.example` to `.env` and fill in your Azure OpenAI credentials:
   ```bash
   cp .env.example .env
   ```

## Tutorial Files

| # | Tutorial Files | Category | Purpose | Description |
|---|----------------|----------|---------|-------------|
| 1 | `1_ask_question_get_ans_rest_call.py`<br>`1_ask_question_get_ans_rest_call.ipynb` | Basic API Interaction | Ask a question and get an answer via REST API | Demonstrates how to interact with Azure OpenAI API using direct REST API calls. Shows the foundational approach to making HTTP requests to Azure OpenAI endpoints. |
| 2 | `2_ask_question_get_ans_azure_api.py`<br>`2_ask_question_get_ans_rest_azure_api.ipynb` | Basic API Interaction | Ask a question and get an answer via Azure OpenAI library | Uses the Azure OpenAI Python library instead of REST API to achieve the same functionality with a more convenient and Pythonic approach. |
| 3 | `3_conversational_chat.py`<br>`3_coversational_chat.ipynb` | Conversational AI | Conversational Chat with Azure OpenAI | Builds upon single question-answer interactions to create a conversational chatbot. The AI maintains context throughout the conversation. |
| 4 | `4_few_shot_prompting.py`<br>`4_few_shot_prompting.ipynb` | Advanced Prompting | Few-Shot Prompting | Demonstrates few-shot prompting technique where you show the model what you want through example conversations rather than just telling it. |
| 5 | `5_conversational_chat_with_token_limit_handling.py`<br>`5_coversational_chat_with_token_limit_handling.ipynb` | Conversational AI | Conversational Chat with Token Limit Handling | Addresses the challenge of growing conversation history consuming more tokens. Implements a token limit handling mechanism. |
| 6 | `6_reproducable_outputs.py`<br>`6_reproducable_outputs.ipynb` | Advanced Prompting | Reproducible Outputs | Explores how to obtain consistent, reproducible outputs using the `seed` parameter as a better solution than setting temperature to 0. |
| 7 | `7_chatbot_for_document.py`<br>`7_chatbot_for_document.ipynb` | Document-Based AI | Chatbot for a Document | Creates a chatbot that can answer questions based on a specific document rather than relying solely on the model's training data. |
| 8 | `8_function_calling.py`<br>`8_function_calling.ipynb` | Function Calling | Function Calling | Introduces function calling to overcome context size limitations. Shows how to define functions that fetch information from external sources. |
| 9 | `9_function_calling_chain_functions.py`<br>`9_function_calling_chain_functions.ipynb` | Function Calling | Function calling with function chaining | Extends function calling by demonstrating how to chain multiple function calls together to achieve complex results. |
| 10 | `10_structured_outputs.py`<br>`10_structured_outputs.ipynb` | Structured Output | Structured Outputs with JSON Schema | Demonstrates how to force models to generate responses in specific JSON formats using Pydantic schemas, including confidence scoring and validation techniques. |
| 11 | `11_code_interpreter_openai_reasoning_model.py`<br>`11_code_interpreter_openai_reasoning_model.ipynb` | Code Interpretation | Code Interpreter | Demonstrates using Azure OpenAI's Code Interpreter feature for mathematical calculations and data analysis using Python code execution. |
| 12 | `12_responses_api/*` | Modern API | Responses API Migration | Demonstrates the required for Responses API migration |
| 13 | `13_ollama/*` | Local AI | Ollama Integration | Examples of using Ollama for running AI models locally |
| 14 | `14_mcp/*` | Model Context Protocol | MCP Server Implementation | Demonstrates how to create MCP servers using FastMCP library |

## Supporting Files

- **`requirements.txt`**: Lists all Python dependencies needed for the tutorials
- **`.env.example`**: Template for environment variables configuration
- **`.gitignore`**: Prevents sensitive files and local development artifacts from being committed
- **`test_document.txt`**: Sample document used in document-based chatbot tutorials
- **`dummy_build_data.json`**: Sample data file used in code interpreter examples
- **`12_responses_api/`**: Folder containing tutorials for OpenAI's new Responses API with detailed migration guides
- **`13_ollama/`**: Folder containing tutorials for using Ollama for running AI models locally
- **`14_mcp/`**: Folder containing tutorials for explaining Model Context Protocol (MCP) servers and their implementation

## Learning Path

For the best learning experience, follow this structured learning path:

| Step | Focus Area | Tutorial Files | Key Concepts | Prerequisites |
|------|------------|----------------|--------------|---------------|
| 1 | **Basic API Interaction** | Tutorial 1-2 | REST API calls, Azure OpenAI Python library, basic chat completions | Python basics, Azure OpenAI account |
| 2 | **Single-Turn Conversations** | Tutorial 1-2 | Request/response patterns, API authentication, basic prompting | Step 1 completed |
| 3 | **Multi-Turn Conversations** | Tutorial 3 | Conversation history, context management, chatbot fundamentals | Step 2 completed |
| 4 | **Advanced Prompting** | Tutorial 4, 6 | Few-shot prompting, reproducible outputs, seed parameter | Step 3 completed |
| 5 | **Conversation Management** | Tutorial 5 | Token limits, conversation pruning, memory management | Step 3-4 completed |
| 6 | **Document-Based AI** | Tutorial 7 | Context injection, document-aware responses, domain-specific knowledge | Step 4 completed |
| 7 | **Function Calling Basics** | Tutorial 8 | External data access, function definitions, dynamic information retrieval | Step 6 completed |
| 8 | **Advanced Function Calling** | Tutorial 9 | Function chaining, multi-step reasoning, orchestrated API calls | Step 7 completed |
| 9 | **Structured Outputs** | Tutorial 10 | JSON schema response format, Pydantic models, confidence scoring | Step 8 completed |
| 10 | **Code Interpretation** | Tutorial 11 | Mathematical reasoning, data analysis, Python code execution | Step 9 completed |
| 11 | **Responses API Migration** | Tutorial 12 | Changes required for Responses API migration | Step 2 completed |
| 12 | **Local AI with Ollama** | Tutorial 13 | Running AI models locally, Ollama setup and usage | Step 2 completed |
| 13 | **Model Context Protocol** | Tutorial 14 | Creating MCP servers, exposing functions to AI systems, FastMCP usage | Step 2 and 7 and 8 completed |

### Quick Start Path
If you're already familiar with APIs and want to focus on Azure OpenAI specifics:
- **Express Path**: Tutorials 2 → 3 → 8 → 9 → 10 → 11  (Core concepts only)
- **Full Path**: Follow steps 1-11 for comprehensive understanding

### Migration Path
- Tutorial 12 provides direct comparison and migration guide from Chat Completions to Responses API

### MCP Development Path
- Tutorial 14 demonstrates how to create MCP servers that expose your functions to AI systems

## Getting Help

Each tutorial file contains detailed comments explaining the concepts and implementation. The Jupyter notebook versions provide an interactive learning experience with explanations and outputs.

For Azure OpenAI documentation, visit: [Microsoft Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
