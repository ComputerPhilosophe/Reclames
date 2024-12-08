from fastapi import APIRouter, Request, logger
from fastapi.responses import HTMLResponse, RedirectResponse
from streamlit import status

from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.mensagens import adicionar_mensagem_erro, adicionar_mensagem_sucesso
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/morador")
templates = obter_jinja_templates("templates")

@router.get("/", response_class=HTMLResponse)
async def get_perfil_administrador(request: Request):
    return RedirectResponse("/morador/perfil_morador", 303)

@router.get("/alterar_perfil_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    if not usuario:
        return RedirectResponse("/login_morador")
    dados_usuario = UsuarioRepo.obter_por_email(usuario.email)
    return templates.TemplateResponse("main/pages/alterar_perfil_morador.html", {"request": request, "dados_usuario": dados_usuario})

@router.get("/perfil_morador_exemplo", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("main/pages/perfil_morador_exemplo.html", {"request": request})

@router.get("/perfil_morador", response_class=HTMLResponse)
async def get_root(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    if not usuario:
        return RedirectResponse("/login_morador")
    dados_usuario = UsuarioRepo.obter_por_email(usuario.email)
    return templates.TemplateResponse("main/pages/perfil_morador.html", {"request": request, "dados_usuario": dados_usuario})

@router.post("/atualizar_dados")
async def post_dados(request: Request):
    dados = dict(await request.form())
    logger.info(f"Dados recebidos no formulário: {dados}")

    usuarioAutenticadoDto = request.state.usuario if hasattr(request.state, "usuario") else None
    if not usuarioAutenticadoDto:
        logger.error("Usuário autenticado não encontrado.")
        return RedirectResponse("/morador/login_morador", status.HTTP_303_SEE_OTHER)

    dados["id"] = usuarioAutenticadoDto.id
    try:
        usuario = Usuario(**dados)
        if UsuarioRepo.atualizar_dados(usuario):
            logger.info(f"Usuário {usuario.id} atualizado com sucesso.")
            response = RedirectResponse("/perfil_morador", status.HTTP_303_SEE_OTHER)
            adicionar_mensagem_sucesso(response, "Cadastro atualizado com sucesso!")
            return response
        else:
            logger.error(f"Falha ao atualizar o usuário {usuario.id}.")
            response = RedirectResponse("/alterar_perfil_morador", status.HTTP_303_SEE_OTHER)
            adicionar_mensagem_erro(response, "Não foi possível atualizar os dados. Tente novamente.")
            return response
    except Exception as e:
        logger.error(f"Erro ao processar atualização: {e}")
        response = RedirectResponse("/morador/alterar_perfil_morador", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(response, "Erro inesperado. Tente novamente mais tarde.")
        return response
