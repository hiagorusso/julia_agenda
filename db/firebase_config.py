import firebase_admin
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
    """Inicializa o Firestore com credenciais fornecidas diretamente."""
    try:
        # Verifica se o Firebase já está inicializado
        if not firebase_admin._apps:
            # Carregar credenciais diretamente do Streamlit Secrets
            firebase_credentials = dict(st.secrets["firebase"])  # Certifique-se de que é um dicionário válido

            # Inicializar o Firebase Admin SDK com credenciais explícitas
            cred = credentials.Certificate(firebase_credentials)
            firebase_admin.initialize_app(cred)

        return firestore.client()
    except Exception as e:
        st.error(f"Erro ao inicializar o Firestore: {e}")
        raise


# Testar a conexão com o Firestore
if __name__ == "__main__":
    try:
        db = iniciar_firestore()
        st.success("Firestore inicializado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao conectar com o Firestore: {e}")
