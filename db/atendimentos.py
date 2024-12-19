from db.firebase_config import iniciar_firestore
import sqlite3
db = iniciar_firestore()

def adicionar_atendimento(data, servico_nome):
    """Adiciona um atendimento no Firestore."""
    atendimentos_ref = db.collection("atendimentos")
    atendimentos_ref.add({"data": data, "servico": servico_nome})

def listar_atendimentos():
    """Lista todos os atendimentos cadastrados."""
    atendimentos_ref = db.collection("atendimentos")
    docs = atendimentos_ref.stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

def deletar_atendimento(atendimento_id):
    """Deleta um atendimento específico."""
    atendimentos_ref = db.collection("atendimentos").document(atendimento_id)
    atendimentos_ref.delete()



# from db.connection import conectar
#
# def adicionar_atendimento(data, servico_id):
#     conexao = conectar()
#     cursor = conexao.cursor()
#     cursor.execute(
#         "INSERT INTO atendimentos (data, servico_id) VALUES (?, ?)",
#         (data, servico_id)
#     )
#     conexao.commit()
#     conexao.close()
