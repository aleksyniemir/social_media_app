from fastapi import FastAPI

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/userssss")
def get_user():
    return {"user": "olek"}

@app.post("/post")
def create_post():
    