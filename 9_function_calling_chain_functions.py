# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Function calling with function chaining
#
# In the previous example, we looked into Function Calling: 
# Instead of giving all the information to the model upfront, define functions that can fetch information from external sources.
#    Then based on the user’s question, let the model decide whether to call one of these functions to formulate the answer.
#
# In some cases, you may want to string together multiple function calls to get the desired result.
#
# Generic example:
# User: "I am in Bangalore. What attire should I wear?"
# To answer this question, the model may need to
# 1. Call a function to get the current temperature in Bangalore.
# 2. Call another function to check what attire is suitable for the current temperature. 
#
#
# In this example, we will demonstrate how to chain function calls together.
# 
# This example is based on the tutorial: 
# - https://github.com/Azure-Samples/openai/blob/main/Basic_Samples/Functions/working_with_functions.ipynb
#

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
#    AZURE_OPENAI_API_VERSION=<your_azure_openai_api_version>
#    AZURE_OPENAI_API_KEY=<your_azure_openai_api_key>
#---------------------------------------------------------------

# --------------------------------------------------------------
# Import Modules
# --------------------------------------------------------------
from openai import AzureOpenAI  # The `AzureOpenAI` library is used to interact with the Azure OpenAI API.
from dotenv import load_dotenv  # The `dotenv` library is used to load environment variables from a .env file.
import os                       # Used to get the values from environment variables.
import json                     # The `json` library is used to work with JSON data in Python.

# --------------------------------------------------------------
# Load environment variables from .env file
# --------------------------------------------------------------
# The `load_dotenv()` function reads the .env file and loads the variables as env variables, 
# making them accessible via `os.environ` or `os.getenv()`.
# --------------------------------------------------------------
load_dotenv()

AZURE_OPENAI_ENDPOINT        = os.environ['AZURE_OPENAI_ENDPOINT']
AZURE_OPENAI_MODEL           = os.environ['AZURE_OPENAI_MODEL']
AZURE_OPENAI_API_VERSION     = os.environ['AZURE_OPENAI_VERSION']
AZURE_OPENAI_API_KEY         = os.environ['AZURE_OPENAI_API_KEY']

# --------------------------------------------------------------
# Difference between os.environ[] and os.getenv()
# os.environ[] raises an exception if the variable is not found
# os.getenv() does not raise an exception, but returns None
# --------------------------------------------------------------

# --------------------------------------------------------------
# Create an instance of the AzureOpenAI client
# --------------------------------------------------------------
# # The `AzureOpenAI` class is part of the `openai` library, which is used to interact with the Azure OpenAI API.
# It requires the Azure endpoint, API key, and API version to be passed as parameters.
# ---------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = AZURE_OPENAI_API_VERSION
)

# --------------------------------------------------------------
# Define functions to aid the LLM in answering 
#  internal build-related questions
#
# Note: The function definitions are unchanged from the previous example.
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
# Use OpenAI’s Function Calling Feature
#
# Note: The `function_descriptions` spec is unchanged from the previous example.
# --------------------------------------------------------------

# First define a dictionary that describes the available functions, their parameters, and expected behavior.
function_descriptions = [
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
    "Provide the status last XYZ120 and XYZ130 build"  #same as Q1 but will require multiple calls to "same" functions
]

for question in questions:    
    print(f"Question: {question}")
    conversation.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL,  # model = "deployment_name".
        messages=conversation,
        
        # Additional parameters to enable function calling
        tools=function_descriptions, # Pass the function_descriptions dictionary
        tool_choice="auto"           # Allow the model to choose which function to call
    )

    # Step 2: check if LLM wanted to call a function
    while response.choices[0].finish_reason == "tool_calls":
        # Collect the LLM response
        response_message = response.choices[0].message

        chosen_function = response_message.tool_calls[0].function.name
        function_params = json.loads(response_message.tool_calls[0].function.arguments)
        print(f"Chosen function: {chosen_function}")
        print(f"Function parameters: {function_params}\n") 

        function_to_call = eval(chosen_function) # Convert the function name to a callable function
        function_response = function_to_call(**function_params)  # Call the function with the parameters
        print(f"Function response: {function_response}\n")

        #---------------------------------------------------------------
        # Send the info on the function call and function response to GPT
        # ---------------------------------------------------------------
        # Add assistant response to messages
        conversation.append(
            {
                "role": response_message.role, 
                "function_call": 
                {   
                    "name": response_message.tool_calls[0].function.name,
                    "arguments": response_message.tool_calls[0].function.arguments,
                },
                "content": None,
            }
        )

        # Add function response to messages
        conversation.append(
            {
                "role": "function",
                "name": chosen_function,
                "content": function_response,
            }
        ) 
        
        response = client.chat.completions.create(
            model=AZURE_OPENAI_MODEL,  # model = "deployment_name".
            messages=conversation,     # message contains the system message, 
                                        # user question,
                                        # chosen function name and arguments from LLM
                                        # and function response from the function
            tools=function_descriptions
        )

    print("------------------------------------------------------")
    print("Final response from LLM:\n")
    print(response.choices[0].message.content)
    print("---------------------------------------------------------------\n")



