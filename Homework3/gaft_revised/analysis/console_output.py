#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..plugin_interfaces.analysis import OnTheFlyAnalysis


class ConsoleOutput(OnTheFlyAnalysis):

    # Analysis interval.
    interval = 1

    # Only analyze in master process?
    master_only = True

    def setup(self, ng, engine):
        generation_info = 'Generation number: {}'.format(ng)
        population_info = 'Population number: {}'.format(engine.population.size)
        self.logger.info('{} {}'.format(generation_info, population_info))

    '''
        Revised by myself, Dec 21 2017
        Add the average fitness individual
    '''
    def register_step(self, g, population, engine):
        best_indv = population.best_indv(engine.fitness)
        avg_indv = population.mean(engine.fitness)
        ng_info = 'Generation: {}, '.format(g+1)
        fit_info = 'best fitness: {:.3f}, '.format(engine.ori_fitness(best_indv))
        #scaled_info = 'scaled fitness: {:.3f}'.format(engine.fitness(best_indv))
        avg_info = 'Mean fitness: {:.3f}'.format(avg_indv)
        #msg = ng_info + fit_info + scaled_info
        msg = ng_info + fit_info + avg_info
        self.logger.info(msg)

    def finalize(self, population, engine):
        best_indv = population.best_indv(engine.fitness)
        x = best_indv.solution
        y = engine.fitness(best_indv)
        msg = 'Optimal solution: ({}, {})'.format(x, y)
        self.logger.info(msg)

