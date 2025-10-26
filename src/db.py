# src/db.py
import sqlite3
from contextlib import contextmanager

# Caminho do banco
DB_PATH = "db/tcc.sqlite3"


def connect():
    # Abre o banco
    con = sqlite3.connect(DB_PATH)

    # 🔹 Aqui é onde ativamos a verificação de chaves estrangeiras
    con.execute("PRAGMA foreign_keys = ON;")

    # 🔹 Essas duas linhas são opcionais, mas deixam o banco mais estável
    con.execute("PRAGMA journal_mode = WAL;")
    con.execute("PRAGMA synchronous = NORMAL;")

    return con

# Função para usar a conexão com segurança


@contextmanager
def get_conn():
    con = connect()
    try:
        yield con  # "entrega" a conexão para o código que for usar
    finally:
        con.close()  # garante que será fechada depois
