from typing import Iterator, Type

from elasticsearch import Elasticsearch
from fastapi import Depends, FastAPI
from pytest import fixture

from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from fastapi_pagination.ext.elasticsearch import paginate

from ..base import BasePaginationTestCase


@fixture(scope="session")
def app(elasticsearch_connection: Type[Elasticsearch], model_cls: Type[object]):
    app = FastAPI()

    def get_elasticsearch() -> Iterator[Elasticsearch]:
        yield elasticsearch_connection

    @app.get("/default", response_model=Page[model_cls])
    @app.get("/limit-offset", response_model=LimitOffsetPage[model_cls])
    def route(connection: Elasticsearch = Depends(get_elasticsearch)):
        return paginate(connection)

    return add_pagination(app)


class TestElasticsearch(BasePaginationTestCase):
    pass
