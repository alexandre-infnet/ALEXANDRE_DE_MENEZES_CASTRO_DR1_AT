import time
import streamlit as st


def show_progress_bar():
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)
    time.sleep(1)
    my_bar.empty()
