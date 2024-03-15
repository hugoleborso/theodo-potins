import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infra.prisma import prisma


from routes.auth.auth import auth_router
from routes.signup import signup_router
from routes.potins import potins_router


MODE = os.getenv("MODE", "dev")

docs_url = None
redoc_url = None
openapi_url = None

if MODE == "dev":
    print("Developper mode enabled, Loading .env ...")
    load_dotenv("../.env")

openapi_url = "/openapi.json"
docs_url = "/docs"
redoc_url = "/redoc"

app = FastAPI(
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
    title="theodo-potins-api",
    description="The backend API for Theodo Potins, a mock API created to teach how to use Postamn in Vulgatech.",
    version="0.0.1",
    contact={
        "name": "Hugo Borsoni",
        "email": "hugobo@theodo.fr",
    },
)


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(signup_router)
app.include_router(potins_router)


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()
