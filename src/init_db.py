from db import get_conn
import os

SCHEMA = os.path.join("db", "schema.sql")
SEED = os.path.join("db", "seed.sql")  # opcional (recomendo manter vazio)


def init_db():
    with get_conn() as con:
        cur = con.cursor()
        # aplica o schema (DDL)
        with open(SCHEMA, "r", encoding="utf-8") as f:
            cur.executescript(f.read())

        # (opcional) aplica seed apenas se existir e tiver conteúdo "útil"
        if os.path.exists(SEED) and os.path.getsize(SEED) > 10:
            with open(SEED, "r", encoding="utf-8") as f:
                cur.executescript(f.read())

        con.commit()
        print("✅ Banco criado/atualizado em: db/tcc.sqlite3")


if __name__ == "__main__":
    init_db()
