# --------------------------------------------------------------
# Azure OpenAI - Server Side Conversation Management
#
# Tired of manually managing conversation history by yourself? 
# Azure OpenAI API now comes with an option of server-side conversation state management.
#
# Key features:
# 1. Alternative to managing conversation state by yourself. 
# 2. If saved, a response is retained for 30 days
# 3. If you are using OpenAI's Responses API, then messages are auto-saved at server-side by default
# 4. To instruct Responses API "NOT" to save a response, set `store: false`
#
# - You can chain responses together by passing the `response.id` of the previous response 
#    to the `previous_response_id` parameter of the current response.
# - Use `responses.input_items.list("{response_id}")` to obtain 
#    the conversation history for the given response id
# - To delete a response, use `responses.delete("{response_id}")`
#
# Note: Even though conversations are saved server-side, input tokens size 
# will grow with each conversation turn as the full conversation context is sent to 
# the model in every API call.
# Therefore, monitor token usage carefully to stay within model limits and manage costs.
# Consider implementing token limit checks and conversation truncation if needed.
#
# Also note that at the time of writing, several known issues exist in the implementation:
#
# Known Issues in Current Implementation
# 1. Incomplete conversation history retrieval:
#    - `responses.input_items.list("{response_id}")` returns the entire context EXCEPT the last output
#      Reference:
#      - https://community.openai.com/t/unable-to-retrieve-full-historic-responses-via-openai-responses-api/1229897
#      - https://community.openai.com/t/unexpected-model-behavior-when-using-previous-response-id-in-responses-api/1150739
#
# 2. Data retention policy confusion:
#    - Unclear documentation regarding data persistence
#    - Reference: https://community.openai.com/t/how-long-do-previous-messages-in-the-previous-response-id-last/1280341
#
# Recommendation: Don't use server-side state management yet. Stick to your own client-side state management solution, as 
# it will be reliable and gives you more control.
# ---------------------------------------------------------------

# --------------------------------------------------------------
# Prerequisites <<NO CHANGES>>
# 1. Make sure that python3 is installed on your system.
# 2. Create and Activate a Virtual Environment:
# `python3 -m venv venv`
# `source venv/bin/activate`
# 3. The required libraries are listed in the requirements.txt file. Use the following command to install them:
#    `pip3 install -r requirements.txt`
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
load_dotenv(".env")

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
# Start a loop to keep the conversation going
# --------------------------------------------------------------
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
        # Call the Responses API to get the AI's response
        # --------------------------------------------------------------
        response = client.responses.create(
            model= AZURE_OPENAI_MODEL,
            instructions="You are a sarcastic AI assistant. You are proud of your amazing memory", 
            input=question,
            previous_response_id=previous_response_id, # None for the first question, then set to the previous response's id
            temperature=0.7,
            max_output_tokens=1000
        )

        # --------------------------------------------------------------
        # Notes:
        # 1. Server-side conversation management facilitates API call simplification:
        #   - System instructions are set via the `instructions` parameter
        #   - Current user input passed as string to the `input` parameter  
        #   - Conversation context is automatically maintained via `previous_response_id`
        #   
        #   No more cramming system instructions, the current user input, and 
        #   past conversations into a single input array -- there are clearly 
        #   defined parameters for each.
        #
        # 2. The `instructions` parameter only applies to the current response generation request. 
        #    If you are managing conversation state with the previous_response_id parameter, 
        #    the instructions used on previous turns will not be present in the context.
        #    Lesson: Always include the `instructions` parameter in every API call,
        # --------------------------------------------------------------

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