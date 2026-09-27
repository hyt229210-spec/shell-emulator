"""Команды эмулятора. На этом этапе ls и cd — заглушки."""


def cmd_ls(args):
    return f"ls {' '.join(args)}"


def cmd_cd(args):
    return f"cd {' '.join(args)}"


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
}


def run_command(command, args):
    """Выполняет команду по имени, возвращает текст результата.

    Неизвестная команда обрабатывается как ошибка.
    """
    handler = COMMANDS.get(command)
    if handler is None:
        return f"Ошибка: неизвестная команда '{command}'"
    return handler(args)