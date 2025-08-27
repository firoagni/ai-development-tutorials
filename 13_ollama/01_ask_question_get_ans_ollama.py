# --------------------------------------------------------------
# Getting Started with Ollama: Ask a question and get an answer from Ollama hosted local model
#
# This script demonstrates how to interact with Ollama via its Python library
# ---------------------------------------------------------------

# --------------------------------------------------------------
# Prerequisites
# 1. Make sure that python3 is installed on your system.
# 2. Make sure Ollama is installed and "running" on your system.
# 3. Create an .env file, and add the following line:
#    `OLLAMA_MODEL=<model_name>`
#   wheremodel_name will be the name of the local model you want to use
# 4. Create and Activate a Virtual Environment:
# `python3 -m venv venv`
# `source venv/bin/activate`
# 5. The required libraries are listed in the requirements.txt file. Use the following command to install them:
#    `pip3 install -r requirements.txt`
#---------------------------------------------------------------
# --------------------------------------------------------------
# Import Modules
# --------------------------------------------------------------
from ollama import chat, ResponseError, pull    # chat API from Ollama. Think of OpenAI chat completion API equivalent
from dotenv import load_dotenv                  # The `dotenv` library is used to load environment variables from a .env file.
import os                                       # Used to get the values from environment variables.
# --------------------------------------------------------------
# Load environment variables from .env file
# --------------------------------------------------------------
# The `load_dotenv()` function reads the .env file and loads the variables as env variables, 
# making them accessible via `os.environ` or `os.getenv()`.
# --------------------------------------------------------------
load_dotenv()
MODEL = os.environ['OLLAMA_MODEL']

# --------------------------------------------------------------
# Prompt user for question
# --------------------------------------------------------------
question = input("Enter your question: ").strip()

# --------------------------------------------------------------
# In Azure OpenAI, you need to create an instance 
# of the AzureOpenAI client first
# In Ollama, client instance creation step is optional!
# You can just call ollama.chat() to get the model response 
# --------------------------------------------------------------

# --------------------------------------------------------------
# Wrap the question to ollama.chat() payload
# --------------------------------------------------------------
# The "model" parameter specifies the model to be used for the request.
# The "messages" array defines the conversation history for the AI model.
#
# Each message includes a "role" and "content".
# - "role" specifies the role in the conversation:
#   - "system": Sets the behavior or personality of the assistant. The first message in the "messages" array
#   - "user": Provides the user's input to the model
#   - "assistant": Represents the AI's response (used in conversations, check later examples).
#
# Additional parameters like "temperature" and "seed" control response behavior.
# --------------------------------------------------------------
try:
    response = chat(
        model = MODEL,
        messages = [
            {"role": "system", "content": "You are a super sarcastic AI assistant"},
            {"role": "user", "content": question}
        ],
        options = {               # See https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values
            "temperature": 0.7,   # Controls the randomness of the output. Lower values make the output more deterministic.
            "seed": 42           # Setting seed to a specific number will make the model generate the same output for the same input
        }
    )

    # --------------------------------------------------------------
    # Print the response for debugging
    # --------------------------------------------------------------
    # The `model_dump_json` method is a custom method provided by the Ollama library to serialize the response object.
    # No need to use json.dumps() to convert to a string, as `model_dump_json` already does that.
    # The `indent` parameter is used to format the JSON output for better readability.
    # ---------------------------------------------------------------
    print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")
    
    # --------------------------------------------------------------
    # Extract answer and print it
    # --------------------------------------------------------------
    answer = response.message.content
    print("\nAnswer from AI:")
    print(answer)

# -------------------------------------------------------------
# Handle if the provided model is not installed
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
# -------------------------------------------------------------
except Exception as e:
    print('Error getting answer from AI:', e)