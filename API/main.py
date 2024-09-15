from fastapi import FastAPI
from routers import auth, blogs

app = FastAPI(title="Amalaiyot API")
app.include_router(auth.router)
app.include_router(blogs.router)