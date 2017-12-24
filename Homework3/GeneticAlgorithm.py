from gaft import GAEngine
from gaft.components import BinaryIndividual
from gaft.components import Population
from gaft.operators import *
from gaft.analysis.fitness_store import FitnessStore
from gaft.analysis.console_output import ConsoleOutput
from gaft.plugin_interfaces.analysis import OnTheFlyAnalysis

import os
from math import sin, cos, pi, exp
import numpy as np

# Define Generation
generation = 50

# Define Population and the Constraints
population_size = 10
indv_template = BinaryIndividual(ranges = [(-3, 12.1), (4.1, 5.8)], eps = 0.001)
population = Population(indv_template = indv_template, size = population_size).init()

# Define Genetic Operators
## Selection : RouletteWheelSelection, TournamentSelection, LinearRankingSelection, ExpotentialRankingSelection
#selection = RouletteWheelSelection()
selection = TournamentSelection()

## Crossover
### pc : probability of crossover(usually between 0.25 - 1.0)
### pe : gene exchange probability
crossover = UniformCrossover(pc=0.8, pe=0.5)

## Mutate
### pm : The probability of mutation (usually between 0.001 ~ 0.1)
### pbm : The probability of big mutation, usually more than 5 times bigger than pm
### alpha : intensive factor
mutation = FlipBitBigMutation(pm=0.1, pbm=0.55, alpha=0.6)

# Construct GA Engine
engine = GAEngine(population=population, 
                  selection=selection,
                  crossover=crossover, 
                  mutation=mutation,
                  analysis=[ConsoleOutput, FitnessStore])

# Define fitness function.
@engine.fitness_register
def fitness(indv):
    x1, x2 = indv.solution
    formula = 21.5 + x1*sin(4*pi*x1) + x2*sin(20*pi*x2)
    return formula
        
# Best Fitness values are export to best_fit.py
engine.run(ng = generation)


import matplotlib.pyplot as plt
from best_avg_fit import best_avg_fit

steps, variants, fits, avgfits = list(zip(*best_avg_fit))
best_step, best_v, best_f, avg_f = steps[-1], variants[-1], fits[-1], avgfits[-1]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(steps, fits, label="Best_so_far")
ax.plot(steps, avgfits, label="Average Fitness")
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness')
ax.legend(loc='lower right')

# Plot the Maximum
print("Close the plot to export surface")
ax.scatter([best_step], [best_f], facecolor='r')
ax.annotate(s='x : [{:.6f}, {:.6f}]\ny : {:.6f}'.format(*best_v, best_f),
                                                     xy=(best_step, best_f),
                                                     xytext=(best_step, best_f-0.15))
plt.title("Genetic Algorithm\nPopulation : " + str(population_size))
plt.show()

user_check = input("Enter y/n to export the surface of each generation : ")

if user_check == "y":
    import mpl_toolkits.mplot3d
    from tqdm import tqdm


    ctr = 0

    # Export the surface
    for i, (x, y), z, a in tqdm(best_avg_fit):
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter([x], [y], [z], zorder=99, c='r', s=100)

        x, y = np.mgrid[-4:13:100j, 4:6:100j]
        z = 21.5+x*np.sin(4*np.pi*x) + y*np.sin(20*np.pi*y)
        ax.plot_surface(x, y, z, rstride=2, cstride=2, cmap=plt.cm.bone_r)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        if not os.path.exists('./surfaces'):
            os.mkdir('./surfaces')
        fig.savefig('./surfaces/{}.png'.format(i+1))
        ctr += 1
        plt.close(fig)
else:
    print("Exit")