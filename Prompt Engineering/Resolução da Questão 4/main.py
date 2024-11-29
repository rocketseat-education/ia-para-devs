from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from uuid import uuid4
from datetime import date, datetime

app = FastAPI()

class Item(BaseModel):
    nome: str = Field(..., max_length=25, description="Nome do item, máximo 25 caracteres.")
    valor: float = Field(..., description="Valor numérico do item.")
    data: str = Field(..., description="Data no formato YYYY-MM-DD. Não pode ser superior à data atual.")
    
    @validator("data")
    def validar_data(cls, v):
        try:
            data_obj = datetime.strptime(v, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("A data deve estar no formato YYYY-MM-DD.")
        if data_obj > date.today():
            raise ValueError("A data não pode ser superior à data atual.")
        return v

@app.post("/processar-item", response_model=dict)
async def processar_item(item: Item):
    """
    Processa e valida um objeto do tipo Item, adicionando um campo 'uuid'.
    
    Parâmetros:
    - item (Item): Objeto contendo os campos nome, valor e data.
    
    Retorna:
    - Objeto validado e modificado com o campo adicional 'uuid'.
    """
    # Gera o campo uuid
    item_com_uuid = item.dict()
    item_com_uuid["uuid"] = str(uuid4())
    
    return item_com_uuid
