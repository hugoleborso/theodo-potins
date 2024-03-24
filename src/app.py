import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infra.prisma import prisma


from routes.auth.auth import auth_router
from routes.signup import signup_router
from routes.potins import potins_router
from routes.users import users_router


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
    servers=[
        {
            "url": "http://ec2-35-180-181-45.eu-west-3.compute.amazonaws.com",
        },
        {
            "url": "http://0.0.0.0:8081",
        },
    ],
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


app.include_router(potins_router)
app.include_router(users_router)
app.include_router(signup_router)
app.include_router(auth_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = app.openapi()
    print(openapi_schema.keys())
    openapi_schema["components"]["schemas"]["Body_login_login_post"][
        "examples"
    ] = [
        {
            "username": "hugobo@theodo.fr",
            "password": "password123!",
            "scope": "",
            "grant_type": "password",
            "client_id": "",
            "client_secret": "",
        },
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


custom_openapi()


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()
