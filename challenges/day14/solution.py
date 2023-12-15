
def add_line_to_columns(columns: list[list[str]], line: str, index: int) -> None:
    input = [*line.strip()]
    for i, val in enumerate(input):
        match val:
            case "O":
                columns[i].append("O")
                continue
            case "#":
                for _ in range(0, index - len(columns[i])):
                    columns[i].append(".")
                columns[i].append("#")
                continue

def print_sol(data: list[str]) -> None:
    for line in data:
        print(line)   

def columns_to_lines(columns: list[list[str]]) -> list[str]:
    result_lines = []
    for i in range(0, len(columns[0])):
        result_line = ""
        for j in range(0, len(columns)):
            result_line = result_line + columns[j][i]
        result_lines.append(result_line)
    return result_lines   

def determine_weight(data: list[str]) -> int:
    row_count = len(data)
    total = 0
    for i in range(0, row_count):
        for val in [*data[i]]:
            if val == "O":
                total = total + row_count - i
    
    return total


def squash_line_left(line: str) -> str:
    parts = line.split("#")
    to_merge = list(map(lambda x: "".join(sorted(x, reverse=True)), parts))
    return "#".join(to_merge)

def squash_line_right(line: str) -> str:
    to_squash = [*line]
    to_squash.reverse()
    to_squash = "".join(to_squash)
    result = squash_line_left(to_squash)
    result = [*result]
    result.reverse()
    return "".join(result)

def roll_north(data: list[str]) -> list[str]:
    results = []
    num_of_rows = len(data)
    num_of_columns = len(data[0])
    for i in range(0, num_of_rows):
        results.append("")

    for i in range(0, num_of_columns):
        line_to_squash = ""
        for j in range(0, num_of_rows):
            line_to_squash = line_to_squash + data[j][i]
    
        squashed = squash_line_left(line_to_squash)
        for index, val in enumerate(squashed):
            results[index] = results[index] + val

    return results

def roll_west(data: list[str]) -> list[str]:
    results = []
    for line in data:
        squashed = squash_line_left(line)
        results.append(squashed)
    return results

def roll_east(data: list[str]) -> list[str]:
    results = []
    for line in data:
        squashed = squash_line_right(line)
        results.append(squashed)
    return results

def roll_south(data: list[str]) -> list[str]:
    results = []
    num_of_rows = len(data)
    num_of_columns = len(data[0])
    for i in range(0, num_of_rows):
        results.append("")

    for i in range(0, num_of_columns):
        line_to_squash = ""
        for j in range(0, num_of_rows):
            line_to_squash = line_to_squash + data[j][i]
    
        squashed = squash_line_right(line_to_squash)
        for index, val in enumerate(squashed):
            results[index] = results[index] + val

    return results

def cycle(data: list[str]) -> list[str]:
    result = roll_north(data)
    result = roll_west(result)
    result = roll_south(result)
    return roll_east(result)

def print_lines(lines: list[str]) -> None:
    for line in lines:
        print(line)

def one_line(data: list[str]) -> str:
    result = ""
    for val in data: 
        result = result + val
    return result

if __name__ == "__main__":
    lines = []
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = [l.strip() for l in file.readlines()]


    print("=====PART 1=====")
    result = roll_north(lines)
    print_sol(result)
    print(determine_weight(result))
    print("================")



    print("======PART 2=======")
    
    result = lines
    cycles = 0
    total = 1000000000
    results = {}
    sequences = []
    current_sequence = []
    ended = 0
    for i in range(0,10000):
        if i > 0 and i % 1000 == 0:
            print(1000 * i)

        result = cycle(result)
        single_line = one_line(result)

        last_seen = results.get(single_line, None)

        if last_seen:
            print(f"Line {i} was last seen at {last_seen}")
            if len(current_sequence) == 0:
                current_sequence.append(last_seen)
            elif len(current_sequence) > 0:
                last = current_sequence[len(current_sequence) - 1]
                if last_seen == last + 1:
                    current_sequence.append(last_seen)
                elif last_seen == current_sequence[0]:
                    if len(sequences) > 0:
                        if sequences[0] == current_sequence:
                            print("WE HAVE A LOOP")
                            ended = i
                            break
                    else:
                        sequences.append(current_sequence)
                        current_sequence = [last_seen]

        else:
            results[single_line] = i

    print(f"We ended at {ended}")
    print(f"With sequence {current_sequence}")
    
    left_to_do = total - ended

    print(f"We had {left_to_do} cycles left")

    after_cycles = left_to_do % len(sequences[0])
    print(f"After cycling sequences we would have had {after_cycles}")

    for i in range(0, after_cycles):
        result = cycle(result)
    
    print_sol(result)
    print(determine_weight(result))






    lines = []
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = [l.strip() for l in file.readlines()]
