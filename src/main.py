import sys

from config import read_config
from graph import build_graph
from repository import load_repository
from visualize import ascii_tree, show_graph


def main():
    if len(sys.argv) != 2:
        print("Запуск: python src/main.py <конфигурация.toml>", file=sys.stderr)
        return 2
    try:
        config = read_config(sys.argv[1])
        repository = load_repository(config)
        root = config["package"]
        graph, cycles, _ = build_graph(repository, root)
        for cycle in cycles:
            print("Цикл: " + " -> ".join(cycle), file=sys.stderr)
        if config["ascii_tree"]:
            print(ascii_tree(graph, root))
        source, image = show_graph(graph, root)
        print(f"D2: {source}")
        print(f"SVG: {image}")
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
