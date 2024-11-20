import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

rendimiento_url = 'https://raw.githubusercontent.com/ElsincejasWasaaaaa/data/main/Tabladerendimientoacademico1.csv'
satisfaccion_url = 'https://raw.githubusercontent.com/ElsincejasWasaaaaa/data/main/ComparativaDeSatisfaccionEstudiantil1.csv'

try:
    df_rendimiento = pd.read_csv(rendimiento_url)
    df_satisfaccion = pd.read_csv(satisfaccion_url)
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

def analisis_rendimiento_academico():
    st.header("Comparativa de Rendimiento Académico")
    st.info("Comparación del rendimiento académico de los estudiantes entre años seleccionados.")
    
    with st.sidebar:
        st.subheader("Opciones de Filtro (Rendimiento)")
        videojuego_seleccionado = st.selectbox("Selecciona el Videojuego Educativo", df_rendimiento['videjueg_Educativo'].unique())
        anio_inicio = st.selectbox("Año de Inicio", sorted(df_rendimiento['año'].unique()))
        anio_fin = st.selectbox("Año de Fin", [x for x in sorted(df_rendimiento['año'].unique()) if x >= anio_inicio])
    
    df_filtrado = df_rendimiento[
        (df_rendimiento['videjueg_Educativo'] == videojuego_seleccionado) & 
        (df_rendimiento['año'].between(anio_inicio, anio_fin))
    ]

    with st.expander("Tabla de Rendimiento Académico Filtrada"):
        st.dataframe(df_filtrado)

    if st.button("Mostrar Comparativa de Rendimiento Académico"):
        fig, ax = plt.subplots()
        rendimiento_por_universidad_anio = df_filtrado.groupby(['universidad', 'año'])['Rendimiento_Promedio'].mean().unstack()
        rendimiento_por_universidad_anio.plot(kind='bar', ax=ax, colormap='viridis')
        ax.set_xlabel("Universidad")
        ax.set_ylabel("Rendimiento Promedio")
        ax.set_title(f"Comparativa de Rendimiento Académico en {anio_inicio} y {anio_fin}")
        ax.legend(title="Año")
        st.pyplot(fig)

def analisis_satisfaccion_y_retencion():
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

def analisis_relacion_uso_rendimiento():
    st.header("Relación entre Uso de Videojuegos y Rendimiento Académico")
    
    datos = {
        'Estudiantes Usando': [200, 150, 100, 220, 160, 110, 250, 180, 120, 230],
        'Rendimiento Promedio (%)': [75, 70, 80, 78, 72, 82, 80, 74, 85, 82],
        'Videojuego': ['MathQuest', 'SciExplorers', 'LitAdventure', 'MathQuest', 'SciExplorers', 
                       'LitAdventure', 'MathQuest', 'SciExplorers', 'LitAdventure', 'MathQuest']
    }

    df = pd.DataFrame(datos)

    colores = {'MathQuest': 'red', 'SciExplorers': 'blue', 'LitAdventure': 'green'}

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x='Estudiantes Usando',
        y='Rendimiento Promedio (%)',
        data=df,
        hue='Videojuego',
        palette=colores,
        s=100,
        edgecolor='black'
    )

    plt.title('Relación entre Uso de Videojuegos y Rendimiento Académico')
    plt.xlabel('Número de Estudiantes Usando Videojuegos')
    plt.ylabel('Rendimiento Promedio (%)')
    plt.legend(title='Videojuego')
    st.pyplot(plt)

def grafico_pastel_satisfaccion():
    st.header("Distribución de Satisfacción Estudiantil por Año y Universidad")
    with st.sidebar:
        st.subheader("Opciones de Filtro (Gráfico de Pastel)")
        anio_seleccionado = st.selectbox("Selecciona el Año", df_satisfaccion['Año'].unique())
        universidad_seleccionada = st.selectbox("Selecciona la Universidad", df_satisfaccion['Universidad'].unique())

    datos_filtrados = df_satisfaccion[df_satisfaccion['Año'] == anio_seleccionado]
    
    if datos_filtrados.empty:
        st.warning("No hay datos disponibles para el año seleccionado.")
    else:
        labels = datos_filtrados['Universidad']
        sizes = datos_filtrados['Satisfaccion']
        explode = [0.1 if uni == universidad_seleccionada else 0 for uni in labels]
        
        fig, ax = plt.subplots()
        ax.pie(
            sizes, labels=labels, explode=explode, autopct='%1.1f%%', 
            startangle=90, colors=sns.color_palette("pastel")  # Cambiado a pastel
        )
        ax.axis('equal')
        ax.set_title(f"Distribución de Satisfacción en {anio_seleccionado}")
        st.pyplot(fig)

def medidas_tendencia_central():
    st.header("Medidas de Tendencia Central")
    with st.sidebar:
        st.subheader("Opciones de Análisis")
        tipo_analisis = st.radio("Selecciona el tipo de análisis", ["Rendimiento Académico", "Satisfacción"])
    
    if tipo_analisis == "Rendimiento Académico":
        columna = 'Rendimiento_Promedio'
        df = df_rendimiento
    else:
        columna = 'Satisfaccion'
        df = df_satisfaccion

    media = df[columna].mean()
    mediana = df[columna].median()
    moda = df[columna].mode()[0]
    
    st.write(f"### Análisis de {tipo_analisis}")
    st.write(f"**Media:** {media:.2f}")
    st.write(f"**Mediana:** {mediana:.2f}")
    st.write(f"**Moda:** {moda:.2f}")

def analisis_distribucion():
    st.header("Análisis de Distribución")
    with st.sidebar:
        st.subheader("Opciones de Análisis")
        tipo_analisis = st.radio("Selecciona el tipo de análisis", ["Rendimiento Académico", "Satisfacción"])
    
    if tipo_analisis == "Rendimiento Académico":
        columna = 'Rendimiento_Promedio'
        df = df_rendimiento
    else:
        columna = 'Satisfaccion'
        df = df_satisfaccion

    plt.figure(figsize=(10, 6))
    sns.histplot(df[columna], kde=True, color="skyblue", bins=15)
    plt.title(f"Distribución de {tipo_analisis}")
    plt.xlabel(tipo_analisis)
    plt.ylabel("Frecuencia")
    st.pyplot(plt)

def regresion_lineal():
    st.header("Modelo Predictivo: Regresión Lineal")
    st.info("Este análisis utiliza un modelo de regresión lineal para predecir el rendimiento académico basado en el uso de videojuegos educativos.")

    datos = {
        'Estudiantes_Usando': [200, 150, 100, 220, 160, 110, 250, 180, 120, 230],
        'Rendimiento_Promedio': [75, 70, 80, 78, 72, 82, 80, 74, 85, 82]
    }
    df = pd.DataFrame(datos)

    st.subheader("Datos utilizados")
    st.dataframe(df)

    plt.figure(figsize=(10, 6))
    sns.regplot(
        x='Estudiantes_Usando', 
        y='Rendimiento_Promedio', 
        data=df, 
        scatter_kws={'color': 'blue', 's': 50}, 
        line_kws={'color': 'red', 'label': 'Línea de Regresión'}
    )
    plt.title("Relación entre Uso de Videojuegos y Rendimiento Académico", fontsize=14)
    plt.xlabel("Estudiantes Usando Videojuegos", fontsize=12)
    plt.ylabel("Rendimiento Promedio (%)", fontsize=12)
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)

    st.subheader("Predicción del Rendimiento Futuro")
    estudiantes_input = st.number_input(
        "Ingresa el número de estudiantes que usarían videojuegos educativos", 
        min_value=50, 
        max_value=300, 
        step=10
    )
    
    if estudiantes_input:
        pendiente = 0.05  
        interseccion = 65

        prediccion = pendiente * estudiantes_input + interseccion
        st.success(f"Si {int(estudiantes_input)} estudiantes usan videojuegos educativos, el rendimiento promedio esperado sería **{prediccion:.2f}%**.")

def main():
    st.title("Dataviz: Datos Educativos Transformados en Conocimiento 🧠✨")
    with st.sidebar:
        st.header("Selecciona el Análisis")
        analisis = st.radio("Opciones", [
            "Rendimiento Académico", 
            "Satisfacción y Retención", 
            "Relación Uso y Rendimiento", 
            "Gráfico de Pastel - Satisfacción", 
            "Medidas de Tendencia Central", 
            "Análisis de Distribución" ,
            "Regresión Lineal"
        ])
    if analisis == "Rendimiento Académico":
        analisis_rendimiento_academico()
    elif analisis == "Satisfacción y Retención":
        analisis_satisfaccion_y_retencion()
    elif analisis == "Relación Uso y Rendimiento":
        analisis_relacion_uso_rendimiento()
    elif analisis == "Gráfico de Pastel - Satisfacción":
        grafico_pastel_satisfaccion()
    elif analisis == "Medidas de Tendencia Central":
        medidas_tendencia_central()
    elif analisis == "Análisis de Distribución":
        analisis_distribucion()
    elif analisis == "Regresión Lineal":
        regresion_lineal()

if __name__ == "__main__":
    main()
