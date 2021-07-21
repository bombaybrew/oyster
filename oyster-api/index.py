from fastapi import FastAPI
import api.home_controller as homeController

VERSION = 'v0.0.1'

# App
# --------------------

app = FastAPI()

# Routes
# --------------------

@app.get("/")
async def root():
    return {"Oyster API": VERSION}

@app.get("/home")
async def home():
    return await homeController.helloHome()