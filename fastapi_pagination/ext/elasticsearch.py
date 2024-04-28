__all__ = ["paginate"]
from typing import Any, Optional

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from ..api import apply_items_transformer, create_page
from ..bases import AbstractParams
from ..types import AdditionalData, SyncItemsTransformer
from ..utils import verify_params


def paginate(
    conn: Elasticsearch,
    query: Search,
    params: Optional[AbstractParams] = None,
    *,
    transformer: Optional[SyncItemsTransformer] = None,  # Optional transformer for items
    additional_data: Optional[AdditionalData] = None,  # Optional additional data for page object
) -> Any:
    params, raw_params = verify_params(params, "limit-offset")
    response = query.using(conn)[raw_params.offset, raw_params.offset + raw_params.limit].execute()
    total = response.hits.total
    items = response.hits[0]
    t_items = apply_items_transformer(items, transformer)
    return create_page(
        t_items,
        total=total,
        params=params,
        **(additional_data or {}),
    )
