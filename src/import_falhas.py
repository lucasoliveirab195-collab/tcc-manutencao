import csv
from db import get_conn


def importar_falhas(cur):
    with open("db/falhas.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cur.execute("""
                INSERT OR REPLACE INTO falhas
                (id, equipamento_id, titulo, sintomas, causa_provavel, severidade, recorrencia)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row["id"].strip(),
                row["equipamento_id"].strip(),
                row["titulo"].strip(),
                row.get("sintomas", "").strip(),
                row.get("causa_provavel", "").strip(),
                int(row.get("severidade") or 0),
                int(row.get("recorrencia") or 0)
            ))


def importar_solucoes(cur):
    with open("db/solucoes.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cur.execute("""
                INSERT OR REPLACE INTO solucoes
                (id, falha_id, passo, descricao, sucesso)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row["id"].strip(),
                row["falha_id"].strip(),
                int(row["passo"]),
                row["descricao"].strip(),
                int(row.get("sucesso") or 0)
            ))


if __name__ == "__main__":
    with get_conn() as con:
        try:
            con.execute("BEGIN")
            cur = con.cursor()
            importar_falhas(cur)
            importar_solucoes(cur)
            con.commit()
            print("✅ falhas + soluções importadas com sucesso!")
        except Exception as e:
            con.rollback()
            print("❌ erro – importação revertida:", e)
            raise
