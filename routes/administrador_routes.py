from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from repositories.usuario_repo import UsuarioRepo
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/administrador")
templates = obter_jinja_templates("templates")

@router.get("/", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return RedirectResponse("/administrador/perfil_administrador", 303)

@router.get("/perfil_administrador_lara", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return templates.TemplateResponse("main/pages/perfil_administrador_lara.html", {"request": request})

@router.get("/alterar_perfil_administrador", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return templates.TemplateResponse("main/pages/alterar_perfil_administrador.html", {"request": request})

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

