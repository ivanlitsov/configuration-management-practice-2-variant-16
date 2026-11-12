def build_graph(repository, root):
    if root not in repository:
        raise ValueError(f"пакет {root} не найден в репозитории")
    graph = {}
    cycles = []
    path = []
    order = []

    def visit(package):
        if package in path:
            cycles.append(path[path.index(package):] + [package])
            return
        if package in graph:
            return
        dependencies = repository.get(package, [])
        graph[package] = dependencies
        path.append(package)
        for dependency in dependencies:
            visit(dependency)
        path.pop()
        order.append(package)

    visit(root)
    if cycles:
        order = []
    return graph, cycles, order
