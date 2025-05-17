# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Code Interpreter
#
# Traditional LLMs are good at generating text, but they struggle with tasks that require maths or calculations.
#
#
# Example: How many "r"s present in the string "strawberry"?
# Answer from LLM: "strawberry" has 2 "r"s.
#
# Yikes!
#
# To solve this problem, OpenAI has introduced a feature called "Code Interpreter". 
# - Code Interpreter allows the Assistants API to write and run Python code in a sandboxed execution environment. 
# - With Code Interpreter enabled, your Assistant can now solve code, math, and data analysis problems.
#
# https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/code-interpreter?tabs=python
# https://platform.openai.com/docs/assistants/quickstart?example=without-streaming
#
#
# Steps:
# Upload a file (CSV, JSON, etc.) to Azure Server.
# Create an "assistant" using assistant API and provide this assistant access to the file
# Create a "thread" for the assistant. Purpose: analyze the file and provide results based on our instructions.
# (Why thread? Because that's how the Assistant API works)
#   - The Assistant will run Python code to analyze the file.
#   - The analysis results will be dumped to a file
# Once the thread execution is completed, the Assistant will return the results.
# Print the results
# Delete the uploaded file from the Azure Server.

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
import json

# --------------------------------------------------------------
# Load environment variables from .env file
# --------------------------------------------------------------
load_dotenv()

AZURE_OPENAI_ENDPOINT        = os.environ['AZURE_OPENAI_ENDPOINT']
AZURE_OPENAI_MODEL           = os.environ['AZURE_OPENAI_MODEL']
AZURE_OPENAI_API_VERSION     = os.environ['AZURE_OPENAI_VERSION']
AZURE_OPENAI_API_KEY         = os.environ['AZURE_OPENAI_API_KEY']

# --------------------------------------------------------------
# Create an instance of the AzureOpenAI client
# --------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = AZURE_OPENAI_API_VERSION
)

# --------------------------------------------------------------
# Step 1: Upload your file to Azure Server with an "assistants" purpose
# --------------------------------------------------------------
# What is a "purpose"?
# When you upload a file to Azure OpenAI, you need to specify the purpose of the file.
# The following purposes are supported:
# https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/code-interpreter?tabs=python#supported-file-types
#
# What file formats are supported for upload?
# https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/code-interpreter?tabs=python#supported-file-types
# --------------------------------------------------------------
file = client.files.create(
    file=open("dummy_build_data.json", "rb"), #multipart file upload requires the file to be in binary not in text
    purpose='assistants' 
)
# Use file.id to refer to the file
print(f"Uploaded file, file ID: {file.id}")
print("\n---------------------\n")

# --------------------------------------------------------------
# Note: You can't view the content of a file uploaded to Azure OpenAI purpose of "assistants"
# The following code will not work:
# uploaded_file_content = client.files.content(file.id)
# The above command will throw an error:
# openai.error.InvalidRequestError: The file content is not available for the purpose of "assistants".
# --------------------------------------------------------------

try:
    # --------------------------------------------------------------
    # Step 2: Create an "assistant" using assistant API 
    # Instruct that code_interpreter is enabled
    # and provide this assistant access to the file
    # --------------------------------------------------------------
    assistant = client.beta.assistants.create(
        model=AZURE_OPENAI_MODEL,
        name="build-analyzer-agent", # name of the agent (optional)    
        instructions="You are an AI assistant that can read and analyze JSON files. "
                "The JSON file contains Jenkins build information under the key `results`. "
                "Each entry in the `results` array contains information about a build. "
                "Build status of a build can be found by checking the `build_status` key. "
                "Build duration (time build took to complete) can be found by checking the `build_duration` key. "
                "Queue time (time build spent in queue) can be found by checking the `queue_time` key. "
                "Build label can be found by checking the `build_label` key. When somebody ask about a build, make sure to provide the build label. ",
        tools=[{"type": "code_interpreter"}],
        tool_resources={"code_interpreter":{"file_ids":[file.id]}}
    )
    print(f"A new assistant {assistant.id} created:\n")
    print(assistant)
    print("---------------------\n")

    # --------------------------------------------------------------
    # Step 3: Create a thread for the assistant
    # ---------------------------------------------------------------
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Provide Total builds and list all build statuses along their counts and percentages. "
                            "Also provide the fastest and the slowest build along with their build duration. "
                            "Also provide the build labels with the longest and shortest queue time. Provide durations too. "
                            "Also provide the average build and queue duration. "
            }
        ]
    )
    print(f"A new thread: {thread.id} created:\n")
    print(thread)
    print("---------------------\n")

    # --------------------------------------------------------------
    # Step 4: Run the thread with the assistant, capture result
    # Ones a thread is created,  you can "run" it with any assistant
    # (in real projects, you may have multiple 
    #   assistants created for different purposes)
    #
    # Also note that thread runs are asynchronous, 
    # which means you'll need to monitor their status 
    # by polling the Run object until a termination status is reached. 
    # 
    # If however, you are not bothered about streaming, 
    # then use the convenience helper method `create_and_poll`
    # that can assist both in creating the run and 
    # then polling for its completion.
    # --------------------------------------------------------------

    print(f"Running thread: {thread.id} with assistant: {assistant.id}...\n")
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    # The above code is equivalent to Thread.run() in Java

    if run.status == 'completed': 
        # https://platform.openai.com/docs/api-reference/messages/listMessages
        messages = client.beta.threads.messages.list(thread_id=thread.id, order='asc')
        # print(messages.model_dump_json(indent=4))
        for message in messages:
            text=client.beta.threads.messages.retrieve(message_id=message.id, thread_id=thread.id)
            print("\n------ Message --------\n")
            print(text.content[0].text.value)
            print("\n---------------------\n")

except Exception as e:
    print(f"Error: {e}")
finally:
    # --------------------------------------------------------------
    # Step 5: delete the original file from the server to free up space
    # --------------------------------------------------------------    
    client.files.delete(file.id)
    print(f"Deleted file, file ID: {file.id}")