import firebase_admin
from firebase_admin import credentials, firestore
import os

# # Verifique se o arquivo existe no caminho especificado
# caminho_credenciais = "C:/Users/HiagoRusso/PycharmProjects/AppAtelie/db/serviceAccountKey.json"
# if not os.path.exists(caminho_credenciais):
#     print(f"O arquivo de credenciais não foi encontrado no caminho: {caminho_credenciais}")
# else:
#     print("Arquivo de credenciais encontrado.")

# Definindo a variável de ambiente manualmente no código
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "db/serviceAccountKey.json"  # Caminho correto para o arquivo JSON

def iniciar_firestore():
    """Inicializa a conexão com o Firestore."""
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])  # Usando a variável de ambiente configurada
        firebase_admin.initialize_app(cred)
    return firestore.client()