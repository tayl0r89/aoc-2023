import math

def matches_target(test: str, target: str | None) -> bool:
    if target:
        return test == target
    
    return test.endswith("Z")

def traverse(
    routes: dict[str, tuple[str,str]], 
    directions: list[str], 
    start_node: str, 
    end_node: str | None = None, 
    direction: int = 0
):
    target = end_node
    current_node = start_node
    step_count = 0
    while not matches_target(current_node, target):
        take = directions[direction]
        dir = 0 if take == "L" else 1
        current_node = routes[current_node][dir]
        direction = direction + 1 if direction + 1 < len(directions) else 0
        step_count = step_count + 1

    return (step_count, direction, current_node)


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as file:
        data = file.readlines()
        directions = [*data[0].strip()]
        routes = {}
        for i in range(2, len(data)):
            node_to_route = data[i].strip().split("=")
            parts = node_to_route[1].split(",")
            left = parts[0].strip()[1:]
            right = parts[1].strip()[:-1]
            route = (left, right)
            routes[node_to_route[0].strip()] = route
        
        ### PART 1
        step_count = traverse(routes, directions, "AAA", "ZZZ")
        print(f"Part 1 solution is: {step_count[0]}")

        data = list(filter(lambda x: x.endswith("A"), routes.keys()))
        possible_ends = list(filter(lambda x: x.endswith("Z"), routes.keys()))

        counts = []
        for val in data:
            # Pre verified against input that all routes end at the end of direction string
            # Pre verified that all inputs have one single output
            # Pre verified that once output is reached, it reaches the same output in the same step count.
            # So LCM can be used after one traversal.
            count, dirs, node = traverse(routes, directions, val)        
            counts.append(count)

        print(f"Part 2 solution is: {math.lcm(*counts)}")
        