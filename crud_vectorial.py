import tkinter as tk
from tkinter import ttk, messagebox
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import os
import numpy as np
import uuid

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
    """
    Inicializa la colección en Qdrant si no existe.
    """
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
class VectorDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vectores Con CRUD Proyecto 4")
        self.root.geometry("800x600")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        # Estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#1e1e1e",
                        foreground="#e0e0e0",
                        rowheight=25,
                        fieldbackground="#1e1e1e",
                        bordercolor="#444444",
                        borderwidth=2)
        style.map("Treeview",
                  background=[("selected", "#666666")],
                  highlightcolor=[("focus", "#444444")])

        self.main_frame = tk.Frame(self.root, bg="#1e1e1e", bd=2, relief="solid")
        self.main_frame.place(x=20, y=20, width=760, height=560)

        self.text_entry = ttk.Entry(self.main_frame, width=50)
        self.text_entry.place(x=20, y=20)

        self.button_frame = tk.Frame(self.main_frame, bg="#1e1e1e")
        self.button_frame.place(x=20, y=500, width=720, height=40)

        self.add_button = tk.Button(self.button_frame, text="Añadir Vector", command=self.add_vector,
                                    bg="#333333", fg="white", relief="flat",
                                    activebackground="#555555", activeforeground="white")
        self.add_button.pack(side="left", padx=10, pady=5, expand=True)

        self.delete_button = tk.Button(self.button_frame, text="Eliminar", command=self.delete_selected,
                                       bg="#333333", fg="white", relief="flat",
                                       activebackground="#555555", activeforeground="white")
        self.delete_button.pack(side="left", padx=10, pady=5, expand=True)

        self.refresh_button = tk.Button(self.button_frame, text="Actualizar", command=self.load_vectors,
                                        bg="#333333", fg="white", relief="flat",
                                        activebackground="#555555", activeforeground="white")
        self.refresh_button.pack(side="left", padx=10, pady=5, expand=True)

        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Text"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Text", text="Text")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Text", width=500, anchor="w")
        self.tree.place(x=20, y=60, width=720, height=400)

        self.load_vectors()

        for button in [self.add_button, self.delete_button, self.refresh_button]:
            button.bind("<Enter>", self.on_enter)
            button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        event.widget.configure(bg="#555555")

    def on_leave(self, event):
        event.widget.configure(bg="#333333")

    def add_vector(self):
        text = self.text_entry.get()
        if not text:
            messagebox.showwarning("Atencion", "Texto no puede estar vacio")
            return

        vector = model.encode([text])[0].tolist()
        insert_vector_qdrant(text, vector)
        messagebox.showinfo("Correcto", "Vector añadido exitosamente")
        self.load_vectors()

    def load_vectors(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        vectors = fetch_vectors_qdrant()
        for vector in vectors:
            self.tree.insert("", "end", values=vector)

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atencion", "No hay elemento seleccionado")
            return

        item = self.tree.item(selected_item)
        vector_id = item["values"][0]
        delete_vector_qdrant(vector_id)
        messagebox.showinfo("Exito", "Vector eliminado exitosamente")
        self.load_vectors()


if __name__ == "__main__":
    init_qdrant()
    root = tk.Tk()
    app = VectorDBApp(root)
    root.mainloop()
