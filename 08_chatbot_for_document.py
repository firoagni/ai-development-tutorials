# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Chatbot for a Document
#
# Chatbots created in previous examples have the limitation that they can answer only from their own knowledge.
# In this example, we will design a chatbot to answer questions based on a specific document.
# This approach allows the chatbot to provide context-specific responses.
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

# --------------------------------------------------------------
# Ask user for file and load its content
# --------------------------------------------------------------
file_path = input("Enter the path to the reference file (the bot will only use this content to answer): ").strip()
try:
    with open(file_path, 'r', encoding='utf-8') as file: 
        file_content = file.read()
except Exception as e:
    print(f"Error reading file: {e}")
    exit(1)

if not file_content.strip():
    print("The file is empty.")
    exit(1)

# --------------------------------------------------------------
# - the open() function opens a file. 
# - open() can take 3 parameters – the filepath, file access mode, and file encoding.
# - mode is optional and defaults to 'r' (read mode). Other modes include 'w' (write), 'a' (append), and 'b' (binary).
# - encoding is also optional and defaults to the system's default encoding.
# - The 'utf-8' encoding is commonly used for text files, especially those containing non-ASCII characters.
# - The read() method reads the entire content of the file into a string.
# 
# my_file = open("hello.txt", "r")
# print(my_file.read())
# my_file.close()
#
# The open() function does not close the file, you need to explicitly close the file with the close() method
#
# A better way to handle files is to use the `with` statement with open, which automatically closes the file when done.
# --------------------------------------------------------------


# ---------------------------------------------------------------
# Set the behavior or personality of the assistant using the "developer" message.
# ----------------------------------------------------------------
# For elaborate developer and user messages, OpenAI recommends using a combination of 
# Markdown formatting and XML tags to help the model understand logical 
# boundaries of your prompt and context data.
# ---------------------------------------------------------------

developer_message = f"""
You are a sarcastic assistant. You respond to every user question with witty, dry humor and light sarcasm.
You can only answer questions based on the following information. If the information is not in the text, admit it sarcastically and refuse to answer.

<context>
{file_content}
</context>

Never break character. Never use any knowledge outside of the reference content.
"""

conversation=[{"role": "developer", "content": developer_message}]

# --------------------------------------------------------------
# Start a loop to keep the conversation going
# --------------------------------------------------------------
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
        print("=" * 80)
        # --------------------------------------------------------------
        # Append the assistant's response to the conversation history
        # --------------------------------------------------------------
        conversation.append({"role": "assistant", "content": answer})
        
        # --------------------------------------------------------------
        # Print the entire conversation history
        # --------------------------------------------------------------
        print("Conversation history:\n")
        pprint(conversation)
        print("=" * 80)
    
    except Exception as e:
        print(f"Error getting answer from AI: {e}")
        continue