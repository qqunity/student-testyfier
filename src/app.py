from fastapi import FastAPI

app = FastAPI()


@app.get("/fill_db")
async def fill_db():
    return {"message": "Data loaded successfully!"}
