import random
import numpy as np
from deap import creator, base, tools, algorithms

import psychsim.beam as bm

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("model_0", random.randint, 1, 3)
toolbox.register("selfish_0", np.random.uniform, 0, 0.5)
toolbox.register("altruistic_0", np.random.uniform, 0, 0.5)
toolbox.register("mean_0", np.random.uniform, 0, 0.5)
toolbox.register("rationality_0", random.randint, 1, 10)
toolbox.register("belief_0", random.randint, 0, 2)

toolbox.register("model_1", random.randint, 1, 3)
toolbox.register("selfish_1", np.random.uniform, 0, 0.5)
toolbox.register("altruistic_1", np.random.uniform, 0, 0.5)
toolbox.register("mean_1", np.random.uniform, 0, 0.5)
toolbox.register("rationality_1", random.randint, 1, 10)
toolbox.register("belief_1", random.randint, 0, 2)

def listCreator(zero,one,two,three,four,five,six,seven,eight,nine,ten,eleven):
    return [zero,one,two,three,four,five,six,seven,eight,nine,ten,eleven]

def initlist(container,zero,one,two,three,four,five,six,seven,eight,nine,ten,eleven):
    return container([zero,one,two,three,four,five,six,seven,eight,nine,ten,eleven])

toolbox.register("buildlist", listCreator, float(random.randint(1, 3)),
                    np.random.uniform(0, 0.5),
                    np.random.uniform(0, 0.5),
                    np.random.uniform(0, 0.5),
                    float(random.randint(1, 10)),
                    float(random.randint(0, 2)),
                    float(random.randint(1, 3)),
                    np.random.uniform(0, 0.5),
                    np.random.uniform(0, 0.5),
                    np.random.uniform(0, 0.5),
                    float(random.randint(1, 10)),
                    float(random.randint(0, 2)))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.buildlist)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return bm.run(individual)

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.10)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    import numpy

    pop = toolbox.population(n=5)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=5, stats=stats, halloffame=hof, verbose=True)

    return pop, logbook, hof

if __name__ == "__main__":
    '''
    ind = toolbox.individual()
    print(ind)
    toolbox.mutate(ind)
    print(ind)
    '''
    pop, log, hof = main()
    print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))
