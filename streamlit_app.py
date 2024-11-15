import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

rendimiento_url = 'https://raw.githubusercontent.com/ElsincejasWasaaaaa/data/main/Tabladerendimientoacademico1.csv'
df = pd.read_csv(rendimiento_url)


def main():
    st.title("Comparativa de Rendimiento Académico 📊")
    st.info("Comparación del rendimiento académico de los estudiantes entre años seleccionados.")

    with st.sidebar:
        st.header("Opciones de Filtro")
        videojuego_seleccionado = st.selectbox("Selecciona el Videojuego Educativo", df['videjueg_Educativo'].unique())
        anio_inicio = st.selectbox("Selecciona el Año de Inicio", sorted(df['año'].unique()))
        anio_fin = st.selectbox("Selecciona el Año de Fin", sorted(df['año'].unique()))

    df_filtrado = df[(df['videjueg_Educativo'] == videojuego_seleccionado) &
                     (df['año'].isin([anio_inicio, anio_fin]))]

    with st.expander("Tabla de Rendimiento Académico Filtrada"):
        st.dataframe(df_filtrado)
        
    if st.button("Mostrar Comparativa de Rendimiento Académico"):
        fig, ax = plt.subplots()

        rendimiento_por_universidad_anio = df_filtrado.groupby(['universidad', 'año'])['Rendimiento_Promedio'].mean().unstack()

        rendimiento_por_universidad_anio.plot(kind='bar', ax=ax)
        ax.set_xlabel("Universidad")
        ax.set_ylabel("Rendimiento Promedio")
        ax.set_title(f"Comparativa de Rendimiento Académico en {anio_inicio} y {anio_fin}")
        ax.legend(title="Año")

        st.pyplot(fig)

if __name__ == "__main__":
    main()
