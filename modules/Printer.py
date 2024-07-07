from pathlib import Path
import os


class Printer:
    def __init__(self):
        pass

    def print(self, target: Path):
        os.startfile(target, "print")
