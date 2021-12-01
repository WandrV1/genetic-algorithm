import math
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

from genetic.individual import Individual
from genetic.point import Point


class GeneticMaster:
    def __init__(self, population_size: int, crossover_count: int, selection_method: str,
                 mutation_type: str, generations_count: int, tour_size):
        # Параметр - размер популяции
        self.population_size = population_size
        # Параметр - кол-во пар участвующих в скрещивании
        # ! Кол-во пар должно быть не больше половины размера популяции
        self.crossover_count = crossover_count
        # Параметр - метод селекции ("tour" или "roulette")
        self.selection_method = selection_method
        # Параметр - тип мутации ( "weak" или "med" или "strong")
        self.mutation_type = mutation_type
        # Параметр - количество поколений
        self.generations_count = generations_count
        # Параметр - размер тура (имеет смысл только тогда когда selection_method == "tour")
        self.tour_size = tour_size
        
        self.points = []
        self.super_genome = []
        self.metrics = {"max": [], "min": [], "avg": []}

    def __individual_creator(self, points: list) -> Individual:
        """
        Создание индивида. Геном формируется случайным образом из списка переданных точек
        :param points: Список точек
        :return: Экземпляр класса Individual
        """
        local_points = points.copy()
        random.shuffle(local_points)
        return Individual(local_points)

    def population_creator(self, points: list) -> list:
        """
        Создание популяции
        :param points: Список точек для формирования генома
        :param population_size: Размер популяции
        :return: Список экземпляров класса Individual
        """
        return [self.__individual_creator(points) for __ in range(self.population_size)]

    def evaluate_population(self):
        """
        Оценка данной популяции
        ! Вызов данного метода обязателен перед проведением операции отбора кандидатов для скрещивания
        :param population: Популяция
        :return: Лучшая пригодность, худшая пригодность, средняя пригодность в популяции (абсолютные значения), лучший индивид
        """
        # Поиск значений функций пригодности
        population = self.population
        population.sort(key=lambda x: x.fitness)
        best_fitness = population[0].fitness
        worst_fitness = population[-1].fitness
        avg_fitness = np.mean([individual.fitness for individual in population])
        best_individual = copy.copy(population[0])
        # Обновление значений нормализованной пригодности
        # Устанавливаются значения относительные для текущей популяции
        for individual in population:
            individual.set_normalized_fitness(worst_fitness)
        # print(best_fitness)
        # print(worst_fitness)
        # print(avg_fitness)
        return best_fitness, worst_fitness, avg_fitness, best_individual

    def candidate_selection(self) -> list:
        """
        Селекция индивидов для скрещивания.
        :param population: Популяция
        :param crossover_count: Количество отбираемых пар
        :param method: Метод селекции "roulette" или "tour"
        :return: Список списков пар отобранных индивидов
        """

        def roulette(selecting_population: list, max_selecting_fitness: float) -> Individual:
            """
            Отбор индивида методом рулетки
            :param selecting_population: Популяция
            :param max_selecting_fitness: Сумма нормализованной пригодности популяции
            :return: Отобранный индивид
            """
            pick = random.uniform(0, max_selecting_fitness)
            current = 0
            for individual in selecting_population:
                current += individual.normalized_fitness
                if current > pick:
                    return individual

        def tour(selecting_population: list, selecting_tour_size: int) -> Individual:
            """
            Отбор индивида методом турнира
            :param selecting_population: Популяция
            :param selecting_tour_size: Размер турнира
            :return: Отобранный индивид
            """
            # Важно чтобы tour_size был меньше размера population
            tour_members = []
            # for _ in range(selecting_tour_size):
            #     potential_member = random.choice(selecting_population)
            #     while potential_member in tour_members:
            #         potential_member = random.choice(selecting_population)
            #     tour_members.append(potential_member)
            tour_indexes = random.sample(range(0, len(selecting_population) - 1), selecting_tour_size)
            for index in tour_indexes:
                tour_members.append(selecting_population[index])
            tour_members.sort(key=lambda x: x.normalized_fitness, reverse=True)
            return tour_members[0]

        population = self.population
        crossover_count = self.crossover_count
        method = self.selection_method
        selected_candidates = []
        if method == "roulette":
            max_fitness = sum(individual.normalized_fitness for individual in population)
            for _ in range(crossover_count):
                individual1 = roulette(population, max_fitness)
                individual2 = roulette(population, max_fitness)
                # while individual1 == individual2:
                #     individual2 = roulette(population, max_fitness)
                # print(individual1.fitness, individual1.normalized_fitness)
                # print(individual2.fitness, individual2.normalized_fitness)
                selected_candidates.append([individual1, individual2])
        elif method == "tour":
            tour_size = self.tour_size
            for _ in range(crossover_count):
                individual1 = tour(population, tour_size)
                individual2 = tour(population, tour_size)
                # while individual1 == individual2:
                #     individual2 = tour(population, tour_size)
                selected_candidates.append([individual1, individual2])
        else:
            raise Exception("Некорректный способ проведения селекции")
        return selected_candidates

    def crossover_candidates(self, candidates: list) -> list:
        """
        Одноточечное скрещивание индивидов
        ! Очень опасная функция, т.к. очень сложно отследить ее выполнение. (Надеюсь, что написал ее правильно)
        ! Запросто может положить все приложение
        :param candidates: Список возвращаемый методом candidate_selection()
        :return: Список новых созданных индивидов
        """
        # Список возвращаемых индивидов
        new_individuals = []
        for pair in candidates:
            # Родительские геномы
            parent1 = pair[0].genome
            parent2 = pair[1].genome
            child_genome1 = []
            child_genome2 = []
            # Выбор точки разбиения геномов случайным образом
            cut_point = random.randint(1, len(parent1) - 1)
            # print(cut_point)
            for i in range(len(parent1)):
                if i < cut_point:
                    child_genome1.append(parent1[i])
                    child_genome2.append(parent2[i])
                else:
                    if parent2[i] in child_genome1:
                        for j in range(i, len(parent1)):
                            if parent2[j] not in child_genome1:
                                child_genome1.append(parent2[j])
                                break
                    if len(child_genome1) < i + 1:
                        for j in range(len(parent1)):
                            if parent2[j] not in child_genome1:
                                child_genome1.append(parent2[j])
                                break
                    if parent1[i] in child_genome2:
                        for j in range(i, len(parent1)):
                            if parent1[j] not in child_genome2:
                                child_genome2.append(parent1[j])
                                break
                    if len(child_genome2) < i + 1:
                        for j in range(len(parent1)):
                            if parent1[j] not in child_genome2:
                                child_genome2.append(parent1[j])
                                break
            # print("Child 1")
            # for i in range(len(child_genome1)):
            #     print(child_genome1[i])
            # print("Child 2")
            # for i in range(len(child_genome2)):
            #     print(child_genome2[i])
            if len(child_genome1) != len(parent1) or len(child_genome2) != len(parent1):
                raise Exception("Ошибка при скрещивании")
            new_individuals.append(Individual(child_genome1))
            new_individuals.append(Individual(child_genome2))
        return new_individuals

    def mutation(self, population):
        """
        Мутация
        :param mutation_type: Тип мутации (вероятность, что ген мутирует)
        :param population: Популяция
        :return:
        """
        mutation_type = self.mutation_type
        if mutation_type == "strong":
            chance = 2 / len(population)
        elif mutation_type == "med":
            chance = 1 / len(population)
        else:  # mutation_type == "weak"
            chance = 0.5 / len(population)
        for individual in population:
            for i in range(len(individual.genome)):
                if random.random() <= chance:
                    j = random.randint(0, len(individual.genome) - 1)
                    while i == j:
                        j = random.randint(0, len(individual.genome) - 1)
                    individual.genome[i], individual.genome[j] = individual.genome[j], individual.genome[i]
                    individual.update_fitness()
                    # print("Got mutation")

    def run(self, ax=None):
        """
        Запуск генетического алгоритма
        :param canvas: FigureCanvasQTAgg для отображения графика
        :return:
        """
        self.population = self.population_creator(self.points)
        self.super_genome.clear()
        for value in self.metrics.values():
            value.clear()

        super_best = math.inf
        # super_individual = None
        super_genome = []
        for _ in range(self.generations_count):
            best, worst, average, ind = self.evaluate_population()
            # print(average)
            # print(f"best: {best}")
            self.metrics["max"].append(best)
            self.metrics["avg"].append(average)
            self.metrics["min"].append(worst)
            if best < super_best:
                super_best = best
                # super_individual = ind
                super_genome = [Point(point.x, point.y) for point in ind.genome]
            candidates = self.candidate_selection()
            legacy = self.crossover_candidates(candidates)
            self.population.sort(key=lambda x: x.fitness)
            self.population = self.population[:-self.crossover_count*2]
            self.mutation(legacy)
            self.population += legacy

        
        # Построение графика
        if (ax):
            generations = list(range(1, self.generations_count+1))
            ax.plot(generations, self.metrics["avg"], label="avg")
            ax.plot(generations, self.metrics["min"], label="min")
            ax.plot(generations, self.metrics["max"], label="max")
            ax.set_xlabel("Поколение")
            ax.set_ylabel("Пригодность (меньше - лучше)")
            ax.set_title("Обучение генетического алгоритма")
            ax.legend(loc=2)
        
        # self.super_genome = super_individual.genome
        self.super_genome = super_genome

        return super_best, Individual(super_genome)

    def clear(self):
        self.points.clear()
        self.super_genome.clear()
