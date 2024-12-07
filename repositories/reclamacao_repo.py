import json
import sqlite3
from typing import Optional
from models.reclamacao_model import Reclamacao
from models.usuario_model import Usuario
from sql.reclamacoes_sql import *
from sql.usuario_sql import *
from util.auth import obter_hash_senha, conferir_senha
from util.database import obter_conexao

class ReclamacaoRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA_RECLAMAR)


     
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
    def inserir(cls, reclamacao: Reclamacao) -> bool:
        with obter_conexao() as db:
            cursor = db.cursor()
        resultado = cursor.execute(
            SQL_INSERIR_RECLAMACAO,
            (
                reclamacao.usuario_id,
                reclamacao.titulo,
                reclamacao.historia,
                reclamacao.celular,
                reclamacao.telefone,
                ",".join(reclamacao.arquivos) if reclamacao.arquivos else None,
                reclamacao.criado_em
            )
        )
        db.commit()
        return cursor.lastrowid > 0         