import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.graph.workflow import app

def run_research(query:str):
    initial_state={
        "query":query,
        "search_result":[],
        "summary":"",
        "fact_check_score":0.0,
        "retry_count":0,
        "status":"initialized"
    }

    try:
        final_state=app.invoke(initial_state)
        print(final_state.get("summary"))

    except Exception as e:
        print(f"\n [error] pipeline failed during execution:{e}")

if __name__ == "__main__":
    sample_query="What is the latest advancement in AI"

    if len(sys.argv)> 1:
        sample_query=" ".join(sys.argv[1:])

    run_research(sample_query)

    