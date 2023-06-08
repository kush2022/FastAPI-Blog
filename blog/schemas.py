from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "felix kuria",
                "email": "felixkuria@gmail.com",
                "password": "password"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None



class Blog(BaseModel):
    title: str
    body: str
