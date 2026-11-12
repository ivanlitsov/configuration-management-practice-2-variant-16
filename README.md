# Граф зависимостей Alpine Linux

Практическая работа № 2, вариант 16. На этапе 3 программа строит граф
зависимостей пакета рекурсивным DFS и выводит списки смежности.

Нужен Python 3.11 или новее. Сборка не требуется.

```powershell
python src/main.py config.toml
python src/main.py tests/data/diamond.toml
python src/main.py tests/data/cycle.toml
python src/main.py tests/data/single.toml
python -m unittest discover -s tests -v
```

- `package` — имя пакета APK или имя из больших латинских букв.
- `repository` — URL каталога Alpine, URL архива APKINDEX.tar.gz
  или путь к тестовому файлу относительно TOML.
- `test_mode` — при `true` читается тестовый файл.
- `ascii_tree` — параметр для этапа визуализации.

Тестовый файл содержит строки вида `A: B C`. Для каждого пакета нужна
собственная строка. Пустой список справа означает отсутствие зависимостей.
Циклическое ребро сохраняется, путь цикла выводится в stderr.
