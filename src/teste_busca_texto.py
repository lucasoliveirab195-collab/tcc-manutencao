# src/teste_busca_texto.py
from src.services.search import buscar_falhas_por_texto


def mostrar(q):
    print(f"\n>>> consulta: {q}")
    resultados = buscar_falhas_por_texto(q, limite=10)
    if not resultados:
        print("  (sem resultados)")
        return
    for r in resultados:
        # r: (falha_id, equipamento_id, equipamento_nome, titulo, descricao)
        print(f" - [{r[0]}] {r[3]}  |  Equip: {r[2]}  |  {r[4][:80]}")


if __name__ == "__main__":
    # coloque aqui termos que você SABE que existem nos CSVs
    mostrar("Robô paletizador parado")
    mostrar("Embaladeira")
    mostrar("Detector de metais")
    mostrar("Masseira Progresso")
