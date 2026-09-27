"""Генерирует тестовые VFS-архивы (ZIP) для проверки этапа 3.

Архивы создаются локально при запуске и не хранятся в репозитории —
задание запрещает коммитить архивы и бинарные файлы.
"""
import zipfile
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "generated_vfs"


def make_minimal_vfs():
    """Создаёт минимальную VFS: один файл в корне."""
    path = OUTPUT_DIR / "minimal.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("readme.txt", "Минимальная VFS для тестов.")
    return path


def make_multi_file_vfs():
    """Создаёт VFS с несколькими файлами на одном уровне."""
    path = OUTPUT_DIR / "multi_file.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("notes.txt", "Заметка 1")
        archive.writestr("todo.txt", "Заметка 2")
        archive.writestr("data.bin", b"\x00\x01\x02\x03")
    return path


def make_deep_vfs():
    """Создаёт VFS с вложенностью от 3 уровней папок."""
    path = OUTPUT_DIR / "deep.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("level1/level2/level3/deep_file.txt", "Файл на 3 уровне")
        archive.writestr("level1/top_file.txt", "Файл на 1 уровне")
        archive.writestr("level1/level2/mid_file.txt", "Файл на 2 уровне")
    return path


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    make_minimal_vfs()
    make_multi_file_vfs()
    make_deep_vfs()
    print(f"Тестовые VFS созданы в {OUTPUT_DIR}")


if __name__ == "__main__":
    main()