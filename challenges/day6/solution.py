import math

def calc_distance(seconds_held, total_time):
    move_time = total_time - seconds_held
    return seconds_held * move_time

def is_winning(held_time, total_time, distance):
    return calc_distance(held_time, total_time) > distance


def find_time_for_win(distance, total_time):
    a = 1
    b = (total_time * -1)
    c = distance

    part = math.sqrt(math.pow(b, 2) - (4 * a * c))

    r1 = ((b*-1) + part) / (2*a)
    r2 = ((b*-1) - part) / (a*2)
    results = [r1, r2]

    min_held = min(results)
    max_held = max(results)

    return(
        math.floor(min_held) if is_winning(math.floor(min_held), total_time, distance) else math.ceil(min_held),
        math.ceil(max_held) if is_winning(math.ceil(max_held), total_time, distance) else math.floor(max_held)
    )

def get_race_range(race):
    time, distance = race

    min_win = None
    max_win = None
    for i in range(0, time):
        if is_winning(i, time, distance):
            if min_win is None:
                min_win = i
            if max_win is None or i > max_win:
                max_win = i

    return (min_win, max_win)

if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        times = [int(x) for x in lines[0].split(":")[1].split()]
        distances = [int(x) for x in lines[1].split(":")[1].split()]
    
    races = []
    for i in range(0, len(times)):
        races.append((times[i], distances[i]))

    differences = []
    for race in races:
        result = find_time_for_win(race[1], race[0])
        print(f"Race margin of error is: {result[1] - result[0] + 1}")
        differences.append(result[1] - result[0] + 1)

    total = 1
    for i in differences:
        total = total * i

    print(f"Variance product is: {total}")