from functools import cache


def count_pattern(pattern: str) -> list[int]:
    counts = []
    count = 0
    for i, val in enumerate(pattern):
        if val == "#":
            count = count + 1
        elif count > 0:
            counts.append(count)
            count = 0

    if count > 0:
        counts.append(count)

    return counts


def inputs_to_key(pattern: str, vals: list[int]) -> str:
    return pattern + "/" + ",".join(list(map(str, vals)))


def can_match_pattern(
    pattern: str, input: str, inputs: list[int], next_in_pattern: str | None
):
    for i, val in enumerate(input):
        if pattern[i] != "?":
            if val != pattern[i]:
                return False

    merged = input + pattern[len(input) :]
    if next_in_pattern:
        merged = merged + next_in_pattern
    counts = count_pattern(merged)

    if counts != inputs:
        if len(inputs) == 1:
            return False

    return count_pattern(merged)[0] == inputs[0]


def min_length_required(inputs: list[int]):
    return sum(inputs) + max(0, len(inputs) - 1)


def val_to_inputs(input: str) -> list[int]:
    return list(map(int, input.strip().split(",")))


@cache
def determine_possibilities(pattern, inputs_val) -> int:
    inputs = val_to_inputs(inputs_val)

    # Next length required
    next_input = inputs[0]
    next_pattern = ["#" for i in range(0, next_input)]

    # Min space required by whole remaining input pattern
    remaining_length_required = (
        0 if len(inputs) == 1 else min_length_required(inputs[1:])
    )
    # possible space
    available_space = len(pattern) - remaining_length_required
    available_places = available_space - len(next_pattern) + 1

    total_possibilities = 0
    for i in range(0, available_places):
        # Pre pad as necessary
        patt = ["." for i in range(0, i)]
        patt.extend(next_pattern)
        next_patt = "".join(patt)

        if len(next_patt) < len(pattern):
            next_patt = next_patt + "."

        # If this works then we add it
        next_in_pattern = None
        if len(pattern) > len(next_patt):
            next_in_pattern = pattern[len(next_patt)]

        if can_match_pattern(pattern, next_patt, inputs, next_in_pattern):
            if len(inputs) == 1:
                total_possibilities = total_possibilities + 1
            else:
                input_str = ",".join(list(map(str, inputs[1:])))
                child_possibilities = determine_possibilities(
                    pattern[len(next_patt) :], input_str
                )

                total_possibilities = total_possibilities + child_possibilities

    return total_possibilities


if __name__ == "__main__":
    data = None
    with open("input.txt", "r", encoding="utf-8") as file:
        data = [l for l in file.readlines()]

    part_1_total = 0
    for row in data:
        pattern, input = row.split(" ")
        possibilities = determine_possibilities(pattern, input)
        # print(f"Pattern {pattern} {input} has {possibilities}")
        part_1_total = part_1_total + possibilities
        # break

    print(f"Part 1: {part_1_total}")

    part_2_total = 0
    for i, row in enumerate(data):
        pattern, input = row.split(" ")
        expanded_pattern = "?".join([pattern.strip() for i in range(0, 5)])
        expanded_input = ",".join([input.strip() for i in range(0, 5)])

        possibilities = determine_possibilities(expanded_pattern, expanded_input)
        print(
            f"Expanded Pattern {expanded_pattern} {expanded_input} has {possibilities}"
        )
        part_2_total = part_2_total + possibilities

    print(f"Part 2: {part_2_total}")