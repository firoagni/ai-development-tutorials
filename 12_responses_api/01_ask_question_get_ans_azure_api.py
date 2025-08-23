# --------------------------------------------------------------
# Azure OpenAI - Responses API: Ask a Question and Get an answer 
#
# Want to switch from Chat Completions API to Responses API?
#
# In this example, we will demonstrate what changes you need
# to generate output from OpenAI models if you switch to Responses API
#
# Major changes:
#
# 1. The API endpoint has changed from `chat.completions` to `responses`.
# 2. `chat.completion.create` requires a `messages` array, while `responses` requires an `input`.
#     `input` can be a string or array of strings.
# 3. The `max_tokens` key in `chat.completions.create` is `max_output_tokens` in `responses.create`.
# 4. The answer from LLM can now be accessed directly from the response object's `output_text` attribute

# --------------------------------------------------------------
# Prerequisites <<NO CHANGES>>
# 1. Make sure that python3 is installed on your system.
# 2. Create and Activate a Virtual Environment:
# `python3 -m venv venv`
# `source venv/bin/activate`
# 3. The required libraries are listed in the requirements.txt file. Use the following command to install them:
#    `pip3 install -r ../requirements.txt`
# 4. Create a `.env` file in the parent directory and add the following variables:
#    AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint>
#    AZURE_OPENAI_MODEL=<your_azure_openai_model>
#    AZURE_OPENAI_API_VERSION=<your_azure_openai_api_version>
#    AZURE_OPENAI_API_KEY=<your_azure_openai_api_key>
#---------------------------------------------------------------

# --------------------------------------------------------------
# Import Modules <<NO CHANGES>>
# --------------------------------------------------------------
from openai import AzureOpenAI  # The `AzureOpenAI` library is used to interact with the Azure OpenAI API.
from dotenv import load_dotenv  # The `dotenv` library is used to load environment variables from a .env file.
import os                       # Used to get the values from environment variables.

# --------------------------------------------------------------
# Load environment variables from .env file <<NO CHANGES>>
# --------------------------------------------------------------
load_dotenv("../.env")

AZURE_OPENAI_ENDPOINT        = os.environ['AZURE_OPENAI_ENDPOINT']
AZURE_OPENAI_MODEL           = os.environ['AZURE_OPENAI_MODEL']
AZURE_OPENAI_API_VERSION     = os.environ['AZURE_OPENAI_VERSION']
AZURE_OPENAI_API_KEY         = os.environ['AZURE_OPENAI_API_KEY']

# --------------------------------------------------------------
# Create an instance of the AzureOpenAI client <<NO CHANGES>>
# --------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = AZURE_OPENAI_API_VERSION
)

# --------------------------------------------------------------
# Define system prompt and user question
# and other parameters
# --------------------------------------------------------------
system_prompt = "You are a super sarcastic AI assistant"
question = input("Enter your question: ").strip()
temperature = 0.7
max_tokens = 1000
# --------------------------------------------------------------

# --------------------------------------------------------------
# Steps to pass the question to the Model 
# via Chat Completion API
# --------------------------------------------------------------
print("=" * 80)
print(f"Response from Chat Completions API:")
print("=" * 80)
try:
    response = client.chat.completions.create(
        model= AZURE_OPENAI_MODEL, 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

# Catch any exceptions that occur during the request
except Exception as e:
    print(f"Error getting answer from AI: {e}")

print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")
print(f"Answer from LLM: {response.choices[0].message.content}")

# --------------------------------------------------------------
# Steps to pass the same question to the Model 
# via the new Responses API
# --------------------------------------------------------------
print("=" * 80)
print(f"Response from Responses API:")
print("=" * 80)
try:
    response = client.responses.create( # Endpoint has changed from `chat.completions.create` to `responses.create`
        model= AZURE_OPENAI_MODEL,      # <<NO CHANGE>>
        instructions=system_prompt,     # Responses API contains a separate parameter to pass system prompt
        input=question,                 # `chat.completion.create` requires a `messages` array, while `responses` requires an `input` instead. 
        temperature=temperature,        # <<NO CHANGE>>
        max_output_tokens=max_tokens    # The key max_tokens in `chat.completions.create` is `max_output_tokens` in `responses.create`
    )

# Catch any exceptions that occur during the request <<NO CHANGE>>
except Exception as e:
    print(f"Error getting answer from AI: {e}")

print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")
# Answer from LLM can now be accessed directly from the response object's `output_text` attribute
# Much more elegant than before's `response.choices[0].message.content`
print(f"Answer from LLM: {response.output_text}")

# --------------------------------------------------------------
# Response API's `input` can accept 
# chat completion style message array too
# --------------------------------------------------------------
print("=" * 80)
print(f"Response from Responses API for chat completion style message array:")
print("=" * 80)
try:
    response = client.responses.create( 
        model= AZURE_OPENAI_MODEL,      
        input=[ # input can also accept chat completion style message array
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=temperature,
        max_output_tokens=max_tokens
    )

# Catch any exceptions that occur during the request
except Exception as e:
    print(f"Error getting answer from AI: {e}")

print(f"Answer from LLM: {response.output_text}")

