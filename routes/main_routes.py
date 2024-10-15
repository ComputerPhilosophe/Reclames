from datetime import date
from os import stat
import bcrypt
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from dtos.usuario_autenticado import UsuarioAutenticado
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import NOME_COOKIE_AUTH, adicionar_token, conferir_senha, criar_token, obter_hash_senha
from util.cookies import adicionar_mensagem_erro, adicionar_mensagem_sucesso
from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")

@router.get("/entrar")
async def get_root(request: Request):
  return templates.TemplateResponse("pages/entrar.html", {"request": request})
    
@router.post("/post_entrar")
async def post_entrar(
    email: str = Form(...), 
    senha: str = Form(...)):
    usuario = UsuarioRepo.checar_credenciais(email, senha)
    if usuario is None:
        response = RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
        return response
    token = criar_token(usuario[0], usuario[1], usuario[2])
    nome_perfil = None
    match (usuario[2]):
        case 1: nome_perfil = "morador"
        case 2: nome_perfil = "patrocinador"
        case 3: nome_perfil = "administrador"
        case _: nome_perfil = ""
    response = RedirectResponse(f"/{nome_perfil}/perfil_{nome_perfil}", status_code=status.HTTP_303_SEE_OTHER)    
    response.set_cookie(
        key=NOME_COOKIE_AUTH,
        value=token,
        max_age=3600*24*365*10,
        httponly=True,
        samesite="lax"
    )
    return response
   
    

@router.get("/cadastro_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/cadastro_morador.html", {"request": request})

@router.get("/cadastro_patrocinador", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("pages/cadastro_patrocinador.html", {"request": request})

@router.post("/cadastro_morador")
async def post_cadastrar(request: Request):
    # captura os dados do formulário de cadastro em um dicionário
    dados = dict(await request.form())
    # normalizar os dados para tipificar os valores corretamente
    dados["data_nascimento"] = date.fromisoformat(dados["data_nascimento"])
    dados["perfil"] = int(dados["perfil"])
    # validar dados do formulário
    erros = []
    if dados["senha"] == dados["confirmacao_senha"]:
        dados.pop("confirmacao_senha")
    else:
        erros.append("As senhas não conferem.")
    if erros:
        response = RedirectResponse("/cadastro_morador", status.HTTP_303_SEE_OTHER)
        html = "<h6>Erros encontrados:</h6>"
        html += "<ul>"
        for erro in erros:
            html += f"<li>{erro}</li>"
        html += "</ul>"
        adicionar_mensagem_erro(response, html)
        return response
    #  bcrypt
    senha_hash = bcrypt.hashpw(dados["senha"].encode(), bcrypt.gensalt())
    dados["senha"] = senha_hash.decode()
    # criar um objeto Usuario com os dados do dicionário
    usuario = Usuario(**dados)
    # inserir o objeto Usuario no banco de dados usando o repositório
    usuario = UsuarioRepo.inserir(usuario)
    # se inseriu com sucesso, redirecionar para a página de login
    if usuario:
        response = RedirectResponse("/login_morador", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_sucesso(response, "Cadastro realizado com sucesso!")
        return response
    # se não inseriu, redirecionar para a página de cadastro com mensagem de erro
    else:
        response = RedirectResponse("/cadastro_morador", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(
            response,
            "Ocorreu um problema ao realizar seu cadastro. Tente novamente mais tarde.",
        )
        return response


@router.post("/cadastro_patrocinador")
async def post_cadastrar(request: Request):
    # capturar os dados do formulário de cadastro como um dicionário
    dados = dict(await request.form())
    # normalizar os dados para tipificar os valores corretamente
    dados["data_nascimento"] = date.fromisoformat(dados["data_nascimento"])
    dados["perfil"] = int(dados["perfil"])
    # validar dados do formulário
    erros = []
    if dados["senha"] == dados["confirmacao_senha"]:
        dados.pop("confirmacao_senha")
    else:
        erros.append("As senhas não conferem.")
    if erros:
        response = RedirectResponse("/cadastro_patrocinador", status.HTTP_303_SEE_OTHER)
        html = "<h6>Erros encontrados:</h6>"
        html += "<ul>"
        for erro in erros:
            html += f"<li>{erro}</li>"
        html += "</ul>"
        adicionar_mensagem_erro(response, html)
        return response
    # criptografar a senha com bcrypt
    senha_hash = bcrypt.hashpw(dados["senha"].encode(), bcrypt.gensalt())
    dados["senha"] = senha_hash.decode()
    # criar um objeto Usuario com os dados do dicionário
    usuario = Usuario(**dados)
    # inserir o objeto Usuario no banco de dados usando o repositório
    usuario = UsuarioRepo.inserir(usuario)
    # se inseriu com sucesso, redirecionar para a página de login
    if usuario:
        response = RedirectResponse("/perfil_patrocinador_exemplo", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_sucesso(response, "Cadastro realizado com sucesso!")
        return response
    # se não inseriu, redirecionar para a página de cadastro com mensagem de erro
    else:
        response = RedirectResponse("/cadastro_patrocinador", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(
            response,
            "Ocorreu um problema ao realizar seu cadastro. Tente novamente mais tarde.",
        )
        return response



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
