import pytest

from postgrest_py import SyncRequestBuilder
from postgrest_py.types import CountMethod
from postgrest_py.utils import SyncClient


@pytest.fixture
def request_builder():
    with SyncClient() as client:
        yield SyncRequestBuilder(client, "/example_table")


def test_constructor(request_builder):
    assert request_builder.path == "/example_table"


class TestSelect:
    def test_select(self, request_builder: SyncRequestBuilder):
        builder = request_builder.select("col1", "col2")

        assert builder.session.params["select"] == "col1,col2"
        assert builder.session.headers.get("prefer") is None
        assert builder.http_method == "GET"
        assert builder.json == {}

    def test_select_with_count(self, request_builder: SyncRequestBuilder):
        builder = request_builder.select(count=CountMethod.exact)

        assert builder.session.params.get("select") is None
        assert builder.session.headers["prefer"] == "count=exact"
        assert builder.http_method == "HEAD"
        assert builder.json == {}


class TestInsert:
    def test_insert(self, request_builder: SyncRequestBuilder):
        builder = request_builder.insert({"key1": "val1"})

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation"
        ]
        assert builder.http_method == "POST"
        assert builder.json == {"key1": "val1"}

    def test_insert_with_count(self, request_builder: SyncRequestBuilder):
        builder = request_builder.insert({"key1": "val1"}, count=CountMethod.exact)

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "count=exact",
        ]
        assert builder.http_method == "POST"
        assert builder.json == {"key1": "val1"}

    def test_insert_with_upsert(self, request_builder: SyncRequestBuilder):
        builder = request_builder.insert({"key1": "val1"}, upsert=True)

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "resolution=merge-duplicates",
        ]
        assert builder.http_method == "POST"
        assert builder.json == {"key1": "val1"}

    def test_upsert(self, request_builder: SyncRequestBuilder):
        builder = request_builder.upsert({"key1": "val1"})

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "resolution=merge-duplicates",
        ]
        assert builder.http_method == "POST"
        assert builder.json == {"key1": "val1"}


class TestUpdate:
    def test_update(self, request_builder: SyncRequestBuilder):
        builder = request_builder.update({"key1": "val1"})

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation"
        ]
        assert builder.http_method == "PATCH"
        assert builder.json == {"key1": "val1"}

    def test_update_with_count(self, request_builder: SyncRequestBuilder):
        builder = request_builder.update({"key1": "val1"}, count=CountMethod.exact)

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "count=exact",
        ]
        assert builder.http_method == "PATCH"
        assert builder.json == {"key1": "val1"}


class TestDelete:
    def test_delete(self, request_builder: SyncRequestBuilder):
        builder = request_builder.delete()

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation"
        ]
        assert builder.http_method == "DELETE"
        assert builder.json == {}

    def test_delete_with_count(self, request_builder: SyncRequestBuilder):
        builder = request_builder.delete(count=CountMethod.exact)

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "count=exact",
        ]
        assert builder.http_method == "DELETE"
        assert builder.json == {}
