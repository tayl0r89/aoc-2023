import math


def compare(before: list[str], after: list[str]) -> bool:
    to_test = min(len(before), len(after))
    before.reverse()
    for i in range(0, to_test):
        if before[i] != after[i]:
            return False
    return True


def to_binary_arr(arr: list[int]) -> list[int]:
    result = []
    for i, val in enumerate(arr):
        if val == 1:
            result.append(int(math.pow(2, i)))
        else:
            result.append(0)
    return result


def compare_binary(before: list[str], after: list[str]) -> int:
    to_test = min(len(before), len(after))
    before_test = before[-to_test:]
    after_test = after[0: to_test]
    before_test.reverse()
    differences = 0
    different_at = None
    for i in range(0, to_test):
        if before_test[i] != after_test[i]:
            differences = differences + 1
            different_at = i

    return (differences, different_at)


def get_vertical_line_symettry(
    pane: list[list[str]], mult: int = 1
) -> tuple[int, list[tuple[int, int]]]:
    count = 0
    potential_change = []
    possibile_points_of_reflection = []
    for i in range(1, len(pane[0])):
        print(" ")
        non_matches = []
        for row in pane:
            before = row[:i]
            after = row[i:]
            differences, different_at = compare_binary(before, after)
            if differences > 0:
                non_matches.append((i * mult, differences, different_at))

        if len(non_matches) == 0:
            count = count + (i * mult)
        elif len(non_matches) == 1:
            possibile_points_of_reflection.append(non_matches[0])

    if len(possibile_points_of_reflection) == 1:
        potential_change.append(
            (
                possibile_points_of_reflection[0][0],
                possibile_points_of_reflection[0][1],
            )
        )

    return (count, potential_change)


def transpose(pane: list[list[str]]) -> list[list[str]]:
    data = []
    for i in range(0, len(pane[0])):
        new_row = []
        for row in pane:
            new_row.append(row[i])
        data.append(new_row)
    return data


def get_horizontal_line_symettry(pane: list[list[str]]) -> tuple[int, tuple[int, int]]:
    transposed = transpose(pane)
    return get_vertical_line_symettry(transposed, mult=100)


def print_pane(pane: list[list[str]]) -> None:
    for line in pane:
        print("".join(line))


if __name__ == "__main__":
    data = []
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
        pane = []
        for line in lines:
            if line == "":
                data.append(pane)
                pane = []
            else:
                pane.append([*line])

        if len(pane) > 0:
            data.append(pane)

    part_1_total = 0
    part_2_total = 0
    for pane in data:
        vertical_line_count, v_changes = get_vertical_line_symettry(pane)
        horizontal_line_count, h_changes = get_horizontal_line_symettry(pane)
        part_1_total = part_1_total + vertical_line_count
        part_1_total = part_1_total + horizontal_line_count
    print(f"Part 1: {part_1_total}")

    for i, pane in enumerate(data):
        print(" ")
        print(f"=========== pattern {i} ============")
        print(" ")
        print_pane(pane)
        print(" ")

        print("PROCESSING VERTICAL")
        vertical_line_count, v_changes = get_vertical_line_symettry(pane)
        print(" ")
        print("PROCESSING HORIZONTAL")
        horizontal_line_count, h_changes = get_horizontal_line_symettry(pane)

        if len(v_changes) == 1:
            index_of_reflection = v_changes[0][0]
            print(f"Found potential new vertical line at {index_of_reflection}")
            part_2_total = part_2_total + index_of_reflection
        elif len(h_changes) == 1:
            # Flip for transpose?
            index_of_reflection = h_changes[0][0]
            print(f"Found potential new horizontal line at {index_of_reflection}")
            part_2_total = part_2_total + index_of_reflection
        else:
            raise ValueError(f"No flip found at {i}")

    print(f"Part 2: {part_2_total}")