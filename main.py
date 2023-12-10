import numpy as np
import random
import math

FILE_NAME = "genAlgData3.txt"
CHROMOSOMES = 10
GENERATIONS = 12
X = 0.1
CROSSOVER = 'uniform'
Z = 0.3


# Swap genes in a chromosome to put them in valid order
def swap_chro(chro):
    if chro[0] > chro[1]:
        chro[0], chro[1] = chro[1], chro[0]
    if chro[2] > chro[3]:
        chro[2], chro[3] = chro[3], chro[2]
    return chro


# Generate a list of chromosomes with the given number of chromosomes (CHROMOSOMES)
def generate():
    chromosomes = []
    for i in range(CHROMOSOMES):
        random_numbers = np.random.normal(0, 1.15, 4).tolist()
        for i in range(len(random_numbers)):
            random_numbers[i] = round(random_numbers[i], 1)
        random_numbers = swap_chro(random_numbers)
        x = np.random.choice([0, 1], size=1)
        random_numbers.append(x[0])
        chromosomes.append(random_numbers)
    return chromosomes


# Calculate the fitness score of a chromosome regarding the given data file
def fitness(chromosome):
    file = open(FILE_NAME, 'r')
    lines = file.readlines()
    score = 0
    no_match = True
    for l in lines:
        l = l.split()
        day1 = float(l[0])
        day2 = float(l[1])
        profit = float(l[2])
        if chromosome[0] <= day1 <= chromosome[1] and chromosome[2] <= day2 <= chromosome[3]:
            if chromosome[4] == 1:
                score += profit
            else:
                score -= profit
            no_match = False
    if no_match:
        score = -5000
    file.close()
    return round(score, 2)


# Create a sorted list of [chromosomes, its fitness score]
def createFitnessList(chromosomes):
    chro_fitness = []
    for c in chromosomes:
        chro_fitness.append([c, fitness(c)])

    # Sort the chro_fitness list based on fitness score in descending order
    chro_fitness.sort(key=lambda x: x[1], reverse=True)

    return chro_fitness


# Return the max, min, avg fitness scores and the chromosome of the max score
def fitnessResult(chromosomes):
    chro_fitness = createFitnessList(chromosomes)
    result = []

    # Exclude chromosomes that don't have any match across the data file (fitness = -5000)
    for cf in chro_fitness:
        if cf[1] != -5000:
            result.append(cf)

    # Return all None if all chromosomes don't have any match (fitness = -5000)
    if len(result) == 0:
        return None, None, None, None

    total = 0
    for cf in result:
        total += cf[1]

    return result[0][1], result[-1][1], round(total / len(result)), result[0][0]


# Do the selection and crossover on a list of chromosomes regarding X% of selection
def selectionAndCrossover(chromosomes):
    chro_fitness = createFitnessList(chromosomes)   # sorted in descending order

    # Add the top X chromosomes to result list
    result = []
    topX = math.ceil(CHROMOSOMES * X)
    for i in range(topX):
        result.append(chro_fitness[i][0])

    # Pop the top X chromosomes out of the chro_fitness, now chro_fitness contains remaining chromosomes
    for i in range(topX):
        chro_fitness.pop(0)

    # Implementation of Roulette Wheel Selection
    # Assign the smallest fitness to 0 to avoid negative number and
    if chro_fitness[-1][1] < 0:
        for i in range(len(chro_fitness)):
            chro_fitness[i][1] = round(chro_fitness[i][1] - chro_fitness[-1][1], 2)

    # In case all remaining chromosomes have the same negative fitness score
    # making their re-assigned values all 0 (above step)
    if chro_fitness[0][1] == chro_fitness[-1][1] == 0:
        for i in range(len(chro_fitness)):
            chro_fitness[i][1] = 1

    total_fitness = 0
    for cf in chro_fitness:
        total_fitness += cf[1]

    # Convert fitness score to percentage
    # Since I use list (array) to implement the Roulette Wheel, I need to round these percentages
    for i in range(len(chro_fitness)):
        chro_fitness[i][1] = round(chro_fitness[i][1] * 100 / total_fitness)

    # If there are more than 1 chromosomes with 0%, I reassign their percentages to 1 in order to have
    # enough chromosomes to perform crossover so that the number of resulted chromosomes is equal to (100-X)%
    # eg. if the remaining chromosomes needed is 6, we need at least 3 chromosomes with > 0% to do crossover
    if chro_fitness[-2][1] == 0:
        for i in range(len(chro_fitness)):
            if chro_fitness[i][1] == 0: chro_fitness[i][1] = 1

    # Generate the Roulette Wheel
    roulette_wheel = []
    for cf in chro_fitness:
        for i in range(cf[1]):
            roulette_wheel.append(cf[0])

    # Randomly choose 2 chromosomes from roulette_wheel and do crossover
    # until reaching the number of remaining chromosomes
    done_crossover = []
    for i in range(CHROMOSOMES - topX):
        # Ensure that the parents are not the same, and crossover has not been done on them
        while 1:
            indexes = np.random.choice(len(roulette_wheel), 2).tolist()
            parent1 = roulette_wheel[indexes[0]]
            parent2 = roulette_wheel[indexes[1]]
            if (parent1 != parent2) and ((parent1, parent2) not in done_crossover):
                break
        done_crossover.append((parent1, parent2))
        new_chromosome = crossover(parent1, parent2)
        result.append(new_chromosome)
    return result


# Do crossover of 2 parent chromosomes and the return the child regarding the given crossover method
def crossover(parent1, parent2):
    result = []
    if CROSSOVER == '1-point':
        result = parent1[:2] + parent2[2:]
    elif CROSSOVER == 'uniform':
        while True:
            result = []
            choose1 = 0
            choose2 = 0
            for z in range(5):
                x = np.random.choice([1, 2], size=1)
                if x[0] == 1:
                    result.append(parent1[z])
                    choose1 += 1
                else:
                    result.append(parent2[z])
                    choose2 += 1
            result = swap_chro(result)

            # to avoid the algorithm always choose genes from 1 parent
            if choose1 != 5 and choose2 != 5: break

    return result


# Do the mutation on a list of chromosomes regarding the Z% of mutation
def mutation(chromosomes):
    # When no mutation is required
    if Z == 0: return chromosomes

    # Create a list of booleans to represent the mutation probability
    probability = [False] * 100
    for i in range(round(Z * 100)):
        probability[i] = True

    for i in range(len(chromosomes)):
        for j in range(5):  # one chromosome contain 5 genes
            # Randomize an element in the probability list to decide whether to mutate
            # True is to mutate and False is not to mutate
            mutate = random.sample(probability, 1)

            if mutate[0]:
                if j < 4:   # mutate the first 4 genes
                    new_gene = np.random.normal(0, 1.15, 1).tolist()
                    chromosomes[i][j] = round(new_gene[0], 1)
                else:       # mutate the last gene (SHORT/BUY)
                    x = np.random.choice([0, 1], size=1)
                    chromosomes[i][j] = x[0]
        chromosomes[i] = swap_chro(chromosomes[i])

    return chromosomes


def main():
    if GENERATIONS < 10:
        raise Exception("Sorry, the number of generations must be larger than 10")
    if CHROMOSOMES < 1:
        raise Exception("The number of chromosomes must be at least 2")
    if Z < 0 or X < 0:
        raise Exception("Z% and X% must not be negative")
    if math.floor(CHROMOSOMES * (1 - X)) <= 1:
        raise Exception("Cannot perform crossover with this number of chromosomes and X%")
    if CROSSOVER not in ['1-point', 'uniform']:
        raise Exception("Sorry, crossover method must be either '1-point' or 'uniform'")

    print("Initial Generation:")
    chromosomes = generate()
    for c in chromosomes:
        print(c)
    print()

    for i in range(1, GENERATIONS + 1):
        print("Generation", i)
        chromosomes = selectionAndCrossover(chromosomes)
        chromosomes = mutation(chromosomes)
        for c in chromosomes:
            print(c)

        if i % 10 == 0 or i == GENERATIONS:
            max_fitness, min_fitness, avg_fitness, max_chro = fitnessResult(chromosomes)
            print("Max fitness score:", max_fitness)
            if i % 10 == 0:
                print("Min fitness score:", min_fitness)
                print("Average fitness score:", avg_fitness)
            else:
                print("Chromosome with max fitness score:", max_chro)
        print()


if __name__ == '__main__':
    main()
