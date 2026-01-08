from fastapi import FastAPI
from routers import auth, admin, agent, user
from core.database import SessionLocal, engine,Base
from core.init_admin import create_default_admin

app = FastAPI(title="Anand Devocation")

# Create tables
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        create_default_admin(db)
    finally:
        db.close()

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(agent.router)
app.include_router(user.router)
