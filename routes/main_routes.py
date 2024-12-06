from datetime import date
from os import stat
from urllib import request
import bcrypt
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from dtos.usuario_autenticado import UsuarioAutenticado
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import NOME_COOKIE_AUTH, adicionar_token, conferir_senha, criar_token, obter_hash_senha
from util.mensagens import adicionar_mensagem_erro, adicionar_mensagem_sucesso
from util.templates import obter_jinja_templates
from util.validators import *

router = APIRouter()
templates = obter_jinja_templates("templates")

@router.get("/entrar")
async def get_root(request: Request):
  return templates.TemplateResponse("main/pages/entrar.html", {"request": request})
    
@router.post("/post_entrar")
async def post_entrar(request: Request):
    dados = dict(await request.form())
    email = dados["email"]
    senha = dados["senha"]
    senha_hash = UsuarioRepo.obter_senha_por_email(email)
    if senha_hash and bcrypt.checkpw(senha.encode(), senha_hash.encode()):
        usuario = UsuarioRepo.obter_dados_por_email(email)
        usuarioAutenticadoDto = UsuarioAutenticado(
            id=usuario.id,
            nome=usuario.nome,
            email=usuario.email,
            perfil=usuario.perfil,
        )
    token = criar_token(usuarioAutenticadoDto)
    nome_perfil = None
    match (usuarioAutenticadoDto.perfil):
        case 1: nome_perfil = "morador"
        case 2: nome_perfil = "patrocinador"
        case 3: nome_perfil = "administrador"
        case _: nome_perfil = ""
    response = RedirectResponse(f"/{nome_perfil}", status_code=status.HTTP_303_SEE_OTHER)    
    adicionar_token(response, token)
    adicionar_mensagem_sucesso(response, "Login realizado com sucesso!")
    return response


@router.post("/post_entrar_admin")
async def post_entrar_admin(request: Request):
    dados = dict(await request.form())
    email = dados["email"]
    senha = dados["senha"]

    # Verifica se o usuário existe e se é um administrador (perfil 3)
    senha_hash = UsuarioRepo.obter_senha_por_email(email)
    if senha_hash and bcrypt.checkpw(senha.encode(), senha_hash.encode()):
        usuario = UsuarioRepo.obter_dados_por_email(email)
        if usuario.perfil == 3:  # Verifica se é um administrador
            usuarioAutenticadoDto = UsuarioAutenticado(
                id=usuario.id,
                nome=usuario.nome,
                email=usuario.email,
                perfil=usuario.perfil,
            )
            token = criar_token(usuarioAutenticadoDto)
            admin_map = {
            "lara@gmail.com": "perfil_administrador_lara",
            "artur@gmail.com": "perfil_administrador_artur",
            "caio@gmail.com": "perfil_administrador_caio",
            "karina@gmail.com": "perfil_administrador_karina",
        }
            nome_perfil = admin_map.get(email, "administrador") 
            response = RedirectResponse(f"/administrador/{nome_perfil}", status_code=status.HTTP_303_SEE_OTHER)
            adicionar_token(response, token)
            adicionar_mensagem_sucesso(response, "Login realizado com sucesso!")
            return response
    

@router.get("/cadastro_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/cadastro_morador.html", {"request": request})

@router.get("/cadastro_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/cadastro_patrocinador.html", {"request": request})

@router.post("/post_cadastro_morador")
async def post_cadastrar(
    cpf: str = Form(...),
    nome: str = Form(...),
    data_nascimento: str = Form(...),
    genero: str = Form(...),
    endereco_cidade: str = Form(...),
    endereco_bairro: str = Form(...),
    endereco_cep: str = Form(...),
    endereco_numero: str = Form(...),
    endereco_complemento: str = Form(None),
    endereco_logradouro: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confsenha: str = Form(...),
):
    if senha != confsenha:
        return RedirectResponse("/cadastro_morador", status_code=status.HTTP_303_SEE_OTHER)
    
    senha_hash = obter_hash_senha(senha)

    usuario = Usuario(
        cpf=cpf,
        nome=nome,
        data_nascimento=date.fromisoformat(data_nascimento), 
        genero=genero,
        endereco_cidade=endereco_cidade,
        endereco_bairro=endereco_bairro,
        endereco_cep=endereco_cep,
        endereco_numero=endereco_numero,
        endereco_complemento=endereco_complemento,
        endereco_logradouro=endereco_logradouro,
        email=email,
        senha=senha_hash,
        perfil=1,
    )

    UsuarioRepo.inserir(usuario)
    return RedirectResponse("/login_morador", status_code=status.HTTP_303_SEE_OTHER)



@router.post("/post_cadastro_patrocinador")
async def post_cadastrar(
    cnpj: str = Form(...),
    nome: str = Form(...),
    data_nascimento: str = Form(...),
    endereco_cidade: str = Form(...),
    endereco_bairro: str = Form(...),
    endereco_cep: str = Form(...),
    endereco_numero: str = Form(...),
    endereco_complemento: str = Form(None),
    endereco_logradouro: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confsenha: str = Form(...),
):
    if senha != confsenha:
        return RedirectResponse("/cadastro_patrocinador", status_code=status.HTTP_303_SEE_OTHER)
    
    senha_hash = obter_hash_senha(senha)

    usuario = Usuario(
        cnpj=cnpj,
        nome=nome,
        data_nascimento=date.fromisoformat(data_nascimento),  
        endereco_cidade=endereco_cidade,
        endereco_bairro=endereco_bairro,
        endereco_cep=endereco_cep,
        endereco_numero=endereco_numero,
        endereco_complemento=endereco_complemento,
        endereco_logradouro=endereco_logradouro,
        email=email,
        senha=senha_hash,
        perfil=2,
    )

    UsuarioRepo.inserir(usuario)
    return RedirectResponse("/login_patrocinador", status_code=status.HTTP_303_SEE_OTHER)





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
    return templates.TemplateResponse("main/pages/index.html", {"request": request})

@router.get("/contato", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/contato.html", {"request": request})

@router.get("/redes_sociais", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/redes_sociais.html", {"request": request})

@router.get("/sobre_nos", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/sobre_nos.html", {"request": request})

@router.get("/termos_uso", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/termos_uso.html", {"request": request})

@router.get("/politica_privacidade", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/politica_privacidade.html", {"request": request})

@router.get("/sobre_o_es", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/sobre_o_es.html", {"request": request})

@router.get("/duvidas_frequentes", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/duvidas_frequentes.html", {"request": request})

@router.get("/reclamar", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/reclamar.html", {"request": request})

@router.get("/esqueci_senha", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/esqueci_senha.html", {"request": request})

@router.get("/mapa", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/mapa.html", {"request": request})

@router.get("/ranking", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/ranking.html", {"request": request})

@router.get("/interacao_proj_sug", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/interacao_proj_sug.html", {"request": request})

@router.get("/instrucoes_mapa", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/instrucoes_mapa.html", {"request": request})

@router.get("/login_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/login_morador.html", {"request": request})

@router.get("/login_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/login_patrocinador.html", {"request": request})

@router.get("/login_administrador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/login_administrador.html", {"request": request})

@router.get("/duvidas_frequentes_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/duvidas_frequentes_morador.html", {"request": request})

@router.get("/duvidas_frequentes_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/duvidas_frequentes_patrocinador.html", {"request": request})

@router.get("/alterar_perfil_patrocinador_exemplo", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/alterar_perfil_patrocinador_exemplo.html", {"request": request})

@router.get("/alterar_perfil_morador_exemplo", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/alterar_perfil_morador_exemplo.html", {"request": request})