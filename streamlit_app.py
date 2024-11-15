import streamlit as st
import pandas as pd

def main():
    st.title("DataViz")
    st.header("Dataframe:")
    st.dataframe(df)
    st.dataframe(df1)

if __name__ == "__main__":
    main()
