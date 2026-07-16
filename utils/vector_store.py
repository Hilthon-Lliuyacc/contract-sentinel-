from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

def cargar_documentos(carpeta="docs"):
    documentos = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".pdf"):
            ruta = os.path.join(carpeta, archivo)
            loader = PyPDFLoader(ruta)
            documentos.extend(loader.load())
            print(f"Cargado: {archivo}")
    return documentos

def crear_vector_store(documentos):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    fragmentos = splitter.split_documents(documentos)
    print(f"Total fragmentos: {len(fragmentos)}")
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(fragmentos, embeddings)
    return vector_store

def cargar_o_crear_vector_store():
    if os.path.exists("faiss_index"):
        print("Cargando índice existente...")
        embeddings = OpenAIEmbeddings()
        return FAISS.load_local(
            "faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        print("Creando nuevo índice...")
        docs = cargar_documentos()
        vs = crear_vector_store(docs)
        vs.save_local("faiss_index")
        print("Índice guardado.")
        return vs