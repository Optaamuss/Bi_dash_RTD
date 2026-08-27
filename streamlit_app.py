import runpy
import traceback


try:
    runpy.run_module("dashboard.app", run_name="__main__")
except Exception:
    traceback.print_exc()

    import streamlit as st

    st.error("The dashboard failed while starting. Please check Manage app > Logs for the detailed error.")
