# --------------------------------------------------------------
# Azure OpenAI - Responses API: Conversational Chat
#
# Want to switch from Chat Completions API to Responses API?
#
# Compared to Chat Completions API, Structured Outputs API shape
# is slightly different in Responses API. 
#
# Major changes:
# 1. The API endpoint has changed from `client.beta.chat.completions.parse` to `client.responses.parse`
# 2. Instead of `response_format`, use `text_format`
# 3. Instead of `messages`, use `input`
# 4. Instead of `max_tokens`, use `max_output_tokens`
# 5. The structured output from LLM can now be accessed directly from the response object's output_parsed` attribute.

# ---------------------------------------------------------------

# --------------------------------------------------------------
# Prerequisites <<NO CHANGES>>
# 1. Make sure that python3 is installed on your system.
# 2. Create and Activate a Virtual Environment:
# `python3 -m venv venv`
# `source venv/bin/activate`
# 3. The required libraries are listed in the requirements.txt file. Use the following command to install them:
#    `pip3 install -r ../requirements.txt`
# 4. Create a `.env` file in the parent directory and add the following variables:
#    AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint>
#    AZURE_OPENAI_MODEL=<your_azure_openai_model>
#    AZURE_OPENAI_API_VERSION=<your_azure_openai_api_version>
#    AZURE_OPENAI_API_KEY=<your_azure_openai_api_key>
#---------------------------------------------------------------

# --------------------------------------------------------------
# Import Modules <<NO CHANGES>>
# --------------------------------------------------------------
from openai import AzureOpenAI             # The `AzureOpenAI` library is used to interact with the Azure OpenAI API.
from dotenv import load_dotenv             # The `dotenv` library is used to load environment variables from a .env file.
import os                                  # Used to get the values from environment variables.
from pydantic import BaseModel, Field      # Pydantic is used to define the structure of the output we want
from typing import List, Optional          # Used for type hints in our Pydantic models

# --------------------------------------------------------------
# Load environment variables from .env file <<NO CHANGES>>
# --------------------------------------------------------------
load_dotenv("../.env")

AZURE_OPENAI_ENDPOINT        = os.environ['AZURE_OPENAI_ENDPOINT']
AZURE_OPENAI_MODEL           = os.environ['AZURE_OPENAI_MODEL']
AZURE_OPENAI_API_VERSION     = os.environ['AZURE_OPENAI_VERSION']
AZURE_OPENAI_API_KEY         = os.environ['AZURE_OPENAI_API_KEY']

# --------------------------------------------------------------
# Create an instance of the AzureOpenAI client <<NO CHANGES>>
# --------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = AZURE_OPENAI_API_VERSION
)

# --------------------------------------------------------------
# Define output JSON schema by writing Pydantic classes <<NO CHANGES>>
# --------------------------------------------------------------
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

# --------------------------------------------------------------
# Define system prompt and other parameters
# --------------------------------------------------------------
system_prompt = "Extract the event information from the provided user input"
temperature = 0

# --------------------------------------------------------------
# Inputs
# --------------------------------------------------------------
inputs = [
    "Mike will attend the Chris Rock Concert on 24 Jan 2025",
    "Vijay and Venu are going to a science fair on Friday.",
    "The project deadline is next Monday.",
    "Vijay and Venu are going to a science fair",
    "Build Team is planning a team outing first week of August",
    "Solve 2+2"
]

# --------------------------------------------------------------
# Structured Output from `chat.completions.parse` API
# --------------------------------------------------------------

print("=" * 80)
print(f"Structured Output from chat.completions.parse API:")
print("=" * 80)

for input in inputs:

    print(f"Input: {input}")
    try:
        response = client.beta.chat.completions.parse(
            model=AZURE_OPENAI_MODEL,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input},
            ],
            response_format=CalendarEventWithConfidence
        )

        print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")

        # If the model refuses to respond, you will get a refusal message
        if (response.choices[0].message.refusal):
            print(response.choices[0].message.refusal)
        else:
            response_json = response.choices[0].message.parsed
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


# --------------------------------------------------------------
# Structured Output from `responses.parse` API
# --------------------------------------------------------------

print("=" * 80)
print(f"Structured Output from responses.parse API:")
print("=" * 80)

for input in inputs:

    print(f"Input: {input}")
    try:
        # Instead of `client.beta.chat.completions.parse`,
        # use `client.responses.parse`
        response = client.responses.parse(
            model=AZURE_OPENAI_MODEL,                # <<NO CHANGE>>
            temperature=temperature,                 # <<NO CHANGE>>
            instructions=system_prompt,              # separate parameter to pass system prompt
            input=input,                             # `input` instead of `messages`
            text_format=CalendarEventWithConfidence  # `text_format` instead of `response_format`
        )

        print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")

        # If the model refuses to respond, you will get a refusal message
        if (response.output[0].content[0].type == "refusal"):
            print(response.output[0].content[0].refusal)
        else:
            response_json = response.output_parsed # instead of response.choices[0].message.parsed
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