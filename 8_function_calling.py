# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Function Calling
#
# In the previous example, we built a chatbot that could answer questions based on the content of a specific document.
# A key limitation of that approach is the context size — every LLM can only process a limited amount of text at once.
#
# To work around this limitation, three common strategies are:
# 1. Retrieval-Augmented Generation (RAG): Divide the document into smaller chunks and store in a database, 
#       when the user asks a question, retrieve and pass only the most relevant chunks to the model for answer.
# 2. Function Calling: Instead of giving all the information to the model upfront, define functions that can fetch information from external sources.
#    Then based on the user’s question, let the model decide whether to call one of these functions to formulate the answer.
# 3. SQL strategy: If the data is stored in a database, the model can generate SQL queries.
#
# In this example, we'll show how to use function calling so the model can automatically fetch relevant information from an external source when needed
# 
# This example is based on the tutorial: 
# - https://youtu.be/aqdWSYWC_LI?si=fMi8Mj-XMatQU_Ze
# - https://github.com/Azure-Samples/openai/blob/main/Basic_Samples/Functions/working_with_functions.ipynb
#
#
# How function calling works:
# 1. Define functions that can fetch information from external sources.
# 2. Create a `function_descriptions` dictionary that describes the available functions, their parameters, and expected behavior.
# 3. Pass the `function_descriptions` dictionary along with the user input to the Azure OpenAI chat completion API.
#
# Azure OpenAI chat completion API "WITHOUT" function calling:
#    response = client.chat.completions.create(
#        model=deployment_name,
#        messages=messages,
#    )
#
# Azure OpenAI chat completion API "WITH" function calling:
#   response = client.chat.completions.create(
#       model=deployment_name,
#       messages=messages,
#       tools=function_descriptions, # Pass the function descriptions dictionary
#       tool_choice="auto"           # Allow the model to choose which function to call
#   )
#
# 4. Use the model’s response to call your API or function
# 5. Call the chat completions API again, and include the response from your function to get a final response
#
# It's important to note that while the models can generate function calls, 
# it's up to the script developer to execute them.

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
# Formulate questions that LLM can correctly answer 
# only if it has access to internal data sources
# --------------------------------------------------------------
questions = [
    "Show me the status of build 12345 for XYZ120?",
    "Who triggered XYZ12 build 1343?",
    "What is the build duration of XYZ 1.1MAIN job 82?",
    "Who triggered XYZ 2_0_MAIN 1234?",
    "Show me the last build of the XYZ 1.2",
    "Show me the latest build of the XYZ12",
    "Show me the first build of the XYZ 1 2 MAIN",
    "Who triggered XYZ_1_2_MAIN?"
]

for question in questions:
    print(f"Question: {question}")
    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL,  # model = "deployment_name".
        messages=[{"role": "user", "content": question}],
    )
    output = response.choices[0].message.content
    print(f"Response without context: {output}\n")

# --------------------------------------------------------------
# Without access to our internal build-related data sources, 
# LLM has failed to correctly answer the above questions
# ---------------------------------------------------------------

# --------------------------------------------------------------
# Define functions to aid the LLM in answering 
#  internal build-related questions
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
# Add the `function_descriptions` dictionary to the payload 
# to enable Azure OpenAI's function calling capabilities.
# --------------------------------------------------------------
print("-----------------------------------------------------")
print("Asking LLM questions with function calling")
print("-----------------------------------------------------")
conversation=[{"role": "system", "content": "You don't assume anything. If anything is not clear, you ask for clarification."}]
for question in questions:    
    print(f"Question: {question}")
    conversation.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL,  # model = "deployment_name".
        messages=conversation,
        temperature=0, # set randomness to 0 to get deterministic results
        
        # Additional parameters to enable function calling
        tools=function_descriptions, # Pass the function_descriptions dictionary
        tool_choice="auto"           # Allow the model to choose which function to call
    )

    # Collect the LLM response
    response_message = response.choices[0].message

    #----------------------------------------------------------------
    # if the model finds that the user query requires a function call to answer, then:
    # function name        = response.choices[0].message.tool_calls[0].function.name
    # function parameters  = response.choices[0].message.tool_calls[0].function.arguments
    #
    # function name will be a string, and function parameters will be a JSON string
    # - Use json.loads() to convert the JSON string to a Python dictionary
    # - Use eval() to convert the function name string to a callable function
    # 
    # if response.choices[0].message.tool_calls is None, 
    # then the model did not find any function to call.
    # In that case, print the response directly.
    # response.choices[0].message.content
    #----------------------------------------------------------------

    # If the model did not find any function to call, print the response directly
    if response_message.tool_calls is None:
        print("------------------------------------------------------")
        print(f"*** No matching function found. Response from AI *** \n {response_message.content}\n") 
    else:
        chosen_function = response_message.tool_calls[0].function.name
        function_params = json.loads(response_message.tool_calls[0].function.arguments)
        print(f"Chosen function: {chosen_function}")
        print(f"Function parameters: {function_params}\n") 

        function_to_call = eval(chosen_function) # Convert the function name to a callable function
        function_response = function_to_call(**function_params)  # Call the function with the parameters
        print(f"Function response: {function_response}\n")

        # ---------------------------------------------------------------
        # Second API call: Get the final response from the model
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
                "content": function_response
            }
        ) 
        
        final_response = client.chat.completions.create(
            model=AZURE_OPENAI_MODEL,  # model = "deployment_name".
            messages=conversation,     # message contains the system message, 
                                        # user question,
                                        # chosen function name and arguments from LLM
                                        # and function response from the function
            temperature=0            # set randomness to 0 to get deterministic results
        )
        print("------------------------------------------------------")
        print("Final response from LLM:\n")
        print(final_response.choices[0].message.content)

    print("-----------------------------------------------------\n")