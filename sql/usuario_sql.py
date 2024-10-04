SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT,
        data_nascimento DATE NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        perfil INT NOT NULL,
        cnpj TEXT,
        genero TEXT,       
        endereco_cep TEXT NOT NULL,
        endereco_logradouro TEXT NOT NULL,
        endereco_numero TEXT NOT NULL,
        endereco_complemento TEXT,
        endereco_bairro TEXT NOT NULL,
        endereco_cidade TEXT NOT NULL,
        endereco_uf TEXT NOT NULL)
    """

SQL_INSERIR = """
    INSERT INTO usuario(nome, cpf, data_nascimento, email, senha, perfil, cnpj, genero, endereco_cep, endereco_logradouro, endereco_numero, endereco_complemento, endereco_bairro, endereco_cidade, endereco_uf)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SQL_ALTERAR_DADOS = """
    UPDATE usuario
    SET nome=?, email=?
    WHERE id=?
"""

SQL_ALTERAR_ENDERECO = """
    UPDATE usuario
    SET endereco_cep=?, endereco_logradouro=?, endereco_numero=?, endereco_complemento=?, endereco_bairro=?, endereco_cidade=?, endereco_uf=?
    WHERE id=?
"""
SQL_ALTERAR_SENHA = """
    UPDATE usuario
    SET senha=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM usuario    
    WHERE id=?
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, email, perfil
    FROM usuario
    WHERE id=?
"""

SQL_OBTER_POR_EMAIL = """
    SELECT id, nome, email, perfil, senha
    FROM usuario
    WHERE email=?
"""

SQL_OBTER_POR_TOKEN = """
    SELECT id, nome, email, perfil
    FROM usuario
    WHERE token=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*)
    FROM usuario
"""

SQL_EMAIL_EXISTE = """
    SELECT COUNT(*)
    FROM usuario
    WHERE email=?
"""
