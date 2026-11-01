import streamlit as st
import os
import sys
API_URL="https://6ft9pqf6hk.execute-api.us-east-1.amazonaws.com"

st.set_page_config(
    page_title="research agent",
    layout="centered"
)
st.title("research agent")
query=st.text_input("What would you like to explore?",placeholder="example explain agentic ai", label_visibility="collapsed")
col1,col2=st.columns([1,4])
with col1:
    run_btn=st.button("run research", type="primary",use_container_width=True)
if run_btn:
    if not query.strip():
        st.warning("Please enter a valid research topic")

    else:
        initial_state={
                "query":query,
                "search_result":[],
                "summary":"",
                "fact_check_score":0.0,
                "retry_count":0,
                "status":"initialized"
            }
        with st.status("agent is working for you", expanded=True) as status:
            st.write("researcher: querying web sources")

            try:
                final_state=app.invoke(initial_state)
                status.update(label="research complete and verified", state="complete", expanded=False)

            except Exception as e:
                 status.update(label="pipeline encountered an error", state="Error")
                 st.error(f"Exception Error: {e}")
                 st.stop()

        summary=final_state.get("summary","No summary generated")
        score=final_state.get("fact_check_score", 0.0)
        retries=final_state.get("retry_count", 0)
        results=final_state.get("search_results", [])
        st.write("")
        st.markdown("###Executive Summary")
        st.markdown(f"""
        <div class = "research-card">
        {summary}
        </div>""",unsafe_allow_html=True)

        m1,m2=st.columns(2)
        with m1:
            st.metric(label="fact-check confidence", value=f"{score:.2f}/1.00")

        with m2:
            st.metric(label="refinement iteration", value=retries)

        if results:
            st.write("")
            with st.expander("view grounding sources"):
                for i, r in enumerate(results):
                    st.markdown(f"**{i+1}. [{r.get("title")}]({r.get("link")})**")
                    st.caption(r.get("snippet"))
                    st.write("")
                    
                    
            

            
            
        
        
        






