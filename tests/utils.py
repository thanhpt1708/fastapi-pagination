from typing import Any, List, Type, TypeVar

from faker import Faker
from pydantic import BaseModel

from fastapi_pagination import LimitOffsetPage, Page
from fastapi_pagination.customization import CustomizedPage, UseOptionalParams
from fastapi_pagination.utils import IS_PYDANTIC_V2

faker = Faker()

T = TypeVar("T", bound=BaseModel)

if IS_PYDANTIC_V2:

    def parse_obj(model: Type[T], obj: Any) -> T:
        return model.model_validate(obj, from_attributes=True)

    def dump_obj(model: Type[T], obj: Any) -> dict:
        return model.model_dump(obj, by_alias=True)
else:

    def parse_obj(model: Type[T], obj: Any) -> T:
        return model.parse_obj(obj)

    def dump_obj(model: Type[T], obj: Any) -> dict:
        return model.dump(obj, by_alias=True)


def normalize(model: Type[T], *models: Any) -> List[T]:
    return [parse_obj(model, m) for m in models]


OptionalPage = CustomizedPage[Page, UseOptionalParams()]
OptionalLimitOffsetPage = CustomizedPage[LimitOffsetPage, UseOptionalParams()]


__all__ = [
    "OptionalLimitOffsetPage",
    "OptionalPage",
    "dump_obj",
    "faker",
    "normalize",
    "parse_obj",
]
