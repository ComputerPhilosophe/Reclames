from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from util.templates import obter_jinja_templates

router = APIRouter(prefix="/patrocinador")
templates = obter_jinja_templates("templates/main")

@router.get("/perfil_patrocinador_exemplo", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/perfil_patrocinador.html", {"request": request})

@router.get("/alterar_perfil_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/alterar_perfil_patrocinador.html", {"request": request})
