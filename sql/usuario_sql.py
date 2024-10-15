SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cpf TEXT,
        cnpj TEXT,
        nome TEXT NOT NULL,
        data_nascimento DATE NOT NULL,
        genero TEXT,
        endereco_cidade TEXT NOT NULL,
        endereco_bairro TEXT NOT NULL,
        endereco_cep TEXT NOT NULL,
        endereco_numero TEXT NOT NULL,
        endereco_complemento TEXT,
        endereco_logradouro TEXT NOT NULL,    
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        perfil INT NOT NULL,   
        token TEXT)
    """

SQL_INSERIR = """
    INSERT INTO usuario(cpf, cnpj, nome,  data_nascimento, genero, endereco_cidade,  endereco_bairro, endereco_cep, endereco_numero, endereco_complemento, endereco_logradouro, email, senha, perfil)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SQL_OBTER_SENHA_POR_EMAIL = """
    SELECT senha
    FROM usuario
    WHERE email = ?
"""

SQL_OBTER_DADOS_POR_EMAIL = """
    SELECT id, nome, email, perfil
    FROM usuario
    WHERE email=?
"""

SQL_ALTERAR_DADOS = """
    UPDATE usuario
    SET nome=?, email=?
    WHERE id=?
"""

SQL_ALTERAR_ENDERECO = """
    UPDATE usuario
    SET endereco_cep=?, endereco_logradouro=?, endereco_numero=?, endereco_complemento=?, endereco_bairro=?, endereco_cidade=?
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
    SELECT id, nome, data_nascimento, email, perfil, token
    FROM usuario
    WHERE id=?
"""

SQL_OBTER_DADOS_POR_EMAIL = """
    SELECT id, nome, email, perfil, token
    FROM usuario
    WHERE email=?
"""

SQL_OBTER_POR_TOKEN = """
    SELECT id, nome, email, perfil, token
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
SQL_CHECAR_CREDENCIAIS = """
    SELECT email, senha, perfil
    FROM usuario
    WHERE email = ?
"""