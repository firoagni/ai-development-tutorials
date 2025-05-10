
# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Ask Questions and Get Answers via Azure OpenAI library
#
# In the previous example, we used the REST API to interact with Azure OpenAI.
# In this example, we will use the Azure OpenAI library to achieve the same functionality.
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
from openai import AzureOpenAI  # The `AzureOpenAI` library is used to interact with the Azure OpenAI API.
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
# Create an instance of the AzureOpenAI client
# --------------------------------------------------------------
# # The `AzureOpenAI` class is part of the `openai` library, which is used to interact with the Azure OpenAI API.
# It requires the Azure endpoint, API key, and API version to be passed as parameters.
# ---------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = AZURE_OPENAI_API_VERSION
)

# --------------------------------------------------------------
# Wrap the question to Azure OpenAI API payload
# --------------------------------------------------------------
# 
# The "model" parameter specifies the model to be used for the request.
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
try:
    response = client.chat.completions.create(
        model= AZURE_OPENAI_MODEL, 
        messages=[
            {"role": "system", "content": "You are a super sarcastic AI assistant"},
            {"role": "user", "content": question}
        ],
        temperature=0.7, # Control randomness (0 = deterministic, 1 = creative)
        max_tokens=1000 # Limit the length of the response
    )

# Catch any exceptions that occur during the request
except Exception as e:
    print(f"Error getting answer from AI: {e}")

# --------------------------------------------------------------
# Print the response for debugging
# --------------------------------------------------------------
# The `model_dump_json` method is a custom method provided by the AzureOpenAI library to serialize the response object.
# No need to use json.dumps() to convert to a string, as `model_dump_json` already does that.
# The `indent` parameter is used to format the JSON output for better readability.
# ---------------------------------------------------------------
print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")

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
answer = response.choices[0].message.content
print(answer)