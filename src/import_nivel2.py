# src/import_nivel2.py
import os
import csv
from db import get_conn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "db")
PATH_LINHAS = os.path.join(DB_DIR, "linhas.csv")
PATH_EQUIP = os.path.join(DB_DIR, "equipamentos.csv")


def importar_linhas(cur):
    """
    Lê db/linhas.csv e insere/atualiza na tabela 'linhas'.
    CSV esperado: id,setor_id,nome
    """
    count = 0
    with open(PATH_LINHAS, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            _id = row["id"].strip()
            setor_id = row["setor_id"].strip()
            nome = row["nome"].strip()

            cur.execute(
                """
                INSERT OR REPLACE INTO linhas (id, setor_id, nome)
                VALUES (?, ?, ?)
                """,
                (_id, setor_id, nome),
            )
            count += 1
    print(f"linhas importadas: {count}")


def importar_equipamentos(cur):
    """
    Lê db/equipamentos.csv e insere/atualiza na tabela 'equipamentos'.
    CSV esperado: id,linha_id,nome,descricao
    O setor_id é obtido olhando a linha associada (FK).
    """
    count = 0
    with open(PATH_EQUIP, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            _id = row["id"].strip()
            linha_id = row["linha_id"].strip()
            nome = row["nome"].strip()
            desc = (row.get("descricao") or "").strip()

            # Descobre o setor_id da linha
            cur.execute(
                "SELECT setor_id FROM linhas WHERE id = ?", (linha_id,))
            r = cur.fetchone()
            if not r:
                # Se a linha não existir, avisa e pula
                print(
                    f"⚠️  linha '{linha_id}' não encontrada para equipamento '{_id}', pulando.")
                continue
            setor_id = r[0]

            cur.execute(
                """
                INSERT OR REPLACE INTO equipamentos
                    (id, linha_id, setor_id, nome, descricao)
                VALUES (?, ?, ?, ?, ?)
                """,
                (_id, linha_id, setor_id, nome, desc),
            )
            count += 1
    print(f"equipamentos importados: {count}")
    print("✅ importação de linhas e equipamentos concluída")


if __name__ == "__main__":
    # transação única para garantir consistência; se algo falhar, faz rollback
    with get_conn() as con:
        try:
            con.execute("BEGIN IMMEDIATE;")
            cur = con.cursor()

            importar_linhas(cur)
            importar_equipamentos(cur)

            con.commit()
        except Exception as e:
            con.rollback()
            print("❌ erro – importação nível 2 revertida:", e)
            raise
