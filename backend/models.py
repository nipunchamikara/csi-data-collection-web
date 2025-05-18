from pydantic import BaseModel


class DataCollectionRequest(BaseModel):
    label: str
    duration: int
    experiment: str
