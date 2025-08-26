# --------------------------------------------------------------
# Azure OpenAI - Responses API: Function Calling
#
# In terms of Function Calling, not much has changed. 
# The main difference is in the emphasis of the term "tools"
#
# Tools allow LLMs to perform tasks beyond their native text generation capabilities. 
#
# Responses API comes with a number of built-in tools like web search, file search, 
# computer use, image generation and remote MCPs.
#
# To define your "own" tools, you write "functions" and make them available to LLMs
#
# In a nutshell:
# - Functions are tool "types" that a model has access to.
# - Functions are made available to LLMs by defining a JSON schema.
#
# Also note that function is not the only tool type. 
# For example, "custom_tool" is another tool type.
# https://platform.openai.com/docs/guides/function-calling#custom-tools
#
# Other key changes:
# - JSON schema slightly changed (less complex)
# - response.choices[0].finish_reason == "tool_calls" in Chat Completions API 
#   is now response.output[0].type == "function_call" in Responses API
# - The model can now return multiple function call requests in a single response


# --------------------------------------------------------------
# Prerequisites <<NO CHANGE>>
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
# Import Modules <<NO CHANGE>>
# --------------------------------------------------------------
from openai import AzureOpenAI             # The `AzureOpenAI` library is used to interact with the Azure OpenAI API.
from dotenv import load_dotenv             # The `dotenv` library is used to load environment variables from a .env file.
import os                                  # Used to get the values from environment variables.
import json                                # The `json` library is used to work with JSON data in Python.

# --------------------------------------------------------------
# Load environment variables from .env file <<NO CHANGE>>
# --------------------------------------------------------------
load_dotenv("../.env")

AZURE_OPENAI_ENDPOINT        = os.environ['AZURE_OPENAI_ENDPOINT']
AZURE_OPENAI_MODEL           = os.environ['AZURE_OPENAI_MODEL']
AZURE_OPENAI_API_VERSION     = os.environ['AZURE_OPENAI_VERSION']
AZURE_OPENAI_API_KEY         = os.environ['AZURE_OPENAI_API_KEY']

# --------------------------------------------------------------
# Create an instance of the AzureOpenAI client <<NO CHANGE>>
# --------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = AZURE_OPENAI_API_VERSION
)

# --------------------------------------------------------------
# Define functions to aid the LLM in answering user queries 
# <<NO CHANGE>>
# --------------------------------------------------------------
def get_build_information(product_name, branch_name, build_id):
    """
    Function to get detailed information about a specific build.
    """
    # Simulate fetching data from an internal system
    build_info = {
        "product_name": product_name,
        "branch_name": branch_name,
        "build_id": build_id,
        "build_label": f"Build #{build_id}",
        "build_url": f"https://builds.artifactory.com/{product_name}/{branch_name}/{build_id}",
        "build_log": f"https://logs.artifactory.com/{product_name}/{branch_name}/{build_id}",
        "build_duration": "2 hours",
        "build_triggered_by": "Mark Twain",
        "build_triggered_time": "2023-10-01T12:00:00Z",
        "build_status": "successful",
        "stages": [
            {
                "stage_name": "Build",
                "status": "successful",
                "duration": "1 hour",
                "logs_url": f"https://logs.artifactory.com/{product_name}/{branch_name}/{build_id}/build"
            },
            {
                "stage_name": "Test",
                "status": "successful",
                "duration": "2 hour",
                "logs_url": f"https://logs.artifactory.com/{product_name}/{branch_name}/{build_id}/test"
            }
        ]
    }

    return json.dumps(build_info, indent=4)


def get_last_build(product_name, branch_name):
    """
    Function to get the last successful build information.
    """
    # Simulate fetching last build data
    build_info = {
        "product_name": product_name,
        "branch_name": branch_name,
        "build_id": "12345",
    }

    return json.dumps(build_info, indent=4)


# --------------------------------------------------------------
# Define a "tool" dictionary that describes the available functions, 
# their parameters, and expected behavior.
#
# JSON schema slightly changed (less complex)
# Also its better to name the dictionary as "tool_descriptions" 
# instead of "function_descriptions"
# --------------------------------------------------------------
tool_descriptions = [
    {
        "type": "function",
        "name": "get_build_information", # Make sure this matches the function name
        "description": "Get detailed information about a specific build. "
                        "Build information includes product name, branch name, build Id, build label, "
                        "build URL, build duration, build log, build triggered by, build triggered time, "
                        "build status, and its stages.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {  # Make sure this matches the function parameter name
                    "type": "string",
                    "description": "The product name, e.g. XYZ"
                },
                "branch_name": { # Make sure this matches the function parameter name
                    "type": "string",
                    "description": "The branch name, e.g. XYZ_1_2_MAIN, XYZ_1_1_MAIN. "
                                    "User might ask for XYZ 120, XYZ 12, XYZ_1_2, XYZ 1.2, XYZ 120 etc., what they mean is XYZ_1_2_MAIN"
                                    "Similarly User might ask for XYZ 110, XYZ 11, XYZ_1_1, XYZ 1.1, XYZ 110 etc., what they mean is XYZ_1_1_MAIN", 
                },
                "build_id": { # Make sure this matches the function parameter name
                    "type": "string",
                    "description": "The build ID, e.g. 12345",
                },
            },
            "required": ["product_name", "branch_name", "build_id"], # Make sure this matches the function parameter name
        }   
    },
    {
        "type": "function",
        "name": "get_last_build",  # Make sure this matches the function name
        "description": "Get information of last build for the given product and branch."
                        "This function is not to be called if the user asks for a specific build ID or"
                        "calls for first build"
                        "The function returns a json containing last build's information."
                        "Format: { \"product_name\": product_name, \"branch_name\": branch_name, \"build_id\": build_id}",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {  # Make sure this matches the function parameter name
                    "type": "string",
                    "description": "The product name, e.g. XYZ"
                },
                "branch_name": {  # Make sure this matches the function parameter name
                    "type": "string",
                    "description": "The branch name, e.g. XYZ_1_2_MAIN, XYZ_1_1_MAIN. "
                                    "User might ask for XYZ 120, XYZ 12, XYZ_1_2, XYZ 1.2, XYZ 120 etc., what they mean is XYZ_1_2_MAIN"
                                    "Similarly User might ask for XYZ 110, XYZ 11, XYZ_1_1, XYZ 1.1, XYZ 110 etc., what they mean is XYZ_1_1_MAIN", 
                },
            },
            "required": ["product_name", "branch_name"],  # Make sure this matches the function parameter name
        }
    }
]

# --------------------------------------------------------------
# Add system prompting to guide the model 
# to call functions in specific ways.
# --------------------------------------------------------------
system_prompt = "Assistant is a helpful assistant that helps users get answers to questions." \
                "Assistant has access to several tools and sometimes " \
                "you may need to call multiple tools " \
                "in sequence to get answers for your users."

# --------------------------------------------------------------
# Formulate questions that LLM can correctly answer 
# only by calling chaining multiple functions
# --------------------------------------------------------------
questions = [
    "Provide the status of last XYZ120",               #requires get_last_build() to get the build_id and then call get_build_information
    "Who triggered the last XYZ 1.2 Build?",           #answer already available in the context (conversation history), no function call needed
    "Provide the status of last build",                #intentionally asked a question without product name and branch name
    "Hello how are you?",                              #unrelated question
    "Provide the status of last XYZ120 and XYZ130 build"  #same as Q1 but will require multiple calls to "same" functions
]

# --------------------------------------------------------------
# Create an array to hold the conversation history
# --------------------------------------------------------------
conversation = []

for question in questions:
    print(f"Question: {question}")
    conversation.append({"role": "user", "content": question})

    #---------------------------------------------------------------
    # First LLM call
    # ---------------------------------------------------------------
    try:
        response = client.responses.create(      # Endpoint has changed from `chat.completions.create` to `responses.create`
            model= AZURE_OPENAI_MODEL,           # <<NO CHANGE>>
            instructions=system_prompt,          # Responses API contains a separate parameter to pass system prompt
            input=conversation,                  # `chat.completion.create` requires a `messages` array, while `responses` requires an `input` instead.
            store=False,                         # Do not store the model response at server-side

            # Additional parameters to enable function calling
            tools=tool_descriptions,             # Pass the tool_descriptions dictionary <<NO CHANGE>>
            tool_choice="auto"                   # Allow the model to choose which function to call <<NO CHANGE>>
        )
        #---------------------------------------------------------------
        # Read the response and check if LLM wanted to call a function
        # if yes: 
        # 1: Determine the function name and function params from the response
        # 2: Execute the function
        # 3: Send the (past conversations + LLM response + function response) to the next LLM call
        #
        # Rinse and repeat until the generated response doesn't 
        # contain any further function call request

        # <<Slight changes from Chat Completions API>>
        #---------------------------------------------------------------
        
        #---------------------------------------------------------------
        # Keep making LLM call(s) until generated response 
        # doesn't contain any further function call request
        #---------------------------------------------------------------
        while response.output[0].type == "function_call":   # response.choices[0].finish_reason in Chat Completions API is now response.output[0].type.
                                                            # value to search = "function_call"
            print("LLM requested function call(s) ...\n")
            
            #---------------------------------------------------------------
            # Append the last LLM's responses to the next LLM's input
            #---------------------------------------------------------------
            conversation += response.output

            #---------------------------------------------------------------
            # Since a LLM response can include zero, one, or multiple 
            # function calls, it is best to assume there are several.
            #---------------------------------------------------------------
            for response_message in response.output: # iterate through the LLM responses
                
                # Skip non-function call responses
                if response_message.type != "function_call": 
                    continue                                
                
                #---------------------------------------------------------------
                # Determine the function and function params from the response
                #---------------------------------------------------------------
                # Each entry with type "function call" will have a call_id, name, and JSON-encoded arguments.
                call_id         = response_message.call_id
                chosen_function = response_message.name                    # response.choices[0].message.tool_calls[0].function.name is now response.output[0].name
                function_params = json.loads(response_message.arguments)   # response.choices[0].message.tool_calls[0].function.arguments is now response.output[0].arguments
                print(f"Chosen function: {chosen_function}")
                print(f"Function parameters: {function_params}\n") 
                
                #---------------------------------------------------------------
                # Execute the function
                #---------------------------------------------------------------
                function_to_call = eval(chosen_function)                    # Convert the function name to a callable function
                function_response = function_to_call(**function_params)     # Call the function with the parameters
                print(f"Function response: {function_response}\n")

                #---------------------------------------------------------------
                # Append the function response to the next LLM's input
                # ---------------------------------------------------------------
                conversation.append({
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": str(function_response)
                })

                # loop to iterate through model responses ends. Function responses collected in `conversation` array

            #---------------------------------------------------------------
            # Next LLM call
            # ---------------------------------------------------------------            
            try:
                response = client.responses.create(  
                    model=AZURE_OPENAI_MODEL, 
                    instructions=system_prompt, 
                    input=conversation, # past conversations + last LLM responses + function responses
                    store=False,
                    tools=tool_descriptions,
                    tool_choice="auto" 
                )
            except Exception as e:
                print(f"Error getting answer from AI: {e}")
                continue

        # --------------------------------------------------------------
        # Last LLM response was devoid of any function call request
        # implying that the response is the final answer to the user's query
        # --------------------------------------------------------------
        print("=" * 80)
        print("Final response from LLM:\n")
        print(response.output_text)
        print("=" * 80)
        print("LLM answer was based on the following context:\n")
        for item in conversation:
            print(f"{item}\n")
        print("=" * 80)
        
        # --------------------------------------------------------------
        # Append the assistant's response to the conversation history
        # --------------------------------------------------------------
        conversation.append({"role": "assistant", "content": response.output_text})

    # Catch any exceptions that occur during the request
    except Exception as e:
        print(f"Error getting answer from AI: {e}")
        continue

