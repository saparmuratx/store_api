from typing import Annotated

from pydantic import BaseModel, HttpUrl

from fastapi import FastAPI, Query, Path

from src.config import settings

from src.inventory.router import router

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    image: Image | None = None


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.put("/items_foo/{item_id}")
def items_foo(
    item_id: Annotated[int, Path(title="Unique identifier", ge=0, le=1000)],
    q: Annotated[str | None, Query(max_length=32)] = None,
    item: Item | None = None,
) -> dict:
    results = {"item_id": item_id}

    if q:
        results.update({"q": q})

    if item:
        results.update({"item": item})

    return results


@app.get("/env/")
def env() -> dict:
    return settings.model_dump()


app.include_router(router, prefix="/inventory", tags=["Inventory"])
