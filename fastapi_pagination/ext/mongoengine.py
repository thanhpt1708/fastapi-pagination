__all__ = ["paginate"]

from typing import Any, Optional, TypeVar, Union, cast

from mongoengine import QuerySet
from mongoengine.base.metaclasses import TopLevelDocumentMetaclass

from fastapi_pagination.api import apply_items_transformer, create_page
from fastapi_pagination.bases import AbstractParams
from fastapi_pagination.types import AdditionalData, SyncItemsTransformer
from fastapi_pagination.utils import verify_params

T = TypeVar("T", bound=TopLevelDocumentMetaclass)


def paginate(
    query: Union[type[T], QuerySet],
    params: Optional[AbstractParams] = None,
    *,
    transformer: Optional[SyncItemsTransformer] = None,
    additional_data: Optional[AdditionalData] = None,
) -> Any:
    params, raw_params = verify_params(params, "limit-offset")

    if isinstance(query, TopLevelDocumentMetaclass):
        query = cast(type[T], query).objects().all()

    total = query.count() if raw_params.include_total else None
    cursor = query.skip(raw_params.offset).limit(raw_params.limit)
    items = [item.to_mongo() for item in cursor]
    t_items = apply_items_transformer(items, transformer)

    return create_page(
        t_items,
        total=total,
        params=params,
        **(additional_data or {}),
    )
