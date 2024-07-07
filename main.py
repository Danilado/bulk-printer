from pathlib import Path
import os
import platform
from modules.FsScanner import FsScanner
from modules.Printer import Printer


class App:
    def __init__(self) -> None:
        self.scanner = FsScanner()
        self.printer = Printer()
        self.running: bool = False

        self.menu_items = {
            1: ("Add target file extensions", self.add_target_types),
            2: ("Add forbidden prefixes", self.add_forbidden_prefixes),
            3: ("Add forbidden suffixes", self.add_forbidden_suffixes),
            4: ("Add target folders", self.add_target_folders),
            5: ("Scan target folders for matching files", self.scan),
            6: ("Remove files from list by index", self.remove_by_indexes),
            7: ("Print files in list", self.print_all),
            0: ("Exit", self.stop)
        }

        self.target_folders: list[Path] = []
        self.targets: list[Path] = []

    def add_target_types(self) -> None:
        print(f"Input file extensions to print (separated with spacebar)")
        data = input("> ").strip().split()

        if len(data) == 0:
            return

        for type in data:
            if not type.startswith("."):
                type = "." + type

            self.scanner.add_target_type(type)

    def add_forbidden_prefixes(self) -> None:
        print(f"Input prefixes (separated with spacebar)")
        print(f"Files and folders starting with prefix will be ignored")
        data = input("> ").strip().split()

        for prefix in data:
            self.scanner.add_forbidden_prefix(prefix)

    def add_forbidden_suffixes(self) -> None:
        print(f"Input suffixes (separated with spacebar)")
        print(f"Files and folders ending with suffix will be ignored")
        data = input("> ").strip().split()

        for suffix in data:
            self.scanner.add_forbidden_suffix(suffix)

    def add_target_folders(self) -> None:
        print(f"Input folder names to scan")
        data = input("> ").strip().split()

        for folder in data:
            fpath = Path(folder).resolve()
            if not fpath.exists():
                print(f"Folder {fpath} not found")
                continue
            if not fpath.is_dir():
                print(f"{fpath} is not a folder")
                continue
            if fpath in self.target_folders:
                print(f"{fpath} already in list")
                continue

            self.target_folders.append(fpath)

    def scan(self) -> None:
        if len(self.target_folders) == 0:
            print(f"No folders to scan")
            return

        for folder in self.target_folders:
            res = self.scanner.scan_dir(folder)
            print(f"{folder} - {len(res)} matching files")

            for file in res:
                if file in self.targets:
                    print(f"{file} already in list")
                else:
                    self.targets.append(file)

        self.target_folders = []

    def list_targets(self) -> None:
        for i, file in enumerate(self.targets):
            print(f"{i+1}: {file.resolve()}")
        print()

    def remove_by_indexes(self) -> None:
        if len(self.targets) == 0:
            print(f"List already empty")
            return

        self.list_targets()
        data = input(
            "Input indexes of files to remove from list\n> ").strip().split()

        rmlist: list[int] = []
        for entry in data:
            try:
                n = int(entry)
                if n > 0 and n <= len(self.targets) and n - 1 not in rmlist:
                    rmlist.append(n - 1)
            except ValueError:
                continue

        rmlist = sorted(rmlist)[::-1]

        for index in rmlist:
            self.targets.pop(index)

    def print_all(self) -> None:
        for target in self.targets:
            try:
                self.printer.print(target)
            except:
                print(f"Could not print {target}")

        self.targets = []

    def print_menu(self) -> None:
        for key in self.menu_items.keys():
            print(f"{key}:\t{self.menu_items[key][0]}")

    def print_status(self) -> None:
        print(f"Target file extensions:")
        if len(self.scanner.target_types) == 0:
            print("\tAny")
        else:
            for text in self.scanner.target_types:
                print(f"\t{text}")

        print(f"Forbidden prefixes:")
        if len(self.scanner.forbidden_prefixes) == 0:
            print("\tNone")
        else:
            for text in self.scanner.forbidden_prefixes:
                print(f"\t{text}")

        print(f"Forbidden suffixes:")
        if len(self.scanner.forbidden_suffixes) == 0:
            print("\tNone")
        else:
            for text in self.scanner.forbidden_suffixes:
                print(f"\t{text}")

        print(f"Target folders:")
        if len(self.target_folders) == 0:
            print("\tNone")
        else:
            for folder in self.target_folders:
                print(f"\t{folder.resolve()}")

        print(f"Target files:")
        if len(self.targets) == 0:
            print("\tNone")
        else:
            for file in self.targets:
                print(f"\t{file.resolve()}")
        print()

    def menu(self) -> None:
        self.print_status()
        self.print_menu()

        try:
            option = int(input("> "))
        except ValueError:
            option = None

        if option not in self.menu_items.keys():
            return

        os.system("cls")
        self.menu_items[option][1]()

    def run(self) -> int:
        self.running = True

        while self.running:
            self.menu()

        return 0

    def stop(self) -> None:
        self.running = False


def main():
    if platform.system() != "Windows":
        print("This application only works on Windows")

    app = App()
    return app.run()


if __name__ == "__main__":
    main()
