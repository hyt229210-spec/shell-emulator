"""Разбор пользовательского ввода на команду и аргументы."""
import os


def parse_line(line):
    """Разбивает строку на команду и список аргументов.

    Поддерживает раскрытие переменных окружения реальной ОС,
    например $HOME превращается в путь к домашней папке пользователя.
    """
    expanded = os.path.expandvars(line)
    parts = expanded.split()
    if not parts:
        return None, []
    command, *args = parts
    return command, args