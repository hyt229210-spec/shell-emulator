"""Точка входа: запускает графический интерфейс эмулятора."""
from gui import EmulatorWindow

VFS_NAME = "myvfs"  # заглушка; в этапе 2 будет браться из параметров запуска


def main():
    app = EmulatorWindow(VFS_NAME)
    app.mainloop()


if __name__ == "__main__":
    main()