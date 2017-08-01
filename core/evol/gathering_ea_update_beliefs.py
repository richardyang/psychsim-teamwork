import random
import numpy as np
from deap import creator, base, tools, algorithms

import psychsim.beamnew as bm

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("model_0", random.randint, 0, 2)
toolbox.register("selfish_0", np.random.uniform, 0, 0.5)
toolbox.register("altruistic_0", np.random.uniform, 0, 0.5)
toolbox.register("mean_0", np.random.uniform, 0, 0.5)
toolbox.register("rationality_0", random.randint, 1, 10)
toolbox.register("belief_0", random.randint, 0, 2)
toolbox.register("belief_about_other", random.randint, 0, 2)

'''
toolbox.register("model_1", random.randint, 1, 3)
toolbox.register("selfish_1", np.random.uniform, 0, 0.5)
toolbox.register("altruistic_1", np.random.uniform, 0, 0.5)
toolbox.register("mean_1", np.random.uniform, 0, 0.5)
toolbox.register("rationality_1", random.randint, 1, 10)
toolbox.register("belief_1", random.randint, 0, 2)
'''

toolbox.register("individual", tools.initCycle, creator.Individual,
                    (toolbox.model_0,
                    toolbox.selfish_0,
                    toolbox.altruistic_0,
                    toolbox.mean_0,
                    toolbox.rationality_0,
                    toolbox.belief_0,
                    toolbox.belief_about_other), n=1)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return bm.run(individual)

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.10)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    import numpy

    pop = toolbox.population(n=25)
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, stats=stats, halloffame=hof, verbose=True)

    return pop, logbook, hof

if __name__ == "__main__":
    myfile = open("07312017_updatebeliefs/log_ga.txt","a")
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
    plt.savefig("07312017_updatebeliefs/gathering.png")
    plt.show()
