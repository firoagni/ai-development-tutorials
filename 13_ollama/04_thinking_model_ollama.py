# --------------------------------------------------------------
# Getting Started with Ollama: Ask a question and get an answer from a thinking Model
#
# Newer models like GPT-5 can think before they answer, 
#
# "Thinking" refers to techniques that allow an AI to generate an internal, 
# hidden thought process before producing a final answer, rather than 
# providing a direct, immediate response. 
#
# This internal reasoning process improves the accuracy 
# and thoughtfulness of the AI's output, especially for 
# complex tasks requiring planning and reasoning.
# ---------------------------------------------------------------

# --------------------------------------------------------------
# Prerequisites 
# <<NO CHANGE FROM PREVIOUS EXAMPLES>>
#
# 1. Make sure that python3 is installed on your system.
# 2. Make sure Ollama is installed and "running" on your system.
# 3. Create an .env file, and add the following line:
#    `OLLAMA_MODEL=<model_name>`
#   model_name will be the name of the local model you want to use
# 4. Create and Activate a Virtual Environment:
# `python3 -m venv venv`
# `source venv/bin/activate`
# 5. The required libraries are listed in the requirements.txt file. Use the following command to install them:
#    `pip3 install -r requirements.txt`
#---------------------------------------------------------------
# --------------------------------------------------------------
# Import Modules 
# <<NO CHANGE FROM PREVIOUS EXAMPLES>>
# --------------------------------------------------------------
from ollama import chat, ResponseError, pull    # chat API from Ollama. Think of OpenAI chat completion API equivalent
from dotenv import load_dotenv                  # The `dotenv` library is used to load environment variables from a .env file.
import os                                       # Used to get the values from environment variables.
# --------------------------------------------------------------

# --------------------------------------------------------------
# Load environment variables from .env file 
# <<NO CHANGE FROM PREVIOUS EXAMPLES>>
# --------------------------------------------------------------
load_dotenv()
MODEL = os.environ['OLLAMA_THINKING_MODEL'] # Make sure to pick a thinking model

# --------------------------------------------------------------
# Prompt user for question
# --------------------------------------------------------------
question = input("Enter your question: ").strip()

# --------------------------------------------------------------
# Wrap the question to ollama.chat() payload 
# <<NO CHANGE FROM PREVIOUS EXAMPLES>>
# --------------------------------------------------------------
try:
    response = chat(
        model = MODEL,
        messages = [
            {"role": "system", "content": "You are a super sarcastic AI assistant"},
            {"role": "user", "content": question}
        ],
        options = {
            "temperature": 0.7,
            "seed": 42
        }
    )

    # --------------------------------------------------------------
    # Print the response for debugging 
    # <<NO CHANGE FROM PREVIOUS EXAMPLES>>
    # --------------------------------------------------------------
    print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")
    
    # --------------------------------------------------------------
    # Extract thinking process and print it
    #
    # In thinking models, expect an additional attribute
    # `message.thinking` in LLM response
    # --------------------------------------------------------------
    thinking = response.message.thinking
    print("Thinking process:")
    print(thinking)

    # --------------------------------------------------------------
    # Extract answer and print it 
    # <<NO CHANGE FROM PREVIOUS EXAMPLES>>
    # --------------------------------------------------------------
    answer = response.message.content
    print("\nAnswer from AI:")
    print(answer)

# -------------------------------------------------------------
# Handle if the provided model is not installed 
# <<NO CHANGE FROM PREVIOUS EXAMPLES>>
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
# <<NO CHANGE FROM PREVIOUS EXAMPLES>>
# -------------------------------------------------------------
except Exception as e:
    print('Error getting answer from AI:', e)