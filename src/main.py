from fastapi import FastAPI

from src.inventory.router import router


app = FastAPI()

app.include_router(router, prefix="/inventory", tags=["Inventory"])
