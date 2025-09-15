# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Function Calling
#
# Function calling (also known as tool calling), is a feature that allows an LLM to detect 
# when a function needs to be called to fulfill the user's request.
#
# To illustrate, let’s say you have defined two functions:
#
# 1. `getTemperature(city)` – Returns the temperature for a given city.
# 2. `getSuggestedAttire(temp)` – Suggests clothing based on the given temperature.
#
# Now imagine the user asks: "What should I wear in London today?".
#
# The LLM detects it doesn’t know the answer directly, but it can fulfill the request by calling functions in sequence:
# User → "What should I wear in London today?"
# LLM → Calls getTemperature("London") → 15°C
# LLM → Calls getSuggestedAttire(15) → "Light jacket"
# LLM → "It’s around 15°C in London. A light jacket should be fine."
#
# Why use function calling?
# Function calling allows you to connect LLMs to external tools and APIs, enabling them to:
# - Fetch real-time data (e.g., weather, stock prices, database values).  
# - Perform actions (e.g., send an email, trigger a workflow).  
#
# In LLM World:
# - Functions that you make available to LLMs are called "tools"
# - Systems where an LLM autonomously decides the steps needed to accomplish 
#   its task by selecting various tools available to its disposal and taking actions are called "agents".
#
# Think of it like this:
# - Tool = a single screwdriver or hammer.  
# - Agent = a handyman who knows which tool to pick, when to use it, and in what sequence to finish the job.
#
# How function calling works:
# 1. Define functions that can fetch information from external sources.
# 2. Create a `tool_descriptions` dictionary that describes the available functions, their parameters, and expected behavior.
# 3. Pass the `tool_descriptions` dictionary along with the user input to the Azure OpenAI responses API.
#
# Azure OpenAI chat completion API "WITHOUT" function calling:
#    response = client.chat.completions.create(
#        model=AZURE_OPENAI_MODEL,
#        input=messages,
#    )
#
# Azure OpenAI responses API "WITH" function calling:
#   response = client.responses.create(
#       model= AZURE_OPENAI_MODEL,
#       input=messages, 
#       tools=tool_descriptions,     # Pass the tool_descriptions dictionary
#       tool_choice="auto"           # Allow the model to choose which function to call
#   )
#
# 4. Use the model’s response to call your API or function
# 5. Call the chat completions API again, and include the response from your function to get a final response
#
# It's important to note that while the models can generate function calls, it's up to the script developer to execute them.

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
from openai import AzureOpenAI             # The `AzureOpenAI` library is used to interact with the Azure OpenAI API.
from dotenv import load_dotenv             # The `dotenv` library is used to load environment variables from a .env file.
import os                                  # Used to get the values from environment variables.
import json                                # The `json` library is used to work with JSON data in Python.

# --------------------------------------------------------------
# Load environment variables from .env file
# --------------------------------------------------------------
load_dotenv()

# --------------------------------------------------------------
# Initialize the Azure OpenAI Client
# --------------------------------------------------------------
# Extract environment variables and store them explicitly to ensure they're available
AZURE_OPENAI_ENDPOINT        = os.environ['AZURE_OPENAI_ENDPOINT']
AZURE_OPENAI_MODEL           = os.environ['AZURE_OPENAI_MODEL']
AZURE_OPENAI_API_VERSION     = os.environ['AZURE_OPENAI_VERSION']
AZURE_OPENAI_API_KEY         = os.environ['AZURE_OPENAI_API_KEY']

# Initialize the client using the extracted variables
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = AZURE_OPENAI_API_VERSION
)

deployment_name = AZURE_OPENAI_MODEL  # The deployment name of the model to use

# --------------------------------------------------------------
# Formulate questions that LLM can correctly answer 
# only by calling chaining multiple functions
# --------------------------------------------------------------
questions = [
    "Show me the status of build 12345 for XYZ120?",
    "Provide the build number of last XYZ120"
]

# Ask
for question in questions:
    print(f"Question: {question}")
    response = client.responses.create(
        model=deployment_name,
        input=[{"role": "user", "content": question}],
    )
    output = response.output_text
    print(f"Response without context: {output}\n")

# --------------------------------------------------------------
# Without access to our internal build-related data sources, 
# LLM has failed to correctly answer the above questions
# ---------------------------------------------------------------

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
conversation = [{"role": "developer", "content": system_prompt}]

# --------------------------------------------------------------
# Adding a few more questions to test the intelligence of LLM
# --------------------------------------------------------------
questions.extend([
    "Provide the status of last XYZ120",                  # requires get_last_build() to get the build_id and then call get_build_information()
    "Who triggered the last XYZ 1.2 Build?",              # answer already available in the context (conversation history), no new function call needed
    "Provide the status of last build",                   # intentionally asked a question without product name and branch name
    "Hello how are you?",                                 # unrelated question
    "Provide the status of last XYZ120 and XYZ130 build"  # same as Q1 but will require multiple calls to "same" functions
])

print("\n" + "#" * 80)
print("LLM answers with function calling")
print("#" * 80 + "\n\n")

for question in questions:
    print(f"Question: {question}")
    conversation.append({"role": "user", "content": question})

    #---------------------------------------------------------------
    # First LLM call
    # ---------------------------------------------------------------
    try:
        response = client.responses.create(      
            model= deployment_name,           
            input=conversation,
            
            # Additional parameters to enable function calling
            tools=tool_descriptions,             # Pass the tool_descriptions dictionary
            tool_choice="auto"                   # Allow the model to choose which function to call
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

                # loop to iterate through model responses ends. Response output and function responses collected in `conversation` array

            #---------------------------------------------------------------
            # Next LLM call
            # ---------------------------------------------------------------            
            try:
                response = client.responses.create(  
                    model=deployment_name, 
                    input=conversation, # past conversations + last LLM output + function responses
                    tools=tool_descriptions,
                    tool_choice="auto" 
                )
            except Exception as e:
                print(f"Error getting answer from AI: {e}")
                continue

        # Loop ends. Last LLM response doesn't contain any function call request

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