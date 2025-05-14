from fastapi import FastAPI
from app.routes import hello_route

app = FastAPI()

app.include_router(hello_route.router)
