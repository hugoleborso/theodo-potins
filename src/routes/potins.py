from typing import Annotated, List
from fastapi import APIRouter, Depends
from prisma.models import Potin, User

from prisma.types import (
    PotinCreateInput,
    PotinWhereUniqueInput,
)
from pydantic import BaseModel

from infra.prisma import getPrisma  # type: ignore
from routes.auth.utils import check_user  # type: ignore

potins_router = APIRouter(prefix="/potins", tags=["potins"])
prisma = getPrisma()


@potins_router.get(
    "", response_model=List[Potin], response_model_exclude_none=True
)
async def get_all_potins():
    potins = await prisma.potin.find_many()
    return potins


class PotinInfos(BaseModel):
    content: str
    concernedUsersGroupEmail: list[str]


@potins_router.post("", response_model=Potin, response_model_exclude_none=True)
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
    "/{potin_id}", response_model=Potin, response_model_exclude_none=True
)
async def update_potin(
    potin_id: int,
    potin: PotinInfos,
    user: Annotated[User, Depends(check_user)],
):

    modified_potin = await prisma.potin.update(
        where=PotinWhereUniqueInput(id=potin_id),
        data=PotinCreateInput(
            content=potin.content,
            concernedUsersGroupEmail=potin.concernedUsersGroupEmail,
            authorEmail=user.email,
        ),
    )
    return modified_potin


@potins_router.delete("/{potin_id}")
async def delete_potin(potin_id: int):
    await prisma.potin.delete(where=PotinWhereUniqueInput(id=potin_id))
