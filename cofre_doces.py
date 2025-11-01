import customtkinter as ctk
from pymongo import MongoClient
from cryptography.fernet import Fernet
from datetime import datetime
from bson.objectid import ObjectId
import os
from PIL import Image, ImageTk


def conectar_mongo():
    cliente = MongoClient("mongodb+srv://root:joao20012009@projetobruno.xwma2xg.mongodb.net/")
    db = cliente["projetoBRUNO"]
    return db["CofreDeDoces"]

collection = conectar_mongo()


def carregar_ou_gerar_chave():
    if not os.path.exists("chave.key"):
        nova = Fernet.generate_key()
        with open("chave.key", "wb") as f:
            f.write(nova)
        return nova
    else:
        with open("chave.key", "rb") as f:
            return f.read()

chave = carregar_ou_gerar_chave()
fernet = Fernet(chave)

def criptografar(texto):
    return fernet.encrypt(texto.encode())

def descriptografar(texto):
    return fernet.decrypt(texto).decode()



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title(" Cofre de Doces Criptografado - Halloween Edition ")
app.geometry("980x650")
app.configure(fg_color="#0d0d0d")


doc_atualizando = None



def mostrar_msg(titulo, texto, cor="#ff6600"):
    popup = ctk.CTkToplevel(app)
    popup.title(titulo)
    popup.geometry("320x200")
    popup.configure(fg_color="#1a1a1a")
    ctk.CTkLabel(popup, text=texto, text_color=cor, font=("Trebuchet MS", 16, "bold"), wraplength=260).pack(pady=30)
    ctk.CTkButton(popup, text="Fechar ", command=popup.destroy, fg_color=cor, hover_color="#cc3300").pack(pady=10)
    popup.grab_set()


def adicionar_ou_atualizar():
    global doc_atualizando

    nome = entry_nome.get().strip()
    doce = entry_doce.get().strip()
    qtd = entry_qtd.get().strip()

    if not nome or not doce or not qtd.isdigit():
        mostrar_msg(" Erro", "Preencha todos os campos corretamente!", cor="#ff3333")
        return

    if doc_atualizando:  # Atualizar
        collection.update_one(
            {"_id": ObjectId(doc_atualizando)},
            {"$set": {
                "child": nome,
                "candy_type": criptografar(doce),
                "qty": int(qtd),
                "timestamp": datetime.utcnow()
            }}
        )
        mostrar_msg(" Atualizado", "Doce atualizado no cofre!", cor="#ffaa00")
        doc_atualizando = None
        botao_salvar.configure(text=" Salvar no Cofre", fg_color="#ff6600", command=adicionar_ou_atualizar)
    else:  # Adicionar novo
        doc = {
            "child": nome,
            "candy_type": criptografar(doce),
            "qty": int(qtd),
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(doc)
        mostrar_msg(" Sucesso", "Doce adicionado ao cofre!", cor="#ff6600")

    entry_nome.delete(0, 'end')
    entry_doce.delete(0, 'end')
    entry_qtd.delete(0, 'end')
    listar_doces()

def preparar_atualizacao(doc_id):
    global doc_atualizando
    doc = collection.find_one({"_id": ObjectId(doc_id)})
    if doc:
        entry_nome.delete(0, 'end')
        entry_doce.delete(0, 'end')
        entry_qtd.delete(0, 'end')

        entry_nome.insert(0, doc["child"])
        entry_doce.insert(0, descriptografar(doc["candy_type"]))
        entry_qtd.insert(0, str(doc["qty"]))

        doc_atualizando = str(doc_id)
        botao_salvar.configure(text=" Salvar Alterações", fg_color="#ffaa00", command=adicionar_ou_atualizar)

def deletar_doce(doc_id):
    collection.delete_one({"_id": ObjectId(doc_id)})
    mostrar_msg(" Removido", "Doce removido do cofre!", cor="#ff3300")
    listar_doces()

def listar_doces():
    for widget in frame_lista.winfo_children():
        widget.destroy()

    docs = collection.find().sort("timestamp", -1)
    for doc in docs:
        item = ctk.CTkFrame(frame_lista, fg_color="#1e0f0f", corner_radius=10)
        item.pack(fill="x", pady=5, padx=10)

        texto = f" {doc['child']} — {descriptografar(doc['candy_type'])} ({doc['qty']} unidades)"
        ctk.CTkLabel(item, text=texto, text_color="#ff7518", font=("Trebuchet MS", 15)).pack(side="left", padx=10, pady=8)

        botoes_frame = ctk.CTkFrame(item, fg_color="transparent")
        botoes_frame.pack(side="right", padx=10)

        ctk.CTkButton(botoes_frame, text=" Atualizar", width=90, fg_color="#ffaa00", hover_color="#cc8800",
                      font=("Trebuchet MS", 13, "bold"),
                      command=lambda id=doc["_id"]: preparar_atualizacao(id)).pack(side="left", padx=5)

        ctk.CTkButton(botoes_frame, text=" Excluir", width=90, fg_color="#ff3333", hover_color="#cc0000",
                      font=("Trebuchet MS", 13, "bold"),
                      command=lambda id=doc["_id"]: deletar_doce(id)).pack(side="left", padx=5)



header = ctk.CTkFrame(app, height=80, fg_color="#260000", corner_radius=0)
header.pack(fill="x")

ctk.CTkLabel(header, text=" Cofre Criptografado de Doces ",
             text_color="#ff7518", font=("Trebuchet MS", 30, "bold")).pack(pady=20)

# Corpo principal
frame_main = ctk.CTkFrame(app, fg_color="#1a1a1a", corner_radius=15)
frame_main.pack(fill="both", expand=True, padx=20, pady=15)

# Painel esquerdo (Formulário)
frame_form = ctk.CTkFrame(frame_main, fg_color="#2a0f0f", width=320, corner_radius=15)
frame_form.pack(side="left", fill="y", padx=20, pady=20)

ctk.CTkLabel(frame_form, text=" Adicionar / Editar Doce ",
             text_color="#ff7518", font=("Trebuchet MS", 22, "bold")).pack(pady=15)

entry_nome = ctk.CTkEntry(frame_form, placeholder_text="Nome da criança ", width=250, font=("Trebuchet MS", 14))
entry_nome.pack(pady=10)
entry_doce = ctk.CTkEntry(frame_form, placeholder_text="Tipo de doce ", width=250, font=("Trebuchet MS", 14))
entry_doce.pack(pady=10)
entry_qtd = ctk.CTkEntry(frame_form, placeholder_text="Quantidade ", width=250, font=("Trebuchet MS", 14))
entry_qtd.pack(pady=10)

botao_salvar = ctk.CTkButton(frame_form, text=" Salvar no Cofre", fg_color="#ff6600", hover_color="#e65c00",
                             font=("Trebuchet MS", 15, "bold"), command=adicionar_ou_atualizar)
botao_salvar.pack(pady=15)

# Painel direito (Lista)
frame_lista = ctk.CTkScrollableFrame(frame_main, fg_color="#0f0f0f", width=580, height=450, corner_radius=15)
frame_lista.pack(side="right", fill="both", expand=True, padx=20, pady=20)

ctk.CTkLabel(frame_lista, text=" Doces no Cofre ", text_color="#ff7518",
             font=("Trebuchet MS", 22, "bold")).pack(pady=10)



listar_doces()
app.mainloop()
