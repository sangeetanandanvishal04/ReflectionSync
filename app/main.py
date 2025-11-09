from fastapi import FastAPI
from .database import get_db, engine
from . import tablesmodel, utils
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, admin

app = FastAPI()

#origins = ["www.youtube.com", "www.google.com"]
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tablesmodel.Base.metadata.create_all(bind = engine)

def create_initial_admin():
    admin_email = settings.initial_admin_email
    admin_password = settings.initial_admin_password
    if admin_email and admin_password:
        db = next(get_db())
        try:
            existing = db.query(tablesmodel.User).filter(tablesmodel.User.email == admin_email).first()
            if not existing:
                hashed = utils.hash(admin_password)
                admin_user = tablesmodel.User(email=admin_email, password=hashed, role="admin", is_verified=True)
                db.add(admin_user)
                db.commit()
                print(f"[startup] Created initial admin: {admin_email}")
        finally:
            db.close()

create_initial_admin()

app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message" : "Welcome to my Intelligent Floor Plan Management System API...."}