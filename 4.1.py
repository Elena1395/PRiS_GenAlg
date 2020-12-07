# Вариант 24
from pyeasyga import pyeasyga
populationSize = 200

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


ga = pyeasyga.GeneticAlgorithm(data)        # initialise the GA with data
ga.population_size = populationSize

# define a fitness function
def fitness(individual, data):
    weight, volume, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            weight += item[0]
            volume += item[1]
            price += item[2]
    if weight > maxWeight or volume > maxSize:
        price = 0
    return price

ga.fitness_function = fitness               # set the GA's fitness function
ga.run()                                    # run the GA
best_individual = ga.best_individual()
print(ga.best_individual())                # print the GA's best solution


selectedItems = []
def WeightSizeValue(vector, items):
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

WeightSizeValue(best_individual[1], data)
