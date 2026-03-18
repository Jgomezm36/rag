import streamlit as st
import os
from rag_engine import ingest_documents, get_chat_engine

# Configuración de la página
st.set_page_config(page_title="Chat RAG Local", page_icon="🧠", layout="wide")

# Asegurar que existe la carpeta de datos
DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)

st.title("🧠 Chat RAG Pro (Ollama + LlamaIndex)")
st.caption("Sube tus documentos y haz preguntas. Todo se ejecuta en local.")

# --- Barra lateral: Subida y Gestión de Archivos ---
with st.sidebar:
    st.header("📄 Tus Documentos")
    uploaded_files = st.file_uploader(
        "Sube archivos (PDF, TXT)", 
        type=["pdf", "txt"], 
        accept_multiple_files=True
    )
    
    if st.button("Procesar e Indexar"):
        if uploaded_files:
            with st.spinner("Guardando archivos y generando embeddings... (Esto puede tardar)"):
                # 1. Guardar los archivos físicos
                for file in uploaded_files:
                    file_path = os.path.join(DATA_DIR, file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                
                # 2. Ingestar en la base de datos vectorial
                ingest_documents(DATA_DIR)
                
                # 3. Recargar el motor de chat para que vea los nuevos datos
                st.session_state.chat_engine = get_chat_engine()
                st.success("¡Documentos procesados con éxito! Ya puedes preguntar.")
        else:
            st.warning("Por favor, sube al menos un archivo antes de procesar.")

# --- Inicialización del estado de la app ---
if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = get_chat_engine()

if "messages" not in st.session_state:
    st.session_state.messages = [] # Guarda el historial visual del chat

# --- Mostrar el historial de mensajes ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input del usuario y generación de respuesta ---
if prompt := st.chat_input("Escribe tu pregunta sobre los documentos..."):
    
    # Validar que existan documentos indexados
    if st.session_state.chat_engine is None:
        st.error("No hay documentos indexados. Por favor, sube un archivo en el menú lateral.")
        st.stop()

    # Mostrar la pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mostrar la respuesta del asistente
    with st.chat_message("assistant"):
        with st.spinner("Consultando documentos..."):
            
            # Consultar al motor RAG
            response = st.session_state.chat_engine.chat(prompt)
            st.markdown(response.response)
            
            # Mostrar las fuentes de dónde sacó la información (Explicabilidad)
            if response.source_nodes:
                with st.expander("🔍 Ver fuentes consultadas"):
                    for i, node in enumerate(response.source_nodes):
                        # Mostrar el nombre del archivo y la relevancia matemática (score)
                        archivo = node.metadata.get('file_name', 'Desconocido')
                        st.markdown(f"**Fuente {i+1}** | Archivo: `{archivo}` | Similitud: `{node.score:.2f}`")
                        # Mostrar un pequeño fragmento del texto original
                        st.info(f"... {node.text[:250]} ...")

    # Guardar la respuesta en el historial visual
    st.session_state.messages.append({"role": "assistant", "content": response.response})