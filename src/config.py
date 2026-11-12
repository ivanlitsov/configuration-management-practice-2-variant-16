import re
import tomllib
from pathlib import Path
from urllib.parse import urlsplit


FIELDS = ("package", "repository", "test_mode", "ascii_tree")


def validate_strings(config):
    for field in ("package", "repository"):
        value = config[field]
        if not isinstance(value, str) or not value or value != value.strip():
            raise ValueError(f"{field}: требуется непустая строка")


def validate_values(config):
    for field in FIELDS:
        if field not in config:
            raise ValueError(f"отсутствует параметр {field}")
    validate_strings(config)
    for field in ("test_mode", "ascii_tree"):
        if not isinstance(config[field], bool):
            raise ValueError(f"{field}: требуется true или false")
    for field in config:
        if field not in FIELDS:
            raise ValueError(f"неизвестный параметр {field}")


def validate_url(repository):
    try:
        url = urlsplit(repository)
        url.port
    except ValueError:
        raise ValueError("repository: неверный URL")
    if url.scheme not in ("http", "https") or not url.hostname:
        raise ValueError("repository: требуется URL HTTP или HTTPS")
    if url.query or url.fragment or any(ch.isspace() for ch in repository):
        raise ValueError("repository: укажите адрес каталога или APKINDEX")


def validate_repository(config, folder):
    repository = config["repository"]
    if config["test_mode"]:
        if not re.fullmatch(r"[A-Z]+", config["package"]):
            raise ValueError("package: требуются большие латинские буквы")
        path = folder / repository
        if not path.is_file():
            raise ValueError(f"repository: файл не найден: {path}")
        config["repository"] = str(path)
    else:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9+_.-]*", config["package"]):
            raise ValueError("package: неверное имя пакета APK")
        validate_url(repository)


def read_config(filename):
    path = Path(filename)
    with path.open("rb") as stream:
        config = tomllib.load(stream)
    validate_values(config)
    validate_repository(config, path.parent)
    return config
