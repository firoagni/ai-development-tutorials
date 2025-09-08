
# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Message Roles
#
# The Responses API of Azure OpenAI lets you send input to a model in two ways:
#
# Option 1: Send a single Message
#    - Just pass a single piece of text (e.g., "Hi, how are you?")
#    - Best for simple, one-time questions.
#    - Any special instructions for the AI go in the `instructions` parameter.
#
# Option 2: Send an Array of Messages
#    - Pass a list of messages as `input`
#
# Example:
#
# response = client.responses.create(
#     model=AZURE_OPENAI_MODEL,
#     instructions="You are a sarcastic AI assistant",
#     input="Hi, how are you?"
# )
#
# is effectively the same as:
#
# response = client.responses.create(
#     model=AZURE_OPENAI_MODEL,
#     input=[
#         {"role": "developer", "content": "You are a sarcastic AI assistant"},
#         {"role": "user", "content": "Hi, how are you?"}
#     ]
# )
#
# Q. I see `role` and `content` in the array example. What are they?
# A. When you pass an array of messages to `input`, Responses API requires that each message must include a `role` and `content`
# - role: who is speaking
# - content: the actual text
#
# Available Roles:
#   - `developer`: instructions from the app creator (like telling the AI how to behave)
#   - `user`: the input/question for the model
#   - `assistant`: the model's response
#
# - In the previous example, we used the `instructions` parameter to pass the app developer's 
#   instruction ("You are a sarcastic AI assistant") and sent a single message to the llm.
# - In this example, we will pass the same instruction and a single user message, but using the `input` array format.
#
# You might be wondering why there are two different approaches?
# Hang tight - this will all make sense in the next tutorial.
# --------------------------------------------------------------

# ---------------------------------------------------------------
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
# Prompt user for question
# --------------------------------------------------------------
question = input("Enter your question: ").strip()

# --------------------------------------------------------------
# Create an instance of the AzureOpenAI client
# --------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = AZURE_OPENAI_API_VERSION
)

# --------------------------------------------------------------
# Send the user question to LLM using Azure OpenAI's Responses API
#
# Notice that the `instructions` parameter is missing 
# and `input` is now an array of messages with roles.
# --------------------------------------------------------------
try:
    response = client.responses.create(
        model= AZURE_OPENAI_MODEL, 
        input=[
            {"role": "developer", "content": "You are a sarcastic AI assistant"},
            {"role": "user", "content": question}
        ],
        temperature=0.7, # Control randomness (0 = deterministic, 1 = creative)
        max_output_tokens=1000 # Limit the length of the response
    )

# Catch any exceptions that occur during the request
except Exception as e:
    print(f"Error getting answer from AI: {e}")

# --------------------------------------------------------------
# Print the response for debugging
# --------------------------------------------------------------
print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")

# --------------------------------------------------------------
# Extract answer and print it
# --------------------------------------------------------------
print("\nAnswer from AI:")
answer = response.output_text
print(answer)
