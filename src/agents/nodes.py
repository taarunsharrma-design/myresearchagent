import re
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from config.settings import FACT_CHECK_MODEL, PRIMARY_MODEL
from src.agents.tools import search_web
from src.graph.state import ResearchState

primary_llm=ChatOpenAI(model=PRIMARY_MODEL,  temperature=0.2)
fact_check_llm=ChatOpenAI(model=FACT_CHECK_MODEL, temperature=0.0)

def researcher_node(state:ResearchState)->Dict[str,Any]:
    """
    peforming websearch based on the query stored in state
    """
    query=state['query']
    print(f"searching for {query}")
    current_retry=state.get("retry_count",0)
    print(f"\n [researcher]:searching for{query}:(Attempt{current_retry+1}")
    result=search_web(query)
    print(f"Found {len(result)} search_result ")
    return {
        "search_result":result,
        "status":"research complete"

    }

def summarizer_node(state:ResearchState)->Dict[str,Any]:
    """
        summarize the search result in the coherent summary
    """
    print("\n [summarizing agent working]:summarizing research result")
    query=state["query"]
    result=state["search_result"]
    valid_results = [r for r in result if r.get("snippet")]

    if not valid_results:
        return {
        "summary": "No search results were found to answer",
        "status": "summary_empty",
        }

    context = "\n\n".join(
        f"Title: {r.get('title')}\nSnippet: {r.get('snippet')}"
        for r in valid_results
    )# list comprehension

    """
    formatted_results = []

    for r in results:
        text = (
            f"Title: {r.get('title')}\n"
            f"Snippet: {r.get('snippet')}"
            )
        formatted_results.append(text)

    context = "\n\n".join(formatted_results)
    """

    prompt=f"""
        based on the following search result, 
        write a comprehensive accurate summary answering the user query
        user query:{query}
        search results:{context}

    """

    messages=[SystemMessage(content="you are an expert research assistant and technical writer"),HumanMessage(content=prompt)]
    response=primary_llm.invoke(messages)
    return {
        "summary":response.content,
        "status":"summary complete"
    }


def factcheck_node(state:ResearchState)->Dict[str,Any]:
    """
        evaluate the generated summary against the search result to assign a confidence score
    """
    print("\n [factcheck agent working]:evaluating the generated summary")
    summary=state["summary"]
    result=state["search_result"]
    current_retry=state.get("retry_count",0)
    context="\n\n".join([f"Snippet:{r.get("snippet")}" for r in result])
    # list comprehension

    """
    formatted_results = []

    for r in results:
        text = (
            f"Title: {r.get('title')}\n"
            f"Snippet: {r.get('snippet')}"
            )
        formatted_results.append(text)

    context = "\n\n".join(formatted_results)
    """

    prompt=f"""
     Evaluate whether the summary accurately reflects the provided search snippets without hallucinations or unsupported claims.
    
    Search Snippets:
    {context}
    
    Summary to Evaluate:
    {summary}
    
    Respond strictly with a score between 0.0 and 1.0 representing your confidence in the summary, followed by a brief rationale. Use this exact format for the score:
    [SCORE: 0.95]
    Rationale: <your brief reasoning here>
    """

    messages=[SystemMessage(content="you are an objective strict fact checker"),HumanMessage(content=prompt)]
    response=fact_check_llm.invoke(messages)
    content=response.content
    print(content)
    score_match=re.search(r"(?:\[)?SCORE:\s*([0-9]*\.?[0-9]+)(?:\])?",content,re.IGNORECASE)
    print(score_match)
    #score=float(score_match.group(1)) if score_match else 0.5
    if score_match:
        score=float(score_match.group(1))
    else:
        print("[factcheck] could not parse score; treating as 0.0")
        score=0.0
    print(f"fact checking confidence is {score}")
    return {
        "fact_check_score":float(score),
        "retry_count":int(current_retry+1),
        "status":"fact_checking_completed"
    }
