#/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio
import aiofiles
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
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.rate_limiters import InMemoryRateLimiter

from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser
import json
import pathvalidate


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


# %%
system_message = '''
You are a helpful research assistant. Your task is to help create a list scientific citation from the given url.. Use the bibtex format. 
   
{bibtex_example}
    
Include only the bibtex without any additional text.
You will be provided with a URL to a scientific article. Your response should be the bibtex citation for the article at that URL.
If the paper abstract is available, include it in the bibtex entry under the 'abstract' field.

If you cannot find the citation, respond with 'Problem: I cannot find the citation for this URL'.
If the URL is not a scientific article, respond with 'Problem: This URL does not point to a scientific article.'
If the URL is not valid, respond with 'Problem: This URL is not valid.'
If the URL is a scientific article but you cannot access it, respond with 'Problem: I cannot access this URL.



'''


user_message = '''
What is the scientific citation (bibtex) of the paper in this url: {url}
'''


class State(TypedDict):
    
    messages: Annotated[list, add_messages]



# # %%
# import nest_asyncio
# nest_asyncio.apply()


def get_urls_list(in_dpath : str):
    all_citations = set()
    for fname in os.listdir(in_dpath):
        fpath = os.path.join(in_dpath,fname)
        with open(fpath) as fh:
            entry = json.load(fh)
            gene_name = entry['gene_name_or_id']
            citations = entry['citations']
            #print(f'{gene_name}: found {len(citations)}')
            all_citations.update(set(citations))
    print(f'found {len(all_citations)} citations')
    #print(all_citations)
    return list(all_citations)


# Define the main async function
async def run_agent(graph, all_citations, prompts, out_dpath):
    # Create individual invocations with unique thread_ids
    
    # Process with limited concurrency
    from asyncio import Semaphore
    semaphore = Semaphore(30)  # Max 30 concurrent requests
    
    async def process_single_url(i):
        async with semaphore:
            try:
                url = all_citations[i]
                config = {
                    "configurable": {"thread_id": str(i)}
                }
                prompt_params = {"bibtex_example": bibtex_example, "url": url}
                # get the prompts
                prompt = prompt_template.invoke(prompt_params)
                print(i, url, config)
                result = await graph.ainvoke(prompt, config=config)
                
                print(i,'success')
                return i, result
            except Exception as e:
                print(i,'error', str(e))
                return i, e
    
    # Run all tasks
    running_tasks = [process_single_url(i) for i, url in enumerate(all_citations)]
    
    # Process results as they complete
    import asyncio
    for completed_task in asyncio.as_completed(running_tasks):
        i, result = await completed_task
        print(i, 'print results')
        #print(result)
        url = all_citations[i]
        res_dict = dict()
        res_dict['url'] = url
        
        # Handle the result
        if isinstance(result, Exception):
            res_dict['status'] = 'error'
            res_dict['error'] = str(result)
        else:
            try:
                res_dict['status'] = 'success'
                # Get the last message content, handling both string and tool call scenarios
                last_message = result["messages"][-1]
                if hasattr(last_message, 'content'):
                    res_dict['content'] = last_message.content
                else:
                    res_dict['content'] = str(last_message)
            except Exception as e:
                res_dict['status'] = 'error'
                res_dict['error'] = f"Error processing result: {str(e)}"
        
        # Save to individual file
        fprefix = pathvalidate.sanitize_filename(url)
        fpath = os.path.join(out_dpath, f'{fprefix}_bibtex.json')
        
        async with aiofiles.open(fpath, 'w') as f:
            await f.write(json.dumps(res_dict, indent=2))
        





# Run the agent using asyncio
if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser('run perplexity to get initial gene reviews')
    parser.add_argument("--indpath", help="output dir", default='batch_results/first_pass')
    parser.add_argument("--outdpath", help="output dir", default='batch_results/citations')
    parser.add_argument("--langsmith_prefix", help="langsmith project name", default='pplx_url2citation')

    args = parser.parse_args()

    load_dotenv(override=True)

    
    os.environ["LANGSMITH_TRACING"] = 'FALSE'

    out_dpath = args.outdpath
    os.makedirs(out_dpath, exist_ok=True)

    in_dpath = args.indpath

    import nest_asyncio
    nest_asyncio.apply()

    # build the graph
    # If you get a NotImplementedError here or later, see the Heads Up at the top of the notebook
    async_browser =  create_async_playwright_browser(headless=True)  # headful mode
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
    tools = toolkit.get_tools()


    # # Initialize the models and create templates
    rate_limiter = InMemoryRateLimiter(
        requests_per_second=10,  # 50 requests per minute
        check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
        max_bucket_size=50,  # Controls the maximum burst size.
    )
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        max_retries=3,  # Will retry up to 3 times
        temperature=0, max_tokens=3000, rate_limiter=rate_limiter
    )
    

    llm_with_tools = llm.bind_tools(tools)


    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}



    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", ToolNode(tools=tools))
    graph_builder.add_conditional_edges( "chatbot", tools_condition, "tools")
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")

    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory
        )



    #The prompt template
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", user_message),
        ]
    )


    
    # update langchain project
    from datetime import datetime
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    langsmith_project = f'{args.langsmith_prefix}_{current_time}'
    os.environ["LANGSMITH_PROJECT"] = langsmith_project
    print('Setting LANGSMITH_PROJECT =', langsmith_project)

    # load the list of citations

    all_citations = get_urls_list(in_dpath)    
    prompt_params = [{"bibtex_example": bibtex_example, "url": url} for url in all_citations ]
    # get the prompts
    prompts = prompt_template.batch(prompt_params)

    # finally, run the agent
    asyncio.run(run_agent(graph, all_citations, prompts, out_dpath ))
