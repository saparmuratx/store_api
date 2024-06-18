from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.inventory.router import router
from src.auth.router import auth_router

app = FastAPI(
    title="Bazar API",
    description="API for Vendors and Items",
    version="0.6.9",
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(router, prefix="/api/inventory", tags=["Inventory"])


@app.get("/")
async def home_redirect():
    return RedirectResponse(url="/docs", status_code=302)
