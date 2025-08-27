# --------------------------------------------------------------
# Getting Started with Ollama: Tool\Function Calling
#
# Tools allow LLMs to perform tasks beyond their native text generation capabilities. 
#
# To define your "own" tools, you write "functions" and make them available to LLMs
#
# In a nutshell:
# - Functions are tool "types" that a model has access to.
# - Functions are made available to LLMs by defining a JSON schema.
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
from pyexpat.errors import messages
from ollama import chat, ResponseError, pull    # chat API from Ollama. Think of OpenAI chat completion API equivalent
from dotenv import load_dotenv                  # The `dotenv` library is used to load environment variables from a .env file.
import os                                       # Used to get the values from environment variables.
import json                                     # The `json` library is used to work with JSON data in Python.
# --------------------------------------------------------------

# --------------------------------------------------------------
# Load environment variables from .env file
# --------------------------------------------------------------
load_dotenv()
MODEL = os.environ['OLLAMA_MODEL']

# --------------------------------------------------------------
# Define functions to aid the LLM in answering user queries 
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
# JSON schema same as OpenAI Chat Completion API, which is a bit
#                            different from OpenAI Responses API
# --------------------------------------------------------------
tool_descriptions = [
    {
        "type": "function",
        "function": {
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
        }
    },
    {
        "type": "function",
        "function": {
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
    }
]

# --------------------------------------------------------------
# Important:
# Add system prompting to guide the model 
# to call functions in specific ways.
# --------------------------------------------------------------
conversation=[{"role": "system", "content": "Assistant is a helpful assistant that helps users get answers to questions."
                                            "Assistant has access to several tools and sometimes "
                                            "you may need to call multiple tools "
                                            "in sequence to get answers for your users."}]

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

for question in questions:
    print(f"Input: {question}")
    conversation.append({"role": "user", "content": question})
    #---------------------------------------------------------------
    # First LLM call
    #
    # Pass function JSON schema to `tools` attribute 
    # <<SAME in OpenAI Responses API>>
    # 
    # Note: `tool_call` attribute in OpenAI APIs is 
    # not available in Ollama API
    # ---------------------------------------------------------------
    try:
        response = chat(
            model = MODEL,
            messages = conversation,
            tools = tool_descriptions, # Pass the tool_descriptions dictionary
            options = {
                "temperature": 0, # Make responses more deterministic
            }
        )
       
        # --------------------------------------------------------------
        # Print the response for debugging
        # --------------------------------------------------------------
        # print(f"DEBUG:: Complete response from LLM:\n{response.model_dump_json(indent=4)}")

        #---------------------------------------------------------------
        # Read the response and check if LLM wanted to call a function
        # if yes: 
        # 1: Determine the function name and function params from the response
        # 2: Execute the function
        # 3: Send the (past conversations + LLM response + function response) to the next LLM call
        #
        # Rinse and repeat until the generated response doesn't 
        # contain any further function call request
        #---------------------------------------------------------------

        #---------------------------------------------------------------
        # Keep making LLM call(s) until generated response 
        # doesn't contain any further function call request
        #---------------------------------------------------------------
        while response.message.tool_calls:
            print("LLM requested function call(s) ...\n")
            
            #---------------------------------------------------------------
            # Append the last LLM's responses to the next LLM's input
            #---------------------------------------------------------------
            conversation.append(response.message)
            
            #---------------------------------------------------------------
            # Since a LLM response can include zero, one, or multiple 
            # function calls, it is best to assume there are several.
            #---------------------------------------------------------------
            for response_message in response.message.tool_calls: # iterate through the LLM responses
                #---------------------------------------------------------------
                # Determine the function and function params from the response
                #---------------------------------------------------------------                
                chosen_function = response_message.function.name
                function_params = response_message.function.arguments
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
                    "role": "tool",                     # OpenAI responses API equivalent -> "type": "function_call_output" in   
                    "tool_name": chosen_function,       # OpenAI responses API equivalent -> "call_id": call_id,         
                    "content": str(function_response),  # OpenAI responses API equivalent -> "output": str(function_response)
                })

                # loop to iterate through model responses ends. Function responses collected in `conversation` array

            #---------------------------------------------------------------
            # Next LLM call
            # --------------------------------------------------------------
            try:
                response = chat(
                    model = MODEL,
                    messages = conversation, # past conversations + last LLM responses + function responses
                    tools = tool_descriptions,
                    options = {
                        "temperature": 0,
                    }
                )
            except Exception as e:
                print('Error getting answer from AI:', e)
                continue
        
        # --------------------------------------------------------------
        # Last LLM response was devoid of any function call request
        # implying that the response is the final answer to the user's query
        # --------------------------------------------------------------
        print("=" * 80)
        print("Final response from LLM:\n")
        print(response.message.content)
        print("=" * 80)
        print("LLM answer was based on the following context:\n")
        for item in conversation:
            print(f"{item}\n")
        print("=" * 80)

        # --------------------------------------------------------------
        # Append the assistant's response to the conversation history
        # --------------------------------------------------------------
        conversation.append({"role": "assistant", "content": response.message.content})

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