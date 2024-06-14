from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.inventory.router import router
from src.auth.router import auth_router

app = FastAPI()

app.include_router(router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])


@app.get("/")
async def home_redirect():
    return RedirectResponse(url="/docs", status_code=302)
