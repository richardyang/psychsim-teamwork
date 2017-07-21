import random
from deap import base, creator, tools, algorithms
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=10)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return sum(individual),

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.10)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    import numpy

    pop = toolbox.population(n=50)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, stats=stats, halloffame=hof, verbose=True)

    return pop, logbook, hof


if __name__ == "__main__":
  pop, log, hof = main()
  print pop
  print log
  print hof
  print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))

  import matplotlib.pyplot as plt
  gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
  plt.plot(gen, avg, label="average")
  plt.plot(gen, min_, label="minimum")
  plt.plot(gen, max_, label="maximum")
  plt.xlabel("Generation")
  plt.ylabel("Fitness")
  plt.legend(loc="lower right")
  plt.show()
