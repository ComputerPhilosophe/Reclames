from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from streamlit import status

from models.usuario_model import Usuario
from repositories import usuario_repo
from repositories.usuario_repo import UsuarioRepo
from util.mensagens import adicionar_mensagem_erro, adicionar_mensagem_sucesso
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/administrador")
templates = obter_jinja_templates("templates")

@router.get("/", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return RedirectResponse("/administrador/perfil_administrador", 303)

@router.get("/perfil_administrador_lara", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return templates.TemplateResponse("main/pages/perfil_administrador_lara.html", {"request": request})

@router.get("/alterar_perfil_administrador_lara", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return templates.TemplateResponse("main/pages/alterar_perfil_administrador_lara.html", {"request": request})

@router.get("/perfil_administrador_caio", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return templates.TemplateResponse("main/pages/perfil_administrador_caio.html", {"request": request})

@router.get("/perfil_administrador_artur", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return templates.TemplateResponse("main/pages/perfil_administrador_artur.html", {"request": request})

@router.get("/perfil_administrador_karina", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return templates.TemplateResponse("main/pages/perfil_administrador_karina.html", {"request": request})

@router.get("/perfil_administrador_lara")
async def perfil_administrador(request: Request):
    # Buscar todos os usuários do banco de dados
    usuarios = UsuarioRepo.listar_todos()  # Adapte isso conforme necessário
    # Renderizar o template com os usuários
    return templates.TemplateResponse("perfil_administrador_lara.html", {"request": request, "usuarios": usuarios})

from flask import app, request, redirect, url_for, flash

@router.post("/atualizar_dados")
async def post_dados(request: Request):
    dados = dict(await request.form())
    usuarioAutenticadoDto = (
        request.state.usuario if hasattr(request.state, "usuario") else None
    )
    dados["id"] = usuarioAutenticadoDto.id
    usuario = Usuario(**dados)
    if UsuarioRepo.atualizar_dados(usuario):
        response = RedirectResponse("perfil_administrador_lara.html", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_sucesso(response, "perfil atualizado com sucesso!")
        return response
    else:
        response = RedirectResponse("alterar_perfil_administrador_lara.html", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(
            response,
            "Ocorreu um problema ao atualizar seu cadastro. Tente novamente mais tarde.",
        )
        return response