SQL_CRIAR_TABELA_RECLAMAR= """
CREATE TABLE IF NOT EXISTS reclamacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    historia TEXT NOT NULL,
    celular TEXT NOT NULL,
    telefone TEXT,
    arquivos TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);
"""

SQL_INSERIR_RECLAMACAO = """
INSERT INTO reclamacoes (usuario_id, titulo, historia, celular, telefone, arquivos)
VALUES (?, ?, ?, ?, ?, ?)
"""

SQL_BUSCAR_RECLAMACOES = """
SELECT r.id, r.usuario_id, r.titulo, r.historia, r.celular, r.telefone, r.arquivos, r.data_criacao, 
       u.nome AS usuario_nome
FROM reclamacoes r
INNER JOIN usuario u ON r.usuario_id = u.id
ORDER BY r.data_criacao DESC;
"""