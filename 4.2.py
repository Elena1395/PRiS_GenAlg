# Вариант 24
# 1.1 случайная генерация
# 2.1 выбор каждой особи пропорционально приспособленности (рулетка)
# 3.1 многоточечный с 3мя точками
# 4.3 добавление 1 случайной вещи 5% особей
# 5.3 замена своих родителей
import random


populationSize = 200
maxGenerations = 500
itemsCount = 30
percentForMutation = 0.05

with open("24.txt") as file:
    array = [row.strip() for row in file]
#print(array)

maxWeight = float(array[0].split(' ')[0])
maxSize = float(array[0].split(' ')[1])
print("maxWeight = ", maxWeight, "maxSize =", maxSize)

data = [0] * (len(array) - 1)
for i in range(1, len(array)):
    data[i - 1] = tuple(float(item) for item in array[i].split(' '))
print("items = ", data)

cheapestValue = data[0][2]
# стоимость самой дешевой вещи
for i in range(len(data)):
    if (data[i][2] < cheapestValue):
        cheapestValue = data[i][2]
print("cheapestValue = ", cheapestValue)


# Вывод разультата
selectedItems = []
def WeightSizeValue(vector, items):
    selectedItems = []
    #print("vector = ", vector)
    weight = 0
    size = 0
    value = 0
    for i in range(0, len(vector)):
        if vector[i] != 0:
            weight += items[i][0]
            size += items[i][1]
            value += items[i][2]
            selectedItems.append(items[i])
    print("Вес = ", weight, "Объем = ", size, "Ценность = ", value)
    print("Выбранные элементы = ", selectedItems)


def GetRandomVector():
    vector = [random.randint(0, 1) for x in range(0, itemsCount)]
    while not (checkWeightSize(vector)):
        vector = [random.randint(0, 1) for x in range(0, itemsCount)]
    return vector


def checkWeightSize(vector):
    weight = 0
    size = 0
    for i in range(0, itemsCount):
        if vector[i] != 0:
            weight += data[i][0]
            size += data[i][1]
    if (weight > maxWeight or size > maxSize):
        return False
    else: return True


def InitialPopulation():
    population = [GetRandomVector() for x in range(0, populationSize)]
    return population

# Ценность всех предметов в векторе предметов
def GetValue(vector):
    value = 0
    for i in range(0, len(vector)):
        if vector[i] != 0:
            value += data[i][2]
    return value

# добавление 1 случайной вещи у вектора
def Mutate(individual):
    item_num = random.randint(0, len(individual) - 1)
    while individual[item_num] != 0:
        item_num = random.randint(0, len(individual) - 1)
    individual[item_num] = 1
    return individual

# отбрасываем всех кто не проходит по весу и объему
def Filter(population):
    filtered_population = list(filter(lambda x: checkWeightSize(x), population))
    return filtered_population

def Sort(population):
    population.sort(key=lambda x: x[itemsCount], reverse=True)

# Трехточечное скрещивание
def GetTwoChildren(first_parent, second_parent):
    point1 = random.randint(0, itemsCount/3)
    point2 = random.randint(point1, itemsCount/3 * 2)
    point3 = random.randint(point2, itemsCount)
    # point1 = random.randint (0, itemsCount)
    # point2 = random.randint (point1, itemsCount)
    # point3 = random.randint (point2, itemsCount)
    # print("points = ", point1, point2, point3)

    child1 = first_parent[0:point1] + second_parent[point1:point2] + first_parent[point2:point3] + second_parent[point3:]
    child2 = second_parent[0:point1] + first_parent[point1:point2] + second_parent[point2:point3] + first_parent[point3:]

    # print ("first_parent[0:point1]", first_parent[0:point1])
    # print ("second_parent [point1:point2]", second_parent [point1:point2])
    # print ("first_parent [point2:point3]", first_parent [point2:point3])
    # print ("second_parent [point3:]", second_parent [point3:])
    #
    # print ("second_parent[0:point1]", second_parent[0:point1])
    # print("first_parent [point1:point2]", first_parent [point1:point2])
    # print ("second_parent [point2:point3]", second_parent [point2:point3])
    # print ("first_parent [point3:]", first_parent [point3:])
    #
    # print("first_parent", first_parent)
    # print ("second_parent", second_parent)
    # print ("child1", child1)
    # print("child2", child2)
    return child1, child2

# Возвращается список всех фитнесов в данной популяции
def GetFitnesses(population):
    fitnesses = []
    for i in range(len(population)):
        fitnesses.append(GetValue(population[i]))
    return fitnesses

# Выбор колеса рулетки. Т.к. особь скрещивается 1 раз за поколение, если мы ее выбрали, то должны ее удалить,
# пересчитать интервалы для колеса, сумму фитнесов и кумулятивную сумму
def roulette_select(population):
    result_population = []
    population_for_roulette = population

    for item in population_for_roulette:
        item.append(GetValue(item))
    population_for_roulette.sort(key=lambda x: x[itemsCount], reverse=False)#Сортируем по возрастанию ценности
    for item in population_for_roulette:
        item.pop()
    # for i in range (len (population_for_roulette)):
    #     print ("init{i}", population_for_roulette [i])
    #     print ("GetValue((init[i]))", GetValue ((population_for_roulette [i])))

    while(len(population_for_roulette) > 0):
        # print ("population_for_roulette", population_for_roulette)
        # print ("len population_for_roulette", len(population_for_roulette))
        fitness_sum = sum(GetFitnesses(population_for_roulette))
        # print ("fitness_sum", fitness_sum)
        previous_probability = 0

        for ind in population_for_roulette:
            # print ("GetValue(ind[0:(itemsCount-1)]",GetValue(ind[0:(itemsCount-1)]))
            if fitness_sum == 0:
                probability = previous_probability
            else:
                probability = previous_probability + (GetValue(ind) / fitness_sum)
            # print ("probability", probability)
            ind.append(probability)
            previous_probability = probability
            # print ("previous_probability", previous_probability)
        r = random.random()
        # print ("random", r)
        selected_ind = population_for_roulette[0]  # initialize
        for ind in population_for_roulette:
            if ind[itemsCount] > r:
                break;
        ind.pop(itemsCount)
        selected_ind = ind
        # print ("selected_ind", selected_ind)
        population_for_roulette.remove(ind)
        result_population.append(selected_ind)

        for i in range(len(population_for_roulette)):
            population_for_roulette[i].pop(itemsCount)

    return result_population

# Получение новой популяции
def Crossing(individuals):
    # print("individuals",individuals)
    individuals = roulette_select(individuals)
    new_population = []
    count = len(individuals) - 1
    while count > 0:
        first_parent = individuals[0]
        individuals.pop(0)
        count -= 1
        second_parent = individuals[0]
        individuals.pop(0)
        count -= 1
        first_child, second_child = GetTwoChildren(first_parent, second_parent)

        # если ребенок получился "нормальным", то он заменит в новой популяции одного
        # из своих родителей, иначе - родитель останется в новой популяции
        if (checkWeightSize(first_child)):
            new_population.append(first_child)
        else: new_population.append(first_parent)
        if (checkWeightSize(second_child)):
            new_population.append(second_child)
        else: new_population.append(second_parent)

    return new_population


def GenAlgorithm(initial_population, min_cost):
    population = initial_population
    best_values = []

    for index in range(0, maxGenerations):
        print("Поколение ", index)

        newPopulation = Crossing(population)
        # print ("newPopulation", newPopulation)
        # print ("len newPopulation", len (newPopulation))

        for i in range(0, round(len(newPopulation) * percentForMutation)):
            individual_for_mutation_number = random.randint(0, len(newPopulation) - 1)
            newPopulation[individual_for_mutation_number] = Mutate(newPopulation[individual_for_mutation_number])

        population = newPopulation
        population = Filter(population)
        # print ("len FilteredPopulation", len (population))

        # Если в результате мутации появились нежизнеспособные особи, то добавим новых, до постоянного числа
        while len(population) < populationSize:
            population.append(GetRandomVector())
        # print ("len Added population", len (population))

        for item in population:
            item.append(GetValue(item))
        Sort(population)
        for item in population:
            item.pop()

        best_value = GetValue(population[0])
        best_values.append(best_value)

        print("best_value ", best_value)
        print("best_values ", best_values)
        print("best_vector", population[0])
        WeightSizeValue(population[0], data)

        # print("min(best_values)", min(best_values))
        # print ("max(best_values)", max(best_values))
        print("\n")
        if index > 1 and abs(min(best_values) - max(best_values)) <= min_cost:
            break

    return population[0]


initialPopulation = InitialPopulation()
best = GenAlgorithm(initialPopulation, cheapestValue)
print("Результат:")
print(best)
WeightSizeValue(best, data)
