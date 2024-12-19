from db.firebase_config import iniciar_firestore

db = iniciar_firestore()


def cadastrar_servico(nome, valor):
    """Cadastra um novo serviço no Firestore."""
    servicos_ref = db.collection("servicos")
    query = servicos_ref.where("nome", "==", nome).stream()

    # Verifica se o serviço já existe
    for doc in query:
        raise Exception("Serviço já existe.")

    servicos_ref.add({"nome": nome, "valor": valor})

def listar_servicos():
    """Lista todos os serviços cadastrados."""
    servicos_ref = db.collection("servicos")
    docs = servicos_ref.stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


def deletar_servico(servico_id):
    """Deleta um serviço com base no ID."""
    servicos_ref = db.collection("servicos")

    # Buscar pelo ID do serviço diretamente
    doc_ref = servicos_ref.document(servico_id)
    doc = doc_ref.get()

    if doc.exists:
        print(f"Serviço encontrado: {doc.id} - {doc.to_dict()}")
        doc_ref.delete()
    else:
        raise Exception(f"Serviço com ID '{servico_id}' não encontrado.")


def atualizar_valor_servico(servico_id, novo_valor):
    """Atualiza o valor de um serviço no Firestore usando o ID."""
    servicos_ref = db.collection("servicos")

    # Buscar o serviço pelo ID
    doc = servicos_ref.document(servico_id).get()

    if doc.exists:
        # Atualiza o valor do serviço encontrado
        doc.reference.update({"valor": novo_valor})
        print(f"Serviço com ID '{servico_id}' atualizado para o novo valor: R${novo_valor:.2f}")
    else:
        raise Exception(f"Serviço com ID '{servico_id}' não encontrado.")


def deletar_atendimento(atendimento_id):
    """
    Deleta um atendimento específico pelo ID do documento no Firestore.
    """
    try:
        atendimentos_ref = db.collection("atendimentos").document(atendimento_id)
        atendimentos_ref.delete()
    except Exception as e:
        raise Exception(f"Erro ao deletar atendimento: {e}")




# import sqlite3
# import streamlit as st
# from db.connection import conectar
#
# def cadastrar_servico(nome, valor):
#     conexao = conectar()
#     cursor = conexao.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO servicos (nome, valor) VALUES (?, ?)",
#             (nome, valor)
#         )
#         conexao.commit()
#     except Exception as e:
#         raise e
#     finally:
#         conexao.close()
#
# def listar_servicos():
#     conexao = conectar()
#     cursor = conexao.cursor()
#     cursor.execute("SELECT id, nome, valor FROM servicos")
#     servicos = cursor.fetchall()
#     conexao.close()
#     return servicos
#
# def deletar_servico(nome):
#     conexao = conectar()
#     cursor = conexao.cursor()
#     cursor.execute("DELETE FROM servicos WHERE nome = ?", (nome,))
#     conexao.commit()
#     conexao.close()
#
# def atualizar_valor_servico(servico_id, novo_valor):
#     """
#     Atualiza o valor de um serviço existente.
#     :param servico_id: ID do serviço a ser atualizado.
#     :param novo_valor: Novo valor do serviço.
#     """
#     conexao = conectar()
#     cursor = conexao.cursor()
#     cursor.execute(
#         "UPDATE servicos SET valor = ? WHERE id = ?",
#         (novo_valor, servico_id)
#     )
#     conexao.commit()
#     conexao.close()
#
# def deletar_atendimento(atendimento_id):
#     """Exclui um atendimento do banco de dados com base no ID."""
#     conexao = sqlite3.connect("atelier.db")
#     cursor = conexao.cursor()
#     try:
#         cursor.execute("DELETE FROM atendimentos WHERE id = ?", (atendimento_id,))
#         conexao.commit()
#         st.success(f"Atendimento com ID {atendimento_id} foi excluído com sucesso.")
#     except sqlite3.Error as e:
#         st.error(f"Erro ao excluir atendimento: {e}")
#     finally:
#         conexao.close()
#
