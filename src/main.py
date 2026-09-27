"""Точка входа: разбирает параметры запуска и запускает графический интерфейс."""
from config import parse_args, resolve_settings
from gui import EmulatorWindow


def main():
    args = parse_args()
    settings = resolve_settings(args)

    print("Параметры запуска эмулятора:")
    for key, value in settings.items():
        print(f"  {key}: {value}")

    app = EmulatorWindow(settings)
    app.mainloop()


if __name__ == "__main__":
    main()