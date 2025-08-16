# --------------------------------------------------------------
# Getting Started with Azure OpenAI: Reproducible Outputs
#
# By default, responses from the Azure OpenAI chat completion model are nondeterministic 
#   - asking the same question multiple times can yield different answers.
#
# If you want to obtain reproducible output for the same question, one solution 
# is to set the temperature to 0. However, setting the temperature to 0 limits 
# creativity in responses.
#
# A better solution for consistent output is to use the optional `seed` parameter.
#
# The seed parameter accepts an integer value.
#
# When provided, the model makes a "best effort" to return the same result for 
# the same parameters and same seed value.
#
# For example, by setting the same seed parameter value of, say 42, while keeping 
# all other parameters in the request the same, the system will try 
# its best to produce the same results.

# However, determinism isn't 100% guaranteed. Even in cases where 
# the seed value and all other parameters are the same across 
# API calls, it's not uncommon to still observe a degree of variability in responses. 
# 
# You will notice that while each response might have similar elements 
# and some verbatim repetition, the longer the response goes on the more they tend to diverge.
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
# The `AzureOpenAI` class is part of the `openai` library, which is used to interact with the Azure OpenAI API.
# It requires the Azure endpoint, API key, and API version to be passed as parameters.
# ---------------------------------------------------------------
client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = AZURE_OPENAI_API_VERSION
)

# --------------------------------------------------------------
# Question to ask the model
# --------------------------------------------------------------
QUESTION = "Tell me a short urban legend in 3 lines"
print("=" * 80)
print(f"Question to ask the model: {QUESTION}")
print("=" * 80)

# --------------------------------------------------------------
# Other Parameters
# --------------------------------------------------------------
SYSTEM_PROMPT = "You are a great storyteller."
TEMPERATURE = 0.9
MAX_TOKENS = 100

# --------------------------------------------------------------
# First, let's demonstrate nondeterministic responses (without seed)
# --------------------------------------------------------------
# Generate three responses to the same question without using seed parameter
# to show the natural variability in responses.
# ---------------------------------------------------------------
print("=" * 80)
print("Generating 3 responses to the same question without using seed parameter...")
print("=" * 80)

for i in range(3):
    print(f'Story Version {i + 1}')
    print('---')
    
    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_MODEL,
            # Note: No seed parameter specified
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": QUESTION}
            ]
        )
        
        print(response.choices[0].message.content)
        print("---\n")
        
    except Exception as e:
        print(f"Error getting response: {e}")
        continue

# --------------------------------------------------------------
# Now let's demonstrate reproducible responses (with seed)
# --------------------------------------------------------------
# Generate multiple responses to the same question using the same seed value
# to show how responses become more consistent and reproducible.
# ---------------------------------------------------------------
print("=" * 80)
print("Generating 3 responses to the same question using seed=42...")
print("=" * 80)
for i in range(3):
    print(f'Story Version {i + 1}')
    print('---')
    
    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_MODEL,
            seed=42,  # Setting seed for reproducible outputs
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": QUESTION}
            ]
        )
        
        print(response.choices[0].message.content)
        print("---\n")
        
    except Exception as e:
        print(f"Error getting response: {e}")
        continue

print("=" * 80)
print("Generating 3 responses to the same question using seed=20...")
print("=" * 80)
for i in range(3):
    print(f'Story Version {i + 1}')
    print('---')
    
    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_MODEL,
            seed=20,  # Setting seed for reproducible outputs
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": QUESTION}
            ]
        ) 
        
        print(response.choices[0].message.content)
        print("---\n")
        
    except Exception as e:
        print(f"Error getting response: {e}")
        continue