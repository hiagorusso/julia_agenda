import sqlite3

DB_PATH = "atelier.db"

def conectar():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DB_PATH)

def criar_tabelas():
    """Cria as tabelas do banco, se não existirem."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            valor REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            servico_id INTEGER NOT NULL,
            FOREIGN KEY (servico_id) REFERENCES servicos(id)
        )
    ''')
    conexao.commit()
    conexao.close()
