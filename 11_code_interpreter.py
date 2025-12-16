# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Code Interpreter
#
# Traditional LLMs are good at generating text, but they struggle with tasks that require maths or calculations.
#
# Example: How many "r"s present in the string "strawberry"?
# Answer from LLM: "strawberry" has 2 "r"s.
#
# Yikes!
#
# Discussions regarding LLMs can’t count:
# - https://community.openai.com/t/should-a-custom-gpt-be-able-to-count-the-number-of-items-in-a-json-list/575999
# - https://community.openai.com/t/assistant-can-not-search-the-whole-file-using-file-search/739661/3
# - https://www.reddit.com/r/OpenAI/comments/15xfcuk/how_do_i_pass_complex_and_nested_large_json_data
#
#
# To solve this problem, OpenAI has introduced a feature called "Code Interpreter". 
# 
# With Code Interpreter enabled:
# - The LLM will generate "Python code" to solve the problem
# - The code is executed in a container.
# - If the code fails, the LLM automatically debugs and refines it until it executes successfully.
# - Based on the code execution results, the LLM generates a final answer.
#
# By writing Python code, your LLM can solve code, math, and data analysis problems now.
#
# Additional cost of using Code Interpreter:
# Code Interpreter has additional charges beyond the token based fees for Azure OpenAI usage. 
# Check: https://azure.microsoft.com/en-gb/pricing/details/cognitive-services/openai-service/

# References:
# - https://platform.openai.com/docs/assistants/tools/code-interpreter
# - https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/responses?tabs=python-key#code-interpreter
# - https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/code-interpreter?tabs=python
# - https://platform.openai.com/docs/assistants/quickstart?example=without-streaming
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
from pprint import pprint       # The `pprint` library is used to pretty-print a dictionary
import json                     # The `json` library is used to work with JSON data in Python.

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
# Step 1: Upload your file to Azure Server with an "assistants" purpose
# --------------------------------------------------------------
# What is purpose?
# When you upload a file to Azure OpenAI, you need to specify the purpose of the file.
# The following purposes are supported:
# https://learn.microsoft.com/en-us/rest/api/azureopenai/files/upload?view=rest-azureopenai-2024-10-21&tabs=HTTP#purpose
#
# What file formats are supported for upload?
# https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/code-interpreter?tabs=python#supported-file-types
# --------------------------------------------------------------
file = client.files.create(
    file=open("dummy_build_data.json", "rb"), #multipart file upload requires the file to be in binary not in text
    purpose='assistants' # This file contains data to be used by AI assistants.
)

# Use file.id to refer to the file
print(f"Uploaded file, file ID: {file.id}")

# --------------------------------------------------------------
# Note: You cannot view the content of a file uploaded 
# to the Azure OpenAI server if the purpose is defined as `assistants`
#
# The following code will not work:
# uploaded_file_content = client.files.content(file.id)
#
# The above command will throw the following error:
# openai.error.InvalidRequestError: The file content is not available for the purpose of "assistants".
# --------------------------------------------------------------

try:
    # --------------------------------------------------------------
    # Step 2: Send your request to the Azure OpenAI API, this time with Code Interpreter enabled
    # --------------------------------------------------------------
    response = client.responses.create(
        model = AZURE_OPENAI_MODEL,
        instructions = f"""
            # Instructions
            - The JSON file contains Jenkins build information under the key `results`
            - Each entry in the `results` array contains information about a build.
            - Build status of a build can be found by checking the `build_status` key.
            - Build duration (time build took to complete) can be found by checking the `build_duration` key.
            - Queue time (time build spent in queue) can be found by checking the `queue_time` key.
            - Build label can be found by checking the `build_label` key. When somebody ask about a build, make sure to provide the build label.
            """,
        input=[
            {
                "role": "user",
                "content": "Provide Total builds and list all build statuses along their counts and percentages. "
                            "Also provide the fastest and the slowest build along with their build duration. "
                            "Also provide the build labels with the longest and shortest queue time. Provide durations too. "
                            "Also provide the average build and queue duration. "
            }
        ],
        tools=[
            {
                "type": "code_interpreter", # Use code interpreter
                "container": {              # Spin up a container for the LLM to run Python code
                    "type": "auto",         # Let Azure OpenAI decide the best container type to create. The container will auto-expire if not used for 20 minutes.
                    "file_ids": [file.id]   # Add the uploaded file to the container so that LLM can access it
                }
            }
        ],
        stream=True     # Its wise to enable streaming for code_interpreter to let users see what's happening behind the scenes
    )

    # --------------------------------------------------------------
    # Step 3: Print the chunks as they come in
    # --------------------------------------------------------------
    # The incoming chunks will also contain LLM's internal monologues related to code generation and interpretation. 
    #
    # Apart from the usual chunk types, when code_interpreter is used, you may also see:
    # - `response.code_interpreter_call_code.delta`: LLM is generating code
    # - `response.code_interpreter_call_code.done`: LLM has finished generating code
    # - `response.code_interpreter_call.interpreting`: LLM code is being interpreted
    # - `response.code_interpreter_call.completed`: LLM code interpretation is complete
    #
    # API Reference:
    # https://platform.openai.com/docs/api-reference/responses-streaming/response/code_interpreter_call
    # --------------------------------------------------------------

    for chunk in response:
        if chunk.type == 'response.created': # LLM has started responding
            print("-" * 80)
            print("AI Analysis Started")
            print("-" * 80)
        elif chunk.type == 'response.code_interpreter_call_code.delta': # LLM is generating code in chunks. Keep printing them as they come in
            code = chunk.delta
            print(code, end='', flush=True)
        elif chunk.type == 'response.code_interpreter_call_code.done': # LLM has finished generating code
            print("\n")
            print("-" * 80)
            print("Code generation complete.")
        elif chunk.type == 'response.code_interpreter_call.interpreting': # LLM code is being interpreted
            print("Code is being interpreted...")
        elif chunk.type == 'response.code_interpreter_call.completed': # LLM code interpretation is complete
            print("Code interpretation complete ...")
            print("-" * 80)
        elif chunk.type == 'response.output_text.delta': # LLM is responding in chunks. Keep printing them as they come in
            partial_llm_response = chunk.delta
            print(partial_llm_response, end='', flush=True)
        elif chunk.type == 'response.output_text.done': # LLM response is complete
            print("\n")
            print("-" * 80)
        elif chunk.type == 'response.completed': # LLM has finished responding
            print("Analysis Complete")
            print("-" * 80)
        elif chunk.type == 'response.error': # Error occurred
            print(f"\nError from LLM: {chunk.error.message}")
            break

except Exception as e:
    print(f"\nError getting answer from LLM: {e}")
finally:
    # --------------------------------------------------------------
    # Step 4: delete the original file from server to free up space
    # --------------------------------------------------------------    
    client.files.delete(file.id)
    print(f"Deleted file, file ID: {file.id}")
