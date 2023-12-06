
class InstructionMap():

    bounds: list[tuple[int, int, int]]

    def __init__(self, bounds):
        self.bounds = sorted(bounds)
        print(self.bounds)
    
    def get_result(self, val: int) -> int | None:
        if val < self.bounds[0][0]:
            return val

        if val > self.bounds[len(self.bounds) - 1][0] + self.bounds[len(self.bounds) - 1][2]:
            return val
        
        for bound in self.bounds:
            if val >= bound[0] and val < bound[0] + bound[2]: 
                return bound[1] + (val - bound[0])
        
        return val
    
    def get_range_results(self, val: tuple[int,int]) -> list[tuple[int, int]]:
        results = []
        i = 0
        start = val[0]
        count = val[1]
        
        print(f"Processing from {start} to {start + count}")
        print(f"Bounds are {self.bounds}")
        i = 0
        while i < len(self.bounds) and count > 0:
            sec_start = self.bounds[i][0]
            sec_dest = self.bounds[i][1]
            sec_end = self.bounds[i][0] + self.bounds[i][2]
            print(f"Assessing bounds {(sec_start, sec_end)}")

            if start < sec_start:
                before_length = sec_start - start
                to_add_size = min(before_length, count)
                # Use the normal value here as its out of mapping range
                print(f"Adding {start} for {to_add_size} before the section")
                results.append((start, to_add_size))
                count = count - to_add_size
                start = start + to_add_size
                print(f"Start is now {start} and count is now {count}")
            
            if start >= sec_start and start < sec_end:
                start_offset = start - sec_start
                to_add_size = min(count, sec_end - sec_start)
                # Use destination here
                print(f"Adding {sec_dest + start_offset} for {to_add_size}")
                results.append((sec_dest + start_offset, to_add_size))
                start = sec_start + to_add_size
                count = count - to_add_size
            
            i = i + 1
        
        if count > 0:
            print(f"Adding {start} for {count} at the end")
            results.append((start, count))
        
        return results

def parse_numbers(line: str) -> list[int]:
    return [int(x) for x in line.strip().split(" ")]

def parse_dict(section_data: list[str]):
    data = []
    section_name = section_data[0][:-5]

    for line in section_data[1:]:
        dest, source, size = parse_numbers(line)
        data.append((source, dest, size))
        
    return section_name, InstructionMap(data)

def get_value(maps: InstructionMap, val: int) -> int:
    return maps.get_result(val)


def get_location(instructions: dict, seed) -> int:
    soil = get_value(instructions["seed-to-soil"], seed)
    fert = get_value(instructions["soil-to-fertilizer"], soil)
    water = get_value(instructions["fertilizer-to-water"], fert)
    light = get_value(instructions["water-to-light"], water)
    temp = get_value(instructions["light-to-temperature"], light)
    humid = get_value(instructions["temperature-to-humidity"], temp)
    location = get_value(instructions["humidity-to-location"], humid)
    return location

def flat(inp):
    data = []
    for val in inp:
        data.extend(val)
    return data

def get_location_tuples(instructions: dict, seed_pair: tuple[int,int]):
    soils = instructions["seed-to-soil"].get_range_results(seed_pair)
    ferts = flat([instructions["soil-to-fertilizer"].get_range_results(x) for x in soils])
    waters = flat([instructions["fertilizer-to-water"].get_range_results(x) for x in ferts])
    lights = flat([instructions["water-to-light"].get_range_results(x) for x in waters])
    temps = flat([instructions["light-to-temperature"].get_range_results(x) for x in lights])
    humids = flat([instructions["temperature-to-humidity"].get_range_results(x) for x in temps])
    locs = flat([instructions["humidity-to-location"].get_range_results(x) for x in humids])
    return locs


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
        locs = get_location_tuples(instructions, pair)
        results.append(min(locs))
        
    
    print(results)
    print(min(results))
        