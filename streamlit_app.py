import streamlit as st
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/ElsincejasWasaaaaa/data/refs/heads/main/Tabladerendimientoacademico1.csv')
df1 = pd.read_csv('https://raw.githubusercontent.com/ElsincejasWasaaaaa/data/refs/heads/main/ComparativaDeSatisfaccionEstudiantil1.csv')

def main():
    st.title("DataViz")
    st.header("Dataframe:")
    st.info("Estamos probando cosas! todavia en mantenimiento")
    with st.expander("Tabla de Rendimiento"):
        st.dataframe(df)
    with st.expander("Tabla de Comparativa"):
        st.dataframe(df1)
    with st.sidebar:
        st.header("Opciones")
        Año = st.selectbox("Año", ("2018", "2017", "2019", "2021"))
        Universidad = st.selectbox("Universidad", ("PUCP", "UNMSM", "UPC"))
        NoseXD = st.slider("Satisfaccion", 80, 90, 43.9)

if __name__ == "__main__":
    main()
