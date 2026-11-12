import io
import tarfile
from urllib.request import urlopen


INDEX_ARCHIVE = "APKINDEX.tar.gz"


def parse_index(text):
    packages = {}
    for block in text.split("\n\n"):
        fields = {}
        for line in block.splitlines():
            key, separator, value = line.partition(":")
            if separator:
                fields[key] = value
        if "P" in fields:
            packages[fields["P"]] = fields
    if not packages:
        raise ValueError("APKINDEX не содержит записей пакетов")
    return packages


def fetch_index(repository):
    url = repository.rstrip("/")
    if not url.endswith("/" + INDEX_ARCHIVE):
        url += "/" + INDEX_ARCHIVE
    with urlopen(url, timeout=20) as response:
        data = response.read()
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            index = archive.extractfile("APKINDEX")
            if index is None:
                raise ValueError("APKINDEX отсутствует в архиве")
            with index:
                return parse_index(index.read().decode("utf-8"))
    except (tarfile.TarError, KeyError, EOFError) as error:
        raise ValueError("не удалось прочитать APKINDEX.tar.gz") from error


def direct_requirements(packages, name):
    if name not in packages:
        raise ValueError(f"пакет {name} не найден в APKINDEX")
    return packages[name].get("D", "").split()
