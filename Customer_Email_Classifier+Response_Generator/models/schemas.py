from pydantic import BaseModel


class EmailClassification(BaseModel):
    category: str
    sentiment: str