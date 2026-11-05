from collections.abc import Callable, Iterable, Iterator
from functools import reduce
from itertools import islice
from typing import Any, TypedDict


class Record(TypedDict, total=False):
    id: int
    name: str
    age: int
    city: str
    purchases: list[float]
    total: float


def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def _c(x: Any) -> Any:
        for f in reversed(funcs):
            x = f(x)
        return x

    return _c


def only_adults(min_age: int = 18) -> Callable[[Iterable[Record]], Iterator[Record]]:
    return lambda recs: (r for r in recs if int(r.get("age", 0)) >= min_age)


def with_total() -> Callable[[Iterable[Record]], Iterator[Record]]:
    return lambda recs: (
        {**r, "total": float(sum(r.get("purchases", [])))} for r in recs
    )


def boost_city(
    city: str, factor: float
) -> Callable[[Iterable[Record]], Iterator[Record]]:
    def _f(recs: Iterable[Record]) -> Iterator[Record]:
        for r in recs:
            t = float(r.get("total", 0.0))
            new_total = t * factor if r.get("city") == city else t
            yield {**r, "total": new_total}

    return _f


def normalize_names() -> Callable[[Iterable[Record]], Iterator[Record]]:
    return lambda recs: (
        {**r, "name": str(r.get("name", "")).strip().title()} for r in recs
    )


def sort_by_total_desc() -> Callable[[Iterable[Record]], list[Record]]:
    return lambda recs: sorted(
        recs, key=lambda r: (-float(r.get("total", 0.0)), int(r.get("id", 0)))
    )


def take(n: int) -> Callable[[Iterable[Record]], list[Record]]:
    return lambda recs: list(islice(recs, n))


def build_pipeline(
    top_n: int = 2, city: str = "Delhi", factor: float = 1.1
) -> Callable[[Iterable[Record]], list[Record]]:
    return compose(
        take(top_n),
        sort_by_total_desc(),
        boost_city(city, factor),
        with_total(),
        only_adults(18),
        normalize_names(),
    )


def reduce_stats(recs: Iterable[Record]) -> dict[str, float]:
    init_acc = {"count": 0.0, "sum_total": 0.0}

    acc = reduce(
        lambda a, r: {
            "count": a["count"] + 1,
            "sum_total": a["sum_total"] + float(r.get("total", 0.0)),
        },
        recs,
        init_acc,
    )

    count = acc["count"]
    avg = acc["sum_total"] / count if count > 0 else 0.0

    return {
        "count": count,
        "sum_total": acc["sum_total"],
        "avg_total": avg,
    }
