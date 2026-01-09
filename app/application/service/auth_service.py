from fastapi import Depends
from app.infrastructure.auth.auth_client import AuthClient


async def get_auth_client() -> AuthClient:
    return AuthClient()


async def get_user_id_by_token(
    token: str,
    auth_client: AuthClient = Depends(get_auth_client)
) -> str:
    return await auth_client.get_user_id_by_token(token)
