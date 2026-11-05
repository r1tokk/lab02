from copy import deepcopy

import pytest

from core import Record, build_pipeline, reduce_stats


@pytest.fixture
def sample_records() -> list[Record]:
    return [
        {"id": 1, "name": "john doe", "age": 20, "city": "Delhi", "purchases": [100.0]},
        {"id": 2, "name": "jane", "age": 16, "city": "Delhi", "purchases": [500.0]},
        {"id": 3, "name": "bob", "age": 25, "city": "London", "purchases": [200.0]},
    ]


def test_pipeline_top_n(sample_records: list[Record]) -> None:
    pipeline = build_pipeline(top_n=2, city="Delhi", factor=1.5)
    result = pipeline(sample_records)

    assert len(result) == 2

    assert result[0]["id"] == 3
    assert result[0]["total"] == 200.0

    assert result[1]["id"] == 1
    assert result[1]["total"] == 150.0

    assert result[1]["name"] == "John Doe"


def test_no_mutation(sample_records: list[Record]) -> None:
    original = deepcopy(sample_records)
    pipeline = build_pipeline(top_n=5, city="Delhi", factor=2.0)

    pipeline(sample_records)

    assert sample_records == original


def test_reduce_stats() -> None:
    recs: list[Record] = [
        {"id": 1, "total": 100.0},
        {"id": 2, "total": 300.0},
    ]

    stats = reduce_stats(recs)

    assert stats["count"] == 2.0
    assert stats["sum_total"] == 400.0
    assert stats["avg_total"] == 200.0
