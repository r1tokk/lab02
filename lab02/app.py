import argparse

from core import Record, build_pipeline, reduce_stats


def load_data(filepath: str) -> list[Record]:
    return [
        {
            "id": 1,
            "name": "john doe",
            "age": 25,
            "city": "Delhi",
            "purchases": [100.0, 50.0],
        },
        {
            "id": 2,
            "name": "jane smith",
            "age": 17,
            "city": "London",
            "purchases": [300.0],
        },
        {"id": 3, "name": "bob", "age": 30, "city": "Paris", "purchases": [200.0]},
        {"id": 4, "name": "alice", "age": 22, "city": "Delhi", "purchases": [200.0]},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Обробка записів клієнтів.")
    parser.add_argument("--top", type=int, default=2, help="Кількість записів у Top-N")
    parser.add_argument(
        "--boost-city", type=str, default="Delhi", help="Місто для бонусу"
    )
    parser.add_argument("--factor", type=float, default=1.1, help="Коефіцієнт бонусу")
    args = parser.parse_args()

    raw_data = load_data("sample_data.json")

    pipeline = build_pipeline(top_n=args.top, city=args.boost_city, factor=args.factor)

    processed_data = pipeline(raw_data)

    stats = reduce_stats(processed_data)

    print(f"=== TOP {args.top} КЛІЄНТІВ ===")
    for rec in processed_data:
        print(
            f"ID: {rec['id']} | Name: {rec['name']} | "
            f"City: {rec['city']} | Total: {rec['total']:.2f}"
        )

    print("\n=== АГРЕГОВАНА СТАТИСТИКА ===")
    print(f"Кількість (count):     {stats['count']}")
    print(f"Сума (sum_total):      {stats['sum_total']:.2f}")
    print(f"Середнє (avg_total):   {stats['avg_total']:.2f}")


if __name__ == "__main__":
    main()
