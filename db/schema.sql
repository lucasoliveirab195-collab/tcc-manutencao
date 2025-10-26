PRAGMA foreign_keys = ON;

-- 1) Ambientes (ex.: Portaria 1, Estacionamento, Fábrica 1, ETE, etc.)
CREATE TABLE IF NOT EXISTS ambientes (
  id   TEXT PRIMARY KEY,   -- código curto, ex.: AMB-F1
  nome TEXT NOT NULL       -- nome descritivo, ex.: Fábrica 1
);

-- 2) Setores (sempre pertencem a um Ambiente)
CREATE TABLE IF NOT EXISTS setores (
  id           TEXT PRIMARY KEY,                                   -- ex.: SET-PROD
  ambiente_id  TEXT NOT NULL REFERENCES ambientes(id) ON DELETE CASCADE,
  nome         TEXT NOT NULL
);
-- =========================
-- Nível 2: linhas e equipamentos
-- =========================

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS linhas (
  id         TEXT PRIMARY KEY,
  setor_id   TEXT NOT NULL,
  nome       TEXT NOT NULL,
  FOREIGN KEY (setor_id) REFERENCES setores(id) ON DELETE CASCADE
);

-- Observação: nem todo equipamento pertence a uma "linha".
-- Por isso, linha_id é opcional (NULL). Porém TODO equipamento pertence a um setor.
CREATE TABLE IF NOT EXISTS equipamentos (
  id         TEXT PRIMARY KEY,
  setor_id   TEXT NOT NULL,
  linha_id   TEXT,               -- pode ser NULL
  nome       TEXT NOT NULL,
  descricao  TEXT,
  FOREIGN KEY (setor_id) REFERENCES setores(id) ON DELETE CASCADE,
  FOREIGN KEY (linha_id) REFERENCES linhas(id)   ON DELETE SET NULL
);

-- Índices úteis para buscas
CREATE INDEX IF NOT EXISTS idx_linhas_setor   ON linhas(setor_id);
CREATE INDEX IF NOT EXISTS idx_equip_setor    ON equipamentos(setor_id);
CREATE INDEX IF NOT EXISTS idx_equip_linha    ON equipamentos(linha_id);
-- Falhas por equipamento
CREATE TABLE IF NOT EXISTS falhas (
  id            TEXT PRIMARY KEY,
  equipamento_id TEXT NOT NULL,
  titulo        TEXT NOT NULL,
  sintomas      TEXT,         -- o que o técnico vê/ouve/medidas
  causa_provavel TEXT,        -- hipótese principal
  severidade    INTEGER,      -- 1..5 (opcional)
  recorrencia   INTEGER,      -- 1..5 (opcional)
  criado_em     TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id)
);

-- Ações/Soluções ligadas a uma falha (uma falha pode ter várias soluções)
CREATE TABLE IF NOT EXISTS solucoes (
  id        TEXT PRIMARY KEY,
  falha_id  TEXT NOT NULL,
  passo     INTEGER NOT NULL, -- 1,2,3...
  descricao TEXT NOT NULL,    -- o que fazer
  sucesso   INTEGER,          -- 0/1 (opcional; se já validado)
  FOREIGN KEY (falha_id) REFERENCES falhas(id)
);

-- Índices para pesquisa rápida
CREATE INDEX IF NOT EXISTS idx_falhas_equip ON falhas(equipamento_id);
CREATE INDEX IF NOT EXISTS idx_solucoes_falha ON solucoes(falha_id);
-- =====================================================
-- Tabela de busca textual (FTS) para falhas
-- =====================================================
CREATE VIRTUAL TABLE IF NOT EXISTS falhas_fts USING fts5(
    titulo,
    descricao,
    content='falhas',
    content_rowid='id'
);
