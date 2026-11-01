from typing import List, Dict, Any, TypedDict
class ResearchState(TypedDict):
    query:str
    search_result:List[Dict[str,Any]]
    summary:str
    fact_check_score:float
    retry_count:int
    status:str
    

