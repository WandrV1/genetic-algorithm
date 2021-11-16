# TODO список точек должен задаваться при взаимодействии пользователя с UI
# TODO добавить функционал сохранения и загрузки списка точек и параметров модели
# import random
# import copy
# import math
# import numpy as np
# import matplotlib.pyplot as plt
#
from point import Point
# from individual import Individual
from genetic_master import GeneticMaster
#
# def individual_creator(points: list) -> Individual:
#     """
#     Создание индивида. Геном формируется случайным образом из списка переданных точек
#     :param points: Список точек
#     :return: Экземпляр класса Individual
#     """
#     local_points = points.copy()
#     random.shuffle(local_points)
#     return Individual(local_points)
#
#
# def population_creator(points: list, population_size: int) -> list:
#     """
#     Создание популяции
#     :param points: Список точек для формирования генома
#     :param population_size: Размер популяции
#     :return: Список экземпляров класса Individual
#     """
#     return [individual_creator(points) for i in range(population_size)]
#
#
# def evaluate_population(population: list):
#     """
#     Оценка данной популяции
#     ! Вызов данного метода обязателен перед проведением операции отбора кандидатов для скрещивания
#     :param population: Популяция
#     :return: Лучшая пригодность, худшая пригодность, средняя пригодность в популяции
#     (абсолютные значения), лучший индивид
#     """
#     # Поиск значений функций пригодности
#     population.sort(key=lambda x: x.fitness)
#     best_fitness = population[0].fitness
#     worst_fitness = population[-1].fitness
#     avg_fitness = np.mean([individual.fitness for individual in population])
#     best_individual = copy.copy(population[0])
#     # Обновление значений нормализованной пригодности
#     # Устанавливаются значения относительные для текущей популяции
#     for individual in population:
#         individual.set_normalized_fitness(worst_fitness)
#     # print(best_fitness)
#     # print(worst_fitness)
#     # print(avg_fitness)
#     return best_fitness, worst_fitness, avg_fitness, best_individual
#
#
# def candidate_selection(population: list, crossover_count: int, method: str) -> list:
#     """
#     Селекция индивидов для скрещивания.
#     :param population: Популяция
#     :param crossover_count: Количество отбираемых пар
#     :param method: Метод селекции "roulette" или "tour"
#     :return: Список списков пар отобранных индивидов
#     """
#
#     def roulette(selecting_population: list, max_selecting_fitness: float) -> Individual:
#         """
#         Отбор индивида методом рулетки
#         :param selecting_population: Популяция
#         :param max_selecting_fitness: Сумма нормализованной пригодности популяции
#         :return: Отобранный индивид
#         """
#         pick = random.uniform(0, max_selecting_fitness)
#         current = 0
#         for individual in selecting_population:
#             current += individual.normalized_fitness
#             if current > pick:
#                 return individual
#
#     def tour(selecting_population: list, selecting_tour_size: int) -> Individual:
#         """
#         Отбор индивида методом турнира
#         :param selecting_population: Популяция
#         :param selecting_tour_size: Размер турнира
#         :return: Отобранный индивид
#         """
#         # Важно чтобы tour_size был меньше размера population
#         tour_members = []
#         for _ in range(selecting_tour_size):
#             potential_member = random.choice(selecting_population)
#             while potential_member in tour_members:
#                 potential_member = random.choice(selecting_population)
#             tour_members.append(potential_member)
#         tour_members.sort(key=lambda x: x.normalized_fitness, reverse=True)
#         return tour_members[0]
#
#     selected_candidates = []
#     if method == "roulette":
#         max_fitness = sum(individual.normalized_fitness for individual in population)
#         for _ in range(crossover_count):
#             individual1 = roulette(population, max_fitness)
#             individual2 = roulette(population, max_fitness)
#             while individual1 == individual2:
#                 individual2 = roulette(population, max_fitness)
#             # print(individual1.fitness, individual1.normalized_fitness)
#             # print(individual2.fitness, individual2.normalized_fitness)
#             selected_candidates.append([individual1, individual2])
#     elif method == "tour":
#         tour_size = 2
#         for _ in range(crossover_count):
#             individual1 = tour(population, tour_size)
#             individual2 = tour(population, tour_size)
#             while individual1 == individual2:
#                 individual2 = tour(population, tour_size)
#             selected_candidates.append([individual1, individual2])
#     else:
#         raise Exception("Некорректный способ проведения селекции")
#     return selected_candidates
#
#
# def crossover_candidates(candidates: list) -> list:
#     """
#     Одноточечное скрещивание индивидов
#     ! Очень опасная функция, т.к. очень сложно отследить ее выполнение. (Надеюсь, что написал ее правильно)
#     ! Запросто может положить все приложение
#     :param candidates: Список возвращаемый методом candidate_selection()
#     :return: Список новых созданных индивидов
#     """
#     # Список возвращаемых индивидов
#     new_individuals = []
#     for pair in candidates:
#         # Родительские геномы
#         parent1 = pair[0].genome
#         parent2 = pair[1].genome
#         child_genome1 = []
#         child_genome2 = []
#         # Выбор точки разбиения геномов случайным образом
#         cut_point = random.randint(1, len(parent1) - 1)
#         # print(cut_point)
#         for i in range(len(parent1)):
#             if i < cut_point:
#                 child_genome1.append(parent1[i])
#                 child_genome2.append(parent2[i])
#             else:
#                 if parent2[i] in child_genome1:
#                     for j in range(i, len(parent1)):
#                         if parent2[j] not in child_genome1:
#                             child_genome1.append(parent2[j])
#                             break
#                 if len(child_genome1) < i+1:
#                     for j in range(len(parent1)):
#                         if parent2[j] not in child_genome1:
#                             child_genome1.append(parent2[j])
#                             break
#                 if parent1[i] in child_genome2:
#                     for j in range(i, len(parent1)):
#                         if parent1[j] not in child_genome2:
#                             child_genome2.append(parent1[j])
#                             break
#                 if len(child_genome2) < i+1:
#                     for j in range(len(parent1)):
#                         if parent1[j] not in child_genome2:
#                             child_genome2.append(parent1[j])
#                             break
#         # print("Child 1")
#         # for i in range(len(child_genome1)):
#         #     print(child_genome1[i])
#         # print("Child 2")
#         # for i in range(len(child_genome2)):
#         #     print(child_genome2[i])
#         if len(child_genome1) != len(parent1) or len(child_genome2) != len(parent1):
#             raise Exception("Ошибка при скрещивании")
#         new_individuals.append(Individual(child_genome1))
#         new_individuals.append(Individual(child_genome2))
#     return new_individuals
#
#
# def mutation(population: list, mutation_type: str):
#     if mutation_type == "strong":
#         chance = 2/len(population)
#     elif mutation_type == "med":
#         chance = 1/len(population)
#     else:  # mutation_type == "weak"
#         chance = 0.5/len(population)
#     for individual in population:
#         for i in range(len(individual.genome)):
#             if random.random() <= chance:
#                 j = random.randint(0, len(individual.genome)-1)
#                 while i == j:
#                     j = random.randint(0, len(individual.genome) - 1)
#                 individual.genome[i], individual.genome[j] = individual.genome[j], individual.genome[i]
#                 # print("Got mutation")

# Параметры ГА
# TODO параметры должны передаваться из UI
# Размер популяции
POPULATION_SIZE = 200
# Метод выбора кандидатов для скрещивания (roulette или tour)
SELECTION_METHOD = "tour"
# Кол-во пар участвующих в скрещивании
CROSSOVER_COUNT = 10
# Кол-во поколений
GENERATIONS_COUNT = 1000
# Тип мутации
MUTATION_TYPE = "med"
# Размер тура (если метод выбора кандидатов tour)
TOUR_SIZE = 5


def main():
    # Генерация списка точек для построения и отладки работы генетического алгоритма
    points_list = [Point(81, 14), Point(3, 94), Point(35, 31), Point(28, 17), Point(94, 13), Point(86, 94),
                   Point(69, 11), Point(75, 54), Point(4, 3), Point(11, 27)]

    # metrics = {"max": [], "min": [], "avg": []}
    # my_population = population_creator(points_list, POPULATION_SIZE)
    # super_best = math.inf
    # super_ind = None
    # for _ in range(GENERATIONS_COUNT):
    #     best, worst, average, ind = evaluate_population(my_population)
    #     print(average)
    #     print(f"best: {best}")
    #     metrics["max"].append(best)
    #     metrics["avg"].append(average)
    #     metrics["min"].append(worst)
    #     if best < super_best:
    #         super_best = best
    #         super_ind = ind
    #     candidates = candidate_selection(my_population, CROSSOVER_COUNT, SELECTION_METHOD)
    #     new_candidates = crossover_candidates(candidates)
    #     my_population.sort(key=lambda x: x.fitness)
    #     my_population = my_population[:-CROSSOVER_COUNT*2]
    #     my_population += new_candidates
    #     mutation(my_population, MUTATION_TYPE)
    # generations = list(range(1, GENERATIONS_COUNT + 1))
    # plt.plot(generations, metrics["avg"], label="avg")
    # plt.plot(generations, metrics["min"], label="min")
    # plt.plot(generations, metrics["max"], label="max")
    # plt.xlabel("Поколение")
    # plt.ylabel("Пригодность (меньше - лучше)")
    # plt.title("Обучение генетического алгоритма")
    # plt.legend(loc=2)
    # plt.show()
    # print(super_best)

    test_master = GeneticMaster(points_list, POPULATION_SIZE, CROSSOVER_COUNT,
                                SELECTION_METHOD, MUTATION_TYPE, GENERATIONS_COUNT, TOUR_SIZE)
    test_master.run()


if __name__ == "__main__":
    main()
