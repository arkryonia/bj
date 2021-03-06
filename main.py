
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local contribs
from core.db import create_db_and_tables

# import routes
from api.lands.departments import departments
from api.lands.towns import towns
from api.lands.districts import districts
from api.auth.auth import auth

app = FastAPI()

origins = [
    "http://localhost:8080",
    "https://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth, prefix="/u", tags=["Users Accounts"])
app.include_router(departments, prefix="/bj/d", tags=["Departments"])
app.include_router(towns, prefix="/bj/t", tags=["Towns"])
app.include_router(districts, prefix="/bj/l", tags=["Districts"])


@app.get('/', tags=["Index"])
def index():
    return {
        "title": "Republic of Benin Lands (API REST)",
        "version": "0.1.0",
        "date": datetime.utcnow(),
        "comapany": {
            "brand": "Nemim Services",
            "name": "Nemim Sarl",
            "contributors": {
                "architect": "Hodonou Sounton",
                "senior_dev": "Lanzy Atamao",
                "admin_lead": "Ife Kouta",
                "commercial": "Bidossessi Sounton"
            },
        }        
    }