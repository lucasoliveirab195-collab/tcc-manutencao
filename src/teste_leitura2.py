import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/tcc.sqlite3")

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

print("\nResumo (contagens):")
for tabela in ["ambientes", "setores", "linhas", "equipamentos"]:
    cur.execute(f"SELECT COUNT(*) FROM {tabela}")
    print(f" - {tabela}: {cur.fetchone()[0]}")

print("\nÁrvore Ambiente > Setor > Linha > Equipamentos (amostra):")
# Lista 2 ambientes qualquer
for (amb_id, amb_nome) in cur.execute("SELECT id, nome FROM ambientes ORDER BY id LIMIT 2"):
    print(f"\nAmbiente: {amb_nome} ({amb_id})")

    # setores do ambiente
    for (set_id, set_nome) in cur.execute(
        "SELECT id, nome FROM setores WHERE ambiente_id = ? ORDER BY id LIMIT 3", (
            amb_id,)
    ):
        print(f"  Setor: {set_nome} ({set_id})")

        # linhas desse setor
        for (lin_id, lin_nome) in cur.execute(
            "SELECT id, nome FROM linhas WHERE setor_id = ? ORDER BY id LIMIT 2", (
                set_id,)
        ):
            print(f"    Linha: {lin_nome} ({lin_id})")

            # equipamentos da linha
            for (eq_id, eq_nome) in cur.execute(
                "SELECT id, nome FROM equipamentos WHERE linha_id = ? ORDER BY id LIMIT 3", (
                    lin_id,)
            ):
                print(f"      Equipamento: {eq_nome} ({eq_id})")

        # equipamentos diretamente no setor (sem linha)
        for (eq_id, eq_nome) in cur.execute(
            "SELECT id, nome FROM equipamentos WHERE setor_id = ? AND linha_id IS NULL ORDER BY id LIMIT 3",
            (set_id,)
        ):
            print(f"    Equipamento (sem linha): {eq_nome} ({eq_id})")

con.close()
