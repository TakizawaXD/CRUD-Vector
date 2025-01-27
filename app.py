import streamlit as st
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import os
import uuid
import pandas as pd

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

qdrant_client = QdrantClient(
    url="https://c8d0665d-a912-48a3-9e99-157e99940ed6.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="KYJoTSboFRSiM0Q1dXTsRKKw6UrMPkEL2fTM5cJiXzLk3gPfIKxVtw",
)

COLLECTION_NAME = "vectors"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def init_qdrant():
    if not qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=384,  # Dimensión del modelo de embeddings
                distance=models.Distance.COSINE
            )
        )

def insert_vector_qdrant(text, vector):
    """
    Inserta un vector en la colección de Qdrant.
    Genera un UUID basado en el texto para usar como ID.
    """
    vector_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))  # Genera un UUID único para cada texto
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[models.PointStruct(
            id=vector_id,  # Usar UUID como ID
            payload={"text": text},
            vector=vector
        )]
    )

def fetch_vectors_qdrant():
    """
    Obtiene todos los vectores almacenados en Qdrant.
    """
    response, _ = qdrant_client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=None,
        limit=100
    )
    return [(point.id, point.payload["text"]) for point in response]

def delete_vector_qdrant(vector_id):
    """
    Elimina un vector de la colección en Qdrant.
    """
    qdrant_client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=[vector_id]
    )

init_qdrant()

st.title("Gestión de Vectores con Qdrant")

text = st.text_input("Texto para añadir un vector:")

if st.button("Añadir Vector"):
    if text:
        vector = model.encode([text])[0].tolist()
        insert_vector_qdrant(text, vector)
        st.success("Vector añadido exitosamente")
    else:
        st.warning("Por favor, ingresa un texto para añadir un vector.")

st.subheader("Vectores Almacenados")

vectors = fetch_vectors_qdrant()
if vectors:
    vector_df = pd.DataFrame(vectors, columns=["ID", "Texto"])
    st.dataframe(vector_df)
st.subheader("Eliminar un Vector")

if vectors:
    vector_id_to_delete = st.selectbox("Selecciona un vector para eliminar", [vector[0] for vector in vectors])
    if st.button("Eliminar Vector"):
        if vector_id_to_delete:
            delete_vector_qdrant(vector_id_to_delete)
            st.success("Vector eliminado exitosamente")
        else:
            st.warning("No se seleccionó ningún vector para eliminar.")
else:
    st.warning("No hay vectores disponibles para eliminar.")
