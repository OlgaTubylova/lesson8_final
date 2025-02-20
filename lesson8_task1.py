# Напишите функцию, которая получает на вход директорию и рекурсивно обходит её и все вложенные директории. Результаты обхода сохраните в файлы json, csv и pickle.
# ○ Для дочерних объектов указывайте родительскую директорию.
# ○ Для каждого объекта укажите файл это или директория.
# ○ Для файлов сохраните его размер в байтах, а для директорий размер файлов в ней с учётом всех вложенных файлов и директорий.

import os
import json
import csv
import pickle
import shutil
from pathlib import Path

def scan_directory(directory: str):
    """
    Обходит директорию рекурсивно и сохраняет результаты в json, csv и pickle.

    :param directory: Путь к директории для сканирования.
    """
    results = []
    dir_sizes = {}

    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        parent_dir = str(root_path.parent) if root_path != Path(directory) else ""

        # Обработка директорий
        for d in dirs:
            dir_path = root_path / d
            dir_sizes[str(dir_path)] = 0  # Запоминаем, чтобы позже обновить размер

        # Обработка файлов
        for f in files:
            file_path = root_path / f
            try:
                size = file_path.stat().st_size
            except (PermissionError, FileNotFoundError):
                size = 0  # Если нет доступа, считаем размер 0

            results.append({
                "name": f,
                "path": str(file_path),
                "parent": parent_dir,
                "type": "file",
                "size_bytes": size
            })

            # Учитываем размер файла в родительской директории
            dir_sizes[str(root_path)] = dir_sizes.get(str(root_path), 0) + size

    # Добавляем директории с их вычисленным размером
    for dir_path, size in dir_sizes.items():
        results.append({
            "name": Path(dir_path).name,
            "path": dir_path,
            "parent": str(Path(dir_path).parent) if Path(dir_path).parent != Path(directory) else "",
            "type": "directory",
            "size_bytes": size
        })

    # Сохранение в JSON
    with open('directory_structure.json', 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)

    # Сохранение в CSV
    with open('directory_structure.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["name", "path", "parent", "type", "size_bytes"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Сохранение в Pickle
    with open('directory_structure.pkl', 'wb') as pickle_file:
        pickle.dump(results, pickle_file)

    print("Файлы directory_structure.json, directory_structure.csv и directory_structure.pkl успешно сохранены.")


# Пример использования
# scan_directory("C:/Users")  # Сканируем директорию C:/Users
# scan_directory(".")  # Сканируем текущую директорию