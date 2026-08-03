from collections.abc import AsyncIterator
from typing import Annotated, NamedTuple

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.tokens import ALGORITHM, SECRET_KEY
from app.infrastructure.database.models import User
from app.infrastructure.database.session import async_session_maker

bearer_scheme = HTTPBearer()


async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


DatabaseSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(bearer_scheme),
    ],
    db: DatabaseSession,
) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="User ID missing in token.",
            )
    except (JWTError, ValueError) as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token.",
        ) from exc

    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive.")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


class CommonContext(NamedTuple):
    db: AsyncSession
    current_user: User


async def get_common_context(
    db: DatabaseSession,
    current_user: CurrentUser,
) -> CommonContext:
    return CommonContext(db=db, current_user=current_user)
