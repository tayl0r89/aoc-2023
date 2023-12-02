
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

# def get_adjacent_numbers(word)


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = [l for l in file.readlines()]
    
    data = read_input(lines)
    total_adjacent_values = 0

    for key, val in data[0].items():
        if does_have_symbol(val, key, data[1]):
            total_adjacent_values = total_adjacent_values + int(val)
    
    print(total_adjacent_values)

    # for key, val in data[1].items():
    #     if val == "*":
    #         print(key)