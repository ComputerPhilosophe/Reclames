from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")


@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/index.html", {"request": request})

@router.get("/contato", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/contato.html", {"request": request})

@router.get("/redes_sociais", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/redes_sociais.html", {"request": request})

@router.get("/sobre_nos", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/sobre_nos.html", {"request": request})

@router.get("/termos_uso", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/termos_uso.html", {"request": request})

@router.get("/politica_privacidade", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/politica_privacidade.html", {"request": request})


@router.get("/entrar", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/entrar.html", {"request": request})