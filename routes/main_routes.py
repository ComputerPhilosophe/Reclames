from os import stat
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import NOME_COOKIE_AUTH, conferir_senha, criar_token, obter_hash_senha
from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")

@router.get("/entrar")
async def get_root(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    if not usuario or not usuario.perfil:
        return templates.TemplateResponse("pages/entrar.html", {"request": request})
    if usuario.perfil == 1:
        return RedirectResponse("/patrocinador", status_code=status.HTTP_303_SEE_OTHER)
    if usuario.perfil == 2:
        return RedirectResponse("/morador", status_code=status.HTTP_303_SEE_OTHER)
    if usuario.perfil == 3:
        return RedirectResponse("/administrador", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/post_entrar")
async def post_entrar(
    email: str = Form(...), 
    senha: str = Form(...)):
    usuario = UsuarioRepo.obter_por_email(email)    
    if usuario is None:
        response = RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
        return response
    if not conferir_senha(senha, usuario.senha):
        response = RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
        return response
    token = criar_token(usuario.nome, usuario.email, usuario.perfil)
    nome_perfil = None
    match (usuario.perfil):
        case 1: nome_perfil = "morador"
        case 2: nome_perfil = "patrocinador"
        case 3: nome_perfil = "administrador"
    
    response = RedirectResponse(f"administrador/perfil_administrador", status_code=status.HTTP_303_SEE_OTHER)    
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=3600*24*365*10,
        httponly=True,
        samesite="lax"
    )
    return response

@router.get("/cadastrar")
async def get_cadastrar(request: Request):
    return templates.TemplateResponse("pages/cadastrar.html", {"request": request})

@router.post("/post_cadastrar_morador")
async def post_cadastrar_morador(
    cpf: str = Form(...),
    nome: str = Form(...),
    data_nasc: str = Form(...),
    genero: str = Form(...),
    cidade: str = Form(...),
    bairro: str = Form(...),
    cep:    str = Form(...),
    numero: str = Form(...),
    complemento: str = Form(...),
    logradouro:  str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confsenha: str = Form(...),
    perfil: int = Form(...)):
    if senha != confsenha:
        return RedirectResponse("/cadastrar", status_code=status.HTTP_303_SEE_OTHER)
    senha_hash = obter_hash_senha(senha)
    usuario = Usuario(None, cpf, nome, data_nasc, genero, cidade, bairro, cep, numero, complemento,logradouro, email, senha_hash, None, perfil)
    UsuarioRepo.inserir(usuario)
    return RedirectResponse("/perfil_morador_exemplo", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/post_cadastrar_patrocinador")
async def post_cadastrar_patrocinador(
    cnpj: str = Form(...),
    nome: str = Form(...),
    data_nasc: str = Form(...),
    cidade: str = Form(...),
    bairro: str = Form(...),
    cep:    str = Form(...),
    numero: str = Form(...),
    complemento: str = Form(...),
    logradouro:  str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confsenha: str = Form(...),
    perfil: int = Form(...)):
    if senha != confsenha:
        return RedirectResponse("/cadastrar", status_code=status.HTTP_303_SEE_OTHER)
    senha_hash = obter_hash_senha(senha)
    usuario = Usuario(None, cnpj, nome, data_nasc, cidade, bairro, cep, numero, complemento,logradouro, email, senha_hash, None, perfil)
    UsuarioRepo.inserir(usuario)
    return RedirectResponse("/perfil_patrocinador_exemplo", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/sair")
async def get_sair():
    response = RedirectResponse("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value="",
        max_age=1,
        httponly=True,
        samesite="lax")
    return response

    

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


@router.get("/sobre_o_es", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/sobre_o_es.html", {"request": request})

@router.get("/duvidas_frequentes", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/duvidas_frequentes.html", {"request": request})

@router.get("/reclamar", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/reclamar.html", {"request": request})

@router.get("/esqueci_senha", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/esqueci_senha.html", {"request": request})

@router.get("/mapa", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/mapa.html", {"request": request})

@router.get("/ranking", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/ranking.html", {"request": request})

@router.get("/interacao_proj_sug", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/interacao_proj_sug.html", {"request": request})

@router.get("/instrucoes_mapa", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/instrucoes_mapa.html", {"request": request})

@router.get("/login_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/login_morador.html", {"request": request})

@router.get("/login_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/login_patrocinador.html", {"request": request})

@router.get("/login_administrador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/login_administrador.html", {"request": request})

@router.get("/cadastro_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/cadastro_morador.html", {"request": request})

@router.get("/cadastro_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/cadastro_patrocinador.html", {"request": request})

@router.get("/perfil_administrador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/perfil_administrador.html", {"request": request})

@router.get("/perfil_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/perfil_patrocinador.html", {"request": request})

@router.get("/perfil_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/perfil_morador.html", {"request": request})

@router.get("/duvidas_frequentes_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/duvidas_frequentes_morador.html", {"request": request})

@router.get("/duvidas_frequentes_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/duvidas_frequentes_patrocinador.html", {"request": request})
