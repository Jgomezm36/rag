# 🧠 RAG Local Pro: Chat con Documentos (Ollama + LlamaIndex)

Este es un sistema de **Generación Aumentada por Recuperación (RAG)** avanzado y 100% privado. Permite interactuar con tus documentos (PDF, TXT) mediante lenguaje natural utilizando modelos de lenguaje de última generación ejecutados localmente.

## ✨ Características Principales

- **Privacidad Total**: Tus documentos nunca salen de tu máquina. No se usan APIs externas.
- **Multiformato**: Soporte nativo para PDFs y archivos de texto plano.
- **Memoria Conversacional**: El sistema recuerda el contexto de la charla para responder preguntas de seguimiento.
- **Citas de Fuentes**: Cada respuesta incluye los fragmentos exactos y el nombre del archivo de donde se extrajo la información.
- **Interfaz Moderna**: Construido con Streamlit para una experiencia de chat fluida.

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
| :--- | :--- |
| **LLM** | Ollama (Llama 3.1) |
| **Embeddings** | Nomic-Embed-Text |
| **Orquestador** | LlamaIndex |
| **Base de Datos** | ChromaDB (Vector Store) |
| **Frontend** | Streamlit |

## 🚀 Instalación Rápida

### 1. Requisitos Previos
Debes tener instalado **Ollama**. Si no lo tienes, descárgalo en [ollama.com](https://ollama.com).
Luego, descarga los modelos necesarios:
ollama pull llama3.1
ollama pull nomic-embed-text

#Clonar el repo
git clone <tu-url-del-repositorio>
cd Proyecto-RAG-Pro

# Crear entorno virtual (Recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
##💻 Uso
Para iniciar la aplicación, simplemente ejecuta:
python -m streamlit run src/app.py
1º Sube tus archivos en la barra lateral izquierda.
2º Haz clic en "Procesar e Indexar".
3º ¡Empieza a chatear con tus documentos!

##📂 Estructura del Proyecto

├── src/
│   ├── app.py           
│   └── rag_engine.py    
├── data/                
├── chroma_db/           
├── requirements.txt     
└── .gitignore           
Desarrollado como un proyecto de Inteligencia Artificial Local.
---

### 3. Recordatorio de los pasos finales

Para que todo funcione perfectamente:

1.  **Crea la carpeta raíz** llamada `Proyecto-RAG-Pro`.
2.  **Crea las subcarpetas**: Dentro de la raíz, crea la carpeta `src`.
3.  **Crea los archivos**:
    * `requirements.txt` en la raíz.
    * `.gitignore` en la raíz.
    * `README.md` en la raíz.
    * `src/rag_engine.py`.
    * `src/app.py`.
4.  **Instala las librerías**: Ejecuta `pip install -r requirements.txt` dentro de tu entorno virtual.
