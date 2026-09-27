"""Точка входа: разбирает параметры запуска и запускает графический интерфейс."""
from config import parse_args, resolve_settings
from gui import EmulatorWindow

VFS_NAME = "myvfs"  # заглушка; станет реальным именем VFS на этапе 3


def main():
    args = parse_args()
    settings = resolve_settings(args)

    print("Параметры запуска эмулятора:")
    for key, value in settings.items():
        print(f"  {key}: {value}")

    app = EmulatorWindow(VFS_NAME, settings)
    app.mainloop()


if __name__ == "__main__":
    main()