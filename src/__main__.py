import sys

from gui import graphical_interface
from genetic.genetic_master import GeneticMaster

def main():
    POPULATION_SIZE = 200
    SELECTION_METHOD = "tour"
    CROSSOVER_COUNT = 10
    GENERATIONS_COUNT = 1000
    MUTATION_TYPE = "med"
    TOUR_SIZE = 5

    genetic_master = GeneticMaster(
        POPULATION_SIZE, CROSSOVER_COUNT, SELECTION_METHOD, MUTATION_TYPE, GENERATIONS_COUNT, TOUR_SIZE
    )

    gui = graphical_interface.GUI(genetic_master)
    gui.engage()

    return 0

if __name__ == "__main__":
    sys.exit(main())
