# --------------------------------------------------------------
# Getting Started with Ollama: Remote Ollama
#
# All previous tutorials are written assuming Ollama is running on
# the same machine where the script is executed. 
# 
# In this tutorial, we will cover how to interact with 
# a remote instance of Ollama.
# ---------------------------------------------------------------

# --------------------------------------------------------------
# Prerequisites
# 1. Make sure that python3 is installed on your system.
# 2. Make sure remote Ollama is accessible (via HTTP) from 
#    the system where the script is executed.
# 3. Create an .env file, and add the following line:
#    `OLLAMA_MODEL=<model_name>`
#   where model_name will be the name of the model you want to use
# 4. Create and Activate a Virtual Environment:
# `python3 -m venv venv`
# `source venv/bin/activate`
# 5. The required libraries are listed in the requirements.txt file. Use the following command to install them:
#    `pip3 install -r requirements.txt`
#---------------------------------------------------------------
# --------------------------------------------------------------
# Import Modules
# --------------------------------------------------------------
from ollama import Client, chat, ResponseError, pull  # chat API from Ollama. Think of OpenAI chat completion API equivalent
from dotenv import load_dotenv                        # The `dotenv` library is used to load environment variables from a .env file.
import os                                             # Used to get the values from environment variables.
# --------------------------------------------------------------
# Load environment variables from .env file
# --------------------------------------------------------------
load_dotenv()
MODEL = os.environ['OLLAMA_MODEL']

# --------------------------------------------------------------
# Prompt user for question
# --------------------------------------------------------------
question = input("Enter your question: ").strip()

# --------------------------------------------------------------
# To create a connection to Ollama hosted to a remote server, 
# instantiate a custom client by passing the Ollama host URL
# as argument
#
# Argument list: https://www.python-httpx.org/api/#client
#
# < This is the only change you require to switch 
#                   from local to remote Ollama  >
#
# --------------------------------------------------------------
client = Client(
  host='http://localhost:11434',
  # headers={'Authorization': (os.getenv('OLLAMA_API_KEY'))}
)

# --------------------------------------------------------------
# Wrap the question to client.chat() payload
# --------------------------------------------------------------
try:
    response = client.chat(
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