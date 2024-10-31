from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from util.templates import obter_jinja_templates

router = APIRouter(prefix="/patrocinador")
templates = obter_jinja_templates("templates")

@router.get("/perfil_patrocinador_exemplo", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/perfil_patrocinador_exemplo.html", {"request": request})

@router.get("/perfil_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/perfil_patrocinador.html", {"request": request})

