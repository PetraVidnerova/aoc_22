class Valve():
    def __init__(self, name, flow_rate, next_valves):
        self.name = name
        self.flow_rate = flow_rate
        self.next_valves = next_valves
        self.travel_time = [1] * len(self.next_valves)

    # def sort(self, valve_dict):
    #     self.next_valves.sort(key=lambda x: valve_dict[x].flow_rate, reverse=True)

    def __repr__(self):
        return f"Valve({self.name})"
    
valve_dict = {
}

closed_dict = {
}

with open("input16t.txt",  "r") as f:
    for line in f:
        parts = line.split(" ")
        valve_name = parts[1]
        flow_rate = int(parts[4].split("=")[-1][:-1])
        next_valves = list(map(
            lambda x: x[:-1], parts[9:]
        ))
        print(valve_name, flow_rate, next_valves)
        valve_dict[valve_name] = Valve(valve_name, flow_rate, next_valves)
        closed_dict[valve_name] = True


# reduce valves
zero_valves = [
    valve
    for valve in valve_dict.values()
    if valve.flow_rate == 0 
]

aa = valve_dict["AA"]
start = [
    (valve_dict[s], closed_dict, 0, 29)
    for s in aa.next_valves
]


while zero_valves:
    for val in valve_dict.values():
        print(val.name, val.flow_rate, list(zip(val.next_valves, val.travel_time)))
    print()
    print()
    
    
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
    for inp, t1  in zip(inputs, travel_times):
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
    if zero in [v for (v, d, p, t) in start]:
        idx = 0
        while start[idx][0] != zero:
            idx += 1
        _, d, p, t = start[idx]
        del start[idx]
        for v, t2  in zip(zero.next_valves, zero.travel_time):
            start.append((valve_dict[v], d, p, t-t2))
            
    del valve_dict[zero.name]
    del closed_dict[zero.name]

print("READY")
for val in valve_dict.values():
    print(val.name, val.flow_rate, list(zip(val.next_valves, val.travel_time)))
print()
print()
print(start)
print()



# for v in valve_dict.values():
#     v.sort(valve_dict)

        
def reduction(states):
    states.sort(key=lambda x: x[3])
    to_delete = [] 
    for i, x in enumerate(states):
        delete = False
        for higher in states[0:i]:
            if higher[0] == x[0] and higher[1] == x[1] and higher[2] >= x[2]:
                delete = True
                break
        if delete:
            to_delete.append(i)

    states = [
        x
        for i, x in enumerate(states)
        if i not in to_delete
    ]
    return states

states = start
results = 0
        

minutes = 30


#states.append((start, closed_dict, 0, 30))
iter = 0
while states:
    iter += 1
    if iter % 1000 == 0:
        print(iter)
    states = reduction(states)
    start, val_dict, press, minutes = states.pop(-1)

    # release = sum([valve_dict[x].flow_rate for x, val in val_dict.items() if not val]) 
    # print(f"Act: {start.name} Opened:{[x for x, val in val_dict.items() if not val]} Release: {release} Press: {press} Minutes:{30-minutes}")
    if minutes <= 0:
        if press > results:
            results = press
        continue
    if val_dict[start.name]:
            new_minutes = minutes - 1
            new_press = press + new_minutes * start.flow_rate
            val_dict_copy = val_dict.copy()
            val_dict_copy[start.name] = False
            states.append((start, val_dict_copy, new_press, new_minutes))
    for x, t in zip(start.next_valves, start.travel_time):
        states.append((valve_dict[x], val_dict, press, minutes-t))
            
print(results)
