import os

import pandas as pd
import streamlit as st
import requests

st.title("Focus Searcher")
user_input = st.text_input("Enter a query:")

if st.button("Send"):
    response = requests.post(f"{os.getenv('UVICORN_APP_URL')}/query-text", json={"text": user_input}).json()

    # Render the answer
    st.markdown("### Answer")
    st.markdown(response["answer"])

    # Display queries in a table
    st.markdown("### Function Calls (Queries)")
    df = pd.DataFrame(response["queries"], columns=["SQL Query"])
    st.dataframe(df, use_container_width=True)