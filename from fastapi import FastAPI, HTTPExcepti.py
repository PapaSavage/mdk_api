from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic model to define the schema of the data
class Item(BaseModel):
    name: str
    description: str = None

# Route to create an item
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    cursor = conn.cursor()
    query = "INSERT INTO items (name, description) VALUES (%s, %s)"
    cursor.execute(query, (item.name, item.description))
    conn.commit()
    item.id = cursor.lastrowid
    cursor.close()
    return item

# Route to read an item
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    cursor = conn.cursor()
    query = "SELECT id, name, description FROM items WHERE id=%s"
    cursor.execute(query, (item_id,))
    item = cursor.fetchone()
    cursor.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item[0], "name": item[1], "description": item[2]}

# Route to update an item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    cursor = conn.cursor()
    query = "UPDATE items SET name=%s, description=%s WHERE id=%s"
    cursor.execute(query, (item.name, item.description, item_id))
    conn.commit()
    cursor.close()
    item.id = item_id
    return item

# Route to delete an item
@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    cursor = conn.cursor()
    query = "DELETE FROM items WHERE id=%s"
    cursor.execute(query, (item_id,))
    conn.commit()
    cursor.close()
    return {"id": item_id}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)