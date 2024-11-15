import streamlit as st
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/ElsincejasWasaaaaa/data/refs/heads/main/Tabladerendimientoacademico1.csv')
df1 = pd.read_csv('https://raw.githubusercontent.com/ElsincejasWasaaaaa/data/refs/heads/main/ComparativaDeSatisfaccionEstudiantil1.csv')

def main():
    st.title("DataViz")
    st.header("Dataframe:")
    st.info("Estamos probando cosas! todavia en mantenimiento")
    st.dataframe(df)
    st.dataframe(df1)

if __name__ == "__main__":
    main()
