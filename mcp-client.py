import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

#Get the Gemini API key from the environment variable
api_key = os.environ.get("GROQ_API_KEY") # Note: corrected variable name based on convention
model_name = os.environ.get("GROQ_MODEL_NAME")

#Create Gemini instance LLM class
model = ChatGroq(
    model_name=model_name, api_key=api_key
)

async def main():
    async with MultiServerMCPClient(
        {
            # "items-python": {
            #     "command": "python",
            #     "args": ["client.py"],
            #     "transport": "sse"
            # }
            # Add more of your own servers here, works with remote servers
            "items": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        # Create ReAct Agent with MCP servers
        graph = create_react_agent(model, client.get_tools())

        # Initialize conversation history using simple tuples
        inputs = {"messages": []}

        print("Agent is ready. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Exiting chat.")
                break

            # Append user message to history
            inputs["messages"].append(("user", user_input))

            # Call our graph with streaming to see the steps
            async for state in graph.astream(inputs, stream_mode="values"):
                last_message = state["messages"][-1]
                last_message.pretty_print()

            # Update the inputs with the agent's response
            inputs["messages"] = state["messages"]

if __name__ == "__main__": # Note: corrected dunder name
    asyncio.run(main())
