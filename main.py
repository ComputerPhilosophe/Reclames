from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from repositories.usuario_repo import UsuarioRepo
from util.exceptions import configurar_excecoes # type: ignore
from util.auth import checar_autenticacao, checar_autorizacao
from routes.main_routes import router as main_routes
from routes.usuario_routes import router as usuario_router
from routes.administrador_routes import router as administrador_router
from routes.patrocinador_routes import router as patrocinador_router
from routes.morador_routes import router as morador_router


load_dotenv()
UsuarioRepo.criar_tabela()
UsuarioRepo.inserir_admins()
app = FastAPI(dependencies=[Depends(checar_autorizacao)])
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.middleware(middleware_type="http")(checar_autenticacao)

app.include_router(main_routes)
app.include_router(usuario_router)
app.include_router(administrador_router)
app.include_router(patrocinador_router)
app.include_router(morador_router)


