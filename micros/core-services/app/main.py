from fastapi import FastAPI, Depends, HTTPException
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from .utils.authJwt import get_current_user
from .routes import (auth_router,
    inventario_router,
    perfil_router,
    permisos_router,
    usuario_router,
    producto_router)

app = FastAPI()

#scheduler = AsyncIOScheduler(timezone="America/Bogota")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://127.0.0.1:9001", "http://127.0.0.1:5500"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, tags=["auth"])

app.include_router(
    permisos_router.router,
    tags=["permission"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    perfil_router.router,
    tags=["profile"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    inventario_router.router,
    tags=["inventory"],
)
app.include_router(
   usuario_router.router,
   tags=["user"],
)
app.include_router(
   producto_router.router,
    tags=["product"],
)
@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")


