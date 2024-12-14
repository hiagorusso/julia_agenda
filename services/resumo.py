from db.connection import conectar

def consultar_resumo(mes, ano):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT s.nome, COUNT(a.id) AS quantidade, SUM(s.valor) AS total
        FROM atendimentos a
        JOIN servicos s ON a.servico_id = s.id
        WHERE strftime('%m', a.data) = ? AND strftime('%Y', a.data) = ?
        GROUP BY s.id
        """,
        (f"{int(mes):02}", str(ano))
    )
    resultados = cursor.fetchall()
    cursor.execute(
        """
        SELECT SUM(s.valor) FROM atendimentos a
        JOIN servicos s ON a.servico_id = s.id
        WHERE strftime('%m', a.data) = ? AND strftime('%Y', a.data) = ?
        """,
        (f"{int(mes):02}", str(ano))
    )
    total = cursor.fetchone()[0] or 0
    conexao.close()
    return resultados, total
