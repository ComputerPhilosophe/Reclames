from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from repositories.usuario_repo import UsuarioRepo
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/morador")
templates = obter_jinja_templates("templates")

@router.get("/", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return RedirectResponse("/morador/perfil_morador", 303)

@router.get("/alterar_perfil_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/alterar_perfil_morador.html", {"request": request})

@router.get("/perfil_morador_exemplo", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/perfil_morador_exemplo.html", {"request": request})

@router.get("/perfil_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    if not usuario:
        return RedirectResponse("/login_morador")
    dados_usuario = UsuarioRepo.obter_por_email(usuario.email)
    return templates.TemplateResponse("main/pages/perfil_morador.html", {"request": request, "dados_usuario": dados_usuario})

