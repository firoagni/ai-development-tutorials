# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Conversational Chat with Azure OpenAI
#
# In the previous example, one can ask a single question, get an answer and the program ends.
# In this example, we will create a loop to keep the conversation going.
# The AI will remember the context of the conversation and respond accordingly.
# This is useful for building chatbots or virtual assistants that can hold a conversation with users.
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
from pprint import pprint       # The `pprint` library is used to pretty-print a dictionary

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
# This loop runs continuously to keep the chat going between the user and the AI.
#
# Here’s what happens in each round:
# 1. The user is asked to type a question.
# 2. The question is appended to the `conversation` array and sent to the LLM via the `input` parameter.
# 3. LLM reads the content of `input` and generate a response.
# 4. The LLM response is presented (printed) to the user.
# 5. The LLM response is also appended to the `conversation` array.
# This loop continues until the user chooses to exit.
#
# Notice that the `conversation` array holds not just the current question but also the previous exchanges.
# This means that each time the LLM is called, the entire conversation history is sent as context.
#
# Why pass the "entire history" instead of just the current question?
# LLMs are stateless — they don’t remember past interactions.
# By maintaining and resending entire conversation in each LLM call, we give the illusion of memory -- allowing
# the LLM "to remember" past exchanges and respond contextually.
# ---------------------------------------------------------------
while True:
    # --------------------------------------------------------------
    # Get user input
    # --------------------------------------------------------------
    question = input("Enter your question (type 'exit' to quit): ").strip()

    # Exit the loop if user types 'exit'
    if question.lower() == 'exit':
        print("Goodbye!")
        break

    # --------------------------------------------------------------
    # Append the user's question to the conversation history
    # --------------------------------------------------------------
    conversation.append({"role": "user", "content": question})

    try:
        # --------------------------------------------------------------
        # Send the conversation history to Responses API to get the AI's response
        # --------------------------------------------------------------
        response = client.responses.create(
            model= AZURE_OPENAI_MODEL,
            input=conversation,
            temperature=0.7,
            max_output_tokens=1000
        )

        # --------------------------------------------------------------
        # Print the response for debugging
        # ---------------------------------------------------------------
        # print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")

        # --------------------------------------------------------------
        # Extract answer and print it
        # --------------------------------------------------------------
        answer = response.output_text
        print(f"Answer from AI = {answer}")
        print(f"input tokens = {response.usage.input_tokens}")
        print(f"output tokens = {response.usage.output_tokens}")
        print(f"total tokens = {response.usage.total_tokens}")
        print("=" * 80)

        # --------------------------------------------------------------
        # Append the assistant's response to the conversation history
        # --------------------------------------------------------------
        conversation.append({"role": "assistant", "content": answer})

        # --------------------------------------------------------------
        # Debug: Print the entire conversation history
        # --------------------------------------------------------------
        print("Conversation history:\n")
        pprint(conversation)
        print("=" * 80)
    
    except Exception as e:
        print(f"Error getting answer from AI: {e}")
        continue