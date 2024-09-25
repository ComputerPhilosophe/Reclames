from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from util.templates import obter_jinja_templates

router = APIRouter(prefix="/morador")
templates = obter_jinja_templates("templates/main")

@router.get("/alterar_perfil_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/alterar_perfil_morador.html", {"request": request})

@router.get("/perfil_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/perfil_morador.html", {"request": request})
