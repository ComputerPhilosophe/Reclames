from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from streamlit import status

from models.usuario_model import Usuario
from repositories import usuario_repo
from repositories.usuario_repo import UsuarioRepo
from util.mensagens import adicionar_mensagem_erro, adicionar_mensagem_sucesso
from util.templates import obter_jinja_templates
