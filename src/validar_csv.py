# src/validar_csv.py
import csv
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "tcc.sqlite3")
LINHAS_CSV = os.path.join(BASE_DIR, "..", "db", "linhas.csv")
EQS_CSV = os.path.join(BASE_DIR, "..", "db", "equipamentos.csv")


def carregar_ids_tabela(conn, tabela):
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM {tabela}")
    return {row[0] for row in cur.fetchall()}


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    setores_ids = carregar_ids_tabela(conn, "setores")

    # Verificar linhas -> setores
    faltando_setor = set()
    with open(LINHAS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["setor_id"].strip()
            if sid not in setores_ids:
                faltando_setor.add(sid)

    if faltando_setor:
        print("❌ Em 'linhas.csv', estes setor_id NÃO existem em 'setores':")
        for x in sorted(faltando_setor):
            print("   -", repr(x))
    else:
        print("✅ Todos os setor_id de 'linhas.csv' existem em 'setores'.")

    # Se quiser também validar equipamentos -> linhas:
    try:
        linhas_ids = carregar_ids_tabela(conn, "linhas")
        faltando_linha = set()
        with open(EQS_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lid = row["linha_id"].strip()
                if lid not in linhas_ids:
                    faltando_linha.add(lid)
        if faltando_linha:
            print("❌ Em 'equipamentos.csv', estes linha_id NÃO existem em 'linhas':")
            for x in sorted(faltando_linha):
                print("   -", repr(x))
        else:
            print("✅ Todos os linha_id de 'equipamentos.csv' existem em 'linhas'.")
    except FileNotFoundError:
        print("ℹ️ 'equipamentos.csv' ainda não encontrado (ok por enquanto).")

    conn.close()


if __name__ == "__main__":
    main()
