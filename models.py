# models.py

from pydantic import BaseModel

class InputTerm(BaseModel):
    term: str

class SpellCheckResponse(BaseModel):
    input_term: str
    corrections: list[str]
