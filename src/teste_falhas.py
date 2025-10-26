from db import get_conn

with get_conn() as con:
    cur = con.cursor()

    print("\nFalhas cadastradas:")
    for r in cur.execute("""
        SELECT f.id, e.nome, f.titulo
        FROM falhas f
        JOIN equipamentos e ON e.id = f.equipamento_id
        ORDER BY e.nome, f.titulo
    """):
        print(" -", r)

    print("\nSoluções da primeira falha:")
    f_id = cur.execute("SELECT id FROM falhas LIMIT 1").fetchone()[0]
    for s in cur.execute("""
        SELECT passo, descricao FROM solucoes WHERE falha_id=? ORDER BY passo
    """, (f_id,)):
        print(f"   [{s[0]}] {s[1]}")
