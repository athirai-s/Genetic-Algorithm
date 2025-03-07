import random
import math


def calc_distance(path,cities):
    dist = 0
    for i in range(len(path)-1):
        c1, c2 = cities[path[i]], cities[path[i+1]]
        dist += math.sqrt((c2[0] - c1[0])**2 + (c2[1] - c1[1])**2 + (c2[2] - c1[2])**2)
    # completing the cycle
    c1, c2 = cities[path[-1]], cities[path[0]]
    dist += math.sqrt((c2[0] - c1[0])**2 + (c2[1] - c1[1])**2 + (c2[2] - c1[2])**2)
    return dist

def create_initial_population(total_cities,pop_size):
    order=list(range(total_cities))
    population=[]
    for _ in range(pop_size):
        population.append(random.sample(order,len(order)))
    return population


def create_initial_population(order,pop_size):
    population = []
    for i in range(pop_size):
        suffle_order = order[:] 
        random.shuffle(suffle_order) 
        population.append(suffle_order)
    return population


def tournament_selection(population,fitness,k=5):
    ans=[]
    for _ in range(k):
        idx=random.randint(0,len(population)-1)
        ans.append((population[idx],fitness[idx]))
    ans.sort(key=lambda x:x[1])
    return ans[0][0]


#ordered crossover
def crossover(p1,p2):
    size = len(p1)
    start,end = sorted(random.sample(range(size), 2))
    
    child=[-1]*size
    for i in range(start, end):
        child[i]=p1[i]
    
    point = end #crossover point

    for x in p2:   #particular gene(x) not in parent2 then give it to child
        if x not in child:
            while point >= size:
                point = 0
            child[point] = x
            point += 1
    return child



def mutation(path):

    i,j = random.sample(range(len(path)), 2)
    #swapping to create mutation
    path[i],path[j] = path[j],path[i]
    return path



def two_opt(path, cities):
    optimal_dist = calc_distance(path, cities)
    optimal_path = path[:]
    for i in range(len(path)-1):
        for j in range(i+2,len(path)):
            new_path = path[:]
            new_path[i:j+1] = reversed(path[i:j+1])
            new_dist = calc_distance(new_path, cities)
            if new_dist<optimal_dist:
                return new_path
    return optimal_path





def output(distance, path, cities, file_path="output.txt"):
    with open(file_path, "w") as file:
        file.write(f"{distance:.6f}\n")  
        for idx in path:
            file.write(f"{cities[idx][0]} {cities[idx][1]} {cities[idx][2]}\n")
        file.write(f"{cities[path[0]][0]} {cities[path[0]][1]} {cities[path[0]][2]}\n")




def read_input(file_path="input.txt"):
    with open(file_path, "r") as file:
        lines = file.readlines()
    total_cities = int(lines[0].strip())
    cities = []
    
    for line in lines[1:total_cities+1]:
        x, y, z = map(int, line.strip().split())
        cities.append((x, y, z))

    return total_cities, cities

#Main Code

#cities = [[158, 147, 135], [56, 24, 160], [162, 194, 104]]
# cities = [
#     [158, 147, 135], [56, 24, 160], [162, 194, 104], [45, 87, 92], [200, 210, 180]
# ]
# total_cities = len(cities)

total_cities, cities = read_input()

#base order sample
order = []
for i in range(total_cities):
    order.append(i)
#print(order)

generations=500
pop_size=100
elite_fraction=0.05
#mutation_rate = 0.2

total_cities = len(cities)
population = create_initial_population(order, pop_size)
elite_pop_size = max(1, int(elite_fraction*pop_size))  # to keep the top fittest(elite) individuals

for g in range(generations):

    fitness = []
    for idx in population:
        fitness.append(calc_distance(idx, cities)) #calculating the fitness for each population
    result_population = [x for _,x in sorted(zip(fitness,population),key=lambda x:x[0])]
    
    next_gen = []  #selecting the next generation by choosing the best parents
    for i in range(elite_pop_size):
        next_gen.append(result_population[i])
    mutation_rate = max(0.05, 0.2*(1 - g/generations))  #increase the mutation rate for each iteration

    while len(next_gen)<pop_size:
        parent1 = tournament_selection(result_population,fitness)
        parent2 = tournament_selection(result_population, fitness)
        child = crossover(parent1, parent2)
        
        if random.random()<mutation_rate:
            child = mutation(child)
            child = two_opt(child, cities)   #using 2-opt to further optimse the results
        
        next_gen.append(child)

    population = next_gen[:pop_size]

optimal_path = population[0]
optimal_distance = calc_distance(optimal_path, cities)
for idx in population:
    dist = calc_distance(idx,cities)
    if dist < optimal_distance:
        optimal_distance = dist
        optimal_path = idx

output(optimal_distance, optimal_path, cities)