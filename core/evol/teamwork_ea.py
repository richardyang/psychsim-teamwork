import random
import numpy as np
from deap import creator, base, tools, algorithms

import psychsim.teamwork as tw

creator.create("FitnessMax", base.Fitness, weights=(1.0,-0.5,-0.2))
#creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("s1", np.random.uniform, -1, 1)
toolbox.register("s2", np.random.uniform, -1, 1)
toolbox.register("b1", np.random.uniform, -1, 1)
toolbox.register("b2", np.random.uniform, -1, 1)
toolbox.register("h1", np.random.uniform, -1, 1)
toolbox.register("h2", np.random.uniform, -1, 1)

toolbox.register("individual", tools.initCycle, creator.Individual,
                    (toolbox.s1,
                    toolbox.s2,
                    toolbox.b1,
                    toolbox.b2,
                    toolbox.h1,
                    toolbox.h2), n=1)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    print individual
    return tw.run(individual)

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.10)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    import numpy
    pop = toolbox.population(n=5)
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # Simple EA
    #pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=5, stats=stats, halloffame=hof, verbose=True)

    # Mu+lambda
    NGEN = 5
    MU = 50
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2
    pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats,
                              halloffame=hof, verbose=True)
    return pop, logbook, hof

if __name__ == "__main__":
    myfile = open("log_tw.txt","a")
    '''
    ind = toolbox.individual()
    print(ind)
    toolbox.mutate(ind)
    print(ind)
    '''
    pop, log, hof = main()
    print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))
    myfile.write(str(pop)+"\n"+str(log)+"\n"+str(hof)+"\n")
    myfile.close()

    import matplotlib.pyplot as plt
    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")
    plt.savefig("teamwork.png")
    plt.show()
