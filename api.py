from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
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

conn = workwithbd("localhost", "root", "", "mdk_bd")


class product_item(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    category: Optional[int] = None
    price: Optional[int] = None


class products(BaseModel):
    count: int
    results: list[product_item]


class category_item(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None


class categories(BaseModel):
    count: int
    results: list[category_item]


class Item(BaseModel):
    name: str
    description: str = None


@app.get("/products/", response_model=products)
def read_item():
    results = conn.get_goods()
    product_items = []
    if len(results) == 0:
        return {
            "count": 0,
            "results": [{"id": None, "title": None, "category": None, "price": None}],
        }

    for i in results:
        product_items.append(
            product_item(id=i[0], title=i[1], category=i[2], price=i[3])
        )

    return {"count": len(results), "results": product_items}


@app.get("/categories/", response_model=categories)
def read_item():
    results = conn.get_category()
    category_items = []
    if len(results) == 0:
        return {
            "count": 0,
            "results": [{"id": None, "title": None}],
        }

    for i in results:
        category_items.append(
            category_item(id=i[0], title=i[1])
        )

    return {"count": len(results), "results": category_items}

# Route to create an item
# @app.post("items/", response_model=Item)
# def create_item(item: Item):
#     cursor = conn.cursor()
#     query = "INSERT INTO items (name, description) VALUES (%s, %s)"
#     cursor.execute(query, (item.name, item.description))
#     conn.commit()
#     item.id = cursor.lastrowid
#     cursor.close()
#     return item


# Route to read an item
# @app.get("items/{item_id}/", response_model=Item)
# def read_item(item_id: int):
#     cursor = conn.cursor()
#     query = "SELECT id, name, description FROM items WHERE id=%s"
#     cursor.execute(query, (item_id,))
#     item = cursor.fetchone()
#     cursor.close()
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"id": item[0], "name": item[1], "description": item[2]}


# Route to update an item
# @app.put("products/{item_id}/", response_model=Item)
# def update_item(item_id: int, item: Item):
#     cursor = conn.cursor()
#     query = "UPDATE items SET name=%s, description=%s WHERE id=%s"
#     cursor.execute(query, (item.name, item.description, item_id))
#     conn.commit()
#     cursor.close()
#     item.id = item_id
#     return item


# # Route to delete an item
# @app.delete("/items/{item_id}", response_model=Item)
# def delete_item(item_id: int):
#     cursor = conn.cursor()
#     query = "DELETE FROM items WHERE id=%s"
#     cursor.execute(query, (item_id,))
#     conn.commit()
#     cursor.close()
#     return {"id": item_id}


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=9010)
