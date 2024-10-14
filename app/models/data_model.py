from pydantic import BaseModel

class InputData(BaseModel):
    id: str
    text: str

class InputTable(BaseModel):
    overlap: list[str]
    page: str
