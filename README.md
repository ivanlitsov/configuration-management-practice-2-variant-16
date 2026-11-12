# Граф зависимостей Alpine Linux

Практическая работа № 2, вариант 16. Этап 2 загружает APKINDEX.tar.gz
по адресу репозитория и печатает поле D указанного пакета.

Нужен Python 3.11 или новее. Сборка не требуется.

```powershell
python src/main.py config.toml
python -m unittest discover -s tests -v
```

- `package` — имя пакета APK.
- `repository` — URL каталога Alpine или самого архива APKINDEX.tar.gz.
- `test_mode` — на этом этапе используется значение `false`.
- `ascii_tree` — параметр для этапа визуализации.

Ошибки выводятся в stderr. Успешный запуск возвращает код 0.
