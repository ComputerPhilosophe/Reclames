from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from util.templates import obter_jinja_templates

router = APIRouter(prefix="/usuario")
templates = obter_jinja_templates("templates/main")

@router.get("/duvidas_frequentes_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/duvidas_frequentes_morador.html", {"request": request})

@router.get("/duvidas_frequentes_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/duvidas_frequentes_patrocinador.html", {"request": request})