import json
import shutil
import subprocess
import webbrowser
from pathlib import Path


def d2_source(graph):
    names = {}
    lines = []
    for number, package in enumerate(graph, 1):
        names[package] = f"n{number}"
        label = json.dumps(package, ensure_ascii=False)
        lines.append(f"{names[package]}: {label}")
    for package, dependencies in graph.items():
        for dependency in dependencies:
            lines.append(f"{names[package]} -> {names[dependency]}")
    return "\n".join(lines) + "\n"


def ascii_tree(graph, root):
    lines = [root]
    seen = {root}
    path = {root}

    def visit(package, prefix):
        dependencies = graph[package]
        for position, child in enumerate(dependencies, 1):
            last = position == len(dependencies)
            branch = "`-- " if last else "|-- "
            line = prefix + branch + child
            if child in path:
                lines.append(line + " (cycle)")
            elif child in seen:
                lines.append(line + " (shown)")
            else:
                lines.append(line)
                seen.add(child)
                path.add(child)
                visit(child, prefix + ("    " if last else "|   "))
                path.remove(child)

    visit(root, "")
    return "\n".join(lines)


def show_graph(graph, root):
    output = Path("out")
    output.mkdir(exist_ok=True)
    source = output / (root + ".d2")
    image = output / (root + ".svg")
    source.write_text(d2_source(graph), encoding="utf-8")
    d2 = shutil.which("d2")
    if d2 is None:
        raise ValueError(f"D2 не найден в PATH. Описание сохранено в {source}")
    result = subprocess.run([d2, str(source), str(image)], check=False)
    if result.returncode:
        raise ValueError(f"D2 не смог построить изображение {image}")
    webbrowser.open(image.resolve().as_uri())
    return source, image
