from pydantic import BaseModel

class FarmaciaBase(BaseModel):
    pass

class FarmaciaCreate(FarmaciaBase):
    pass

class FarmaciaRead(FarmaciaBase):
    id: int

    class Config:
        from_attributes = True
