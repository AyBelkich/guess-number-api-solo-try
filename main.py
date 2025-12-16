from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

## Classes
class Item(BaseModel):
    id: int
    name: str
    description: str | None = None

class ItemCreate(BaseModel):
    name: str
    description: str | None = None

items: list[Item] = []
next_id = 1

## Endpoints

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/items")
def get_items():
    return items

@app.post("/items", status_code=201)
def create_item(item: ItemCreate):
    global next_id
    new_name = item.name.strip().lower()
    for existing_item in items:
        if existing_item.name.strip().lower() == new_name:
            raise HTTPException(status_code=400, detail="Item with this name already exists")   
    new_item = Item(id=next_id, name=item.name, description=item.description)
    items.append(new_item)
    next_id += 1
    return new_item

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")