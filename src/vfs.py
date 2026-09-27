"""Загрузка виртуальной файловой системы (VFS) из ZIP-архива в память."""
import base64
import zipfile


class VfsError(Exception):
    """Ошибка загрузки или работы с VFS."""


def load_vfs(zip_path):
    """Читает ZIP-архив и строит дерево VFS в памяти.

    Возвращает вложенный словарь: ключ — имя папки/файла, значение —
    либо другой словарь (папка), либо строка с содержимым файла в
    base64 (файл). Сам ZIP-файл на диске не изменяется и не
    распаковывается физически.
    """
    tree = {}
    try:
        with zipfile.ZipFile(zip_path) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                content = archive.read(info.filename)
                encoded = base64.b64encode(content).decode("ascii")
                _insert_into_tree(tree, info.filename, encoded)
    except (OSError, zipfile.BadZipFile) as error:
        raise VfsError(f"Не удалось загрузить VFS из '{zip_path}': {error}")
    return tree


def _insert_into_tree(tree, path, encoded_content):
    """Вставляет файл в нужное место дерева по его пути внутри архива."""
    parts = path.split("/")
    node = tree
    for part in parts[:-1]:
        node = node.setdefault(part, {})
    node[parts[-1]] = encoded_content


def list_dir(tree, path_parts):
    """Возвращает список имён внутри папки по указанному пути (списком частей)."""
    node = tree
    for part in path_parts:
        if part not in node or not isinstance(node[part], dict):
            raise VfsError(f"Каталог не найден: {'/'.join(path_parts)}")
        node = node[part]
    return sorted(node.keys())