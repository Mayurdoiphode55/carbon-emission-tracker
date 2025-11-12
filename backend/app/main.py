from fastapi import FastAPI
from app import db
from app.routers import user_router

app = FastAPI(title="Carbon Emission Tracker API")

@app.on_event("startup")
async def startup():
    await db.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()

@app.get("/health")
def health():
    return {"status": "ok"}

# include router
app.include_router(user_router.router)
