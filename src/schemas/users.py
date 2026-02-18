from pydantic import BaseModel


class UserDto(BaseModel):
    tg_id: str
    username: str


class UserResponse(UserDto):
    id: int
