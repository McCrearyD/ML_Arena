import random
import math

from test.genome import *


def assert_near_equal(net1, net2, inverse=False, chances=5):
    equal = 0

    for i, layer in enumerate(net1.layer_weights):
        layer_clone = net2.layer_weights[i]

        res = np.allclose(layer, layer_clone, 0.0001)

        if inverse and res:  # want non-equality
            equal += 1

        if not inverse:
            assert res, \
                '(Layer: + %i) Inputs MUST have the same layer weights.\n\n1:\n\n%s\n\n2:\n\n%s' % (
                    i,
                    layer,
                    layer_clone
                )
            print('Assertion passed for layer equivilence at index %i' % i)

    if inverse:
        assert equal < chances, 'Assertion failed... Inputs MUST **NOT** have the same layer weights.'
        print('Assertion passed for layer non-equivilence at index %i' % i)


class GenomePopulation:
    genomes: list
    generation = 0
    last_best = None

    def __init__(self, *genomes):
        self.genomes = list(genomes)

    def size(self):
        return len(self.genomes)

    def pick_random(self, fitness_sum) -> Genome:
        if fitness_sum <= 0:
            return random.choice(self.genomes)

        r = random.randrange(start=0, stop=math.floor(fitness_sum))

        for genome in self.genomes:
            r -= genome.calculate_fitness()
            if r < 1:
                return genome

        raise Exception('This shouldn\'t be possible..')

    def best(self) -> Genome:
        best = max(self.genomes, key=lambda g: g.calculate_fitness())
        return best

    def natural_selection(self):
        """Uses natural selection to alter the current Neural Network population."""

        print('Selecting new generation...')
        new_best = self.best().clone()

        new_genomes = [
            new_best,
            new_best.clone().mutate()
        ]

        fit_sum = np.sum([genome.calculate_fitness()
                          for genome in self.genomes])

        l = round(len(self.genomes) / 2 - 1)

        for i in range(l):

            if i < l / 2:
                parentA = self.pick_random(fit_sum)
                parentB = self.pick_random(fit_sum)

                children = parentA.crossover(parentB)
                [child.mutate() for child in children]
                new_genomes.extend(children)

            else:
                genomes = (
                    self.pick_random(fit_sum).clone(),
                    self.pick_random(fit_sum).clone()
                )
                genomes[0].mutate()
                new_genomes.extend(genomes)

        self.genomes = new_genomes
