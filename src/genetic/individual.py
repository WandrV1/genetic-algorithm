class Individual:
    def __init__(self, genome: list):
        self.genome = genome
        self.fitness = self.__fitness()
        self.normalized_fitness = -1

    def __fitness(self) -> float:
        """
        Функция пригодности
        :return: Значение функции пригодности (меньше - лучше)
        """
        curr_fitness = 0
        for i in range(len(self.genome)):
            if i == len(self.genome) - 1:
                curr_fitness += self.genome[i].distance(self.genome[0])
            else:
                curr_fitness += self.genome[i].distance(self.genome[i + 1])
        return curr_fitness

    def update_fitness(self):
        # print("Update fitness")
        curr_fitness = 0
        for i in range(len(self.genome)):
            if i == len(self.genome) - 1:
                curr_fitness += self.genome[i].distance(self.genome[0])
            else:
                curr_fitness += self.genome[i].distance(self.genome[i + 1])
        self.fitness = curr_fitness

    def set_normalized_fitness(self, min_fitness: float):
        """
        Нормализовать значения функции пригодности
        :param min_fitness: Значение худшей пригодности в текущем поколении
        :return:
        """
        self.normalized_fitness = -1 * self.fitness + min_fitness

    def __eq__(self, other):
        """
        Метод equals
        :param other: Другой индивид
        :return: True если индивиды равны и False в любом другом случае
        """
        if not isinstance(other, Individual):
            return False
        if len(self.genome) != len(other.genome):
            return False
        for i in range(len(self.genome)):
            if self.genome[i] != other.genome[i]:
                return False
        return True
