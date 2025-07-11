#/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from IPython.display import Image, display
import gradio as gr
from langgraph.prebuilt import ToolNode, tools_condition
import requests
import os
from langchain.agents import Tool

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser

from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum

# bibtex format
# @article{10.1093/ismejo/wraf106,
#     author = {Sheyn, Uri and Poff, Kirsten E and Eppley, John M and Leu, Andy O>
#     title = {Mesoscale eddies shape Prochlorococcuscommunity structure and dyna>
#     journal = {The ISME Journal},
#     pages = {wraf106},
#     year = {2025},
#     month = {05},
#     abstract = {Mesoscale eddies, horizontally rotating currents sometimes refe>
#     issn = {1751-7362},
#     doi = {10.1093/ismejo/wraf106},
#     url = {https://doi.org/10.1093/ismejo/wraf106},
#     eprint = {https://academic.oup.com/ismej/advance-article-pdf/doi/10.1093/is>
# }


# the reference class - describe a paper
class Reference(BaseModel):
    """Reference to the literature supporting a finding"""
    title: str = Field(description="Title of the research paper")
    author: str = Field(description="Authors of the research paper, comma-separated")
    journal: str = Field(description="Journal where the research was published")
    year: int = Field(description="Year of publication")
    url: str = Field(default=None, description="URL to access the research paper")
    month: Optional[str] = Field(default=None, description="Month of publication, if available")
    abstract: Optional[str] = Field(default=None, description="Abstract of the research paper, if available")
    issn: Optional[str] = Field(default=None, description="ISSN of the journal, if available")
    # doi is a unique identifier for the paper, usually in the format "10.xxxx/xxxxx"
    # it is used to access the paper online 
    doi: Optional[str] = Field(default=None, description="DOI of the research paper, if available")
    organism: Optional[str] = Field(description="Organisms studied in this paper, if available")
    experimental_approach: Optional[str] = Field(description="Experimental approach used in the paper, if available")




# load dotenv
# This is needed to load the environment variables from the .env file
load_dotenv(override=True)


# playwright tools
async_browser =  create_async_playwright_browser()  
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
tools = toolkit.get_tools()



class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)



# openai 
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# the langgaraph graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))
graph_builder.add_conditional_edges( "chatbot", tools_condition, "tools")
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
#display(Image(graph.get_graph().draw_mermaid_png()))

config = {"configurable": {"thread_id": "10"}}

async def chat(user_input: str, history):
    result = await graph.ainvoke({"messages": [{"role": "user", "content": user_input}]}, config=config)
    return result["messages"][-1].content


gr.ChatInterface(chat, type="messages").launch()




