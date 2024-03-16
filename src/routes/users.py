from typing import List
from fastapi import APIRouter

from prisma.types import (
    _StringListFilterHasInput,
    PotinWhereInput,
)

from infra.prisma import getPrisma
from routes.potins import PotinOut  # type: ignore

users_router = APIRouter(prefix="/users", tags=["users"])
prisma = getPrisma()


@users_router.get(
    "/{user_email}/written-potins",
    response_model=List[PotinOut],
    response_model_exclude_none=True,
)
async def get_all_potins_from_user(user_email: str):
    potins = await prisma.potin.find_many(
        where=PotinWhereInput(authorEmail=user_email)
    )
    return potins


@users_router.get(
    "/{user_email}/in-potins",
    response_model=List[PotinOut],
    response_model_exclude_none=True,
)
async def get_all_potins_on_user(user_email: str):
    potins = await prisma.potin.find_many(
        where=PotinWhereInput(
            concernedUsersGroupEmail=_StringListFilterHasInput(has=user_email)
        )
    )
    return potins
