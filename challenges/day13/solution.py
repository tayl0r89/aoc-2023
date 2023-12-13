
def compare(before: list[str], after: list[str]) -> bool:
    to_test = min(len(before), len(after))
    before.reverse()
    for i in range(0, to_test):
        if before[i] != after[i]:
            return False
    return True

def get_vertical_line_symettry(pane: list[list[str]], mult: int = 1) -> int:
    count = 0
    for i in range(1, len(pane[0])):
        all_rows_work = True
        for row in pane:
            before = row[:i]
            after = row[i:]
            if not compare(before, after):
                all_rows_work = False
                break
        
        if all_rows_work:
            count = count + (i * mult)
    return count

def transpose(pane: list[list[str]]) -> list[list[str]]:
    print_pane(pane)
    print(len(pane))
    data = []
    for i in range(0, len(pane[0])):
        new_row = []
        for row in pane:
            print(row)
            new_row.append(row[i])
        data.append(new_row)
    return data

def get_horizontal_line_symettry(pane: list[list[str]]) -> int:
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
    for pane in data:
        vertical_line_count = get_vertical_line_symettry(pane)
        horizontal_line_count = get_horizontal_line_symettry(pane)
        part_1_total = part_1_total + vertical_line_count
        part_1_total = part_1_total + horizontal_line_count
    
    print(f"Part 1: {part_1_total}")