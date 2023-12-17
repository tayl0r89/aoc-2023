
def get_value_at(grid, coord):
    if coord[0] < 0 or coord[0] >= len(grid):
        return None
    
    if coord[1] < 0 or coord[1] >= len(grid[0]):
        return None
    
    return grid[coord[1]][coord[0]]
 
def get_next_directions(grid, visited, path):
    endpoint = path[len(path) - 1]
    route = list(map(lambda x: (x[0], x[1]), path))
    potential_next = []
    potential_next.append((endpoint[0] + 1, endpoint[1], 'E'))
    potential_next.append((endpoint[0] - 1, endpoint[1], 'W'))
    potential_next.append((endpoint[0], endpoint[1] - 1, 'N'))
    potential_next.append((endpoint[0], endpoint[1] + 1, 'S'))

    path_options = []
    for potential in potential_next:
        if f"{(potential[0], potential[1])}-{potential[2]}" in visited:
            continue

        if (potential[0], potential[1]) in route:
            continue
        
        if potential[0] < 0 or potential[1] < 0:
            continue

        val = get_value_at(grid, potential)

        if not val:
            continue

        if len(path[-3:]) == 3:
            directions = list(map(lambda x: x[2], path[-3:]))
            unique = set(directions)
            if len(unique) == 1 and list(unique)[0] == potential[2]:
                continue

        path_options.append((potential, val))
    
    if len(path_options) == 4:
        for coord in list(map(lambda x: x[0], path_options)):
            if coord in path:
                raise ValueError("VERY BAD")

    return path_options

class Node:

    def __init__(self, grid, coords, heading, parent = None) -> None:
        self.parent = parent
        self.node_weight = get_value_at(grid, coords)
        self.coords = coords
        self.heading = heading

    def key(self):
        return f"{self.coords}-{self.heading}"

    def take_cheapest(self, visited, grid):
        current_path = get_node_path(self)
        choices = get_next_directions(grid, visited, current_path)
        if len(choices) == 0:
            return None

        sorted_choices = sorted(choices, key=lambda x: x[1])
        choice = sorted_choices[0]
        choice_coords = (choice[0][0], choice[0][1])
        choice_heading = choice[0][2]
        result_node = Node(grid, choice_coords, choice_heading, self)
        return result_node


def get_node_path(node: Node):
    path = []
    tracker = node
    while tracker is not None:
        path.append((tracker.coords[0], tracker.coords[1], tracker.heading))
        tracker = tracker.parent
    
    path.reverse()
    return path

def get_total_node_value(node: Node):
    total = 0
    tracker = node
    while tracker:
        total = total + tracker.node_weight
        tracker = tracker.parent
    
    return total


def get_route_str(dir):
    if dir is None:
        return "-"

    match dir:
        case "W": return "<"
        case "E": return ">"
        case "S": return "v"
        case "N": return "^"

path_index = -1
if __name__ == "__main__":
    grid = []

    with open("input.txt", "r", encoding="utf-8") as file:
        grid = [list(map(int,[*line.strip()])) for line in file.readlines()]
    
    # target = (len(grid) - 1, len(grid[0]) -1)
    target = (2,0)
    total = sum(map(lambda x: sum(x), grid))

    root = Node(grid, (0,0), None)
    nodes = {}
    nodes[root.key()] = root
    to_explore = [root]

    not_found = True
    while not_found:
        
        if len(to_explore) == 0:
            raise ValueError("Failed")

        print("==========")
        for val in to_explore:
            print(f"{val.coords} - {val.node_weight}")
        expand = to_explore[0]
        next_node = expand.take_cheapest(nodes, grid)

        if next_node:
            # We have one so process
            if next_node.coords == target:
                not_found = False

            to_explore.append(next_node)
            to_explore = sorted(to_explore, key=lambda x: x.node_weight)
            nodes[next_node.key()] = next_node
        else:
            # No options so remove this node from nodes to explore
            to_explore = to_explore[1:]

        
    result = list(filter(lambda x: x.coords == target, nodes.values()))[0]
    print("=========================")
    print(result)
    result_path = get_node_path(result) 
    print(result_path)
    print(get_total_node_value(result))

    result_dirs = {}
    for val in result_path:
        result_dirs[(val[0], val[1])] = val[2]

    for y, line in enumerate(grid):
        to_print = []
        for x, val in enumerate(line):
            if (x,y) in result_dirs:
                to_print.append(get_route_str(result_dirs[(x,y)]))
            else:
                to_print.append(str(val))
        print("".join(to_print))
            



 