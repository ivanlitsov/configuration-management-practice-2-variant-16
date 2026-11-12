import sys

from apk_index import direct_requirements, fetch_index
from config import read_config


def main():
    if len(sys.argv) != 2:
        print("Запуск: python src/main.py <конфигурация.toml>", file=sys.stderr)
        return 2
    try:
        config = read_config(sys.argv[1])
        if config["test_mode"]:
            raise ValueError("тестовый репозиторий появится на этапе 3")
        packages = fetch_index(config["repository"])
        dependencies = direct_requirements(packages, config["package"])
        print("\n".join(dependencies) if dependencies else "Зависимостей нет")
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
