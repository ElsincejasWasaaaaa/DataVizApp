import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

rendimiento_url = 'https://raw.githubusercontent.com/ElsincejasWasaaaaa/data/main/Tabladerendimientoacademico1.csv'
satisfaccion_url = 'https://raw.githubusercontent.com/ElsincejasWasaaaaa/data/main/ComparativaDeSatisfaccionEstudiantil1.csv'  # Ajusta la ruta si es necesario

df_rendimiento = pd.read_csv(rendimiento_url)
df_satisfaccion = pd.read_csv(satisfaccion_url)

def main():
    st.title("Análisis Académico y Estudiantil 📊")
    st.info("Analiza el rendimiento académico y la satisfacción estudiantil a lo largo de los años.")

    with st.sidebar:
        st.header("Selecciona el Análisis")
        analisis = st.radio("Opciones", ["Rendimiento Académico", "Satisfacción y Retención"])

    if analisis == "Rendimiento Académico":
        st.header("Comparativa de Rendimiento Académico")
        st.info("Comparación del rendimiento académico de los estudiantes entre años seleccionados.")
        
        with st.sidebar:
            st.subheader("Opciones de Filtro (Rendimiento)")
            videojuego_seleccionado = st.selectbox("Selecciona el Videojuego Educativo", df_rendimiento['videjueg_Educativo'].unique())
            anio_inicio = st.selectbox("Año de Inicio", sorted(df_rendimiento['año'].unique()))
            anio_fin = st.selectbox("Año de Fin", sorted(df_rendimiento['año'].unique()))

        df_filtrado = df_rendimiento[
            (df_rendimiento['videjueg_Educativo'] == videojuego_seleccionado) & 
            (df_rendimiento['año'].isin([anio_inicio, anio_fin]))
        ]

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

    elif analisis == "Satisfacción y Retención":
        st.header("Comparativa de Satisfacción y Retención Estudiantil")

        with st.sidebar:
            st.subheader("Opciones de Filtro (Satisfacción y Retención)")
            uni1 = st.selectbox("Universidad 1", options=["UPC", "PUCP", "UNMSM"], index=0)
            uni2 = st.selectbox("Universidad 2 (diferente a la 1)", options=["UPC", "PUCP", "UNMSM"], index=1)
            anio_inicio = st.selectbox("Año de Inicio", options=[2015, 2016, 2017, 2018, 2019, 2020, 2021], index=0)
            anio_fin = st.selectbox("Año de Fin", options=[2015, 2016, 2017, 2018, 2019, 2020, 2021], index=6)

        if uni1 == uni2:
            st.error("Universidad 1 y Universidad 2 no deben ser iguales.")
        elif anio_inicio > anio_fin:
            st.error("El año de inicio debe ser menor o igual al año de fin.")
        else:
            universidades = [uni1, uni2]
            filtered_data = df_satisfaccion[
                (df_satisfaccion['Universidad'].isin(universidades)) & 
                (df_satisfaccion['Año'].between(anio_inicio, anio_fin))
            ]
            if filtered_data.empty:
                st.warning("No hay datos para los filtros seleccionados.")
            else:
                filtered_data['Etiqueta'] = filtered_data['Año'].astype(str) + '-' + filtered_data['Universidad']
                filtered_data = filtered_data.sort_values(by=['Año', 'Universidad'])
                etiquetas = filtered_data['Etiqueta']
                satisfaccion = filtered_data['Satisfaccion']
                retencion = filtered_data['Retencion']
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(etiquetas, satisfaccion, label='Satisfacción', color='blue')
                ax.bar(etiquetas, retencion, bottom=satisfaccion, label='Retención', color='orange')
                ax.set_xlabel('Universidad y Año')
                ax.set_ylabel('Porcentaje (%)')
                ax.set_title(f'Comparativa de Satisfacción y Retención ({anio_inicio}-{anio_fin})')
                ax.legend()
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig)

if __name__ == "__main__":
    main()
