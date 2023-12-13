
def count_pattern(pattern: str) -> list[int]:
    counts = []
    count = 0
    for i, val in enumerate(pattern):
        if val == '#':
            count = count + 1
        elif count > 0:
            counts.append(count)
            count = 0
    
    if count > 0:
        counts.append(count)

    return counts

def can_match_pattern(pattern: str, input: str, inputs: list[int], next_in_pattern: str | None):
    for i, val in enumerate(input):
        if pattern[i] != "?":
            if val != pattern[i]:
                return False

    merged = input + pattern[len(input):]
    if next_in_pattern:
        merged = merged + next_in_pattern
    counts = count_pattern(merged)

    if counts != inputs:
        if len(inputs) == 1:
            return False

    # if counts[0] != inputs[0]:
    #     print(f"{pattern} compared to {input} made {merged} counted as {counts} for {inputs}")
    return count_pattern(merged)[0] == inputs[0]

def min_length_required(inputs: list[int]):
    return sum(inputs) + max(0, len(inputs) - 1)

class TreeNode():

    pattern: str
    inputs: list[int]
    children: list["TreeNode"] | None
    current: str

    def __init__(self, pattern, inputs, current = "") -> None:
        self.pattern = pattern
        self.inputs = inputs
        self.children = None
        self.current = current
        self.generate_possibilities()

    def count_possibilities(self):
        if len(self.children) == 0 and len(self.inputs) == 0:
            # print(self.current)
            return 1
        
        return sum(list(map(lambda x: x.count_possibilities(), self.children)))

    def generate_possibilities(self):
        if len(self.inputs) == 0:
            self.children = []
            return
        
        # Next length required
        next_input = self.inputs[0]
        next_pattern = ['#' for i in range(0,next_input)]

        # Min space required by whole remaining input pattern
        remaining_length_required = 0 if len(self.inputs) == 1 else min_length_required(self.inputs[1:])
        # possible space
        available_space = len(self.pattern) - remaining_length_required
        available_places = available_space - len(next_pattern) + 1
        # print(f"Available space: {available_space}")
        # print(f"Available places for {next_input} is {available_places}")
        self.children = []
        for i in range(0, available_places):
            # Pre pad as necessary
            patt = ["." for i in range(0, i)]
            patt.extend(next_pattern)
            next_patt = "".join(patt)

            if len(next_patt) < len(self.pattern):
                next_patt = next_patt + "."
            
            # If this works then we add it
            next_in_pattern = None
            if len(self.pattern) > len(next_patt):
                next_in_pattern = self.pattern[len(next_patt)]

            if can_match_pattern(self.pattern, next_patt, self.inputs, next_in_pattern):
                current = self.current + next_patt
                self.children.append(TreeNode(self.pattern[len(next_patt):], self.inputs[1:], current=current))


if __name__ == "__main__":
    data = None
    with open("input.txt", "r", encoding="utf-8") as file:
        data = [l for l in file.readlines()]
    
    part_1_total = 0
    for row in data:
        pattern, input = row.split(" ")
        input_lengths = list(map(int, input.strip().split(",")))
        root_node = TreeNode(pattern, input_lengths)

        possibilities = root_node.count_possibilities()
        print(f"Pattern {pattern} {input_lengths} has {possibilities}")
        part_1_total = part_1_total + possibilities
        # break
        
    print(f"Part 1: {part_1_total}")

    part_2_total = 0
    for row in data:
        pattern, input = row.split(" ")
        expanded_pattern = ".".join([pattern.strip() for i in range(0, 5)])
        expanded_input = ",".join([input.strip() for i in range(0,5)])

        input_lengths = list(map(int, expanded_input.strip().split(",")))
        root_node = TreeNode(expanded_pattern, input_lengths)
        possibilities = root_node.count_possibilities()
        print(f"Expanded Pattern {expanded_pattern} {input_lengths} has {possibilities}")
        part_2_total = part_2_total + possibilities
    
    print(f"Part 2: {part_2_total}")



