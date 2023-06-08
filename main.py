from fastapi import FastAPI

from blog.routers import blog, auth, authentication
from blog import models, database


models.Base.metadata.create_all(database.engine)


app = FastAPI(
    title="Felix's Blog API",
    contact={
        "name": "Felix Kuria",
        "url": "https://www.linkedin.com/in/felix-kuria/",
        "email": "felixkuria12@gmail.com",
    },
)

app.include_router(auth.router)
app.include_router(authentication.router)
app.include_router(blog.router)
