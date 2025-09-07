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
# Set the behavior or personality of the assistant by providing fake conversations
# ----------------------------------------------------------------
# In this example, we are expecting the assistant to respond in Hindi.
# To achieve this, we will provide a series of examples in the `developer` message that simulate such conversation
# and instruct the model to answer based on the pattern of the conversation.
#
# For elaborate developer and user messages, OpenAI recommends using a combination of 
# Markdown formatting and XML tags to help the model understand logical 
# boundaries of your prompt and context data.
#
# ---------------------------------------------------------------
llm_message = f"""
# Instruction
You answer based on the pattern of the conversation.

# Examples
<user_query id="example-1">Hi, how are you?</user_query>
<assistant_response id="example-1">Main accha hoon, aap kaise hain?</assistant_response>
<user_query id="example-2">I am fine, can you tell me something?</user_query>
<assistant_response id="example-2">Haan, bilkul! Aapko kya jaanana hai?</assistant_response>
"""
conversation=[{"role": "developer", "content": llm_message}]

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
            input=conversation,
            temperature=0.7,
            max_output_tokens=1000
        )

        # --------------------------------------------------------------
        # Print the response for debugging
        # --------------------------------------------------------------
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
    
    except Exception as e:
        print(f"Error getting answer from AI: {e}")
        continue