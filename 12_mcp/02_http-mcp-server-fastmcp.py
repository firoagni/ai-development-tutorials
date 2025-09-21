# --------------------------------------------------------------
# Getting Started with MCP: Using FastMCP to create a MCP server 
# and expose it as a web service
#
# The only change you will find from the previous example 
# is the transport method parameters used to run the server.
# --------------------------------------------------------------

# --------------------------------------------------------------
# Prerequisites
# 1. Make sure that python3 is installed on your system.
# 2. Create and Activate a Virtual Environment:
# `python3 -m venv venv`
# `source venv/bin/activate`
# 3. The required libraries are listed in the requirements.txt file. Use the following command to install them:
#    `pip3 install -r requirements.txt`
#---------------------------------------------------------------

from fastmcp import FastMCP
import json
import sys
from typing import Annotated
from pydantic import Field

# ----------------------------------------------
# Step 1: Instantiate an MCP server.
#  
# <<NO CHANGE FROM LAST EXAMPLE>>
# ----------------------------------------------
mcp = FastMCP("build-server-http")

# ----------------------------------------------
# Step 2: To all the function you wish to expose via MCP,
# add the @mcp.tool() decorator.
# <<NO CHANGE FROM LAST EXAMPLE>>
# ----------------------------------------------
@mcp.tool()
def get_build_information(
        product_name: Annotated[str, Field(description="The product name, e.g. XYZ")],
        branch_name: Annotated[str, Field(description="The branch name, e.g. XYZ_1_2_MAIN, XYZ_1_1_MAIN" \
                                    "User might ask for XYZ 120, XYZ 12, XYZ_1_2, XYZ 1.2, XYZ 120 etc., what they mean is XYZ_1_2_MAIN" \
                                    "Similarly User might ask for XYZ 110, XYZ 11, XYZ_1_1, XYZ 1.1, XYZ 110 etc., what they mean is XYZ_1_1_MAIN")],
        build_id: Annotated[int, Field(description="The ID of the build.")]
    ) -> str:
    """
    Get detailed information about a specific build.
    Build information includes product name, branch name, build Id, build label,
    build URL, build duration, build log, build triggered by, build triggered time,
    build status, and its stages.
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

@mcp.tool()
def get_last_build(        
        product_name: Annotated[str, Field(description="The product name, e.g. XYZ")],
        branch_name: Annotated[str, Field(description="The branch name, e.g. XYZ_1_2_MAIN, XYZ_1_1_MAIN" \
                                    "User might ask for XYZ 120, XYZ 12, XYZ_1_2, XYZ 1.2, XYZ 120 etc., what they mean is XYZ_1_2_MAIN" \
                                    "Similarly User might ask for XYZ 110, XYZ 11, XYZ_1_1, XYZ 1.1, XYZ 110 etc., what they mean is XYZ_1_1_MAIN")]
    ) -> str:
    """
    Get information of last build for the given product and branch.
    This function is not to be called if the user asks for a specific build ID or
    calls for first build.
    """
    # Simulate fetching last build data
    build_info = {
        "product_name": product_name,
        "branch_name": branch_name,
        "build_id": "12345",
    }

    return json.dumps(build_info, indent=4)
# ----------------------------------------------
# Step 3: Configure the MCP server to run 
# as a web service on http://0.0.0.0:8000/mcp
#
# Difference between 0.0.0.0 and 127.0.0.1
# - 127.0.0.1: hosted webservice will be accessible only from the host machine.
# - 0.0.0.0: Hosted webservice will be accessible even from outside of the host machine.
# ----------------------------------------------
if __name__ == "__main__":
    try:
        print("\n\n==== Starting MCP server =====")
        mcp.run(transport="http", host="0.0.0.0", port=8000, path="/mcp")
    except KeyboardInterrupt:
        print("[DEBUG] Server shutting down gracefully")
    except Exception as e:
        print(f"[ERROR] Server failed: {e}")
        sys.exit(1)


# ----------------------------------------------
# Step 4: Test the script to script to start the server
# Run this python file. You should see the message:
#
# Starting MCP server 'build-server-http' with transport 'http' on http://0.0.0.0:8000/mcp
#
# Check the screenshots in `screenshots/02_http-mcp-server-fastmcp`
# to learn how to add this server to VSCode Copilot
# ------------------------------------------------