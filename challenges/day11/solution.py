import math

def expand_and_get_planets(data, expansion = 1):
    col_expansion = []
    row_expansion = []
    for y, row in enumerate(data):
        contains_planet = False
        for x, item in enumerate(data[y]):
            if data[x][y] == "#":
                contains_planet = True
        col_expansion.append(0 if contains_planet else expansion)
        
        if list(set(row)) == ["."]:
            row_expansion.append(expansion)
        else:
            row_expansion.append(0)
    
    planets = []
    for y, row in enumerate(data):
        for x, item in enumerate(row):
            if item == "#":
                planets.append((x + sum(col_expansion[0:x]), y + sum(row_expansion[0:y])))
    
    return planets

def get_distance(planet_a, planet_b) -> int:
    x_diff = abs(planet_a[0] - planet_b[0])
    y_diff = abs(planet_a[1] - planet_b[1])

    if x_diff == 0:
        return y_diff
    elif y_diff == 0:
        return x_diff
    
    distance = (y_diff * 2) + (x_diff - y_diff)

    # print(f"From {planet_a} to {planet_b} distance {distance}")
    # print(f"Distance {distance}")
    return distance


def calculate_shortest_all_pairs(planets):
    total_distance = 0
    planet_pair_count = 0
    for i, val in enumerate(planets):
        for j in range(i + 1, len(planets)):
            distance = get_distance((val), planets[j])
            total_distance = total_distance + distance
            planet_pair_count = planet_pair_count + 1
    print(f"Total pair count is {planet_pair_count}")
    return total_distance

if __name__ == "__main__":
    x_offset = 0
    y_offset = 0
    data = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            data.append([*line.strip()])
    

    print("===== PART 1 =======")

    planets = expand_and_get_planets(data)
    
    total_distance = calculate_shortest_all_pairs(planets)
    print(total_distance)


    print("===== PART 2 =======")

    planets = expand_and_get_planets(data, expansion=999999)
    
    total_distance = calculate_shortest_all_pairs(planets)
    print(total_distance)
    