from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio

# from database import *
from database import *
import uvicorn

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# conn = workwithbd("localhost", "root", "", "mdk_bd")


class product_item(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    category: Optional[int] = None
    price: Optional[float] = None
    images: Optional[str] = None

    class Config:
        from_attributes = True


class add_product_item(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    category: Optional[int] = None
    price: Optional[float] = None

    class Config:
        from_attributes = True


class products(BaseModel):
    count: int
    results: list[product_item]

    class Config:
        from_attributes = True


class category_item(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None

    class Config:
        from_attributes = True


class categories(BaseModel):
    count: int
    results: list[category_item]

    class Config:
        from_attributes = True


class Item(BaseModel):
    name: str
    description: str = None

    class Config:
        from_attributes = True


@app.get("/products/", response_model=products)
async def read_item():
    results = await conn.get_goods()

    product_items = []
    if len(results) == 0:
        return {
            "count": 0,
            "results": [
                {"id": None, "title": None, "category_id": None, "price": None}
            ],
        }

    for i in results:
        product_items.append(
            product_item(id=i[0], title=i[1], category=i[2], price=i[3], images=i[4])
        )

    return {"count": len(results), "results": product_items}


@app.get("/categories/", response_model=categories)
async def read_item():
    results = await conn.get_category()
    category_items = []
    if len(results) == 0:
        return {
            "count": 0,
            "results": [{"id": None, "title": None}],
        }

    for i in results:
        category_items.append(category_item(id=i[0], title=i[1]))

    return {"count": len(results), "results": category_items}


@app.post("/products/", response_model=product_item)
async def create_good(product: product_item):
    result = await conn.post_goods(product)
    return result


# Route to update an item
@app.put("/products/{item_id}/", response_model=product_item)
async def update_item(product: product_item, item_id: int):
    result = await conn.put_good(product, item_id)
    return result


@app.delete("/products/{item_id}/")
async def delete_product(item_id: int):
    result = await conn.delete_product(item_id)
    return result


@app.delete("/categories/{item_id}/")
async def delete_category(item_id: int):
    result = await conn.delete_category(item_id)
    return result


@app.post("/categories/", response_model=category_item)
async def create_category(category: category_item):
    result = await conn.post_categories(category)
    return result


if __name__ == "__main__":

    conn = workwithbd()

    # asyncio.run(conn.check_connection())

    # asyncio.run(
    #     conn.post_goods(product_item(title="Карбонара", category_id=2, price=1500))
    # )

    uvicorn.run(app, host="127.0.0.1", port=9010)
