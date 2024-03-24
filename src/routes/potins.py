from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from prisma.models import User

from prisma.types import (
    PotinCreateInput,
    PotinWhereInput,
)
from pydantic import BaseModel

from infra.prisma import getPrisma  # type: ignore
from routes.auth.utils import check_user  # type: ignore

BASE_POTIN_CONTENT = (
    "Je crois que la CEO de Theodo et le CTO de Sipios sont en couple ..."
)

BASE_POTIN_CONCERNED_USERS_GROUP_EMAIL = [
    "carolines@theodo.fr",
    "woodyr@sipios.fr",
]


BASE_POTIN_USER = "hugobo@theodo.fr"


class PotinOut(BaseModel):
    id: int
    content: str
    concernedUsersGroupEmail: List[str]
    authorEmail: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "content": BASE_POTIN_CONTENT,
                    "concernedUsersGroupEmail": BASE_POTIN_CONCERNED_USERS_GROUP_EMAIL,  # type: ignore
                    "authorEmail": BASE_POTIN_USER,
                }
            ]
        }
    }


class PotinInfos(BaseModel):
    content: str
    concernedUsersGroupEmail: list[str]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "content": BASE_POTIN_CONTENT,
                    "concernedUsersGroupEmail": BASE_POTIN_CONCERNED_USERS_GROUP_EMAIL,  # type: ignore
                }
            ]
        }
    }


class Message(BaseModel):
    message: str


potins_router = APIRouter(
    prefix="/potins",
    tags=["potins"],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
)
prisma = getPrisma()


@potins_router.get(
    "",
    response_model=List[PotinOut],
    response_model_exclude_none=True,
)
async def get_all_potins():
    potins = await prisma.potin.find_many()
    return potins


@potins_router.post(
    "",
    response_model=PotinOut,
    response_model_exclude_none=True,
)
async def create_potin(
    potin: PotinInfos,
    user: Annotated[User, Depends(check_user)],
):

    created_potin = await prisma.potin.create(
        data=PotinCreateInput(
            content=potin.content,
            concernedUsersGroupEmail=potin.concernedUsersGroupEmail,
            authorEmail=user.email,
        )
    )
    return created_potin


@potins_router.put(
    "/{potin_id}",
    response_model=PotinOut,
    responses={
        404: {"description": "Potin Not found"},
    },
    response_model_exclude_none=True,
)
async def update_potin(
    potin_id: int,
    potin: PotinInfos,
    user: Annotated[User, Depends(check_user)],
):

    modified_potin = await prisma.potin.update(
        where=PotinWhereInput(id=potin_id, authorEmail=user.email),
        data=PotinCreateInput(
            content=potin.content,
            concernedUsersGroupEmail=potin.concernedUsersGroupEmail,
            authorEmail=user.email,
        ),
    )
    if not modified_potin:
        raise HTTPException(status_code=404, detail="Potin not found")
    return modified_potin


@potins_router.delete(
    "/{potin_id}",
    response_model=PotinOut,
    responses={
        404: {"description": "Potin Not found"},
    },
    response_model_exclude_none=True,
)
async def delete_potin(
    potin_id: int, user: Annotated[User, Depends(check_user)]
):
    deleted_potin = await prisma.potin.delete(
        where=PotinWhereInput(
            id=potin_id,
            authorEmail=user.email,
        )
    )
    if not deleted_potin:
        raise HTTPException(status_code=404, detail="Potin not found")
    return deleted_potin
