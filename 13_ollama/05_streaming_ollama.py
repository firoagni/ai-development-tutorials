# --------------------------------------------------------------
# Getting Started with Ollama: Ask a question and get an answer from a thinking Model
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
# <<NO CHANGE FROM PREVIOUS EXAMPLE>>
# 1. Make sure that python3 is installed on your system.
# 2. Make sure Ollama is installed and "running" on your system.
# 3. Create an .env file, and add the following line:
#    `OLLAMA_THINKING_MODEL=<model_name>`
#   where model_name will be the name of the thinking model you want to use
# 4. Create and Activate a Virtual Environment:
# `python3 -m venv venv`
# `source venv/bin/activate`
# 5. The required libraries are listed in the requirements.txt file. Use the following command to install them:
#    `pip3 install -r requirements.txt`
#---------------------------------------------------------------
# --------------------------------------------------------------
# Import Modules
# <<NO CHANGE FROM PREVIOUS EXAMPLE>>
# --------------------------------------------------------------
from ollama import chat, ResponseError, pull    # chat API from Ollama. Think of OpenAI chat completion API equivalent
from dotenv import load_dotenv                  # The `dotenv` library is used to load environment variables from a .env file.
import os                                       # Used to get the values from environment variables.
# --------------------------------------------------------------

# --------------------------------------------------------------
# Load environment variables from .env file
# <<NO CHANGE FROM PREVIOUS EXAMPLE>>
# --------------------------------------------------------------
load_dotenv()
MODEL = os.environ['OLLAMA_THINKING_MODEL'] # Make sure to pick a thinking model

# --------------------------------------------------------------
# Prompt user for question
# <<NO CHANGE FROM PREVIOUS EXAMPLE>>
# --------------------------------------------------------------
question = input("Enter your question: ").strip()

# --------------------------------------------------------------
# Wrap the question to ollama.chat() payload
#
# Only change - stream=True
# --------------------------------------------------------------
try:
    response = chat(
        model = MODEL,
        stream=True, # Enable streaming to get streaming responses
        messages = [
            {"role": "system", "content": "You are a super sarcastic AI assistant"},
            {"role": "user", "content": question}
        ]
    )

    first_thinking_chunk = True
    first_message_content = True

    # --------------------------------------------------------------
    # Print the chunks as they come in
    # --------------------------------------------------------------
    for chunk in response:
        if chunk.message.thinking: # AI is currently thinking
            if first_thinking_chunk:
                print("\nThinking .... :")
                first_thinking_chunk = False
            print(chunk.message.thinking, end='', flush=True)

        if chunk.message.content: # AI has finished thinking and is now responding
            if first_message_content:
                print("\n\nAnswer from AI:")
                first_message_content = False
            print(chunk.message.content, end='', flush=True)

# -------------------------------------------------------------
# Handle if the provided model is not installed
# <<NO CHANGE FROM PREVIOUS EXAMPLE>>
# -------------------------------------------------------------
except ResponseError as e:
    print('Error getting answer from AI:', e)
    if e.status_code == 404: # Model not installed
        try:
            print('Pulling model:', MODEL)
            pull(MODEL) 
            print('Model pulled successfully:', MODEL)
            print('Restart the program again ...')

        except Exception as e:
            print('Error pulling model. Error:', e)

# -------------------------------------------------------------
# Catch any exceptions that occur during the request
# <<NO CHANGE FROM PREVIOUS EXAMPLE>>
# -------------------------------------------------------------
except Exception as e:
    print('Error getting answer from AI:', e)