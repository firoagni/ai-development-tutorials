# --------------------------------------------------------------
# Getting Started with Ollama: Structured Outputs
#
# By default, models return responses in plain text format.
#
# Structured Outputs is a feature that can force a model to generate responses
# in JSON format, based on the JSON schema provided by you.
#
# Structured Outputs is available in two forms in the OpenAI API:
# - Function Calling: Demonstrated in next example.
# - JSON Schema Response Format: Specify a `format` to directly control the structure of the model's output
#
# In this demo, we'll focus on using the JSON Schema Response Format.
#
# Steps:
# Define your schema: Write Pydantic classes to define the object schema 
#            that represents the structure of the desired output.
# Supply your schema to the API call: Pass the object schema
#            to the model using the `format` parameter.
# Handle edge cases: In some cases, the model might not generate a valid response
#                      that matches the provided JSON schema.
#
# Difference from OpenAI responses API
# 1. Instead of `response_format`, Ollama chat API has `format` attribute
# 2. `response_format` accepts the Pydantic class name, 
#          while `format` accepts the "JSON schema" of the Pydantic Class
# 3. The model output response of Ollama API is plain JSON. 
#    To use the output in your python code, you'll need to convert it 
#    into the appropriate Pydantic model instance.
#
# Important notes:
# - Structured output not working with gpt-oss model 
#   Issue: https://github.com/ollama/ollama/issues/11691
# - Structured output response is not great with llama3.2:3b model,
#   its a bit better with gemma3:4b and deepseek-r1:8b, but still unreliable
# - qwen2.5:7b model seems to work best with structured output
# ---------------------------------------------------------------

# --------------------------------------------------------------
# Prerequisites
# <<NO CHANGE FROM PREVIOUS EXAMPLE>>
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
# <<NO CHANGE FROM PREVIOUS EXAMPLE>>
# --------------------------------------------------------------
from ollama import chat, ResponseError, pull    # chat API from Ollama. Think of OpenAI chat completion API equivalent
from dotenv import load_dotenv                  # The `dotenv` library is used to load environment variables from a .env file.
import os                                       # Used to get the values from environment variables.
from pydantic import BaseModel, Field           # Pydantic is used to define the structure of the output we want
from typing import List                         # Used for type hints in our Pydantic models
# --------------------------------------------------------------

# --------------------------------------------------------------
# Load environment variables from .env file
# <<NO CHANGE FROM PREVIOUS EXAMPLE>>
# --------------------------------------------------------------
load_dotenv()
MODEL = os.environ['OLLAMA_MODEL']

# --------------------------------------------------------------
# Define the output structure we want by writing a Pydantic class
# --------------------------------------------------------------
class LLMConfidence(BaseModel):
    confidence: float = Field(description="Confidence level in the prediction. " \
                                    "Value between 0 lowest to 100 highest." \
                                    "Highest confidence - when all values are clearly mentioned in the input. " \
                                    "More the assumptions made by the model, lower the confidence. "
                                    )
    confidence_reason: str = Field(description="Reasoning behind the confidence level.")
    assumptions: List[str] = Field(description="List of assumptions made by the model.")

class CalendarEvent(BaseModel):
    name: str = Field(description="The name of the event")
    date: str = Field(description="The date of the event")
    participants: List[str] = Field(description="List of participants attending the event")
    llm_confidence: LLMConfidence = Field(description="Confidence information from the model")

# --------------------------------------------------------------
# Define some example inputs for which we generate JSON 
# output in the above format
# --------------------------------------------------------------
inputs = [
    "Mike will attend the Chris Rock Concert on 24 Jan 2025",
    "Vijay and Venu are going to a science fair on Friday.",
    "The project deadline is next Monday.",
    "Vijay and Venu are going to a science fair",
    "Build Team is planning a team outing first week of August",
    "Solve 2+2"
]

for input in inputs:
    print(f"Input: {input}")
    #--------------------------------------------------------
    # Call the model and pass the pydantic class's JSON 
    # schema to its `format` attribute
    #--------------------------------------------------------
    try:
        response = chat(
            model = MODEL,
            messages = [
                {"role": "system", "content": "Extract the event information from the provided user input"},
                {"role": "user", "content": input}
            ],
            format = CalendarEvent.model_json_schema(), # Use Pydantic to generate the JSON schema of the Class
            options = {
                "temperature": 0, # Make responses more deterministic
            }
        )

        # --------------------------------------------------------------
        # Extract answer and print it
        # --------------------------------------------------------------
        print("\nLLM Response:")

        # response output is in json format.
        response_json = response.message.content

        # Use `model_validate_json` class method to convert
        # the response JSON into a Pydantic model instance.
        response_content = CalendarEvent.model_validate_json(response_json)
        print(response_content)
        print("\nExtracted Event Information:")
        print(f"Name: {response_content.name}")
        print(f"Date: {response_content.date}")
        print(f"Participants: {', '.join(response_content.participants)}")
        print(f"Confidence: {response_content.llm_confidence.confidence}")
        print(f"Confidence Reason: {response_content.llm_confidence.confidence_reason}")
        print(f"Assumptions: {', '.join(response_content.llm_confidence.assumptions)}")
        print("-------\n")
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