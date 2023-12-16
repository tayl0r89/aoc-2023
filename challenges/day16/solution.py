

def get_south_direction(value: str) -> str:
    match value:
        case '\\': 
            return "E"
        case '/': 
            return "W"
        case '|': 
            return "S"

    raise ValueError(f"Cant handle: {value}")

def get_north_direction(value: str) -> str:
    match value:
        case '\\': 
            return "W"
        case '/': 
            return "E"
        case '|': 
            return "N"

    raise ValueError(f"Cant handle: {value}")

def get_east_direction(value: str) -> str:
    match value:
        case '\\': 
            return "S"
        case '/': 
            return "N"
        case '-': 
            return "E"

    raise ValueError(f"Cant handle: {value}")

def get_west_direction(value: str) -> str:
    match value:
        case '\\': 
            return "N"
        case '/': 
            return "S"
        case '-': 
            return "W"

    raise ValueError(f"Cant handle: {value}")
 
def get_next_direction(current: str, value: str):
    match current:
        case 'W': return get_west_direction(value)
        case 'E': return get_east_direction(value)
        case 'N': return get_north_direction(value)
        case 'S': return get_south_direction(value)

    raise ValueError("CANT GET NEXT DIRECTION")

def get_split(dir: str, value: str):
    if (dir == "N" or dir == "S") and value == "-":
        return ["W", "E"]
    elif (dir == "W" or dir == "E") and value == "|":
        return ["N", "S"]

def get_next(coords: tuple[int, int], dir: str):
    if dir == "E":
        return (coords[0] + 1, coords[1])
    if dir == "W":
        return (coords[0] - 1, coords[1])
    if dir == "S":
        return (coords[0], coords[1] + 1)
    if dir == "N":
        return (coords[0], coords[1] - 1)

    raise ValueError("Cant determine next")

def print_grid(grid: list[str], visited):
    for y in range(0, len(grid)):
        to_print = ""
        for x in range(0, len(grid[y])):
            if (x,y) in visited:
                to_print = to_print + "#"
            else:
                to_print = to_print + "."
        print(to_print)


def determine_energy(grid, entry):
    rays = [entry]
    visited = {}

    while len(rays) > 0:
        next_rays = []
        for i, val in enumerate(rays):
            next_loc = get_next(val[0], val[1])
            visited_dirs = visited.get(val[0], [])
            if val[1] in visited_dirs:
                continue
            else:
                visited[val[0]] = [*visited_dirs, val[1]] 
            
            is_dead = False
            if next_loc[0] >= len(grid[0]) or next_loc[0] < 0:
                is_dead = True
            elif next_loc[1] >= len(grid) or next_loc[1] < 0:
                is_dead = True
            
            if is_dead:
                continue
            
            next_space = grid[next_loc[1]][next_loc[0]]
            
            if next_space == ".":
                next_rays.append((next_loc, val[1]))
                continue
                
            split = get_split(val[1], next_space)

            if split:
                for s in split:
                    next_rays.append((next_loc, s))
                continue

            next_direction = get_next_direction(val[1], next_space)
            next_rays.append((next_loc, next_direction))

        rays = [*next_rays]
    return visited



if __name__ == "__main__":    
    grid = []

    with open("input.txt", "r", encoding="utf-8") as file:
        grid = [[*line.strip()] for line in file.readlines()]

    visited = determine_energy(grid, ((-1,0), "E"))
    print("======== PART 1 ============")
    print(f"Energised: {len(visited) - 1}")

    print("======== PART 2 ===========")

    current_max = 0
    print("TESTING TOP")
    for i in range(0, len(grid[0])):
        visited = determine_energy(grid, ((0, i - 1), "S"))
        if len(visited) - 1 > current_max:
            current_max = len(visited) - 1

    print("TESTING BOTTOM")
    for i in range(0, len(grid[0])):
        visited = determine_energy(grid, ((0, len(grid)), "N"))
        if len(visited) - 1 > current_max:
            current_max = len(visited) - 1
    
    print("TESTING LEFT")
    for i in range(0, len(grid)):
        visited = determine_energy(grid, ((-1, i), "E"))
        if len(visited) - 1 > current_max:
            current_max = len(visited) - 1
    
    print("TESTING RIGHT")
    for i in range(0, len(grid)):
        visited = determine_energy(grid, ((len(grid[i]), i), "W"))
        if len(visited) - 1 > current_max:
            current_max = len(visited) - 1

    print(f"Max energy: {current_max}")

    # rays = [((-1,0), "E")]
    # visited = {}

    # while len(rays) > 0:
    #     next_rays = []
    #     for i, val in enumerate(rays):
    #         next_loc = get_next(val[0], val[1])
    #         visited_dirs = visited.get(val[0], [])
    #         if val[1] in visited_dirs:
    #             continue
    #         else:
    #             visited[val[0]] = [*visited_dirs, val[1]] 
            
    #         is_dead = False
    #         if next_loc[0] >= len(grid[0]) or next_loc[0] < 0:
    #             is_dead = True
    #         elif next_loc[1] >= len(grid) or next_loc[1] < 0:
    #             is_dead = True
            
    #         if is_dead:
    #             continue
            
    #         next_space = grid[next_loc[1]][next_loc[0]]
            
    #         if next_space == ".":
    #             next_rays.append((next_loc, val[1]))
    #             continue
                
    #         split = get_split(val[1], next_space)

    #         if split:
    #             for s in split:
    #                 next_rays.append((next_loc, s))
    #             continue

    #         next_direction = get_next_direction(val[1], next_space)
    #         next_rays.append((next_loc, next_direction))

    #     rays = [*next_rays]
    
        
    # print("============= PART 1 =============")
    # print_grid(grid, visited)
    
    # print("")
    # print(f"Energised: {len(visited) - 1}")
        
