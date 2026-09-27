"""Графический интерфейс эмулятора на Tkinter."""
import tkinter as tk

from commands import run_command
from parser import parse_line


class EmulatorWindow(tk.Tk):
    """Главное окно эмулятора."""

    def __init__(self, vfs_name):
        super().__init__()
        self.vfs_name = vfs_name
        self.title(f"Эмулятор — {vfs_name}")
        self.geometry("700x450")

        self.output = tk.Text(self, state="disabled", bg="black", fg="white")
        self.output.pack(fill="both", expand=True)

        self.entry = tk.Entry(self)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

        self._print(f"Добро пожаловать в эмулятор VFS '{vfs_name}'. Введите команду.")

    def _print(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")

    def on_enter(self, event):
        line = self.entry.get()
        self.entry.delete(0, "end")
        self._print(f"{self.vfs_name}> {line}")

        command, args = parse_line(line)
        if command is None:
            return
        if command == "exit":
            self.destroy()
            return

        result = run_command(command, args)
        self._print(result)