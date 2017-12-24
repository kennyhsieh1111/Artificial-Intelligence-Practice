#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..plugin_interfaces.analysis import OnTheFlyAnalysis

class FitnessStore(OnTheFlyAnalysis):

    # Analysis interval.
    interval = 1

    # Only analyze in master process?
    master_only = True

    def setup(self, ng, engine):
        # Generation numbers.
        self.ngs = []

        # Best fitness in each generation.
        self.fitness_values = []

        # Best solution.
        self.solution = []

        # Avg fitness in each generation.
        self.avg_fitness_values = []

    '''
        Revised by myself, Dec 21 2017
        Add the average fitness individual
    '''
    def register_step(self, g, population, engine):
        # Collect data.
        best_indv = population.best_indv(engine.fitness)
        best_fit = engine.ori_fitness(best_indv)

        avg_val = population.mean(engine.fitness)

        self.ngs.append(g)
        self.solution.append(best_indv.solution)
        self.fitness_values.append(best_fit)
        self.avg_fitness_values.append(avg_val)

    '''
        Revised by myself, Dec 21 2017
        Add the result of average fitness score to best_fit
    '''
    def finalize(self, population, engine):
        with open('best_avg_fit.py', 'w', encoding='utf-8') as f:
            f.write('best_avg_fit = [\n')
            for ng, x, y, z in zip(self.ngs, self.solution, self.fitness_values, self.avg_fitness_values):
                f.write('    ({}, {}, {}, {}),\n'.format(ng, x, y, z))
            f.write(']\n\n')

        self.logger.info('Best fitness values are written to best_avg_fit.py')

