# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Structured Outputs
#
# By default, models return responses in plain text format.
#
# Structured Outputs is a feature that can force a model to generate responses
# in JSON format, based on the JSON schema provided by you.

# Structured Outputs is available in two forms in the OpenAI API:
# - Function Calling: Demonstrated in the next examples.
# - JSON Schema Response Format: Specify a `text_format` to directly control the structure of the model's output
#
# In this demo, we'll focus on using the JSON Schema Response Format.
#
# Steps:
# Define your schema: Write Pydantic classes to define the object schema 
#            that represents the structure of the desired output.
# Supply your schema to the API call: Pass the object schema 
#            to the model using the `text_format` parameter. 
# Handle edge cases: In some cases, the model might not generate a valid response 
#            that matches the provided JSON schema.
#
# Important: Instead of `client.responses.create`,use `client.responses.parse` for structured output
#
# This example is based on the documentation:
# - https://platform.openai.com/docs/guides/structured-outputs
# - https://cookbook.openai.com/examples/structured_outputs_intro
# - https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/structured-outputs

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
#    AZURE_OPENAI_VERSION=<your_azure_openai_api_version>  # Should be 2023-05-15 or newer
#    AZURE_OPENAI_API_KEY=<your_azure_openai_api_key>
#---------------------------------------------------------------

# --------------------------------------------------------------
# Import Modules
# --------------------------------------------------------------
from openai import AzureOpenAI            # The `AzureOpenAI` library is used to interact with the Azure OpenAI API
from dotenv import load_dotenv            # The `dotenv` library is used to load environment variables from a .env file
import os                                 # Used to get the values from environment variables
from pydantic import BaseModel, Field     # Pydantic is used to define the structure of the output we want
from typing import List                   # Used for type hints in our Pydantic models
import json                               # Used to work with JSON data

# --------------------------------------------------------------
# Load Environment Variables
# --------------------------------------------------------------
load_dotenv()  # Load environment variables from .env file

# --------------------------------------------------------------
# Initialize the Azure OpenAI Client
# --------------------------------------------------------------
# Extract environment variables and store them explicitly to ensure they're available
AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_MODEL = os.environ.get('AZURE_OPENAI_MODEL')
AZURE_OPENAI_VERSION = os.environ.get('AZURE_OPENAI_VERSION')  # Make sure this matches your .env file
AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')

# Initialize the client using the extracted variables
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,  # The endpoint URL for the Azure OpenAI service
    api_key=AZURE_OPENAI_API_KEY,          # The API key for the Azure OpenAI service
    api_version=AZURE_OPENAI_VERSION       # The API version to use (should be 2024-10-21 or newer)
)

deployment_name = AZURE_OPENAI_MODEL  # The deployment name of the model to use

# --------------------------------------------------------------
# Example 1: Basic Structured Output
# --------------------------------------------------------------
print("\n\n=== Example 1: Basic Structured Output ===")

# Define the output structure we want by writing a Pydantic class
class CalendarEvent(BaseModel):
    name: str = Field(description="The name of the event")
    date: str = Field(description="The date of the event")
    participants: List[str] = Field(description="List of participants attending the event")

# Some example inputs for which we generate JSON output in the above format
inputs = [
    "Mike will attend the Chris Rock Concert on 24 Jan 2025",
    "Vijay and Venu are going to a science fair on Friday."
]

for input in inputs:

    print(f"Input: {input}")
    # Call the model and pass the the pydantic class name to `response_format`

    try:
        # Instead of `client.responses.create`,
        # use `client.responses.parse` for structured output
        response = client.responses.parse(
            model=deployment_name,
            temperature=0,
            input=[
                {"role": "developer", "content": "Extract the event information from the provided user input"},
                {"role": "user", "content": input},
            ],
            text_format=CalendarEvent # Pass the Pydantic class to `text_format`
        )

        # print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")

        # If the model refuses to respond, you will get a refusal message
        if (response.output[0].content[0].type == "refusal"):
            print(response.output[0].content[0].refusal)
        else:
            response_json = response.output_parsed
            print("\nLLM Response:")
            print(response_json)
            print("\nExtracted Event Information:")
            print(f"Name: {response_json.name}")
            print(f"Date: {response_json.date}")
            print(f"Participants: {', '.join(response_json.participants)}")
            print("-------\n")
    
    # Catch any exceptions that occur during the request
    except Exception as e:
            print(f"Error getting answer from AI: {e}")

# --------------------------------------------------------------
# Example 2: Structured Output with confidence score
# --------------------------------------------------------------
# With structured output, the model will always try to 
# adhere to the provided schema, which can result in hallucinations 
# if the data in input is insufficient or the data is completely unrelated to the schema.
# In most cases, we don't have control over the input data quality.
# Therefore, its suggested to force the model to provide a confidence score too
print("\n\n=== Structured Output with confidence score ===")

class LLMConfidence(BaseModel):
    confidence: float = Field(description="Confidence level in the prediction. " \
                                    "Highest confidence - when all values are clearly mentioned in the input. " \
                                    "More the assumptions made by the model, lower the confidence. " \
                                    "Value between 0 lowest to 100 highest.")
    confidence_reason: str = Field(description="Reasoning behind the confidence level.")
    assumptions: List[str] = Field(description="List of assumptions made by the model.")

class CalendarEventWithConfidence(BaseModel):
    name: str = Field(description="The name of the event")
    date: str = Field(description="The date of the event")
    participants: List[str] = Field(description="List of participants attending the event")
    llm_confidence: LLMConfidence = Field(description="Confidence information from the model")

inputs = [
    "Mike will attend the Chris Rock Concert on 24 Jan 2025",
    "Vijay and Venu are going to a science fair on Friday.",
    "The project deadline is next Monday.",
    "Vijay and Venu are going to a science fair",
    "Build Team is planning a team outing first week of August",
    "My name is Agni. How are you?"
]

for input in inputs:

    print(f"Input: {input}")
    # Call the model and pass the the pydantic class name to `response_format`

    try:
        # Instead of `client.responses.create`,
        # use `client.responses.parse` for structured output
        response = client.responses.parse(
            model=deployment_name,
            temperature=0,
            input=[
                {"role": "system", "content": "Extract the event information from the provided user input"},
                {"role": "user", "content": input},
            ],
            text_format=CalendarEventWithConfidence
        )

        # print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")

        # If the model refuses to respond, you will get a refusal message
        if (response.output[0].content[0].type == "refusal"):
            print(response.output[0].content[0].refusal)
        else:
            response_json = response.output_parsed
            print("\nLLM Response:")
            print(response_json)
            print("\nExtracted Event Information:")
            print(f"Name: {response_json.name}")
            print(f"Date: {response_json.date}")
            print(f"Participants: {', '.join(response_json.participants)}")
            print(f"Confidence: {response_json.llm_confidence.confidence}")
            print(f"Confidence Reason: {response_json.llm_confidence.confidence_reason}")
            print(f"Assumptions: {', '.join(response_json.llm_confidence.assumptions)}")
            print("-------\n")
    
    # Catch any exceptions that occur during the request
    except Exception as e:
            print(f"Error getting answer from AI: {e}")