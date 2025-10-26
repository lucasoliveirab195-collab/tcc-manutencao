import os
import sqlite3

# Caminho do banco
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/tcc.sqlite3")

# Conexão
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

print("\nTabelas e contagens:")

# Verifica as tabelas e mostra o número de registros
for tabela in ["ambientes", "setores"]:
    cur.execute(f"SELECT COUNT(*) FROM {tabela}")
    count = cur.fetchone()[0]
    print(f" - {tabela}: {count} registro(s)")

print("\nPrimeiros ambientes:")
for row in cur.execute("SELECT id, nome FROM ambientes LIMIT 5"):
    print(row)

print("\nPrimeiros setores:")
for row in cur.execute("SELECT id, ambiente_id, nome FROM setores LIMIT 5"):
    print(row)

con.close()
