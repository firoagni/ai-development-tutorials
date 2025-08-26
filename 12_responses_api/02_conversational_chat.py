# --------------------------------------------------------------
# Azure OpenAI - Responses API: Conversational Chat
#
# Want to switch from Chat Completions API to Responses API?
#
# Unlike Chat Completions, where developers must manually manage 
# conversation history and re-send full messages, 
# the Responses API additionally supports server-side conversation 
# state management.
#
# Key features:
# 1. Chat Completions API requires you to manage conversation state yourself, 
#    while in Responses API, responses are auto-saved at server-side. 
# 2. You can chain responses together by passing the `response.id` of the previous response 
#    to the `previous_response_id` parameter of the current response.
# 3. To instruct Responses API "NOT" to save a response, set `store: false`
# 4. If saved, a response is retained for 30 days
# 5. Use `responses.input_items.list("{response_id}")` to obtain 
#    the conversation history for the given response id
# 6. To delete a response, use `responses.delete("{response_id}")`
#
# Note: Even though conversations are saved server-side, input tokens size 
# will grow with each conversation turn as the full conversation context is sent to 
# the model in every API call.
# Therefore, monitor token usage carefully to stay within model limits and manage costs.
# Consider implementing token limit checks and conversation truncation if needed.
#
# Also note that at the time of writing, several known issues exist in the Responses API:
#
# Known Issues in Current Implementation
# 1. Incomplete conversation history retrieval:
#    - `responses.input_items.list("{response_id}")` returns the entire context EXCEPT the last output
#      Reference:
#      - https://community.openai.com/t/unable-to-retrieve-full-historic-responses-via-openai-responses-api/1229897
#      - https://community.openai.com/t/unexpected-model-behavior-when-using-previous-response-id-in-responses-api/1150739
#
#
# 2. Data retention policy confusion:
#    - Unclear documentation regarding data persistence
#    - Reference: https://community.openai.com/t/how-long-do-previous-messages-in-the-previous-response-id-last/1280341
#
# Recommendation: Switch to Responses API but don't use server-side state management yet.
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
from openai import AzureOpenAI  # The `AzureOpenAI` library is used to interact with the Azure OpenAI API.
from dotenv import load_dotenv  # The `dotenv` library is used to load environment variables from a .env file.
import os                       # Used to get the values from environment variables.

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
# Define system prompt
# and other parameters
# --------------------------------------------------------------
system_prompt = "You are a sarcastic AI assistant. You are proud of your amazing memory"
temperature = 0.7
max_tokens = 1000

# --------------------------------------------------------------
# Start a loop to keep the conversation going
# --------------------------------------------------------------
# The loop will continue until the user decides to exit.
# In each iteration, the user will be prompted to enter a question.
# ---------------------------------------------------------------

previous_response_id = None

while True:
    # --------------------------------------------------------------
    # Get user input and add it to the conversation history
    # --------------------------------------------------------------
    question = input("Enter your question (type 'exit' to quit): ").strip()
    
    # Exit the loop if user types 'exit'
    if question.lower() == 'exit':
        print("Goodbye!")
        break

    try:
        # --------------------------------------------------------------
        # Call the Azure OpenAI API to get the AI's response
        # --------------------------------------------------------------

        response = client.responses.create(
            model= AZURE_OPENAI_MODEL,
            instructions=system_prompt, 
            input=question,
            previous_response_id=previous_response_id, # None for the first question, then set to the previous response's id
            temperature=temperature,
            max_output_tokens=max_tokens
        )

        answer = response.output_text
        response_id = response.id
        previous_response_id = response.previous_response_id

        print(f"\nAnswer from AI = {answer}")
        print(f"response id = {response.id}")
        print(f"previous response id = {response.previous_response_id}")
        print(f"input tokens = {response.usage.input_tokens}")
        print(f"output tokens = {response.usage.output_tokens}")
        print(f"total tokens = {response.usage.total_tokens}")
        print("=" * 80)

        # Update the previous_response_id for the next iteration
        previous_response_id = response.id

    except Exception as e:
        print(f"Error getting answer from AI: {e}")
        continue

# --------------------------------------------------------------
# List all input items for the given response id
# and then delete the model response from the servers
# --------------------------------------------------------------
if previous_response_id is not None:
    response = client.responses.input_items.list(previous_response_id)
    print(f"Input items for response id: {previous_response_id}")
    print(response.model_dump_json(indent=4))
    print("\n**Note** There's a bug "
          "in the output of `responses.input_items.list()`. "
          "The response returns the entire context EXCEPT the 'last' output\n")

    # documentation mentions that client.responses.delete() return the status of the delete operation
    # however, in reality it is returning None
    response = client.responses.delete(previous_response_id)

    print(f"Deleted response with id: {previous_response_id}")