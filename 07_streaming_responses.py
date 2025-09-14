# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Ask a question and get an answer from a thinking Model
# https://platform.openai.com/docs/guides/streaming-responses?api-mode=responses
#
# Problem Statement:
# By default, when you make a request to a Model, entire output is 
# first generated and then sent. When generating long outputs, 
# waiting for a response can take time. 
# 
# Solution:
# Streaming responses lets you start printing the model's output 
# while it continues generating the full response.
#
# This allows for a more interactive experience, as you can start seeing the output
# before the entire response is complete.

# To generate streaming responses, set `stream=True` in your request

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
load_dotenv()

AZURE_OPENAI_ENDPOINT        = os.environ['AZURE_OPENAI_ENDPOINT']
AZURE_OPENAI_MODEL           = os.environ['AZURE_OPENAI_MODEL']
AZURE_OPENAI_API_VERSION     = os.environ['AZURE_OPENAI_VERSION']
AZURE_OPENAI_API_KEY         = os.environ['AZURE_OPENAI_API_KEY']

# --------------------------------------------------------------
# Create an instance of the AzureOpenAI client
# --------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = AZURE_OPENAI_API_VERSION
)

# ---------------------------------------------------------------
# Set the behavior or personality of the assistant using the "developer" role.
# ----------------------------------------------------------------
conversation=[{"role": "developer", "content": "You are a sarcastic AI assistant. You are proud of your amazing memory"}]

# --------------------------------------------------------------
# Start a loop to keep the conversation going
# --------------------------------------------------------------
while True:
    question = input("Enter your question (type 'exit' to quit): ").strip()

    # Exit the loop if user types 'exit'
    if question.lower() == 'exit':
        print("Goodbye!")
        break

    conversation.append({"role": "user", "content": question})

    try:
        response = client.responses.create(
            model= AZURE_OPENAI_MODEL,
            stream=True, # Enable streaming to get streaming responses
            input=conversation,
            temperature=0.7,
            max_output_tokens=1000
        )

        # --------------------------------------------------------------
        # Print the chunks as they come in
        # --------------------------------------------------------------
        # When streaming is enabled, the response comes in chunks with different types:
        # - `response.created`: LLM has started responding
        # - `response.output_text.delta`: LLM is sending response in chunks (this is where we get the actual text)
        # - `response.completed`: LLM has finished responding (contains the complete response)
        # - `response.error`: An error occurred during generation
        # 
        # The key advantage is that we can start displaying text to the user immediately as `response.output_text.delta` 
        # chunks arrive, rather than waiting for the entire response to be generated.
        # --------------------------------------------------------------
        for chunk in response:
            if chunk.type == 'response.created': # LLM has started responding
                print("Answer from LLM:")
            elif chunk.type == 'response.output_text.delta': # LLM is sending response in chunks. Keep printing them as they come in
                partial_llm_response = chunk.delta
                print(partial_llm_response, end='', flush=True)
            elif chunk.type == 'response.completed': # LLM has finished responding, add the complete response to the conversation history
                complete_llm_response = chunk.response.output[0].content[0].text
                conversation.append({"role": "assistant", "content": complete_llm_response})
            elif chunk.type == 'response.error': # Error occurred
                print(f"\nError from LLM: {chunk.error.message}")
                break
        print() # Print a new line after the response is complete
        print("=" * 80)

    except Exception as e:
        print(f"\nError getting answer from LLM: {e}")
        continue
