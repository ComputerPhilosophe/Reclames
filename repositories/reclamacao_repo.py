import json
import sqlite3
from typing import Optional
from models.reclamacao_model import Reclamacao
from models.usuario_model import Usuario
from sql.reclamacoes_sql import *
from sql.usuario_sql import *
from util.auth import obter_hash_senha, conferir_senha
from util.database import obter_conexao
import os
from werkzeug.utils import secure_filename
from sqlite3 import Error

class ReclamacaoRepo:
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA_RECLAMAR)


    @classmethod
    def listar_reclamacoes(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_BUSCAR_RECLAMACOES)
        resultados = cursor.fetchall()

        reclamacoes = []
        for linha in resultados:
            reclamacao = {
            "id": linha["id"],
            "usuario_id": linha["usuario_id"],
            "titulo": linha["titulo"],
            "historia": linha["historia"],
            "celular": linha["celular"],
            "arquivos": linha["arquivos"].split(",") if linha["arquivos"] else [],
            "data_criacao": linha["data_criacao"],
            "usuario_nome": linha["usuario_nome"],
        }
            reclamacoes.append(reclamacao)

        return reclamacoes




# Diretório onde os arquivos serão armazenados
UPLOAD_FOLDER = 'static/reclamacoes'

# Definindo as extensões permitidas (opcional)
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def inserir_reclamacao_com_arquivo(usuario_id: int, titulo: str, historia: str, celular: str, arquivo=None):
    try:
        # Se houver um arquivo, fazemos o upload
        arquivo_path = None
        if arquivo and allowed_file(arquivo.filename):
            # Garantir que o nome do arquivo seja seguro para o sistema de arquivos
            filename = secure_filename(arquivo.filename)
            arquivo_path = os.path.join(UPLOAD_FOLDER, filename)

            # Salvar o arquivo no diretório especificado
            arquivo.save(arquivo_path)
        
        # Inserir a reclamação no banco de dados
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_INSERIR_RECLAMACAO, (
                usuario_id,
                titulo,
                historia,
                celular,
                arquivo_path  # Salva o caminho do arquivo no banco de dados
            ))
            conexao.commit()
            
        return "Reclamação registrada com sucesso!", 201
    except Error as e:
        print(f"Erro ao registrar reclamação: {e}")
        return "Erro ao registrar reclamação", 500

