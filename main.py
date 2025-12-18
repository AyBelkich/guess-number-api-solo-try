from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()  # I create my FastAPI app object (this is where I register all routes/endpoints).

# ----------------------------
# Models
# ----------------------------
class Item(BaseModel):
    id: int  # I store a unique numeric ID for each item.
    name: str  # I store the item name (required).
    description: Optional[str] = None  # I store an optional description (can be missing / None).

class ItemCreate(BaseModel):
    name: str  # When I create an item, I only require the name from the user.
    description: Optional[str] = None  # Description is optional during creation too.

# ----------------------------
# In-memory store (demo only)
# ----------------------------
items: list[Item] = []  # I keep all items in a simple list in memory (it resets when the server restarts).
next_id = 1  # I use this counter to generate the next unique ID.

# ----------------------------
# Functions
# ----------------------------
def normalize_name(name: str) -> str:
    return name.strip().lower()  # I trim spaces and lowercase so name comparisons are consistent.

def find_item(item_id: int) -> Optional[Item]:
    for item in items:  # I loop through my stored items...
        if item.id == item_id:  # ...and if the ID matches...
            return item  # ...I return the matching item.
    return None  # If I didn't find it, I return None.

def ensure_unique_name(name: str) -> None:
    normalized = normalize_name(name)  # I normalize the incoming name to compare fairly.
    for item in items:  # I check all existing items...
        if normalize_name(item.name) == normalized:  # ...and if any name matches (ignoring case/spaces)...
            # I raise an HTTP 400 error because the request is not valid (duplicate name).
            raise HTTPException(status_code=400, detail="Item with this name already exists")

# ----------------------------
# Endpoints
# ----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}  # I return a simple response to show the API is running.

@app.get("/items", response_model=list[Item])
def get_items():
    return items  # I return the full list of stored items.

@app.post("/items", status_code=201)
def create_item(item: ItemCreate):
    global next_id  # I tell Python I'm updating the global next_id variable.
    
    ensure_unique_name(item.name)  # I prevent creating an item if the name already exists.

    new_item = Item(  # I build a full Item object (including generated ID).
        id=next_id,
        name=item.name,
        description=item.description,
    )

    items.append(new_item)  # I save the new item in my in-memory list.
    next_id += 1  # I increment the counter so the next item gets a new ID.
    return new_item  # I return the created item (client can see the generated ID).

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = find_item(item_id)  # I look up the item by ID.
    if item is None:  # If it doesn't exist...
        raise HTTPException(status_code=404, detail="Item not found")  # ...I return a 404 Not Found error.
    return item  # Otherwise I return the item.

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    item = find_item(item_id)  # I look up the item I want to delete.
    if item is None:  # If it doesn't exist...
        raise HTTPException(status_code=404, detail="Item not found")  # ...I return 404.
    items.remove(item)  # If it exists, I remove it from the list.
    return  # I return nothing because 204 means "No Content".
