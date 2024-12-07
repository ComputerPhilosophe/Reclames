import json
import sqlite3
from typing import Optional
from models.usuario_model import Usuario
from sql.usuario_sql import *
from util.auth import obter_hash_senha, conferir_senha
from util.database import obter_conexao


class UsuarioRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)


    @classmethod
    def inserir(cls, usuario: Usuario) -> Optional[Usuario]:
            with obter_conexao() as db:
                cursor = db.cursor()
                resultado = cursor.execute(
                    SQL_INSERIR, 
                    (   
                        usuario.cpf,
                        usuario.cnpj,                     
                        usuario.nome,
                        usuario.data_nascimento,
                        usuario.genero,
                        usuario.endereco_cidade,
                        usuario.endereco_bairro,
                        usuario.endereco_cep,
                        usuario.endereco_numero,
                        usuario.endereco_complemento,
                        usuario.endereco_logradouro,
                        usuario.email,
                        usuario.senha,
                        usuario.perfil  
   
                    ))
            return resultado.rowcount > 0        

    @classmethod
    def inserir_admins(cls):
        try:
            senha_hash_lara = obter_hash_senha("123456")  
            senha_hash_caio = obter_hash_senha("123")  
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR, 
                    (    
                        "2086022569",          
                        "",                     
                        "Lara Zanotelli",       
                        "1998-08-12",           
                        "Feminino",             
                        "Cachoeiro de Itapemirim", 
                        "Zumbi",               
                        "29308115",             
                        "22",                   
                        "hospital elefante branco", 
                        "Rua Parecis",          
                        "lara@gmail.com",       
                        senha_hash_lara,        
                        3                       
                    ))

                cursor.execute(
                    SQL_INSERIR, 
                    (    
                        "12345678900",         
                        "",                    
                        "Caio Brun de Oliveira", 
                        "1990-03-24",          
                        "Masculino",           
                        "Vitória",             
                        "Centro",              
                        "29308115",            
                        "22",                  
                        "hospital elefante branco", 
                        "Rua Parecis",         
                        "caio@gmail.com",      
                        senha_hash_caio,       
                        3                      
                    ))

        except sqlite3.Error as ex:
            print(ex)
        return None
            
    @staticmethod
    def obter_senha_por_email(email: str) -> Optional[str]:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_SENHA_POR_EMAIL, (email,))
            dados = cursor.fetchone()
            if dados is None:
                return None
            return dados["senha"]
        
    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_ID, (id,)).fetchone()
                if tupla:
                    usuario = Usuario(*tupla)
                    return usuario
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None    

    @staticmethod
    def obter_dados_por_email(email: str) -> Optional[Usuario]:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_DADOS_POR_EMAIL, (email,))
            dados = cursor.fetchone()
            if dados is None:
                return None
            return Usuario(**dados)
        

    @classmethod
    def obter_por_token(cls, token: str) -> Optional[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_TOKEN, (token,)).fetchone()
                if tupla:
                    usuario = Usuario(*tupla)
                    return usuario
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None          
    
   
         
    @staticmethod
    def atualizar_dados(usuario: Usuario) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(
            SQL_ALTERAR_DADOS,
            (
                usuario.cpf,
                usuario.cnpj,
                usuario.nome,
                usuario.data_nascimento,
                usuario.genero,
                usuario.endereco_cidade,
                usuario.endereco_bairro,
                usuario.endereco_cep,
                usuario.endereco_numero,
                usuario.endereco_complemento,
                usuario.endereco_logradouro,
                usuario.email,
                usuario.id,
            ),
        )
        if cursor.rowcount == 0:
            return False
        return True

        
    @classmethod
    def alterar_endereco(cls, usuario: Usuario) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR_ENDERECO,
                    (
                        usuario.endereco_cep,
                        usuario.endereco_logradouro,
                        usuario.endereco_numero,
                        usuario.endereco_complemento,
                        usuario.endereco_bairro,
                        usuario.endereco_cidade,
                        usuario.endereco_uf,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def alterar_senha(cls, usuario: Usuario) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR_DADOS,
                    (
                        usuario.senha,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_ID, (id,)).fetchone()
                if tupla:
                    usuario = Usuario(*tupla)
                    return usuario
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def obter_por_email(cls, email: str) -> Optional[Usuario]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                (id, nome, data_nascimento, cpf, cnpj, email, senha, endereco_bairro, endereco_cidade, perfil) = cursor.execute(SQL_OBTER_DADOS_POR_EMAIL, (email,)).fetchone()
                if id:
                    usuario = Usuario(
                        id=id, 
                        nome=nome,
                        data_nascimento=data_nascimento,
                        cpf=cpf,
                        cnpj=cnpj,                         
                        email=email, 
                        perfil=perfil, 
                        senha=senha,
                        endereco_bairro=endereco_bairro,
                        endereco_cidade=endereco_cidade)
                    return usuario
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_quantidade(cls) -> int:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return 0

    @classmethod
    def inserir_dados_json(cls):
        if UsuarioRepo.obter_quantidade() == 0:
            with open("sql/usuarios.json", "r", encoding="utf-8") as arquivo:
                usuarios = json.load(arquivo)
                for usuario in usuarios:
                    UsuarioRepo.inserir(Usuario(**usuario))

    @classmethod
    def email_existe(cls, email: str) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_EMAIL_EXISTE, (email,)).fetchone()
                return tupla[0] > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
        
    @classmethod
    def checar_credenciais(cls, email: str, senha: str) -> Optional[tuple]:
        with obter_conexao() as db:
            cursor = db.cursor()
            dados = cursor.execute(
                SQL_CHECAR_CREDENCIAIS, (email,)).fetchone()
            if dados:
                if conferir_senha(senha, dados[3]):
                    return (dados[0], dados[1], dados[2])
            return None
        
    @classmethod
    def obter_todos(cls) -> list[Usuario]:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            usuarios = cursor.execute("SELECT id, nome, email FROM usuario").fetchall()
            return [Usuario(id=u[0], nome=u[1], email=u[2]) for u in usuarios]


    @staticmethod
    def obter_dados_por_email(email: str) -> Optional[Usuario]:
            with obter_conexao() as db:
                cursor = db.cursor()
                cursor.execute(SQL_OBTER_DADOS_POR_EMAIL, (email,))
                dados = cursor.fetchone()
                if dados is None:
                    return None
                return Usuario(**dados)


@staticmethod
def obter_senha_por_email(email: str) -> Optional[str]:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_SENHA_POR_EMAIL, (email,))
            dados = cursor.fetchone()
            if dados is None:
                return None
            return dados["senha"]


@staticmethod
def listar_todos():
        try:
            # Conectando ao banco de dados (ajuste o caminho do arquivo para seu banco)
            conn = sqlite3.connect( )
            cursor = conn.cursor()

            # Query SQL para selecionar todos os usuários
            cursor.execute("SELECT id, nome, email, perfil, cpf, data_nascimento, endereco_cidade, endereco_bairro FROM usuarios")
            usuarios = cursor.fetchall()  # Retorna uma lista de tuplas com os dados dos usuários

            # Convertendo as tuplas para dicionários (opcional, para facilitar o uso)
            lista_usuarios = [
                {
                    "id": usuario[0],
                    "nome": usuario[1],
                    "email": usuario[2],
                    "perfil": usuario[3],
                    "cpf": usuario[4],
                    "data_nascimento": usuario[5],
                    "endereco_cidade": usuario[6],
                    "endereco_bairro": usuario[7],
                }
                for usuario in usuarios
            ]

            return lista_usuarios

        except sqlite3.Error as e:
            print(f"Erro ao listar usuários: {e}")
            return []
        finally:
            if conn:
                conn.close()                            