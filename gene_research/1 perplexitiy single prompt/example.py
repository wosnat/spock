import asyncio
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

# Define a simple tool for demonstration
def get_weather(city: str) -> str:
    '''A simple tool that returns a weather message for a given city.'''
    return f"It's sunny in {city}!"

# Create the ReAct agent
checkpointer = InMemorySaver()
agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    checkpointer=checkpointer
)

# Define the main async function
async def run_agent():
    config = {"configurable": {"thread_id": "1"}}
    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="what is the weather in sf")]},
        config
    )
    print("Agent response:", response["messages"][-1].content)

# Run the agent using asyncio
if __name__ == "__main__":
    asyncio.run(run_agent())