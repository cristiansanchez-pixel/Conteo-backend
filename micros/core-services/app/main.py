from fastapi import FastAPI, Depends, HTTPException
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from .utils.authJwt import get_current_user
from .routes import (auth_router,
    email_router,
    permission_router,
    profile_router,)

app = FastAPI()

#scheduler = AsyncIOScheduler(timezone="America/Bogota")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:9001", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, tags=["auth"])

app.include_router(
    permission_router.router,
    tags=["permission"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    profile_router.router,
    tags=["profile"],
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    email_router.router,
    tags=["email"],
)
@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")


app.mount("/files", StaticFiles(directory="files"), name="static")