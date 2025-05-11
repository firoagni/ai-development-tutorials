# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Few-Shot Prompting
#
# In some cases, it's easier to show the model what you want rather than tell the model what you want.
#
# One way to show the model what you want is with creating a few fake back-and-forth messages 
# between user and assistant. This is called few-shot prompting. 
# 
# The opposite of few-shot prompting is zero-shot prompting (previous examples).
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

# ---------------------------------------------------------------
# Set the behavior or personality of the assistant by providing fake conversations
# ----------------------------------------------------------------
# In this example, we are expecting the assistant to respond in Hindi.
# The `conversation` list contains a series of messages that simulate such conversation.
#
#
# To help clarify that the example messages are not part of a real conversation, 
# and shouldn't be referred back by the model, 
# set the message role as `system` followed by a `name` field
# The value of `name` field can either by `example_user` or `example_assistant`
# ---------------------------------------------------------------
conversation=[
        {"role": "system", "content": "You answer based on the pattern of the conversation."},
        {"role": "system", "name":"example_user", "content": "Hi, how are you?"},
        {"role": "system", "name": "example_assistant", "content": "Main accha hoon, aap kaise hain?"},
        {"role": "system", "name":"example_user", "content": "I am fine, can you tell me something?"},
        {"role": "system", "name": "example_assistant", "content": "Haan, bilkul! Aapko kya jaanana hai?"}
    ]

# --------------------------------------------------------------
# Start a loop to keep the conversation going
# --------------------------------------------------------------
# The loop will continue until the user decides to exit.
# In each iteration, the user will be prompted to enter a question.
# The question will be added to the conversation history, and the AI will respond based on the entire conversation.
# The conversation history is maintained in the `conversation` list, which is updated with each user input and AI response.
# ---------------------------------------------------------------
while True:
    # --------------------------------------------------------------
    # Get user input and add it to the conversation history
    # --------------------------------------------------------------
    question = input("Enter your question: ").strip()
    conversation.append({"role": "user", "content": question})

    try:
        # --------------------------------------------------------------
        # Call the Azure OpenAI API to get the AI's response
        # --------------------------------------------------------------
        response = client.chat.completions.create(
            model= AZURE_OPENAI_MODEL, # model = "deployment_name".
            messages=conversation,
            temperature=0.7, # Control randomness (0 = deterministic, 1 = creative)
            max_tokens=1000  # Limit the length of the response
        )

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
        print("\nAnswer from AI:\n")
        answer = response.choices[0].message.content
        print("\n" + answer + "\n")

        # --------------------------------------------------------------
        # Append the assistant's response to the conversation history
        # --------------------------------------------------------------
        conversation.append({"role": "assistant", "content": response.choices[0].message.content})
        
        # --------------------------------------------------------------
        # Debug: Print the entire conversation history
        # --------------------------------------------------------------
        print("\nDEBUG: Conversation history:\n")
        pprint(conversation)
        print("\n-----------------------------------------------------\n")
    
    except Exception as e:
        print(f"Error getting answer from AI: {e}")
        continue