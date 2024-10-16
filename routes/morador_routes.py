from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from util.templates import obter_jinja_templates

router = APIRouter(prefix="/morador")
templates = obter_jinja_templates("templates")

@router.get("/alterar_perfil_morador_exemplo", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/alterar_perfil_morador_exemplo.html", {"request": request})

@router.get("/perfil_morador_exemplo", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/perfil_morador_exemplo.html", {"request": request})

