"""Графический интерфейс эмулятора на Tkinter."""
import tkinter as tk

from commands import run_command
from parser import parse_line


class EmulatorWindow(tk.Tk):
    """Главное окно эмулятора."""

    def __init__(self, vfs_name, settings=None):
        super().__init__()
        self.vfs_name = vfs_name
        self.settings = settings or {}
        self.title(f"Эмулятор — {vfs_name}")
        self.geometry("700x450")

        self.output = tk.Text(self, state="disabled", bg="black", fg="white")
        self.output.pack(fill="both", expand=True)

        self.entry = tk.Entry(self)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

        self._print(f"Добро пожаловать в эмулятор VFS '{vfs_name}'. Введите команду.")

        script_path = self.settings.get("script")
        if script_path:
            self.after(300, lambda: self.run_script(script_path))

    def _print(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")

    def _execute_line(self, line):
        """Печатает строку ввода и результат её выполнения.

        Возвращает False, если после этой строки выполнение нужно
        остановить (например, была команда exit).
        """
        self._print(f"{self.vfs_name}> {line}")
        command, args = parse_line(line)
        if command is None:
            return True
        if command == "exit":
            self.destroy()
            return False
        self._print(run_command(command, args))
        return True

    def on_enter(self, event):
        line = self.entry.get()
        self.entry.delete(0, "end")
        self._execute_line(line)

    def run_script(self, path, delay_ms=700):
        """Читает стартовый скрипт и запускает его построчное выполнение.

        Строки-комментарии (#) пропускаются. Между командами делается
        небольшая пауза, чтобы визуально имитировать диалог с пользователем.
        """
        try:
            with open(path, encoding="utf-8") as script_file:
                lines = script_file.readlines()
        except OSError as error:
            self._print(f"Ошибка чтения стартового скрипта: {error}")
            return

        commands = [
            line.strip() for line in lines
            if line.strip() and not line.strip().startswith("#")
        ]
        self._play_script(commands, delay_ms)

    def _play_script(self, commands, delay_ms):
        """Выполняет команды списком по одной с задержкой между ними.

        Ошибка в одной строке не прерывает выполнение остальных.
        """
        if not commands:
            return
        line, rest = commands[0], commands[1:]
        try:
            should_continue = self._execute_line(line)
        except Exception as error:
            self._print(f"Ошибка в строке '{line}': {error}")
            should_continue = True
        if should_continue and rest:
            self.after(delay_ms, lambda: self._play_script(rest, delay_ms))