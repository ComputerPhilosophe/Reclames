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
    def inserir(cls, usuario: Usuario) -> bool:
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
            senha_hash = obter_hash_senha("123456")
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR, (    
                        "15447833925",
                        "",                    
                        "Caio Brun de Oliveira",
                        "2005-04-18",
                        "Masculino",
                        "Cachoeiro de Itapemirim",
                        "Aquidaban",
                        "29308115",
                        "22",
                        "hospital elefante branco",
                        "Rua Parecis",
                        "caiobrundeoliveira@gmail.com",
                        senha_hash,
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
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla  = cursor.execute(SQL_OBTER_DADOS_POR_EMAIL, (email,)).fetchone()
                if tupla:
                    usuario = Usuario(*tupla)
                    return usuario
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None
        
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
    
   
                # inserir Lara
         
    @classmethod
    def alterar_dados(cls, usuario: Usuario) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR_DADOS,
                    (
                        usuario.nome,
                        usuario.cpf,
                        usuario.data_nascimento,
                        usuario.email,
                        usuario.senha,
                        usuario.perfil,
                        usuario.cnpj,
                        usuario.genero,    
                        usuario.endereco_cep,
                        usuario.endereco_logradouro,
                        usuario.endereco_numero,
                        usuario.endereco_complemento,
                        usuario.endereco_bairro,
                        usuario.endereco_cidade,
                        usuario.endereco_uf
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
        
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
                (id, nome, email, perfil, senha) = cursor.execute(SQL_OBTER_DADOS_POR_EMAIL, (email,)).fetchone()
                if id:
                    usuario = Usuario(
                        id=id, 
                        nome=nome, 
                        email=email, 
                        perfil=perfil, 
                        senha=senha)
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
                if conferir_senha(senha, dados[1]):
                    return (dados[0], dados[1], dados[2])
            return None