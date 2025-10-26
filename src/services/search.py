# src/services/search.py

"""
Serviços de busca textual (FTS5) nas falhas cadastradas.

Funções principais:
- preparar_query_fts(q): normaliza o texto do usuário para a sintaxe do FTS5
- buscar_falhas_por_texto(q, limite=10): retorna [(id, equipamento, titulo, descricao), ...]

Requisitos:
- Tabela 'falhas' com colunas (id, equipamento_id, titulo, descricao)
- Tabela virtual 'falhas_fts' (FTS5) indexando ao menos (titulo, descricao)
- Tabela 'equipamentos' (id, nome) para o JOIN
"""

from __future__ import annotations

import re
from typing import List, Tuple

from src.db import get_conn


def preparar_query_fts(q: str) -> str:
    """
    Converte o texto digitado pelo usuário em uma consulta segura para o FTS5.

    Estratégia:
    - remove aspas e pontuações problemáticas
    - quebra em termos por espaço
    - aplica '*' (prefixo) para permitir casar inícios de palavras
    - por padrão, espaços em MATCH são AND, então "motor parado"
      vira "motor* parado*" (ambos precisam aparecer)

    Ex.: "robô paletizador parado" -> "robô* paletizador* parado*"
    """
    if not q:
        return ""

    # tira aspas e pontuações que atrapalham a sintaxe do MATCH
    q = q.strip()
    q = re.sub(r"[\"'`]", " ", q)           # aspas
    # pontuação exceto _, -, espaços e acentos comuns
    q = re.sub(r"[^\wÀ-ÿ\s_-]", " ", q)

    termos = [t for t in q.split() if t]
    if not termos:
        return ""

    # aplica prefixo para cada termo
    termos_prefix = [f"{t}*" for t in termos]
    # espaço = AND em FTS5
    return " ".join(termos_prefix)


def buscar_falhas_por_texto(q: str, limite: int = 10) -> List[Tuple[int, str, str, str]]:
    """
    Busca falhas usando FTS5 e retorna uma lista de tuplas:
      (falha_id, equipamento_nome, titulo, descricao)

    Parâmetros:
      q      -> texto digitado pelo usuário
      limite -> máximo de linhas a retornar (default 10)
    """
    fts_query = preparar_query_fts(q)
    if not fts_query:
        return []

    with get_conn() as con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT
                f.id,
                e.nome AS equipamento,
                f.titulo,
                f.descricao
            FROM falhas_fts AS fts
            JOIN falhas       AS f ON fts.rowid = f.id
            JOIN equipamentos AS e ON e.id      = f.equipamento_id
            WHERE fts MATCH ?
            LIMIT ?
            """,
            (fts_query, limite),
        )
        resultados = cur.fetchall()

    # resultados vem como lista de tuplas já no formato esperado
    return resultados
