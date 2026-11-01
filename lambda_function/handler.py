import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.graph.workflow import app

def lambda_handler(event, context):
    """aws lambda entrypoint for our multiagent research pipeline
    aws accepts json payloads such as {"query:"search question"}"""

    print(f"received lambda event:{json.dumps(event)}")
    try:
        if "body" in event: # via api gateway
            body =json.loads(event["body"]) if isinstance(event["body"],str) else event["body"]
            query = body.get("query","default research query")
        else: # direct invocation or aws console test or sdk call
            query = event.get("query","how is the weather today")

        print(f"executing research workflow for querying: {query}")

        initial_state={
                "query":query,
                "search_result":[],
                "summary":"",
                "fact_check_score":0.0,
                "retry_count":0,
                "status":"initialized"
            }
        final_state=app.invoke(initial_state)
        response_payload={ # successful response format
                "query":query,
                "summary":final_state.get("summary"),
                "fact_check_score":final_state.get("fact_check_score"),
                "retry_count":final_state.get("retry_count"),
                "status":"success"
        

        }

        return{
            "statusCode": 200,
            "headers": {"Content-Type":"application/json"},
            "body": json.dumps(response_payload)

        }
    except Exception as e:
        print(f"error during lambda execution:{str(e)}")
        return{
             "statusCode": 500,
            "headers": {"Content-Type":"application/json"},
            "body": json.dumps({
                "error":str(e),
                "status":"failed"

            })
        }
                




        