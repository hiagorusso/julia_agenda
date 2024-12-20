import firebase_admin
import json
from firebase_admin import credentials, firestore
import os
import streamlit as st

# # Verifique se o arquivo existe no caminho especificado
# caminho_credenciais = "C:/Users/HiagoRusso/PycharmProjects/AppAtelie/db/serviceAccountKey.json"
# if not os.path.exists(caminho_credenciais):
#     print(f"O arquivo de credenciais não foi encontrado no caminho: {caminho_credenciais}")
# else:
#     print("Arquivo de credenciais encontrado.")

# Definindo a variável de ambiente manualmente no código
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "db/serviceAccountKey.json"  # Caminho correto para o arquivo JSON
#
# def iniciar_firestore():
#     """Inicializa a conexão com o Firestore."""
#     if not firebase_admin._apps:
#         cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])  # Usando a variável de ambiente configurada
#         firebase_admin.initialize_app(cred)
#     return firestore.client()

# def iniciar_firestore():
#     """Inicializa o Firestore de forma segura."""
#     if not firebase_admin._apps:
#         # Obter o conteúdo das credenciais da variável de ambiente
#         service_account_content = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_CONTENT")
#         if not service_account_content:
#             raise ValueError("A variável GOOGLE_APPLICATION_CREDENTIALS_CONTENT não está configurada.")
#
#         # Criar o arquivo temporário para usar as credenciais
#         service_account_path = "serviceAccountKey.json"
#         with open(service_account_path, "w") as f:
#             f.write(service_account_content)
#
#         # Inicializar o Firebase
#         cred = credentials.Certificate(service_account_path)
#         firebase_admin.initialize_app(cred)
#
# #     return firestore.client()
# service_account_content = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_CONTENT")
# if service_account_content:
#     print("Credenciais carregadas com sucesso.")
# else:
#     print("A variável de credenciais não foi encontrada.")
#


def iniciar_firestore():
    """Inicializa o Firestore de forma segura."""
    if not firebase_admin._apps:
        # Obter o conteúdo das credenciais da variável de ambiente
        service_account_content = st.secrets["firebase"]["GOOGLE_APPLICATION_CREDENTIALS_CONTENT"]
        if not service_account_content:
            raise ValueError("A variável GOOGLE_APPLICATION_CREDENTIALS_CONTENT não está configurada.")

        # Criar o arquivo temporário para usar as credenciais
        service_account_path = "serviceAccountKey.json"
        with open(service_account_path, "w") as f:
            f.write(service_account_content)

        # Inicializar o Firebase
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)

    return firestore.client()
