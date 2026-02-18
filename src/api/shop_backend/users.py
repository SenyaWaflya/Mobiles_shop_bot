from httpx import AsyncClient, _status_codes

from src.schemas.users import UserDto, UserResponse
from src.settings import settings


class UsersApi:
    @staticmethod
    async def add(user_dto: UserDto) -> UserResponse | None:
        user_dto = user_dto.model_dump()
        async with AsyncClient() as client:
            resp = await client.post(url=f'{settings.SHOP_BACKEND_API_URL}/users/register', json=user_dto)
            if resp.status_code == _status_codes.code.CONFLICT:
                return None
            return UserResponse.model_validate(resp.json())

    @staticmethod
    async def get(tg_id: int) -> UserResponse:
        async with AsyncClient() as client:
            resp = await client.get(url=f'{settings.SHOP_BACKEND_API_URL}/users/{tg_id}')
            resp.raise_for_status()
            return UserResponse.model_validate(resp.json())
