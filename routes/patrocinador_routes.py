from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from repositories.usuario_repo import UsuarioRepo
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/patrocinador")
templates = obter_jinja_templates("templates")

@router.get("/", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return RedirectResponse("/patrocinador/perfil_patrocinador", 303)

@router.get("/perfil_patrocinador_exemplo", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/perfil_patrocinador_exemplo.html", {"request": request})


@router.get("/perfil_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    if not usuario:
        return RedirectResponse("/login_patrocinador")
    dados_usuario = UsuarioRepo.obter_por_email(usuario.email)
    return templates.TemplateResponse("main/pages/perfil_patrocinador.html", {"request": request, "dados_usuario": dados_usuario})