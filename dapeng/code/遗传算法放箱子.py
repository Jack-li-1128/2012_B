import random
import numpy as np

# 设定箱子和物品的尺寸
BOX_WIDTH = 10.1
BOX_HEIGHT = 6.51153
ITEMS = [(1.58, 0.8), (0.8, 1.58)]

# 初始化种群
def initialize_population(pop_size, items):
    population = []
    for _ in range(pop_size):
        individual = items[:]
        random.shuffle(individual)
        population.append(individual)
    return population

# 评估适应度
def fitness(individual, box_width, box_height):
    box = np.zeros((int(box_height*100), int(box_width*100)))  # 将箱子和物品尺寸放大100倍，避免浮点数运算误差
    positions = []
    for item in individual:
        item_width, item_height = int(item[0]*100), int(item[1]*100)
        placed = False
        for y in range(box.shape[0] - item_height + 1):
            for x in range(box.shape[1] - item_width + 1):
                if np.all(box[y:y+item_height, x:x+item_width] == 0):
                    box[y:y+item_height, x:x+item_width] = 1
                    positions.append((x, y, item_width, item_height))
                    placed = True
                    break
            if placed:
                break
        if not placed:
            return np.sum(box) / (box.shape[0] * box.shape[1]), positions
    return np.sum(box) / (box.shape[0] * box.shape[1]), positions

# 选择
def selection(population, fitness_scores):
    selected = random.choices(population, weights=fitness_scores, k=len(population))
    return selected

# 交叉
def crossover(parent1, parent2):
    if len(parent1) > 2:
        index = random.randint(1, len(parent1) - 2)
        child1 = parent1[:index] + parent2[index:]
        child2 = parent2[:index] + parent1[index:]
        return child1, child2
    else:
        return parent1, parent2

# 变异
def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]

# 遗传算法
def genetic_algorithm(items, box_width, box_height, pop_size=50, generations=100, mutation_rate=0.01):
    population = initialize_population(pop_size, items)
    best_individual = None
    best_fitness = 0
    for gen in range(generations):
        fitness_results = [fitness(ind, box_width, box_height) for ind in population]
        fitness_scores = [fr[0] for fr in fitness_results]
        population = selection(population, fitness_scores)
        new_population = []
        for i in range(0, len(population), 2):
            parent1 = population[i]
            parent2 = population[i + 1]
            child1, child2 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.extend([child1, child2])
        population = new_population
        current_best_individual = max(population, key=lambda ind: fitness(ind, box_width, box_height)[0])
        current_best_fitness = fitness(current_best_individual, box_width, box_height)[0]
        if current_best_fitness > best_fitness:
            best_individual = current_best_individual
            best_fitness = current_best_fitness
    return best_individual, best_fitness

# 运行遗传算法
best_solution, best_fitness = genetic_algorithm(ITEMS, BOX_WIDTH, BOX_HEIGHT)
print("Best solution:", best_solution)
print("Best fitness:", best_fitness)
