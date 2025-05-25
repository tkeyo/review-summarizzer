from fastapi import FastAPI
from app.routers import health, summarize
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = FastAPI()



app.include_router(health.router)
app.include_router(summarize.router) 