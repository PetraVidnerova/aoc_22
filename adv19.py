import time
from copy import deepcopy

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

dictionary = {
    "ore": ORE,
    "clay": CLAY,
    "obsidian": OBSIDIAN,
    "geode": GEODE
}


robots = {
    ORE: 1,
    CLAY: 0,
    OBSIDIAN: 0,
    GEODE: 0
}


class Factory():
    def __init__(self, robots, costs, supply=None):
        self.t = 0
        self.robots = robots.copy()
        if supply is not None:
            self.supply = supply.copy()
        else:
            self.supply = {
                ORE: 0,
                CLAY: 0,
                OBSIDIAN: 0,
                GEODE: 0
            }
        self.costs = costs.copy()

    def get_geode(self):
        return self.supply[GEODE]

    def tick(self):
        self.t += 1
        for key, count in self.robots.items():
            self.supply[key] += count

    def buy_robot(self, material):
        cost = self.costs[material]
        for key, value in cost.items():
            self.supply[key] -= value
        self.robots[material] += 1

    def possible_robots(self):
        possible_robots = []
        for robot in ORE, CLAY, OBSIDIAN, GEODE:
            cost = self.costs[robot]
            have_all = True
            for material in cost:
                if cost[material] > self.supply[material]:
                    have_all = False
                    break
            if have_all:
                possible_robots.append(robot)
        return possible_robots

    #     for key, count in self.costs.items():
    #         if self.supply[key] >= self.costs[key]:
    #             amount = self.supply[key]
    #             self.supply[key] = amount % self.costs[key]
    #             self.robots[key+1] += amount // self.costs[key]

    def possible_max(self):
        maximum = self.supply[GEODE]
        time_left = 24-self.t
        for i in range(time_left):
            maximum += self.robots[GEODE]+i
        return maximum

    def possible_shortest(self):
        count = 0
        time_left = 24 - self.t

        for material, value in self.costs[GEODE].items():
            count = max(
                count, (value - self.supply[material]+1) // (self.robots[material]+time_left+1))

        return count

    def display(self):
        print(self.t, self.robots, self.supply)


def shortest(factory):

    states = []
    states.append(factory)

    shortest = 25
    result_factory = None

    while states:
        print(shortest)
        factory = states.pop(-1)
        if factory.t == 24:
            continue
        if GEODE in factory.possible_robots():
            if factory.t < shortest:
                shortest = factory.t
                result_factory = factory
            continue

        new_factory = deepcopy(factory)
        new_factory.tick()
        if new_factory.possible_shortest() < shortest:
            states.append(new_factory)

        for robot in factory.possible_robots():
            new_factory = deepcopy(factory)
            new_factory.tick()
            new_factory.buy_robot(robot)
            if new_factory.possible_shortest() < shortest:
                states.append(new_factory)

    return result_factory


def run_factory(costs):

    # factory = Factory(robots, costs)
    # factory.display()
    # new_factory = shortest(factory)

    #    factory.display()
    states = []
    initial_factory = Factory(robots, costs)
    states.append(initial_factory)
    maximum = 5

    iter = 0

    start = time.time()

    while states:
        iter += 1
        print(len(states), maximum, (time.time() - start) // 60)
        factory = states.pop(-1)
        #        factory.display()
        if factory.t == 24:
            geodes = factory.get_geode()
            if geodes > maximum:
                maximum = geodes
            continue

        possible_bots = factory.possible_robots()
        new_factory = deepcopy(factory)
        new_factory.tick()
        if factory.possible_max() > maximum:
            states.append(new_factory)

        # if GEODE in possible_bots:
        #     bot_to_buy = GEODE
        # elif OBSIDIAN in possible_bots:
        #     bot_to_buy = OBSIDIAN
        # elif CLAY in possible_bots:
        #     bot_to_buy = CLAY
        # elif ORE in possible_bots:
        #     bot_to_buy = ORE
        # else:
        #     bot_to_buy = None
        # if bot_to_buy is not None:
        for bot_to_buy in possible_bots:
            new_factory = deepcopy(factory)
            new_factory.tick()
            new_factory.buy_robot(bot_to_buy)
            if new_factory.possible_max() > maximum:
                states.append(new_factory)

    return maximum


blueprints = []

with open("input19t.txt") as f:
    for line in f:
        line = line.strip()
        costs = {
        }
        line = line.split(":")[1]
        parts = line.split(".")
        for part in parts:
            if part:
                words = part.split()
                what = words[1]
                cost = {}
                price = " ".join(words[4:])
                what = dictionary[what]
                for c in price.split("and"):
                    c = c.strip()
                    number, material = c.split(" ")
                    material = dictionary[material]
                    cost[material] = int(number)
                costs[what] = cost
        blueprints.append(costs)

print(blueprints)

result = 0
for i, costs in enumerate(blueprints):
    if i == 0:
        continue
    geodes = run_factory(costs)
    print(geodes)
    result += geodes*(i+1)

print(result)
