from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resp = client.responses.create(
    model="gpt-4o",
    tools=[
        {
            "type": "mcp",
            "server_label": "data_visualizer_mcp",  # MUST match FastMCP name
            "server_url": "http://127.0.0.1:8000/mcp",
            "require_approval": "never",
        }
    ],
    input="List available tools"
)

print(resp.output_text)
print("Tools available from MCP server:")