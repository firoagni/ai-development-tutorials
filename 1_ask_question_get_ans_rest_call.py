
# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Ask Questions and Get Answers from Azure OpenAI via REST API
#
# This script demonstrates how to interact with the Azure OpenAI API via REST API.
# ---------------------------------------------------------------

# --------------------------------------------------------------
# Prerequisites
# 1. Make sure that python3 is installed on your system.
# 2. Create and Activate a Virtual Environment:
# `python3 -m venv venv`
# `source venv/bin/activate`
# 3. The required libraries are listed in the requirements.txt file. Use the following command to install them:
#    `pip3 install -r requirements.txt`
# 4. Create a `.env` file in the same directory as this script and add the following variables:
#    AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint>
#    AZURE_OPENAI_MODEL=<your_azure_openai_model>
#    AZURE_OPENAI_API_VERSION=<your_azure_openai_api_version>
#    AZURE_OPENAI_API_KEY=<your_azure_openai_api_key>
#---------------------------------------------------------------
# --------------------------------------------------------------
# Import Modules
# --------------------------------------------------------------
import requests                 # The `requests` library is used to send HTTP requests in Python.
import json                     # The `json` library is used to work with JSON data in Python.
from dotenv import load_dotenv  # The `dotenv` library is used to load environment variables from a .env file.
import os                       # Used to get the values from environment variables.

# --------------------------------------------------------------
# Load environment variables from .env file
# --------------------------------------------------------------
# The `load_dotenv()` function reads the .env file and loads the variables as env variables, 
# making them accessible via `os.environ` or `os.getenv()`.
# --------------------------------------------------------------
load_dotenv()

AZURE_OPENAI_ENDPOINT        = os.environ['AZURE_OPENAI_ENDPOINT']
AZURE_OPENAI_MODEL           = os.environ['AZURE_OPENAI_MODEL']
AZURE_OPENAI_API_VERSION     = os.environ['AZURE_OPENAI_VERSION']
AZURE_OPENAI_API_KEY         = os.environ['AZURE_OPENAI_API_KEY']

# --------------------------------------------------------------
# Difference between os.environ[] and os.getenv()
# os.environ[] raises an exception if the variable is not found
# os.getenv() does not raise an exception, but returns None
# --------------------------------------------------------------

# --------------------------------------------------------------
# Prompt user for question
# --------------------------------------------------------------
question = input("Enter your question: ").strip()

# --------------------------------------------------------------
# Wrap the question to Azure OpenAI API payload
# --------------------------------------------------------------
# The "messages" array defines the conversation history for the AI model.
#
# Each message includes a "role" and "content".
# - "role" specifies the role in the conversation:
#   - "system": Sets the behavior or personality of the assistant. The first message in the "messages" array
#   - "user": Provides the user's input to the model
#   - "assistant": Represents the AI's response (used in conversations, check later examples).
#
# Additional parameters like "temperature" and "max_tokens" control the 
# response's creativity and length, respectively.
#
# Documentation: 
# https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chatgpt
# https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#chat-completions
# --------------------------------------------------------------
payload = {
    "messages": [
        {"role": "system", "content": "You are a super sarcastic AI assistant"},
        {"role": "user", "content": question}
    ],
    "temperature": 0.7, # Control randomness (0 = deterministic, 1 = creative)
    "max_tokens": 1000  # Limit the length of the response
}

# --------------------------------------------------------------
# Form the URL to POST the payload to Azure OpenAI
# --------------------------------------------------------------
#
# URI Parameters in Azure OpenAI API URL:
# https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#uri-parameters-2
#---------------------------------------------------------------
url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_MODEL}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"

# --------------------------------------------------------------
# Set headers for Azure OpenAI API
# --------------------------------------------------------------
# Important to note is that the api-key will go in the message header.
# Documentation: https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#request-header-2
# --------------------------------------------------------------
headers = {
    "Content-Type": "application/json",
    "api-key": os.environ['AZURE_OPENAI_API_KEY'] # API key for authentication
}

# --------------------------------------------------------------
# Send the request to Azure OpenAI API and collect the response
# --------------------------------------------------------------
# The `requests` library is used to send HTTP requests in Python.
# The `post()` method of `requests` library sends a POST request to the specified URL with the given headers and payload.
# ---------------------------------------------------------------
try:
    response = requests.post(url, headers=headers, json=payload)
    
    # Check for errors in the response
    if response.status_code != 200:
        raise Exception(f"Error from Azure OpenAI API: {response.status_code} - {response.text}")

# Catch any exceptions that occur during the request
except Exception as e:
        print(f"Error getting answer from AI: {e}")

# --------------------------------------------------------------
# Parse the response to JSON
# --------------------------------------------------------------
# The `json()` method parses the JSON response into a Python dictionary.
# ---------------------------------------------------------------
result = response.json()

# --------------------------------------------------------------
# Print the response for debugging
# --------------------------------------------------------------
# The `json.dumps()` method converts a Python object into a JSON string.
# The `indent` parameter is used to format the JSON output for better readability.
# ---------------------------------------------------------------
print(f"DEBUG:: Complete response from LLM:\n{json.dumps(result, indent=4)}")

# --------------------------------------------------------------
# prompt token and completion tokens
# "prompt tokens" refer to the input text fed into the model, including any instructions or context provided to the model.  
# "completion tokens" represent the output generated by the model in response to that prompt. Control via "max_tokens"
#
# The maximum number of tokens a model can process (both prompt and completion) is defined by its "context window"
# The cost of using Azure OpenAI is typically based on the number of tokens used, both prompt and completion. 
# ---------------------------------------------------------------

# --------------------------------------------------------------
# Extract answer and print it
# --------------------------------------------------------------
print("\nAnswer from AI:")
answer = result['choices'][0]['message']['content']
print(answer)