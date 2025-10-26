import csv
from db import get_conn

CSV_AMB = "db/ambientes.csv"
CSV_SET = "db/setores.csv"


def importar_ambientes(cur) -> int:
    count = 0
    with open(CSV_AMB, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            _id = (row.get("id") or "").strip()
            nome = (row.get("nome") or "").strip()
            if not _id or not nome:
                continue
            cur.execute("""
                INSERT OR REPLACE INTO ambientes (id, nome)
                VALUES (?, ?)
            """, (_id, nome))
            count += 1
    return count


def importar_setores(cur) -> int:
    count = 0
    with open(CSV_SET, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            _id = (row.get("id") or "").strip()
            ambiente_id = (row.get("ambiente_id") or "").strip()
            nome = (row.get("nome") or "").strip()
            if not _id or not ambiente_id or not nome:
                continue
            cur.execute("""
                INSERT OR REPLACE INTO setores (id, ambiente_id, nome)
                VALUES (?, ?, ?)
            """, (_id, ambiente_id, nome))
            count += 1
    return count


if __name__ == "__main__":
    with get_conn() as con:
        try:
            con.execute("BEGIN IMMEDIATE;")
            cur = con.cursor()

            c1 = importar_ambientes(cur)
            print(f"ambientes importados: {c1}")

            c2 = importar_setores(cur)
            print(f"setores importados: {c2}")

            con.commit()
            print("✅ importação mínima concluída")
        except Exception as e:
            con.rollback()
            print("❌ erro – importação mínima revertida:", e)
            raise
