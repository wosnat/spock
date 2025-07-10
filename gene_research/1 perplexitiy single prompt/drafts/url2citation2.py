#/usr/bin/env python
##-- coding: utf-8 -*-

# %%

"""Create a React agent with a tool and visualize the graph."""
from dotenv import load_dotenv



# the agent prebuilt imports
import asyncio
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver

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
bibtex_example = ''' 
# Example of bibtex format:
@article{10.1093/ismejo/wraf106,
    author = {Sheyn, Uri and Poff, Kirsten E and Eppley, John M and Leu, Andy O and Bryant, Jessica A and Li, Fuyan and Romano, Anna E and Burger, Andy and Barone, Benedetto and DeLong, Edward F},
    title = {Mesoscale eddies shape Prochlorococcuscommunity structure and dynamics in the oligotrophic open ocean},
    journal = {The ISME Journal},
    pages = {wraf106},
    year = {2025},
    month = {05},
    abstract = {Mesoscale eddies, horizontally rotating currents sometimes referred to as “ocean weather,” influence open ocean macronutrient distributions, primary production, and microbial community structure. Such eddies impact ecosystems like the North Pacific Subtropical Gyre, where year-round thermal stratification limits the mixing of subsurface macronutrients with surface waters. Populations of the dominant primary producer Prochlorococcusin the North Pacific Subtropical Gyre consist of genetic variants with differential adaptive traits to light intensity, temperature, and macronutrient availability. How Prochlorococcuspopulation variants respond to transient, localized environmental changes, however, remains an open question. Leveraging microbial community phylogenetic, metagenomic, and metatranscriptomic data, we report here a consistent, specific enrichment of Prochlorococcushigh-light I ecotypes around the deep chlorophyll maximum in cyclonic eddies, but not adjacent anticyclonic eddies. The shallower deep chlorophyll maximum depths of cyclones had lower temperatures, higher light intensities, and elevated nutrient concentrations compared to adjacent anticyclones, which favored Prochlorococcushigh-light I ecotype proliferation. Prochlorococcushigh-light I ecotypes in the cyclone deep chlorophyll maximum exhibited unique genetic traits related to nitrogen metabolism and were enriched in gene transcripts associated with energy production, cell replication, and proliferation. Prochlorococcusgene transcripts involved in amino acid transport, metabolism, and biosynthesis were also elevated in the cyclone. These results suggest the potential importance of nitrogen metabolism in Prochlorococcushigh-light I ecotype proliferation in cyclonic eddies. Our findings demonstrate how mesoscale eddies shape microbial community structure in the oligotrophic ocean and how Prochlorococcuscommunities respond to short-term localized environmental variability.},
    issn = {1751-7362},
    doi = {10.1093/ismejo/wraf106},
    url = {https://doi.org/10.1093/ismejo/wraf106},
    eprint = {https://academic.oup.com/ismej/advance-article-pdf/doi/10.1093/ismejo/wraf106/63350536/wraf106.pdf},
}
'''

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

checkpointer = InMemorySaver()


agent_chain = create_react_agent(
    llm,
    tools=playwright_tools,
    #response_format=Reference,
    checkpointer=checkpointer,
)

#agent_chain.get_graph().draw_mermaid_png()


# %%
system_message = SystemMessage(
    content="You are a helpful research assistant. Your task is to help create a list of citations for a paper. Use the bibtex format."
)
user_message = HumanMessage(
    content="what is the citation of url: https://sfamjournals.onlinelibrary.wiley.com/doi/10.1046/j.1462-2920.2003.00456.x"
)

# Define the main async function
async def run_agent():

    config = {"configurable": {"thread_id": "1"}}
    response = await agent_chain.ainvoke(
        {"messages": [system_message, user_message]},
        config
    )
    print("Agent response:", response["messages"][-1].content)

# Run the agent using asyncio
if __name__ == "__main__":
    asyncio.run(run_agent())


