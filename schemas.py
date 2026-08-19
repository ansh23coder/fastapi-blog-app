from pydantic import BaseModel

# Input Schema
class BlogCreate(BaseModel):
    title: str
    content: str

# Output Schema
class BlogResponse(BaseModel):
    id:int
    title:str
    content:str
    class Config:
        from_attributes = True
