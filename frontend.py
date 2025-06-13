import streamlit as st
import threading
from monitor import run_capture_session, build_index, answer_question

st.title("VLM Monitor Prototype")

if "records" not in st.session_state:
    st.session_state.records = []
    st.session_state.index = None
    st.session_state.stop_event = threading.Event()

if not st.session_state.records:
    if st.button("Start Capture Session"):
        st.session_state.stop_event.clear()

        def runner():
            st.session_state.records = run_capture_session(st.session_state.stop_event)
            st.session_state.index = build_index(st.session_state.records)

        threading.Thread(target=runner, daemon=True).start()

    if st.button("Stop Capture"):
        st.session_state.stop_event.set()
        st.write("Stopping capture...")
else:
    st.write(f"Finished capturing {len(st.session_state.records)} screenshots")
    for r in st.session_state.records:
        st.text(r["meta"])

    question = st.text_input("Ask a question about the session:")
    if question:
        answer = answer_question(st.session_state.index, st.session_state.records, question)
        st.write(answer)
