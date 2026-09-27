"""Чтение параметров запуска: командная строка и XML-конфигурационный файл."""
import argparse
import xml.etree.ElementTree as ET


def parse_args():
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(description="GUI-эмулятор командной строки")
    parser.add_argument("--vfs", help="путь к физическому расположению VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    parser.add_argument("--config", help="путь к XML-конфигурационному файлу")
    return parser.parse_args()


def parse_config_file(path):
    """Читает XML-конфигурационный файл и возвращает словарь параметров."""
    tree = ET.parse(path)
    root = tree.getroot()
    result = {}

    vfs_elem = root.find("vfs")
    if vfs_elem is not None and vfs_elem.text:
        result["vfs"] = vfs_elem.text.strip()

    script_elem = root.find("script")
    if script_elem is not None and script_elem.text:
        result["script"] = script_elem.text.strip()

    return result


def resolve_settings(args):
    """Объединяет параметры CLI и конфиг-файла.

    Значения из конфигурационного файла имеют приоритет над
    значениями из командной строки.
    """
    settings = {"vfs": args.vfs, "script": args.script}

    if args.config:
        settings.update(parse_config_file(args.config))

    return settings