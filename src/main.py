import sys

from config import read_config
from graph import build_graph
from repository import load_repository


def main():
    if len(sys.argv) != 2:
        print("Запуск: python src/main.py <конфигурация.toml>", file=sys.stderr)
        return 2
    try:
        config = read_config(sys.argv[1])
        repository = load_repository(config)
        root = config["package"]
        _, cycles, order = build_graph(repository, root)
        if cycles:
            cycle = " -> ".join(cycles[0])
            raise ValueError(f"порядок загрузки невозможен, цикл {cycle}")
        print(" -> ".join(order[:-1]) or "Нет зависимостей")
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
