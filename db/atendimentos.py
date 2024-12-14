from db.connection import conectar

def adicionar_atendimento(data, servico_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO atendimentos (data, servico_id) VALUES (?, ?)",
        (data, servico_id)
    )
    conexao.commit()
    conexao.close()
