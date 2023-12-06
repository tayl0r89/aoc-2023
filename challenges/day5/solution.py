

def to_from_to(val):
    return (val[0], val[0] + val[2] - 1, val[1])


def get_intersection(t1, t2):
    if t1[1] < t2[0]:
        return None
    if t1[0] > t2[1]:
        return None

    return (max(t1[0], t2[0]), min(t1[1], t2[1]))

def get_ranges(input, ranges):
    data = input
    results = []
    ranges = sorted(ranges)

    if data[0] > ranges[len(ranges) - 1][1]:
        results.append(data)
        return results

    for range in ranges:
        if data[0] < range[0]:
            if data[1] < range[1]:
                results.append((data[0], data[1]))
                return results
            else:
                results.append((data[0], range[0] - 1))
                data = (range[0], data[1])

        intersection = get_intersection(data, range)
        if intersection:
            offset = intersection[0] - range[0]
            intersection_length = intersection[1] - intersection[0]
            mapped = range[2] + offset
            mapped_end = mapped + intersection_length
            results.append((mapped, mapped_end))
            if intersection[1] + 1 >= data[1]:
                return results
            data = (intersection[1] + 1, data[1])

    if data[0] != data[1] and data[0] + 1 > ranges[len(ranges) - 1][1]:
        results.append((data[0] + 1, data[1]))

    return results


class InstructionMap():

    def __init__(self, bounds):
        self.ranges = sorted(list(map(to_from_to, bounds)))
    
    def get_range_results(self, val: tuple[int,int]) -> list[tuple[int, int]]:
        return get_ranges(val, self.ranges)

def parse_numbers(line: str) -> list[int]:
    return [int(x) for x in line.strip().split(" ")]

def parse_dict(section_data: list[str]):
    data = []
    section_name = section_data[0][:-5]

    for line in section_data[1:]:
        dest, source, size = parse_numbers(line)
        data.append((source, dest, size))
        
    return section_name, InstructionMap(data)

def flat(inp):
    data = []
    for val in inp:
        data.extend(val)
    return data

def get_location_tuples(instructions: dict, seed_pair: tuple[int,int]):
    soils = sorted(instructions["seed-to-soil"].get_range_results((seed_pair[0], seed_pair[0] + seed_pair[1] - 1)))
    ferts = sorted(flat([instructions["soil-to-fertilizer"].get_range_results(x) for x in soils]))
    waters = sorted(flat([instructions["fertilizer-to-water"].get_range_results(x) for x in ferts]))
    lights = sorted(flat([instructions["water-to-light"].get_range_results(x) for x in waters]))
    temps = sorted(flat([instructions["light-to-temperature"].get_range_results(x) for x in lights]))
    humids = sorted(flat([instructions["temperature-to-humidity"].get_range_results(x) for x in temps]))
    locs = sorted(flat([instructions["humidity-to-location"].get_range_results(x) for x in humids]))
    return {
        "soil": soils,
        "fert": ferts,
        "water": waters,
        "light": lights,
        "temp": temps,
        "humid": humids,
        "location": locs
    }


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as file:
        data = file.read().split("\n\n")

    instructions = {}

    for section in data:
        section_data = section.split("\n")
        section_name = section_data[0].strip()
        if section_name.startswith("seeds:"):
            _, seed_list = section_name.split(":")
            seeds = parse_numbers(seed_list)
            instructions["seeds"] = seeds

            seed_pairs = []
            for i,_ in enumerate(seeds):
                if i % 2 == 0:
                    seed_pairs.append((seeds[i], seeds[i+1]))
            instructions["seed_pairs"] = seed_pairs
        else:
            name, data = parse_dict(section_data)
            instructions[name] = data

    results = []

    for pair in seed_pairs:
        resu = get_location_tuples(instructions, pair)
        locs = resu["location"]
        min_loc = min(locs)
        results.append(min_loc)

        print(f"Working on {pair}")
        for key, val in resu.items():
            print(f"{key}: Min: {min(val)}")
        print("=====================================")
        
    print(min(results))
        