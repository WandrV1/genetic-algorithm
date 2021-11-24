"""
Модуль отвечают за реализацию графического интерфейса программы.
"""

import sys

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import gui
from gui import main_window
from gui import widgets_design_override
from genetic.genetic_master import GeneticMaster
from genetic.point import Point


class MainWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, genetic_master):
        super().__init__()
        self.setupUi(self)

        self.setup_canvas()

        self.genetic_master = genetic_master
        self.graphLabel.genetic_master = genetic_master

        max_population_size = 10000
        self.populationSizeLineEdit.setText(str(self.genetic_master.population_size))
        self.populationSizeLineEdit.textEdited.connect(self.update_population_size)
        self.populationSizeLineEdit.setValidator(QIntValidator(1, max_population_size))

        self.crossover_count_validator = QIntValidator(1, genetic_master.population_size * .5)
        self.crossoverCountLineEdit.setText(str(self.genetic_master.crossover_count))
        self.crossoverCountLineEdit.textEdited.connect(self.update_crossover_count)
        self.crossoverCountLineEdit.setValidator(self.crossover_count_validator)
        
        max_generations_count = 10000
        self.generationsCountLineEdit.setText(str(self.genetic_master.generations_count))
        self.generationsCountLineEdit.textEdited.connect(self.update_generations_count)
        self.generationsCountLineEdit.setValidator(QIntValidator(1, max_generations_count))

        max_tour_size = 10000
        self.tourSizeLineEdit.setText(str(self.genetic_master.tour_size))
        self.tourSizeLineEdit.textEdited.connect(self.update_tour_size)
        self.tourSizeLineEdit.setValidator(QIntValidator(1, max_tour_size))

        self.selectionMethodCombo.currentTextChanged.connect(self.update_selection_method)
        self.mutationTypeCombo.currentTextChanged.connect(self.update_mutation_type)

        self.runButton.clicked.connect(self.run_algorithm)
        self.clearButton.clicked.connect(self.clear_points)


    def contextMenu(self, event):
        """
        Контекстное меню
        """
        menu = QMenu()
        if self.galleryList.itemAt(event):
            openAction = QAction("Открыть", menu)
            copyAction = QAction("Копировать", menu)
            favAction = QAction("Добавить/удалить из избранных", menu)
            deleteAction = QAction("Удалить", menu)
            openAction.triggered.connect(self.show_selected_meme)
            copyAction.triggered.connect(self.copy_selected_meme_to_clip)
            favAction.triggered.connect(self.toggle_selected_meme_fav)
            deleteAction.triggered.connect(self.delete_selected_meme)

            menu.addAction(openAction)
            menu.addAction(copyAction)
            menu.addAction(favAction)
            menu.addAction(deleteAction)
        else:
            pass
        menu.exec(self.galleryList.mapToGlobal(event))

    def message(self, message: str, error: bool = False):
        """
        Метод показывает сообщение в статусбаре окна и выводит его в консоль.
        Принимает:
            message – текст сообщения, str;
            error – необхоимость вызова отдельного диалогового окна, bool.
        """

        print(message)
        self.statusbar.showMessage(message)
        if error:
            pass

    def setup_canvas(self):
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.plotGroup.layout().addWidget(self.canvas)

    def update_population_size(self, value):
        population_size = int(value) if value else 0
        self.genetic_master.population_size = population_size

        max_crossover_count = population_size * .5
        self.crossover_count_validator.setTop(max_crossover_count)

    def update_crossover_count(self, value):
        crossover_count = int(value) if value else 0
        self.genetic_master.crossover_count = crossover_count
    
    def update_max_crossover_count(self, max_crossover_count):
        crossover_count = int(self.crossoverCountLineEdit.text())
        crossover_count = int(max(crossover_count, max_crossover_count))
        self.genetic_master.crossover_count = crossover_count
        self.crossoverCountLineEdit.setText(str(crossover_count))

    def update_generations_count(self, value):
        self.genetic_master.generations_count = int(value) if value else 0

    def update_selection_method(self, value):
        self.genetic_master.selection_method = value
        self.tourSize.setHidden(value != "tour")

    def update_tour_size(self, value):
        self.genetic_master.tour_size = int(value) if value else 0
    
    def update_mutation_type(self, value):
        self.genetic_master.mutation_type = value

    def run_algorithm(self):
        MIN_POINTS = 3
        if len(self.genetic_master.points) < MIN_POINTS:
            self.message("Требуется задать более двухточек!", True)
            return

        super_best, super_individual = self.genetic_master.run(self.figure)
        self.canvas.draw()
        print(f"Лучший индивид: {super_best}")
        self.graphLabel.update_graph()

    def clear_points(self):
        self.genetic_master.clear()
        self.graphLabel.update_graph()


class GUI:
    def __init__(self, genetic_master):
        self.genetic_master = genetic_master

    def engage(self):
        app = QApplication(sys.argv)
        form = MainWindow(self.genetic_master)
        form.show()
        app.exec()
