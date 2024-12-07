from urllib import request
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from flask import app
from streamlit import status

from models.usuario_model import Usuario
from repositories import usuario_repo
from repositories.reclamacao_repo import inserir_reclamacao_com_arquivo
from repositories.usuario_repo import UsuarioRepo
from util.mensagens import adicionar_mensagem_erro, adicionar_mensagem_sucesso
from util.templates import obter_jinja_templates


@app.route('/reclamares', methods=['POST'])
def registrar_reclamacao():
    usuario_id = request.form['usuario_id']
    titulo = request.form['titulo']
    historia = request.form['historia']
    celular = request.form['celular']
    arquivo = request.files.get('arquivo')
    
    mensagem, status_code = inserir_reclamacao_com_arquivo(usuario_id, titulo, historia, celular, telefone, arquivo)
    return mensagem, status_code