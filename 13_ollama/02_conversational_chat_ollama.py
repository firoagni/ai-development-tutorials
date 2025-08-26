# --------------------------------------------------------------
# Getting Started with Ollama: Conversational Chat
#
# In the previous example, one can ask a single question and get an answer.
# In this example, we will use the Ollama python library to have a conversational chat with the AI.
# The AI will remember the context of the conversation and respond accordingly.
# This is useful for building chatbots or virtual assistants that can hold a conversation with users.
# ---------------------------------------------------------------

# --------------------------------------------------------------
# Prerequisites
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
# --------------------------------------------------------------
from ollama import chat, ResponseError, pull    # chat API from Ollama. Think of OpenAI chat completion API equivalent
from dotenv import load_dotenv                  # The `dotenv` library is used to load environment variables from a .env file.
import os                                       # Used to get the values from environment variables.
# --------------------------------------------------------------
# Load environment variables from .env file
# --------------------------------------------------------------
load_dotenv()
MODEL = os.environ['OLLAMA_MODEL']

# ---------------------------------------------------------------
# Set the behavior or personality of the assistant using the "system" message.
# ----------------------------------------------------------------
conversation=[{"role": "system", "content": "You are a sarcastic AI assistant. You are proud of your amazing memory"}]

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

    # --------------------------------------------------------------
    # Wrap the question to ollama.chat() payload
    # --------------------------------------------------------------
    try:
        response = chat(
            model = MODEL,
            messages = conversation,
            options = {
                "temperature": 0.7,
                "seed": 42
            }
        )

        # --------------------------------------------------------------
        # Print the response for debugging
        # --------------------------------------------------------------
        print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")
        
        # --------------------------------------------------------------
        # Extract answer and print it
        # --------------------------------------------------------------
        answer = response.message.content
        print("\nAnswer from AI:")
        print(answer)

        # --------------------------------------------------------------
        # Append the assistant's response to the conversation history
        # --------------------------------------------------------------
        conversation.append({"role": "assistant", "content": answer})

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
                print('Please ask the question again.')

            except Exception as e:
                print('Error pulling model. Error:', e)

    # -------------------------------------------------------------
    # Catch any exceptions that occur during the request
    # -------------------------------------------------------------
    except Exception as e:
        print('Error getting answer from AI:', e)