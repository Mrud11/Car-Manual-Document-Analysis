# utils/websearch.py
from langchain.tools import DuckDuckGoSearchRun

ddg_search = DuckDuckGoSearchRun()

def web_search(query):
    """
    Perform live web search using DuckDuckGo
    """
    results = ddg_search.run(query)
    return results

