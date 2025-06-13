import streamlit as st
from monitor import run_capture_session

st.title("VLM Monitor Prototype")

if st.button("Start Capture Session"):
    records = run_capture_session()
    st.write("Finished capturing", len(records), "screenshots")
    for r in records:
        st.text(r["meta"])

