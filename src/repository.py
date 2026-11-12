import re
from pathlib import Path

from apk_index import direct_requirements, fetch_index


TEST_NAME = r"[A-Z]+"


def parse_test_line(line, number):
    name, separator, items = line.partition(":")
    name = name.strip()
    dependencies = items.split()
    if not separator or not re.fullmatch(TEST_NAME, name):
        raise ValueError(f"строка {number}: ожидается запись A: B C")
    for dependency in dependencies:
        if not re.fullmatch(TEST_NAME, dependency):
            raise ValueError(f"строка {number}: неверное имя {dependency}")
    return name, list(dict.fromkeys(dependencies))


def load_test_repository(filename):
    graph = {}
    lines = Path(filename).read_text(encoding="utf-8").splitlines()
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        name, dependencies = parse_test_line(line, number)
        if name in graph:
            raise ValueError(f"строка {number}: пакет {name} уже описан")
        graph[name] = dependencies
    for dependencies in graph.values():
        for dependency in dependencies:
            if dependency not in graph:
                raise ValueError(f"не описан тестовый пакет {dependency}")
    return graph


def provider_map(packages):
    providers = {}
    for name, fields in packages.items():
        entries = [name + "=" + fields.get("V", "")]
        entries += fields.get("p", "").split()
        for entry in entries:
            feature, _, version = entry.partition("=")
            providers.setdefault(feature, []).append((name, version))
    return providers


def resolve_requirement(requirement, packages, providers):
    feature = re.split(r"[<>=~]", requirement, maxsplit=1)[0]
    constraint = requirement[len(feature):]
    candidates = []
    for name, version in providers.get(feature, []):
        if not constraint or constraint == "=" + version:
            candidates.append(name)
    if feature in packages and feature in candidates:
        return feature
    names = list(dict.fromkeys(candidates))
    if len(names) == 1:
        return names[0]
    return requirement


def apk_graph(packages):
    providers = provider_map(packages)
    repository = {}
    for name in packages:
        dependencies = []
        for requirement in direct_requirements(packages, name):
            if not requirement.startswith("!"):
                target = resolve_requirement(requirement, packages, providers)
                if target not in dependencies:
                    dependencies.append(target)
        repository[name] = dependencies
    return repository


def load_repository(config):
    if config["test_mode"]:
        return load_test_repository(config["repository"])
    return apk_graph(fetch_index(config["repository"]))
