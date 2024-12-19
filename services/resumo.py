from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

def consultar_resumo(mes, ano):
    """
    Consulta o resumo de atendimentos em um mês específico.

    Args:
        mes (int): Mês do resumo.
        ano (int): Ano do resumo.

    Returns:
        tuple: Uma lista de dicionários com resumo por serviço e o total geral.
    """
    try:
        # Filtrar atendimentos por mês e ano
        atendimentos_ref = db.collection("atendimentos")
        atendimentos = atendimentos_ref.stream()

        # Recuperar todos os serviços
        servicos_ref = db.collection("servicos")
        servicos = {servico.id: servico.to_dict() for servico in servicos_ref.stream()}

        resumo = {}
        total = 0.0

        # Verificar cada atendimento
        for atendimento in atendimentos:
            dados = atendimento.to_dict()

            # O campo "servico" no atendimento contém o nome ou ID do serviço
            nome_servico_atendimento = dados.get("servico")
            if not nome_servico_atendimento:
                # Caso o campo "servico" não exista, podemos pular o atendimento
                print(f"Atendimento {atendimento.id} sem campo 'servico'. Pulando...")
                continue

            # Ajuste para garantir que a data seja corretamente convertida
            data_atendimento = datetime.strptime(dados["data"], "%Y-%m-%d")

            # Verifique se a data do atendimento corresponde ao mês e ano desejado
            if data_atendimento.month == mes and data_atendimento.year == ano:
                # Agora procuramos o serviço, tanto pelo nome quanto pelo ID
                servico = None
                if nome_servico_atendimento in servicos:
                    servico = servicos[nome_servico_atendimento]
                else:
                    # Verifica se o "servico" é um ID válido de um serviço
                    for servico_item in servicos.values():
                        if servico_item.get("nome") == nome_servico_atendimento:
                            servico = servico_item
                            break

                # Se o serviço não for encontrado, registramos como "Serviço desconhecido"
                if not servico:
                    nome_servico = "Serviço desconhecido"
                    valor_servico = 0.0
                else:
                    nome_servico = servico.get("nome", "Serviço desconhecido")
                    valor_servico = servico.get("valor", 0.0)

                # Atualiza o resumo com o serviço encontrado
                if nome_servico_atendimento not in resumo:
                    resumo[nome_servico_atendimento] = {
                        "nome": nome_servico,
                        "quantidade": 0,
                        "total": 0.0,
                    }

                resumo[nome_servico_atendimento]["quantidade"] += 1
                resumo[nome_servico_atendimento]["total"] += valor_servico
                total += valor_servico

        # Formatar o resultado
        resumo_list = [
            {"nome": dados["nome"], "quantidade": dados["quantidade"], "total": dados["total"]}
            for dados in resumo.values()
        ]
        return resumo_list, total

    except Exception as e:
        raise Exception(f"Erro ao consultar resumo: {e}")


# from google.cloud import firestore
# from datetime import datetime
#
# db = firestore.Client()
#
#
# def consultar_resumo(mes, ano):
#     """
#     Consulta o resumo de atendimentos em um mês específico.
#
#     Args:
#         mes (int): Mês do resumo.
#         ano (int): Ano do resumo.
#
#     Returns:
#         tuple: Uma lista de dicionários com resumo por serviço e o total geral.
#     """
#     try:
#         # Filtrar atendimentos por mês e ano
#         atendimentos_ref = db.collection("atendimentos")
#         atendimentos = atendimentos_ref.stream()
#
#         servicos_ref = db.collection("servicos")
#         servicos = {servico.id: servico.to_dict() for servico in servicos_ref.stream()}
#
#         resumo = {}
#         total = 0.0
#
#         for atendimento in atendimentos:
#             dados = atendimento.to_dict()
#             data_atendimento = datetime.strptime(dados["data"], "%Y-%m-%d")
#
#             if data_atendimento.month == mes and data_atendimento.year == ano:
#                 servico_id = dados["servico_id"]
#                 servico = servicos.get(servico_id, {})
#                 nome_servico = servico.get("nome", "Serviço desconhecido")
#                 valor_servico = servico.get("valor", 0.0)
#
#                 if servico_id not in resumo:
#                     resumo[servico_id] = {
#                         "nome": nome_servico,
#                         "quantidade": 0,
#                         "total": 0.0,
#                     }
#                 resumo[servico_id]["quantidade"] += 1
#                 resumo[servico_id]["total"] += valor_servico
#                 total += valor_servico
#
#         # Formatar o resultado
#         resumo_list = [
#             {"nome": dados["nome"], "quantidade": dados["quantidade"], "total": dados["total"]}
#             for dados in resumo.values()
#         ]
#         return resumo_list, total
#     except Exception as e:
#         raise Exception(f"Erro ao consultar resumo: {e}")

# from db.connection import conectar
#
# def consultar_resumo(mes, ano):
#     conexao = conectar()
#     cursor = conexao.cursor()
#     cursor.execute(
#         """
#         SELECT s.nome, COUNT(a.id) AS quantidade, SUM(s.valor) AS total
#         FROM atendimentos a
#         JOIN servicos s ON a.servico_id = s.id
#         WHERE strftime('%m', a.data) = ? AND strftime('%Y', a.data) = ?
#         GROUP BY s.id
#         """,
#         (f"{int(mes):02}", str(ano))
#     )
#     resultados = cursor.fetchall()
#     cursor.execute(
#         """
#         SELECT SUM(s.valor) FROM atendimentos a
#         JOIN servicos s ON a.servico_id = s.id
#         WHERE strftime('%m', a.data) = ? AND strftime('%Y', a.data) = ?
#         """,
#         (f"{int(mes):02}", str(ano))
#     )
#     total = cursor.fetchone()[0] or 0
#     conexao.close()
#     return resultados, total
