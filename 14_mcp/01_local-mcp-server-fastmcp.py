# --------------------------------------------------------------
# Getting Started with MCP: Creating a local MCP server using FastMCP
# --------------------------------------------------------------
from fastmcp import FastMCP
import json
import sys

# ----------------------------------------------
# Step 1: Instantiate an MCP server. 
# Server Name we chose: build-server
# ----------------------------------------------
mcp = FastMCP("build-server")

# ----------------------------------------------
# Step 2: To all the function you wish to expose via MCP,
# add the @mcp.tool() decorator.
#
# - FastMCP handles schema generation from type hints 
#   and docstrings. 
# - Tools can return various types, including text, 
#   JSON-serializable objects, and even images 
#   or audio aided by the FastMCP media helper classes.
# ----------------------------------------------
@mcp.tool()
def get_build_information(product_name, branch_name, build_id):
    """
    Get detailed information about a specific build.
    Build information includes product name, branch name, build Id, build label,
    build URL, build duration, build log, build triggered by, build triggered time,
    build status, and its stages.

    args:
        product_name: The product name, e.g. XYZ
        branch_name: The branch name, e.g. XYZ_1_2_MAIN, XYZ_1_1_MAIN. 
                    User might ask for XYZ 120, XYZ 12, XYZ_1_2, XYZ 1.2, XYZ 120 etc., what they mean is XYZ_1_2_MAIN
                    Similarly User might ask for XYZ 110, XYZ 11, XYZ_1_1, XYZ 1.1, XYZ 110 etc., what they mean is XYZ_1_1_MAIN
        build_id: The ID of the build.

    returns:
        A JSON string containing the build information.
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
def get_last_build(product_name, branch_name):
    """
    Get information of last build for the given product and branch.
    This function is not to be called if the user asks for a specific build ID or
    calls for first build.

    args:
        product_name: The product name, e.g. XYZ
        branch_name: The branch name, e.g. XYZ_1_2_MAIN, XYZ_1_1_MAIN. 
                    User might ask for XYZ 120, XYZ 12, XYZ_1_2, XYZ 1.2, XYZ 120 etc., what they mean is XYZ_1_2_MAIN
                    Similarly User might ask for XYZ 110, XYZ 11, XYZ_1_1, XYZ 1.1, XYZ 110 etc., what they mean is XYZ_1_1_MAIN

    returns:
        A JSON string containing the last build's information.
        Format: { "product_name": product_name, "branch_name": branch_name, "build_id": build_id }
    """
    # Simulate fetching last build data
    build_info = {
        "product_name": product_name,
        "branch_name": branch_name,
        "build_id": "12345",
    }

    return json.dumps(build_info, indent=4)

# ----------------------------------------------
# Step 3: Run the FastMCP server by calling 
# the run() method on the server instance
# ----------------------------------------------
if __name__ == "__main__":
    try:
        print("\n\n==== Starting MCP server =====")
        mcp.run(transport="stdio") # FastMCP supports three transport protocols: stdio, http, and sse
                                   # stdio = For MCP server hosted locally
    except KeyboardInterrupt:
        print("[DEBUG] Server shutting down gracefully")
    except Exception as e:
        print(f"[ERROR] Server failed: {e}")
        sys.exit(1)


# ----------------------------------------------
# Step 4: Test the script: 
# Run this python file. If you see output similar to the following, your script is correct:
#
#/Users/agni/code/azure-open-ai-tutorials/14_mcp/venv/bin/python /Users/agni/code/azure-open-ai-tutorials/14_mcp/01_local-mcp-server-fastmcp.py
#
#
#==== Starting MCP server =====
#
#
#╭─ FastMCP 2.0 ──────────────────────────────────────────────────────────────╮
#│                                                                            │
#│        _ __ ___ ______           __  __  _____________    ____    ____     │
#│       _ __ ___ / ____/___ ______/ /_/  |/  / ____/ __ \  |___ \  / __ \    │
#│      _ __ ___ / /_  / __ `/ ___/ __/ /|_/ / /   / /_/ /  ___/ / / / / /    │
#│     _ __ ___ / __/ / /_/ (__  ) /_/ /  / / /___/ ____/  /  __/_/ /_/ /     │
#│    _ __ ___ /_/    \__,_/____/\__/_/  /_/\____/_/      /_____(_)____/      │
#│                                                                            │
#│                                                                            │
#│                                                                            │
#│    🖥️  Server name:     build-server                                       │
#│    📦 Transport:       STDIO                                               │
#│                                                                            │
#│    📚 Docs:            https://gofastmcp.com                               │
#│    🚀 Deploy:          https://fastmcp.cloud                               │
#│                                                                            │
#│    🏎️  FastMCP version: 2.11.3                                             │
#│    🤝 MCP version:     1.13.1                                              │
#│                                                                            │
#╰────────────────────────────────────────────────────────────────────────────╯
#
#
#[08/29/25 19:43:19] INFO     Starting MCP server 'build-server' with transport 'stdio'                                        server.py:1445
# ----------------------------------------------

#----------------------------------------------------------
# The above output indicates that all dependencies are met 
# and client systems in the "same machine", when configured,
# will be able to access it.
#
# Ctrl + C to exit
#-----------------------------------------------