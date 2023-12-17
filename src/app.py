import os

from fastapi import FastAPI
from db import DbInteractions

app = FastAPI()


@app.post("/recreate-db")
async def recreate_db():
    db_interactions = DbInteractions(
        host=os.getenv('DB_HOST'),
        port='5434',
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        db_name=os.getenv('POSTGRES_DB'),
        rebuild_db=False
    )
    db_interactions.recreate_tables()

    return {"message": "DB recreated successfully!"}


@app.post("/fill-db")
async def fill_db():
    return {"message": "Data loaded successfully!"}
