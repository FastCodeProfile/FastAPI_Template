"""
Schemas Users
"""

from pydantic import ConfigDict, BaseModel, Field, EmailStr

from app.database.structures import Role


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RoleUser(BaseUser):
    role: Role = Field(examples=[Role.USER])


class EmailUser(BaseUser):
    email: EmailStr = Field(examples=["fast.code.auth@gmail.com"])


class PasswordUser(BaseUser):
    password: str = Field(examples=["12345"])


class GetUser(EmailUser, RoleUser):
    id: int = Field(examples=[0])


class NewUser(PasswordUser, EmailUser):
    pass


class AuthUser(PasswordUser, EmailUser):
    pass
