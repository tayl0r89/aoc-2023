
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def to_key(x: int,y: int) -> str:
    return f"{x},{y}"

def read_input(data: list[str]) -> tuple[dict[str, int], dict[str, str]]:
    """Read input and return lookup of numbers and lookup of symbols"""
    numbers = {}
    symbols = {}
    for y, line in enumerate(data):
        current_number = None
        starting = None
        for x, character in enumerate(line.strip()):
            if character in digits:
                # if the character is a digit
                if x == (len(line.strip()) - 1):
                    # if end of line
                    current_number = current_number + character
                    numbers[(starting,y)] = current_number
                    current_number=None
                    starting=None
                elif current_number is None:
                    current_number = character
                    starting = x
                else:
                    current_number = current_number + character
            elif character == ".":
                if current_number is not None:
                    numbers[(starting,y)] = current_number
                current_number = None
                starting = None
            else:
                symbols[(x,y)] = character
                if current_number is not None:
                    numbers[(starting,y)] = current_number
                    current_number = None
                    starting = None

    return (numbers, symbols)


def does_have_symbol(word: str, coords: tuple[int, int], symbols: dict[tuple[int, int], str]) -> bool:
    x, y = coords
    x_start = x - 1 
    x_end = x_start + len(word) + 1
    for i in range(x_start, x_end + 1):
        if (i, y-1) in symbols:
            return True
        if (i, y+1) in symbols:
            return True

    before_or_after = (x_start, y) in symbols or (x_end, y) in symbols
    return before_or_after

def get_adjacent_numbers(coord: tuple[int,int], words: dict[tuple[int,int], str], max_x: int) -> bool:
    results: list[int] = []
    for x in range(0, max_x):
        if (x, coord[1] - 1) in words:
            value = words[(x, coord[1] - 1)]
            value_x = x
            value_x_end = x + len(value)
            if coord[0] >= (value_x - 1) and coord[0] <= (value_x_end):
                results.append(value)
        
        if (x, coord[1] + 1) in words:
            value = words[(x, coord[1] + 1)]
            value_x = x
            value_x_end = x + len(value)
            if coord[0] >= (value_x - 1) and coord[0] <= (value_x_end):
                results.append(value)
            
        if (x, coord[1]) in words:    
            value = words[(x, coord[1])]
            value_x = x
            value_x_end = x + len(value)
            if value_x_end == coord[0] or value_x == coord[0] + 1:
                results.append(value)
        
    return results


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = [l for l in file.readlines()]
    
    data = read_input(lines)
    total_adjacent_values = 0

    for key, val in data[0].items():
        if does_have_symbol(val, key, data[1]):
            total_adjacent_values = total_adjacent_values + int(val)
    
    print(total_adjacent_values)

    total_ratios = 0
    for key, val in data[1].items():
        if val == "*":
            adjacents = get_adjacent_numbers(key, data[0], len(lines[0]))
            if len(adjacents) == 2:
                total_ratios = total_ratios + (int(adjacents[0]) * int(adjacents[1]))
    
    print(total_ratios)