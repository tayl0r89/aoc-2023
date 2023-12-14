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


def arr_to_flip_bit(point: int, binary_diff: int, row_num: int) -> tuple[int,int]:
    y = row_num
    x = to_position(binary_diff)
    
    return (x,y)



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
                non_matches.append((i, bin_comp, row_num))
                if len(non_matches) > 1:
                    break
        
        if len(non_matches) == 0:
            count = count + (i * mult)
        elif len(non_matches) == 1:
            non_match_rows.append(non_matches[0])

    if len(non_match_rows) == 1:
        potential_change.append(arr_to_flip_bit(non_match_rows[0][0], non_match_rows[0][1], non_match_rows[0][2]))

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

    for pane in data:
        vertical_line_count, v_changes = get_vertical_line_symettry(pane)
        horizontal_line_count, h_changes = get_horizontal_line_symettry(pane)

        print(f"Before flip {vertical_line_count} and {horizontal_line_count}")

        if len(v_changes) > 0:
            x = v_changes[0][0]
            y = v_changes[0][1]
            to_flip = pane[y][x]
            to_value = "." if to_flip == "#" else "#"
            pane[y][x] = to_value
            print(f"Flipping for vert reflection {(x,y)} from {to_flip} to {to_value}")
            vertical_line_count, v_changes = get_vertical_line_symettry(pane)
            part_2_total = part_2_total + vertical_line_count
            print(f"Adding new vertical of {vertical_line_count}")
        elif len(h_changes) > 0:
            # Flip for transpose?
            x = h_changes[0][1]
            y = h_changes[0][0]
            to_flip = pane[y][x]
            to_value = "." if to_flip == "#" else "#"
            pane[y][x] = to_value
            print(f"Flipping for horiz reflection {(x,y)} from {to_flip} to {to_value}")
            horizontal_line_count, h_changes = get_horizontal_line_symettry(pane)
            part_2_total = part_2_total + horizontal_line_count
            print(f"Adding new horizontal of {horizontal_line_count}")

    print(f"Part 2: {part_2_total}")