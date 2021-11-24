"""
Модуль нужен исключительно для удобства разработки
и подлежит удалению после релиза.

Заменяет классы Qt в файлах окон на классы из widgets_design_override.
"""

def main():
    replacements = {
        "main_window.py": {
            "self.graphLabel = QtWidgets.QLabel(self.graphGroup)":
            "self.graphLabel = GraphWidget(self.graphGroup)"
        }
    }

    add_import = """from PyQt5 import QtCore, QtGui, QtWidgets

from gui.widgets_design_override import *"""
    
    for filename, pairs in replacements.items():
        content = ""

        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            print(f"Открыли {filename}, размер: {len(content)}")
            file.close()

        if not content:
            print("Не удалось заменить содержимое файла.")
            return

        content = content.replace(
            """from PyQt5 import QtCore, QtGui, QtWidgets""",
            add_import)
    
        for from_str, to_str in pairs.items():
            print(f"Пытаемся заменить {from_str} на {to_str}")
            content = content.replace(from_str, to_str)

        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
            file.close()

if __name__ == "__main__":
    main()