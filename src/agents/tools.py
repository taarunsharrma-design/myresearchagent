import requests
from config.settings import SERPER_API_KEY, ADD_MAX_RESULT

def search_web(query:str, num_results:int=5)-> list:
    url="https://google.serper.dev/search"
    payload= {
        "q":query,
        "num":num_results+ADD_MAX_RESULT
    }
    headers={"X-API-KEY":SERPER_API_KEY,"CONTENT-TYPE":"application/json"}

    try:

        response=requests.post(url,json=payload,headers=headers,timeout=10)
        response.raise_for_status()
        data=response.json()
        result=[]

        for item in data.get("organic", ()):
            result.append({
                "title":item.get("title"),
                "snippet":item.get("snippet"),
                "link":item.get("link")
            })
        return result

    except Exception as e:
        print(f"Error Fetching Search Result{e}")
        return[]
    


    
