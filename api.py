from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
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
    "http://localhost:3001",
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
    quantity: Optional[int] = None

    class Config:
        from_attributes = True


class order_item(BaseModel):
    id: Optional[int] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    goods: list[add_product_item]

    class Config:
        from_attributes = True


class orders(BaseModel):
    count: int
    results: list[order_item]

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


@app.get("/orders/")
async def read_item():
    results = await conn.get_orders()

    order_items = []
    if len(results) == 0:
        return {
            "count": 0,
            "results": [
                {
                    "id": None,
                    "customer_name": None,
                    "customer_phone": None,
                    "customer_email": None,
                    "status": None,
                    "description": None,
                    "goods": [],
                }
            ],
        }
    for i in results:
        order_items.append(
            order_item(
                id=i[0],
                customer_name=i[1],
                customer_phone=i[2],
                customer_email=i[3],
                status=i[4],
                description=i[5],
                goods=i[6],
            )
        )

    return {"count": len(results), "results": order_items}


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


# @app.post("/products/", response_model=product_item)
# async def create_good(product: product_item):
#     result = await conn.post_goods(product)
#     return result


@app.post("/products/")
async def create_good(
    file: UploadFile = File(...),
    title: str = Form(...),
    category: int = Form(...),
    price: float = Form(...),
):
    content = await file.read()
    result = await conn.post_goods(content, title, category, price)
    return result


@app.put("/orders/{order_id}/")
async def update_order(order_id: int, status: str = Form(...)):
    result = await conn.put_orders(order_id, status)
    return result


# Route to update an item
@app.put("/products/{item_id}/")
async def update_item(
    item_id: int,
    file: UploadFile = File(None),
    title: str = Form(...),
    category: int = Form(...),
    price: float = Form(...),
):
    print(file)
    if file is None:
        result = await conn.put_good_without_image(title, category, price, item_id)
    else:
        print(file)
        result = await conn.put_good_with_image(
            await file.read(), title, category, price, item_id
        )
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


@app.put("/file/{item_id}")
async def upload_file(file: UploadFile, item_id: int):
    contents = await file.read()
    await conn.put_image(contents, item_id)
    return {"filename": file.filename}


if __name__ == "__main__":

    conn = workwithbd()

    # asyncio.run(conn.check_connection())

    # asyncio.run(
    #     conn.post_goods(product_item(title="Карбонара", category_id=2, price=1500))
    # )

    uvicorn.run(app, host="127.0.0.1", port=9010)
