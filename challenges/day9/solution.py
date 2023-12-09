def diff(a: int, b: int) -> int:
    return abs(a - b) * (-1 if a > b else 1)

def next_sequence(seq: list[int]) -> list[int]:
    return [diff(seq[i-1], seq[i]) for i in range(1, len(seq))]

def get_next(seq: list[int]) -> int:
    last = seq[len(seq) - 1]
    if seq == [0 for i in range(0, len(seq))]:
        return 0
    
    next_seq = next_sequence(seq)
    next_val_of_prev = get_next(next_seq)
    return last + next_val_of_prev

def get_prev(seq: list[int]) -> int:
    first = seq[0]
    if seq == [0 for i in range(0, len(seq))]:
        return 0
    
    next_seq = next_sequence(seq)
    before_val_of_prev = get_prev(next_seq)
    return first - before_val_of_prev

if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as file:
        data = [list(map(int, l.strip().split(" "))) for l in file.readlines()]

    part_1_total = 0
    part_2_total = 0
    for sequence in data:
        result = get_next(sequence)
        before_result = get_prev(sequence)
        part_1_total = part_1_total + result
        part_2_total = part_2_total + before_result
    
    print(f"Part 1: {part_1_total}")
    print(f"Part 2: {part_2_total}")



    