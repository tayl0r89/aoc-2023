import math

class BaseComponent:
    high_sent: int
    low_sent: int
    key: str
    destinations: list[str]

    def __init__(self, key):
        self.key = key
        self.high_sent = 0
        self.low_sent = 0
        self.destinations = []

    def send(self, pulse) -> list[tuple[str, str, int]]:
        instructions = list(map(lambda x: (self.key, x, pulse), self.destinations))
        for i in instructions:
            if i[2] == 0:
                self.low_sent = self.low_sent + 1
            else:
                self.high_sent = self.high_sent + 1
        return instructions

    def get_state(self):
        return None

    def process(self, pulse, from_key) -> list[tuple[str, str, int]]:
        result = self.handle_pulse(pulse, from_key)
        if result is not None:
            return self.send(result)

        return []

    def handle_pulse(self, pulse, from_key) -> "int | None":
        # Abstract to be implemented
        pass

    def reset(self) -> None:
        pass


class Output(BaseComponent):
    low_recieved: int

    def __init__(self, key):
        super().__init__(key)
        self.low_recieved = 0

    def handle_pulse(self, pulse, from_key) -> "int | None":
        if pulse == 0:
            self.low_recieved = self.low_recieved + 1
        return None


class Broadcaster(BaseComponent):
    def __init__(self, key: str):
        super().__init__(key)

    def handle_pulse(self, pulse, _) -> "int | None":
        # Does nothing to the pulse, sends it on to others
        return pulse


class FlipFlop(BaseComponent):
    active: bool

    def __init__(self, key: str):
        super().__init__(key)
        self.active = False

    def reset(self) -> None:
        self.active = False

    def get_state(self):
        return self.active

    def process(self, pulse, _) -> list[tuple[str, str, int]]:
        # print(f"FLIP FLOP RECIEVED - {pulse}")
        if pulse == 1:
            # print("HIGH")
            return []
        else:
            # print("LOW")
            self.active = not self.active
            if self.active:
                return self.send(1)
            else:
                return self.send(0)


class Conjunction(BaseComponent):
    input_state: dict[str, int]

    def __init__(self, key):
        super().__init__(key)
        self.input_state = {}

    def get_state(self):
        return self.input_state

    def reset(self) -> None:
        for key in self.input_state.keys():
            self.input_state[key] = 0

    def handle_pulse(self, pulse, from_key) -> "int | None":
        self.input_state[from_key] = pulse
        if 0 in self.input_state.values():
            return 1

        return 0


def print_instructions(ins):
    for i in ins:
        print(f"{i[0]} -{'high' if i[2] == 1 else 'low'}-> {i[1]}")


def push_button(comps, count=0):
    processed = []
    instructions = [("button", "broadcaster", 0)]
    if count % 1000000 == 0:
        print(count)
    had = False
    while len(instructions) > 0:
        processed.append(instructions[0])
        from_comp, to_comp, pulse = instructions[0]
        result = comps[to_comp].process(pulse, from_comp)
        # if to_comp in ["vr", "pf", "xd", "ts"]:
        #     # print(comps[to_comp].get_state())
        #     if list(set(comps[to_comp].get_state().values())) == [1]:
        #         print(f"{to_comp} at count {count}")

        if sum(comps["dt"].input_state.values()) > 0:
            had = True
            print(f"{comps['dt'].input_state} at {count}")

        # if from_comp in ["pm", "ks", "vk", "dl"]:
        #     if pulse==1:
        #         print(f"{from_comp} high pulse at count {count}")


        instructions = [*instructions[1:], *result]
    
    if had:
        print(comps["dt"].input_state)
        print(result)
        print("----------------------")
    
    return processed

def get_mapped_to(val, mapps):
    result = []
    for m in mapps:
        if m[1] == val:
            result.append(m[0])
    return result


if __name__ == "__main__":
    mappings = []
    components = {}
    comps = {}

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            from_comp, to_comps = line.split("->")

            from_comp_name = from_comp.strip()
            if from_comp_name == "broadcaster":
                components[from_comp_name] = from_comp_name
                from_comp_name_parsed = from_comp_name
            else:
                components[from_comp_name[1:]] = from_comp_name[0]
                from_comp_name_parsed = from_comp_name[1:]

            for comp in to_comps.strip().split(","):
                if comp not in components:
                    components[comp] = "no"

                mappings.append((from_comp_name_parsed, comp.strip()))

    for key, val in components.items():
        if val == "broadcaster":
            comps[key] = Broadcaster(key)
        elif val == "%":
            comps[key] = FlipFlop(key)
        elif val == "&":
            comps[key] = Conjunction(key)
        else:
            comps[key] = Output(key)

    for mapping in mappings:
        comps[mapping[0]].destinations.append(mapping[1])

        if components[mapping[1]] == "&":
            comps[mapping[1]].input_state[mapping[0]] = 0

    pushes = 1000
    for i in range(0, pushes):
        push_button(comps)
        # instructions = [("button", "broadcaster", 0)]
        # while len(instructions) > 0:
        #     # print_instructions([instructions[0]])
        #     from_comp, to_comp, pulse = instructions[0]
        #     result = comps[to_comp].process(pulse, from_comp)

        #     # print(f"{from_comp} {to_comp} {pulse} created {result}")

        #     instructions = [*instructions[1:], *result]

    print("Done")

    total_high = 0
    total_low = pushes
    for c in comps.values():
        # print(f"{c.key} processed {c.high_sent} high")
        # print(f"{c.key} processed {c.low_sent} low")
        total_high = total_high + c.high_sent
        total_low = total_low + c.low_sent

    print(total_high)
    print(total_low)

    print("======== PART 1 ===========")
    print(total_low * total_high)

    print("======== PART 2 ===========")
    for c in comps.values():
        c.reset()

    print(len(comps))

    next_comps = ["rx"]
    seen = ["rx"]
    while len(next_comps) > 0:
        next_up = []
        for n in next_comps:
            results = get_mapped_to(n, mappings)
            next_up.extend(results)

        next_up = list(set(next_up))
        next_up = list(filter(lambda x: x not in seen, next_up))
        seen.extend(next_up)
        next_comps = next_up

    
    import networkx as nx

    graph = nx.Graph()

    for comp in comps.keys():
        graph.add_node(comp)
    
    for mapping in mappings:
        graph.add_edge(mapping[0], mapping[1])

    nx.draw(graph)
    ignorable = list(filter(lambda x: x not in seen, comps.keys()))
    print(len(ignorable))

    for ignore in ignorable:
        comps.pop(ignore)

    for comp in comps.values():
        comp.destinations = list(
            filter(lambda x: x not in ignorable, comp.destinations)
        )

    results = []
    states = []
    values = []
    for i in range(1,1000):
        r = push_button(comps, count=i)
        results.append(r)
        state = list(map(lambda x: x.get_state(), comps.values()))
        states.append(state)

        values.append(len(r))
        

    print(math.lcm(3769, 3833, 3877, 3917))
        # if len(r) > 298:
            # print(i)
        # print("=========================")
        # print(len(r))
        # print(comps["ks"].input_state)
        # print(comps["vr"].input_state)
        # print(comps["pf"].input_state)
        # print(comps["ts"].input_state)
        # print(comps["xd"].input_state)
        # print("----------------------")
        # print(comps["ks"].input_state)
        # print(comps["pm"].input_state)
        # print(comps["dl"].input_state)
        # print(comps["vk"].input_state)
        # print("----------------------")
        # print(comps["dt"].input_state)


    # print(max(values))

    # for i, result in enumerate(results):
    #     print("-----")
    #     print(len(result))
    #     print(result[len(result) - 1])
    #     if i > 1 and i % 2 == 0:
    #         different = []
    #         for j in range(0, len(state)):
    #             if states[i - 2][j] != states[i][j]:
    #                 different.append(f"{list(comps.keys())[j]}={states[i][j]}")
    #         print(different)

    # rx_pulses = 0
    # push_counter = 0
    # while rx_pulses != 1:
    #     if push_counter % 1000000 == 0:
    #         print(push_counter)
    #     push_button(comps)
    #     push_counter = push_counter + 1
    #     lows_recieved = comps["rx"].low_recieved
    #     rx_pulses = rx_pulses - lows_recieved
