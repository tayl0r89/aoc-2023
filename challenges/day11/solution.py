import math

def expand(data):
    additional_cols = []
    for y, row in enumerate(data):
        contains_planet = False
        for x, item in enumerate(data[y]):
            if data[x][y] == "#":
                contains_planet = True
        additional_cols.append(contains_planet)

    expanded = []
    for y, row in enumerate(data):
        new_row = []
        for x, item in enumerate(row):
            if additional_cols[x] == False:
                new_row.extend([".", "."])
            else:
                new_row.append(item)
        expanded.append(new_row)
        if list(set(row)) == ["."]:
            expanded.append(new_row)
    
    return expanded

def get_distance(planet_a, planet_b) -> int:
    x_diff = abs(planet_a[0] - planet_b[0])
    y_diff = abs(planet_a[1] - planet_b[1])

    if x_diff == 0:
        print(f"From {planet_a} to {planet_b} distance {y_diff}")
        return y_diff
    elif y_diff == 0:
        print(f"From {planet_a} to {planet_b} distance {x_diff}")
        return x_diff
    
    distance = (y_diff * 2) + (x_diff - y_diff)

    # print(f"From {planet_a} to {planet_b} distance {distance}")
    # print(f"Distance {distance}")
    return distance


if __name__ == "__main__":
    x_offset = 0
    y_offset = 0
    data = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            data.append([*line.strip()])
    
    expanded = expand(data)

    for i, val in enumerate(expanded):
        print("".join(val))

    
    planets = []
    for y, row in enumerate(expanded):
        for x, item in enumerate(row):
            if item == "#":
                planets.append((x,y))
    
    total_distance = 0
    planet_pair_count = 0
    for i, val in enumerate(planets):
        for j in range(i + 1, len(planets)):
            distance = get_distance((val), planets[j])
            total_distance = total_distance + distance
            planet_pair_count = planet_pair_count + 1
    
    print(total_distance)
    print(planet_pair_count)

    