import os
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from starlette.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set")
client = MongoClient(MONGO_URI)
db = client["app-directory"]
apps_collection = db["apps"]
profiles_collection = db["profiles"]

BASE_URL = "https://mixpeek.com/apps/"


@app.get("/{path}")
def redirect_to_mp_apps(path: str):
    # Check if the path exists in the apps collection
    if apps_collection.find_one({"slug": path}):
        target_url = f"{BASE_URL}{path}"
        return RedirectResponse(url=target_url)
    else:
        return RedirectResponse(url="https://mixpeek.com")


@app.get("/p/{path}")
def redirect_to_mp_profiles(path: str):
    # Check if the path exists in the profiles collection
    if profiles_collection.find_one({"path": path}):
        target_url = f"{BASE_URL}profiles/{path}"
        return RedirectResponse(url=target_url)
    else:
        return RedirectResponse(url="https://mixpeek.com")
