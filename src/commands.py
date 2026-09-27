"""Команды эмулятора, работающие с виртуальной файловой системой (VFS)."""
from datetime import datetime

from vfs import VfsError, get_node, resolve_path


def cmd_ls(args, ctx):
    """Выводит содержимое текущего каталога или каталога, указанного в аргументе."""
    target = args[0] if args else None
    path = resolve_path(ctx.cwd, target) if target else ctx.cwd
    node = get_node(ctx.vfs_tree, path)
    if not isinstance(node, dict):
        raise VfsError(f"'{'/'.join(path)}' не является каталогом")
    return "  ".join(sorted(node.keys())) or "(пусто)"


def cmd_cd(args, ctx):
    """Меняет текущий каталог внутри VFS."""
    if not args:
        raise VfsError("cd: не указан путь")
    new_path = resolve_path(ctx.cwd, args[0])
    node = get_node(ctx.vfs_tree, new_path)
    if not isinstance(node, dict):
        raise VfsError(f"'{args[0]}' не является каталогом")
    ctx.cwd[:] = new_path
    return "/" + "/".join(ctx.cwd)


def cmd_clear(args, ctx):
    """Очищает окно вывода."""
    ctx.clear_output()
    return ""


def cmd_tail(args, ctx):
    """Показывает последние строки файла (по умолчанию 10 строк)."""
    if not args:
        raise VfsError("tail: не указан файл")
    file_path = resolve_path(ctx.cwd, args[0])
    count = int(args[1]) if len(args) > 1 else 10
    content = ctx.read_file(file_path)
    lines = content.splitlines()
    return "\n".join(lines[-count:])


def cmd_who(args, ctx):
    """Показывает информацию о текущем сеансе эмулятора."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"user   emulator   {now}   vfs={ctx.vfs_name}"


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "clear": cmd_clear,
    "tail": cmd_tail,
    "who": cmd_who,
}


def run_command(command, args, ctx):
    """Выполняет команду по имени, возвращает текст результата.

    Ошибка внутри команды не прерывает работу эмулятора — она просто
    выводится как текст с описанием ошибки.
    """
    handler = COMMANDS.get(command)
    if handler is None:
        return f"Ошибка: неизвестная команда '{command}'"
    try:
        return handler(args, ctx)
    except VfsError as error:
        return f"Ошибка: {error}"