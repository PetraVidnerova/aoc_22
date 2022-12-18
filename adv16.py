import copy
import itertools
import numpy as np
from tqdm import tqdm


class Valve():
    def __init__(self, name, flow_rate, next_valves):
        self.name = name
        self.flow_rate = flow_rate
        self.next_valves = next_valves
        self.travel_time = [1] * len(self.next_valves)

    def sort(self, valve_dict):
        doubles = list(zip(self.next_valves, self.travel_time))
        doubles.sort(key=lambda x: valve_dict[x[0]].flow_rate)

        self.next_valves = [x[0] for x in doubles]
        self.travel_time = [x[1] for x in doubles]

    def __repr__(self):
        return f"Valve({self.name})"


def read_valves():
    valve_dict = {}

    with open("input16.txt",  "r") as f:
        for line in f:
            parts = line.split(" ")
            valve_name = parts[1]
            flow_rate = int(parts[4].split("=")[-1][:-1])
            next_valves = list(map(
                lambda x: x[:-1], parts[9:]
            ))
            print(valve_name, flow_rate, next_valves)
            valve_dict[valve_name] = Valve(valve_name, flow_rate, next_valves)

    return valve_dict


def reduce_valves(valve_dict):
    zero_valves = [
        valve
        for valve in valve_dict.values()
        if valve.flow_rate == 0 if valve.name != "AA"
    ]

    while zero_valves:

        zero = zero_valves.pop()
        inputs = [
            val
            for val in valve_dict.values()
            if zero.name in val.next_valves
        ]
        travel_times = [
            val.travel_time[val.next_valves.index(zero.name)]
            for val in inputs
        ]
        outputs = zero.next_valves
        costs = zero.travel_time
        for inp, t1 in zip(inputs, travel_times):
            idx = inp.next_valves.index(zero.name)
            del inp.next_valves[idx]
            del inp.travel_time[idx]
            for out, t2 in zip(outputs, costs):
                if inp.name == out:
                    continue
                if out not in inp.next_valves:
                    inp.next_valves.append(out)
                    inp.travel_time.append(t1+t2)
                else:
                    idx = inp.next_valves.index(out)
                    inp.travel_time[idx] = min(inp.travel_time[idx], t1+t2)

        del valve_dict[zero.name]

    return valve_dict


class Graph():
    def __init__(self, valve_dict):
        self.nodes = [v.flow_rate for v in valve_dict.values()]
        self.closed = np.ones(len(self.nodes), dtype=bool)
        self.n_nodes = len(self.nodes)
        self.edges = np.zeros((self.n_nodes, self.n_nodes), dtype=float)

        keys = list(valve_dict.keys())
        self.start = keys.index("AA")
        self.closed[self.start] = False
        for i, v in enumerate(valve_dict.values()):
            edges = zip(v.next_valves, v.travel_time)
            for name, time in edges:
                idx = keys.index(name)
                self.edges[i][idx] = time

    def reset_closed(self):
        self.closed.fill(True)
        self.closed[self.start] = False

    def way_to_node(self, snode, enode):
        if snode == enode:
            return 0
        # if self.edges[snode, enode] > time:
        #     return self.edges[snode, enode]
        nodes_to_go = [(snode, 0)]
        nodes_in_time = set()
        time = -1
        while enode not in nodes_in_time:
            time += 1
            print("->", time, nodes_to_go)
            for i, x in enumerate([node for node, stime in nodes_to_go if stime == time]):
                nodes_in_time.add(x)
                for y, cost in [(n, t) for n, t in enumerate(self.edges[x]) if t > 0]:
                    nodes_to_go.append((y, time+cost))

        return time

    def fill_edges(self):
        graph2 = copy.deepcopy(self)
        for snode in range(self.n_nodes):
            for enode in range(self.n_nodes):
                self.edges[snode, enode] = graph2.way_to_node(snode, enode)

    def display(self):
        print(self.nodes)
        print()
        print(self.edges)
        print()

    def find_pressure(self):
        pressure = 0
        cursor = self.start
        time = 30
        while time > 0:
            maxtime = min(time, max([x for i, x in enumerate(
                self.edges[cursor]) if self.closed[i]])+2)
            print("maxtime", maxtime)
            pressures = (
                maxtime - self.edges[cursor]-1) * self.nodes * self.closed
            print("pressures", pressures)
            next_valve = pressures.argmax()
            time -= self.edges[cursor][next_valve] + 1
            cursor = next_valve
            self.closed[cursor] = False
            print("next", list(valve_dict.keys())[cursor])
            if time > 0:
                pressure += time * self.nodes[cursor]
            if all(self.closed == False):
                break

        return pressure

    def pressure(self, nodes):
        cursor = self.start
        time = 30
        pressure = 0
        for next_node in nodes:
            time -= self.edges[cursor][next_node]
            time -= 1
            if time > 0:
                pressure += time * self.nodes[next_node]
            else:
                break
            cursor = next_node

        return pressure


class State():
    def __init__(self, closed, cursor, pressure, time):
        self.closed = closed
        self.cursor = cursor
        self.pressure = pressure
        self.time = time

    def test(self, maximum, graph):
        pressures = sorted([graph.nodes[i]
                            for i, cl in enumerate(self.closed) if cl])
        times = range(self.time - len(pressures), self.time, 1)
        times = [x if x > 0 else 0
                 for x in times]
        assert len(pressures) == len(times)
        possible = 0
        for p, t in zip(pressures, times):
            possible += p*t

        if self.pressure + possible < maximum:
            return False
        else:
            return True

    def __repr__(self):
        return f"State({self.closed} {self.cursor} {self.pressure} {self.time})"


class States():

    def __init__(self, maximum, graph):
        self.states = []
        self.maximum = maximum
        self.graph = graph

    def empty(self):
        return not self.states

    def pop(self, x=0):
        return self.states.pop(x)

    def append(self, state):
        if state.pressure > self.maximum:
            self.maximum = state.pressure

        if state.time <= 0:
            return

        if sum(state.closed) == 0:
            return

        if state.test(self.maximum, self.graph):
            self.states.append(state)


valve_dict = read_valves()
valve_dict = reduce_valves(valve_dict)
print("READY")
for val in valve_dict.values():
    print(val.name, val.flow_rate, list(zip(val.next_valves, val.travel_time)))
print()
print()

graph = Graph(valve_dict)
graph.display()

graph.fill_edges()
graph.display()


maximum = graph.find_pressure()
print(maximum)
graph.reset_closed()


states = States(maximum, graph)
states.append(State(graph.closed, graph.start, 0, 30))

iter = 0
while not states.empty():

    if iter % 1000 == 0:
        print(iter)
    iter += 1

    state = states.pop(-1)
    pressure = state.pressure

    closed = state.closed.copy()
    if closed[state.cursor]:
        closed[state.cursor] = False
        pressure += (state.time - 1)*graph.nodes[state.cursor]
        opening = 1
    else:
        opening = 0

    for next_node, cost in enumerate(graph.edges[state.cursor]):
        if cost > 0 and next_node != state.cursor and graph.closed[next_node]:
            states.append(
                State(closed, next_node, pressure,
                      int(state.time-cost)-opening)
            )

print()
print(states.maximum)
