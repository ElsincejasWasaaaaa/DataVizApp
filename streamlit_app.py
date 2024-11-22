import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class CargaDatos:
    def __init__(self, rendimiento_url, satisfaccion_url):
        self.rendimiento_url = rendimiento_url
        self.satisfaccion_url = satisfaccion_url
        self.df_rendimiento = None
        self.df_satisfaccion = None

    def load_data(self):
        try:
            self.df_rendimiento = pd.read_csv(self.rendimiento_url)
            self.df_satisfaccion = pd.read_csv(self.satisfaccion_url)
        except Exception as e:
            st.error(f"Error al cargar los datos: {e}")
            st.stop()

class Analisis:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def rendimiento_academico(self): #yo
        st.header("Comparativa de Rendimiento Académico")
        st.info("Comparación del rendimiento académico de los estudiantes entre años seleccionados.")
        
        with st.sidebar:
            st.subheader("Opciones de Filtro (Rendimiento)")
            videojuego_seleccionado = st.selectbox(
                "Selecciona el Videojuego Educativo", 
                self.data_manager.df_rendimiento['videjueg_Educativo'].unique()
            )
            año_inicio = st.selectbox("Año de Inicio", sorted(self.data_manager.df_rendimiento['año'].unique()))
            año_fin = st.selectbox(
                "Año de Fin", 
                [x for x in sorted(self.data_manager.df_rendimiento['año'].unique()) if x >= año_inicio]
            )
        
        df_filtrado = self.data_manager.df_rendimiento[
            (self.data_manager.df_rendimiento['videjueg_Educativo'] == videojuego_seleccionado) & 
            (self.data_manager.df_rendimiento['año'].between(año_inicio, año_fin))
        ]

        with st.expander("Tabla de Rendimiento Académico Filtrada"):
            st.dataframe(df_filtrado)


        #mean() sirve para calcular el promedio y unstack() sirve para convertir el DataFrame agrupado de formato largo a formato ancho, donde los años se colocan como columnas, y las universidades como filas.
        if st.button("Mostrar Comparativa de Rendimiento Académico"):
            fig, ax = plt.subplots()
            rendimiento_por_universidad_anio = df_filtrado.groupby(['universidad', 'año'])['Rendimiento_Promedio'].mean().unstack() 
            rendimiento_por_universidad_anio.plot(kind='bar', ax=ax, colormap='viridis')
            ax.set_xlabel("Universidad")
            ax.set_ylabel("Rendimiento Promedio")
            ax.set_title(f"Comparativa de Rendimiento Académico en {año_inicio} y {año_fin}")
            ax.legend(title="Año")
            st.pyplot(fig)

    def satisfaccion_y_retencion(self): #yair
        st.header("Comparativa de Satisfacción y Retención Estudiantil")
        
        with st.sidebar:
            st.subheader("Opciones de Filtro (Satisfacción y Retención)")
            uni1 = st.selectbox("Universidad 1", options=["UPC", "PUCP", "UNMSM"], index=0)
            uni2 = st.selectbox("Universidad 2 (diferente a la 1)", options=["UPC", "PUCP", "UNMSM"], index=1)
            año_inicio = st.selectbox("Año de Inicio", options=list(range(2015, 2022)), index=0)
            año_fin = st.selectbox("Año de Fin", options=list(range(2015, 2022)), index=6)

        if uni1 == uni2:
            st.error("Universidad 1 y Universidad 2 no deben ser iguales.")
            return

        if año_inicio > año_fin:
            st.error("El año de inicio debe ser menor o igual al año de fin.")
            return

        universidades = [uni1, uni2]
        filtered_data = self.data_manager.df_satisfaccion[
            (self.data_manager.df_satisfaccion['Universidad'].isin(universidades)) & 
            (self.data_manager.df_satisfaccion['Año'].between(año_inicio, año_fin))
        ]

        if filtered_data.empty:
            st.warning("No hay datos para los filtros seleccionados.")
            return

        filtered_data['Etiqueta'] = filtered_data['Año'].astype(str) + '-' + filtered_data['Universidad']
        filtered_data = filtered_data.sort_values(by=['Año', 'Universidad'])

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(filtered_data['Etiqueta'], filtered_data['Satisfaccion'], 
               label='Satisfacción', color='blue')
        ax.bar(filtered_data['Etiqueta'], filtered_data['Retencion'], 
               bottom=filtered_data['Satisfaccion'], label='Retención', color='orange')
        
        ax.set_xlabel('Universidad y Año')
        ax.set_ylabel('Porcentaje (%)')
        ax.set_title(f'Comparativa de Satisfacción y Retención ({año_inicio}-{año_fin})')
        ax.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

    def analisis_relacion_uso_rendimiento(self): #alvaro 
        st.header("Relación entre Uso de Videojuegos y Rendimiento Académico")
        
        datos = {
            'Estudiantes Usando': [200, 150, 100, 220, 160, 110, 250, 180, 120, 230],
            'Rendimiento Promedio (%)': [75, 70, 80, 78, 72, 82, 80, 74, 85, 82],
            'Videojuego': ['MathQuest', 'SciExplorers', 'LitAdventure'] * 3 + ['MathQuest']
        }
        
        df = pd.DataFrame(datos)
        colores = {'MathQuest': 'red', 'SciExplorers': 'blue', 'LitAdventure': 'green'}

        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=df,
            x='Estudiantes Usando',
            y='Rendimiento Promedio (%)',
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

    def grafico_pastel_satisfaccion(self): #yo
        st.header("Distribución de Satisfacción Estudiantil por Año y Universidad")
        
        with st.sidebar:
            st.subheader("Opciones de Filtro (Gráfico de Pastel)")
            año_seleccionado = st.selectbox(
                "Selecciona el Año", 
                self.data_manager.df_satisfaccion['Año'].unique()
            )
            universidad_seleccionada = st.selectbox(
                "Selecciona la Universidad", 
                self.data_manager.df_satisfaccion['Universidad'].unique()
            )

        datos_filtrados = self.data_manager.df_satisfaccion[
            self.data_manager.df_satisfaccion['Año'] == año_seleccionado
        ]
        
        
        Lado = datos_filtrados['Universidad']
        Piezas = datos_filtrados['Satisfaccion']
        Elegido = [0.1 if uni == universidad_seleccionada else 0 for uni in Lado]
        
        fig, ax = plt.subplots()
        ax.pie(Piezas, labels=Lado, explode=Elegido, autopct='%1.1f%%', 
               startangle=90, colors=sns.color_palette("pastel"))
        ax.axis('equal')
        ax.set_title(f"Distribución de Satisfacción en {año_seleccionado}")
        st.pyplot(fig)

    def medidas_tendencia_central(self): #yo xddddd
        st.header("Medidas de Tendencia Central")
        
        with st.sidebar:
            st.subheader("Opciones de Análisis")
            tipo_analisis = st.radio(
                "Selecciona el tipo de análisis", 
                ["Rendimiento Académico", "Satisfacción"]
            )
        
        if tipo_analisis == "Rendimiento Académico":
            columna = 'Rendimiento_Promedio'
            df = self.data_manager.df_rendimiento
        else:
            columna = 'Satisfaccion'
            df = self.data_manager.df_satisfaccion

        media = df[columna].mean()
        mediana = df[columna].median()
        moda = df[columna].mode()[0]
        
        st.write(f"### Análisis de {tipo_analisis}")
        st.write(f"**Media:** {media:.2f}")
        st.write(f"**Mediana:** {mediana:.2f}")
        st.write(f"**Moda:** {moda:.2f}")

    def analisis_distribucion(self): #yop
        st.header("Análisis de Distribución")
        
        with st.sidebar:
            st.subheader("Opciones de Análisis")
            tipo_analisis = st.radio(
                "Selecciona el tipo de análisis", 
                ["Rendimiento Académico", "Satisfacción"]
            )
        
        if tipo_analisis == "Rendimiento Académico":
            columna = 'Rendimiento_Promedio'
            df = self.data_manager.df_rendimiento
        else:
            columna = 'Satisfaccion'
            df = self.data_manager.df_satisfaccion

        plt.figure(figsize=(10, 6))
        sns.histplot(df[columna], kde=True, color="skyblue", bins=15)
        plt.title(f"Distribución de {tipo_analisis}")
        plt.xlabel(tipo_analisis)
        plt.ylabel("Frecuencia")
        st.pyplot(plt)

    def regresion_lineal(self): #lo hizo yair pero estaba remal y lo tube que arreglar xd
        st.header("Modelo Predictivo: Regresión Lineal")
        st.info("Este análisis utiliza un modelo de regresión lineal para predecir el rendimiento académico basado en el uso de videojuegos educativos.")

        datos = {
            'Estudiantes_Usando': [200, 150, 100, 220, 160, 110, 250, 180, 120, 230],
            'Rendimiento_Promedio': [75, 70, 80, 78, 72, 82, 80, 74, 85, 82]
        }
        df = pd.DataFrame(datos)

        with st.expander("Datos utilizados"):
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

class App:
    def __init__(self):
        self.data_manager = CargaDatos(
            rendimiento_url='https://raw.githubusercontent.com/ElsincejasWasaaaaa/data/main/Tabladerendimientoacademico1.csv',
            satisfaccion_url='https://raw.githubusercontent.com/ElsincejasWasaaaaa/data/main/ComparativaDeSatisfaccionEstudiantil1.csv'
        )
        self.analysis = Analisis(self.data_manager)

    def run(self):
        self.data_manager.load_data()
        st.title("Dataviz: Datos Educativos Transformados en Conocimiento 🧠✨")
        
        with st.sidebar:
            st.header("Selecciona el Análisis")
            analisis = st.radio("Opciones", [
                "Rendimiento Académico", 
                "Satisfacción y Retención", 
                "Relación Uso y Rendimiento", 
                "Gráfico de Pastel - Satisfacción", 
                "Medidas de Tendencia Central", 
                "Análisis de Distribución",
                "Regresión Lineal"
            ])

        Analisis_metodos = {
            "Rendimiento Académico": self.analysis.rendimiento_academico,
            "Satisfacción y Retención": self.analysis.satisfaccion_y_retencion,
            "Relación Uso y Rendimiento": self.analysis.analisis_relacion_uso_rendimiento,
            "Gráfico de Pastel - Satisfacción": self.analysis.grafico_pastel_satisfaccion,
            "Medidas de Tendencia Central": self.analysis.medidas_tendencia_central,
            "Análisis de Distribución": self.analysis.analisis_distribucion,
            "Regresión Lineal": self.analysis.regresion_lineal
        }

        Analisis_metodos[analisis]()

if __name__ == "__main__":
    app = App()
    app.run()
