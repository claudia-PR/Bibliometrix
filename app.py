import streamlit as st
import pandas as pd

# Función para procesar archivos cargados
def process_files(files):
    data_frames = []

    for file in files:
        # Intentar leer el archivo como CSV
        try:
            df = pd.read_csv(file)
            st.success(f"Archivo cargado correctamente: {file.name}")

            # Verificar si existe una columna DOI
            if 'DOI' not in df.columns:
                st.warning(f"El archivo {file.name} no contiene una columna 'DOI'. Será omitido.")
                continue

            # Agregar DataFrame procesado
            data_frames.append(df)

        except Exception as e:
            st.error(f"Error al cargar {file.name}: {str(e)}")

    # Concatenar todos los DataFrames y eliminar duplicados por DOI
    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
        deduplicated_df = combined_df.drop_duplicates(subset='DOI', keep='first')
        return deduplicated_df
    else:
        return None

# Configuración de la página
st.title("Generador de Input para Bibliometrix")
st.markdown(
    """Esta aplicación permite cargar archivos CSV de bases de datos como Scopus, WoS y PubMed,
    eliminar duplicados basados en el DOI y generar un archivo compatible con Bibliometrix."""
)

# Entrada de archivos CSV
uploaded_files = st.file_uploader("Sube uno o más archivos CSV:", type="csv", accept_multiple_files=True)

if uploaded_files:
    # Procesar los archivos cargados
    with st.spinner("Procesando archivos..."):
        result_df = process_files(uploaded_files)

    if result_df is not None:
        st.success(f"Se procesaron {len(uploaded_files)} archivos. Total de registros únicos: {len(result_df)}")

        # Mostrar una vista previa del resultado
        st.write("### Vista previa de los datos procesados:")
        st.dataframe(result_df.head(20))

        # Descargar el archivo resultante
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar archivo procesado",
            data=csv,
            file_name="bibliometrix_input.csv",
            mime="text/csv"
        )
    else:
        st.error("No se generó ningún archivo procesado. Asegúrate de cargar archivos con una columna 'DOI'.")
else:
    st.info("Carga uno o más archivos CSV para comenzar.")

# Ejemplo de datos por defecto
if st.checkbox("¿Quieres ver un ejemplo por defecto?"):
    example_data = {
        'Title': ["Artículo 1", "Artículo 2", "Artículo 3", "Artículo 4"],
        'DOI': ["10.1000/xyz123", "10.1000/xyz456", "10.1000/xyz123", "10.1000/xyz789"],
        'Year': [2020, 2021, 2020, 2022]
    }
    example_df = pd.DataFrame(example_data)

    st.write("### Ejemplo de archivo con duplicados:")
    st.dataframe(example_df)

    deduplicated_example_df = example_df.drop_duplicates(subset='DOI', keep='first')
    st.write("### Archivo sin duplicados:")
    st.dataframe(deduplicated_example_df)
