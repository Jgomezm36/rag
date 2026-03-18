import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.memory import ChatMemoryBuffer

# --- Configuración Global de Modelos ---
# Usamos los modelos locales de Ollama
Settings.llm = Ollama(model="llama3.1", request_timeout=120.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
# Chunking inteligente: recortes de 512 tokens con un solapamiento de 50 tokens
Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)

DB_DIR = "./chroma_db"
COLLECTION_NAME = "mi_proyecto_rag"

def get_vector_store():
    """Inicializa y devuelve la conexión a la base de datos vectorial ChromaDB."""
    db = chromadb.PersistentClient(path=DB_DIR)
    chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
    return ChromaVectorStore(chroma_collection=chroma_collection)

def ingest_documents(data_dir="./data"):
    """Lee los documentos de la carpeta, crea los embeddings y los guarda en ChromaDB."""
    if not os.path.exists(data_dir) or not os.listdir(data_dir):
        return None
    
    # LlamaIndex detectará automáticamente PDFs, TXTs, etc., gracias a SimpleDirectoryReader
    documents = SimpleDirectoryReader(data_dir).load_data()
    
    vector_store = get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Crea el índice y lo guarda en la base de datos
    index = VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context, 
        show_progress=True
    )
    return index

def get_chat_engine():
    """Crea un motor de chat con memoria para mantener conversaciones fluidas."""
    vector_store = get_vector_store()
    
    try:
        # Carga el índice existente desde la base de datos
        index = VectorStoreIndex.from_vector_store(vector_store)
        
        # Le damos memoria al chat (recuerda hasta los últimos 3000 tokens)
        memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
        
        # condense_plus_context reescribe la pregunta actual basándose en el historial
        chat_engine = index.as_chat_engine(
            chat_mode="condense_plus_context",
            memory=memory,
            verbose=True
        )
        return chat_engine
    except Exception as e:
        # Si la base de datos está vacía o no existe, devuelve None
        return None