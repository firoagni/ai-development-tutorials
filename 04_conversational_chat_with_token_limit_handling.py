# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Conversational Chat with Azure OpenAI with Token Limit Handling
#
# In the previous example, we created a conversational chatbot 
# by creating a loop, where in each iteration:
# - the user is prompted to enter a question
# - The question is then added to the conversation history
# - The conversation history is passed to the AI. The AI response will be based on the entire conversation
# - The AI response is appended to the conversation history
# Rinse and repeat.
# 
# With each question asked and answer received, the conversation history grows in size.
# The larger the conversation history (input to LLM), the more tokens are used. 
#
# Therefore, if the user does not exit, the conversation 
# will eventually reach the token limit of the model.
#
# In this example, we will implement a simple token limit handling mechanism.
# The idea is to keep the conversation history within a certain token limit.
# If the conversation history exceeds the token limit,
# we will remove the oldest messages from the conversation history.
#
# This example will use the `tiktoken` library to count the number of tokens in the conversation.
# Reference: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
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

import tiktoken                 # The `tiktoken` library is used to count the number of tokens in a string.

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
# ---------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = AZURE_OPENAI_API_VERSION
)

#--------------------------------------------------------------
# Function to calculate the total token count of the conversation
# --------------------------------------------------------------
def calculate_token_count(conversation):
    # Different models use different encodings to convert text into tokens.
    # You can retrieve the encoding for a model using `tiktoken.encoding_for_model()`
    try:
        encoding = tiktoken.encoding_for_model(AZURE_OPENAI_MODEL)
    except KeyError:
        print("WARNING: model not found. Using o200k_base encoding.")
        encoding = tiktoken.get_encoding("o200k_base")

    # The `encoding.encode()` method can convert a string into tokens.
    # One can then use `len()` against the result of `encoding.encode()` to get the number of tokens.
    #
    # One caveat:
    # Since models like gpt-4o-mini and gpt-4 uses a message-based formatting, 
    # it's more difficult to count how many tokens will be used by a conversation, 
    # as each conversation is primed with additional metadata (strings)
    #
    # Deep Dive:
    # - https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chatgpt#manage-conversations
    # - https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb    
    total_tokens = 3  # Initialize total token count with 3 (not 0) as every reply is primed with <|start|>assistant<|message|
    for message in conversation:
        total_tokens += 3 # every message follows <|start|>{role/name}\n{content}<|end|>\n
        for key, value in message.items():
            message_converted_to_tokens = encoding.encode(value) # convert the message strings to tokens 
            total_tokens += len(message_converted_to_tokens)     # count the number of tokens and add to total
            if key == "name":
                total_tokens += 1 # if "name" attribute is set in the message, then 1 additional token   
    return total_tokens

# --------------------------------------------------------------
# Function to trim conversation history to fit within the token limit
# --------------------------------------------------------------
def trim_conversation(conversation, max_response_tokens, token_limit):
    total_tokens_in_conversation = calculate_token_count(conversation)

    # Keep deleting the oldest user + assistant prompts until the conversation history fits within the token limit
    # Make sure to leave at least 2 messages in the conversation history (1 system and 1 just asked user message)
    while total_tokens_in_conversation + max_response_tokens > token_limit and len(conversation) > 2:
        print("Trimming conversation history to fit within token limit...")
        deleted_oldest_user_message = conversation.pop(1)  # Remove the oldest user message (index 1), first message is a system message
        print(f"Deleted message: {deleted_oldest_user_message}")
        deleted_oldest_assistant_message = conversation.pop(1)  # After removing the user message, index 1 is assistant message. Remove
        print(f"Deleted message: {deleted_oldest_assistant_message}") 
        total_tokens_in_conversation = calculate_token_count(conversation) # recalculate token count
        print("\n-----------------------------------------------------\n") 
    return conversation

# --------------------------------------------------------------
# Set the token limit and max_tokens for this example
# --------------------------------------------------------------
TOKEN_LIMIT = 150
MAX_RESPONSE_TOKENS = 50

# ---------------------------------------------------------------
# Set the behavior or personality of the assistant
# ----------------------------------------------------------------
conversation=[{"role": "developer", "content": "You are a sarcastic AI assistant. You are proud of your amazing memory"}]

# --------------------------------------------------------------
# Start a loop to keep the conversation going. 
# Ensure the conversation history do not blow the context limit
# --------------------------------------------------------------
# - Append the `conversation` array with user's question
# - Check that token size of `conversation` array + `max_output_tokens` token value does not exceed the token limit. 
#   Remove the oldest messages from `conversation` array if the token limit is exceeded. 
#   Rinse and repeat until it fits the token limit OR only 2 messages 
#        are left in the `conversation` array - 1 system and 1 the current question
# - Send the `conversation` array to Responses API to get the AI's response
# - Append the AI's response to the `conversation` array
# Rinse and repeat
# ---------------------------------------------------------------
while True:

    # --------------------------------------------------------------
    # Get user input and add it to the conversation history
    # --------------------------------------------------------------
    question = input("Enter your question: ").strip()

    # Exit the loop if user types 'exit'
    if question.lower() == 'exit':
        print("Goodbye!")
        break

    conversation.append({"role": "user", "content": question})

    # --------------------------------------------------------------
    # Trim the conversation history to fit within the token limit
    # --------------------------------------------------------------
    conversation = trim_conversation(conversation, MAX_RESPONSE_TOKENS, TOKEN_LIMIT)

    try:
        # --------------------------------------------------------------
        # Call the Azure OpenAI API to get the AI's response
        # --------------------------------------------------------------
        response = client.responses.create(
            model= AZURE_OPENAI_MODEL,
            input=conversation, # developer instruction + user question + past conversation
            temperature=0.7,
            max_output_tokens=MAX_RESPONSE_TOKENS
        )

        # --------------------------------------------------------------
        # Extract answer and print it
        # --------------------------------------------------------------
        answer = response.output_text
        print(f"Answer from AI = {answer}")
        print(f"input tokens = {response.usage.input_tokens}")
        print(f"output tokens = {response.usage.output_tokens}")
        print(f"total tokens = {response.usage.total_tokens}")
        print(f"Token Limit = {TOKEN_LIMIT}")
        print("=" * 80)

        # --------------------------------------------------------------
        # Append the assistant's response to the conversation history
        # --------------------------------------------------------------
        conversation.append({"role": "assistant", "content": answer})
        
        # --------------------------------------------------------------
        # Debug: Print the entire conversation history
        # --------------------------------------------------------------
        print("\nConversation history:\n")
        pprint(conversation)
        print("\n-----------------------------------------------------\n")
    
    except Exception as e:
        print(f"Error getting answer from AI: {e}")
        continue