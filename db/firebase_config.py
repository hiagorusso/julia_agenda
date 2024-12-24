import firebase_admin
import os
import streamlit as st
from firebase_admin import credentials, firestore

# #funcio certinho com local
# caminho_credenciais = "C:/Users/HiagoRusso/PycharmProjects/AppAtelie/db/serviceAccountKey.json"
# if not os.path.exists(caminho_credenciais):
#     print(f"O arquivo de credenciais não foi encontrado no caminho: {caminho_credenciais}")
# else:
#     print("Arquivo de credenciais encontrado.")
#
# # Definindo a variável de ambiente manualmente no código
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "db/serviceAccountKey.json"  # Caminho correto para o arquivo JSON
#
# def iniciar_firestore():
#     """Inicializa a conexão com o Firestore."""
#     if not firebase_admin._apps:
#         cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])  # Usando a variável de ambiente configurada
#         firebase_admin.initialize_app(cred)
#     return firestore.client()


def iniciar_firestore():
    """Inicializa a conexão com o Firestore usando as credenciais do Streamlit Secrets."""
    try:
        if not firebase_admin._apps:
            # Carregar as credenciais do Streamlit Secrets
            firebase_credentials = st.secrets["firebase"]

            # Inicializar o Firebase com as credenciais
            cred = credentials.Certificate(firebase_credentials)
            firebase_admin.initialize_app(cred)

        return firestore.client()
    except Exception as e:
        st.error(f"Erro ao inicializar o Firebase: {e}")
        raise


# Testar a conexão
if __name__ == "__main__":
    db = iniciar_firestore()
    st.write("Firestore inicializado com sucesso!")
