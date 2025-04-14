from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

db = [] #banco de dados que sera temporario

class Item(BaseModel):
    id: int
    nome: str
    preco: float

@app.post("/itens/", response_model=Item) #Essa parte irá criar um item
def criar_item(item: Item):
    db.append(item.dict())
    return item

@app.get("/itens/", response_model=List[Item]) #Essa e a parte de read(ler) um item
def ler_itens():
    return db

@app.get("/itens/{item_id}", response_model=Item) #Essa parte buscará um item por numero para ficar mais organizado
def ler_item(item_id: int):
    for item in db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item não encontrado")

@app.put("/itens/{item_id}", response_model=Item) #parte de atualizar um item, caso necessario
def atualizar_item(item_id: int, item: Item):
    for index, item_db in enumerate(db):
        if item_db["id"] == item_id:
            db[index] = item.dict()
            return item
    raise HTTPException(status_code=404, detail="Item não encontrado")

@app.delete("/itens/{item_id}") #parte de deletar um item
def deletar_item(item_id: int):
    for index, item_db in enumerate(db):
        if item_db["id"] == item_id:
            db.pop(index)
            return {"mensagem": "Item deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Item não encontrado")