import os
from typing import Optional
import bcrypt
from fastapi.responses import RedirectResponse
import jwt
from datetime import datetime
from datetime import timedelta
from fastapi import HTTPException, Request, status

from dtos.usuario_autenticado import UsuarioAutenticado

NOME_COOKIE_AUTH = "jwt-token"

async def obter_usuario_logado(request: Request) -> dict:
    try:
        token = request.cookies[NOME_COOKIE_AUTH]
        if token.strip() == "":
            return None
        dados = validar_token(token)
        usuario = UsuarioAutenticado(
            nome = dados["nome"], 
            email = dados["email"], 
            perfil= dados["perfil"])
        if "mensagem" in dados.keys():
            usuario.mensagem = dados["mensagem"]
        return usuario
    except KeyError:
        return None
    

async def checar_autenticacao(request: Request, call_next):
    token = request.cookies.get("jwt_token", None)
    if token:
        usuario_autenticado = validar_token(token)
        request.state.usuario = usuario_autenticado
    response = await call_next(request)
    return response


async def checar_autorizacao(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    area_do_usuario = request.url.path.startswith("/usuario")
    area_do_patrocinador = request.url.path.startswith("/patrocinador")
    area_do_morador = request.url.path.startswith("/morador")
    area_do_administrador = request.url.path.startswith("/administrador")
    if (area_do_usuario or area_do_morador or area_do_patrocinador or area_do_administrador) and (not usuario or usuario.perfil):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if area_do_morador and usuario.perfil != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if area_do_patrocinador and usuario.perfil != 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if area_do_administrador and usuario.perfil != 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def obter_hash_senha(senha: str) -> str:
    try:
        hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        return hashed.decode()
    except ValueError:
        return ""


def conferir_senha(senha: str, hash_senha: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False
    

def criar_token(UsuarioAutenticado: UsuarioAutenticado) -> str:
    dados_token = {
        "id": UsuarioAutenticado.id,
        "nome": UsuarioAutenticado.nome,
        "email": UsuarioAutenticado.email,
        "perfil": UsuarioAutenticado.perfil,
        "exp": datetime.now() + timedelta(days=1),
    }
    secret_key = os.getenv("JWT_TOKEN_SECRET_KEY")
    return jwt.encode(dados_token, secret_key, "HS256")

def validar_token(token: str) -> Optional[UsuarioAutenticado]:
    secret_key = os.getenv("JWT_TOKEN_SECRET_KEY")
    try:
        dados_token = jwt.decode(token, secret_key, "HS256")
        return UsuarioAutenticado(
            id=int(dados_token["id"]),
            nome=dados_token["nome"],
            email=dados_token["email"],
            perfil=int(dados_token["perfil"]),
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None



def adicionar_token(response: RedirectResponse, token: str):
    response.set_cookie(
        key="jwt_token",
        value=token,
        max_age=3600 * 24,
        httponly=True,
        samesite="strict",
    )

def remover_token(response: RedirectResponse):
    response.set_cookie(
        key="jwt_token",
        value="",
        max_age=0,
        httponly=True,
        samesite="strict",
    )

