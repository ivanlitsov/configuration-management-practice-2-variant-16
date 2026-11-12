import sys

from config import read_config


def main():
    if len(sys.argv) != 2:
        print("Запуск: python src/main.py <конфигурация.toml>", file=sys.stderr)
        return 2
    try:
        config = read_config(sys.argv[1])
        for key in config:
            print(f"{key} = {config[key]}")
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
