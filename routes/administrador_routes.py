from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from util.templates import obter_jinja_templates

router = APIRouter(prefix="/administrador")
templates = obter_jinja_templates("templates")

@router.get("/", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return RedirectResponse("/administrador/perfil_administrador", 303)

@router.get("/perfil_administrador", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return templates.TemplateResponse("main/pages/perfil_administrador.html", {"request": request})

@router.get("/alterar_perfil_administrador", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return templates.TemplateResponse("main/pages/alterar_perfil_administrador.html", {"request": request})

