import requests
import streamlit as st
API_URL=st.secrets["API_URL"]

st.title("Multi-Agent Research Assistant")
query = st.text_input("What would you like to research?")

if st.button("Run Research"):
  with st.spinner("Agents are thinking..."):
    response = requests.post(API_URL, json={"query": query})
    if response.status_code == 200:
      st.success("Research Complete!")
      st.write(response.json())
    else:
      st.error(f"Error {response.status_code}: {response.text}")
