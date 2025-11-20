from pydantic import BaseModel


class MerseBaseModel(BaseModel):
    class Config:
        extra = "ignore"
        frozen = False