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
            result.append(math.pow(val, i))
        else:
            result.append(0)
    return result


def compare_binary(before: list[str], after: list[str]) -> int:
    before_bin = to_binary_arr([0 if d == "." else 1 for d in before])
    after_bin = to_binary_arr([0 if d == "." else 1 for d in after])
    before_bin.reverse()
    to_test = min(len(before_bin), len(after_bin))
    before_count = 0
    after_count = 0
    for i in range(0, to_test):
        before_count = before_count + before_bin[i]
        after_count = after_count + after_bin[i]
    
    difference = abs(before_count - after_count)
    return difference

def to_position(bin: int) -> int:
    if bin == 1:
        return 0
    if bin == 2:
        return 1
    return math.sqrt(bin)

def get_vertical_line_symettry(pane: list[list[str]], mult: int = 1) -> tuple[int, tuple[int,int]]:
    count = 0
    potential_change = []
    non_match_rows = []
    for i in range(1, len(pane[0])):
        non_matches = []
        for row_num, row in enumerate(pane):
            before = row[:i]
            after = row[i:]
            bin_comp = compare_binary(before, after)
            if not bin_comp == 0:
                # position = math.sqrt(bin_comp)
                non_matches.append((i * mult, bin_comp))
                if len(non_matches) > 1:
                    break
        
        if len(non_matches) == 0:
            count = count + (i * mult)
        elif len(non_matches) == 1:
            non_match_rows.append(non_matches[0])

    if len(non_match_rows) == 1:
        potential_change.append((non_match_rows[0][0], to_position(non_match_rows[0][1])))

    print(non_matches)
    return (count, potential_change)

def transpose(pane: list[list[str]]) -> list[list[str]]:
    data = []
    for i in range(0, len(pane[0])):
        new_row = []
        for row in pane:
            new_row.append(row[i])
        data.append(new_row)
    return data

def get_horizontal_line_symettry(pane: list[list[str]]) -> tuple[int, tuple[int,int]]:
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
        if i == 73:
            print_pane(pane)
            
        vertical_line_count, v_changes = get_vertical_line_symettry(pane)
        horizontal_line_count, h_changes = get_horizontal_line_symettry(pane)

        if i == 73:
            print(v_changes)
            print(h_changes)
            break

        if len(v_changes) > 0:
            index_of_reflection = v_changes[0][0]
            print(f"Found potential new vertical line at {index_of_reflection}")
            part_2_total = part_2_total + index_of_reflection
        elif len(h_changes) > 0:
            # Flip for transpose?
            index_of_reflection = h_changes[0][0]
            print(f"Found potential new horizontal line at {index_of_reflection}")
            part_2_total = part_2_total + index_of_reflection
        else:
            raise ValueError(f"No flip found at {i}")

    print(f"Part 2: {part_2_total}")