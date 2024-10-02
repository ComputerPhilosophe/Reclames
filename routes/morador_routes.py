from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from util.templates import obter_jinja_templates

router = APIRouter(prefix="/morador")
templates = obter_jinja_templates("templates/main")

@router.get("/alterar_perfil_morador_exemplo", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/alterar_perfil_morador_exemplo.html", {"request": request})

#@router.get("/perfil_morador_exemplo", response_class=HTMLResponse)
#async def get_root(request: Request):
    # captura o usuário logado
    # usuario = {id==1, nome =="Fulano"}
    # return templates.TemplateResponse("pages/perfil_morador_exemplo.html", {"request": request, "usuario": usuario})
