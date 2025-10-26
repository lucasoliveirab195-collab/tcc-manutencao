import os
import sqlite3

# Caminho até o banco
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/tcc.sqlite3")

# Conexão
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

print("\nAmbientes (id, nome):")
for r in cur.execute("SELECT id, nome FROM ambientes ORDER BY id"):
    print(r)

print("\nSetores (id, ambiente_id, nome):")
for r in cur.execute("SELECT id, ambiente_id, nome FROM setores ORDER BY id"):
    print(r)

con.close()
