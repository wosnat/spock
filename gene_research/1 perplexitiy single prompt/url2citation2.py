#/usr/bin/env python
##-- coding: utf-8 -*-

# %%

"""Create a React agent with a tool and visualize the graph."""
from dotenv import load_dotenv



# the agent prebuilt imports
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import asyncio


from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


# %%
# playwright imports
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import (
    create_async_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.\n",	  },
)


# %%



# %%
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



# %%
# load dotenv
# This is needed to load the environment variables from the .env file
load_dotenv(override=True)


# %%
# This import is required only for jupyter notebooks, since they have their own eventloop
#import nest_asyncio

#nest_asyncio.apply()



# %%
# playwright tools
async_browser =  create_async_playwright_browser()  
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
playwright_tools = toolkit.get_tools()


# %%
# the model
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="gemma3", temperature=0)

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")


# %%

agent_chain = create_react_agent(
    llm,
    tools=playwright_tools,
    response_format=Reference,
)

agent_chain.get_graph().draw_mermaid_png()


# %%
# SuperFastPython.com
# example of await within a coroutine
 
# define coroutine
async def main():
    # entry point of the program
    print('Main is running')
    
    url = "https://www.langchain.com/langsmith"
    url = "https://sfamjournals.onlinelibrary.wiley.com/doi/10.1046/j.1462-2920.2003.00456.x"
    params = {"messages": [("user", f"get me a citation for the url: {url}")]}
    print(params)
    # run a coroutine
    result = await agent_chain.ainvoke(params)
    print(result)

 
# run the coroutine
asyncio.run(main())

