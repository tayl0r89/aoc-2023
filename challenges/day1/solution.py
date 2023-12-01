import re

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
matcher = '(?=(\d|one|two|three|four|five|six|seven|eight|nine))'

def parse_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return numbers.index(value) + 1
    

def get_number(line: str) -> int:
    digits = re.findall(matcher, line)
    full = str(parse_int(digits[0])) + str(parse_int(digits[-1]))
    return int(full)


if __name__ == "__main__":
    total = 0
    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            total = total + get_number(line)
    print(total)