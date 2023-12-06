
def calc_distance(seconds_held, total_time):
    move_time = total_time - seconds_held
    return seconds_held * move_time

def is_winning(held_time, total_time, distance):
    return calc_distance(held_time, total_time) > distance

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
        variance = get_race_range(race)
        differences.append(variance[1] - variance[0] + 1)

    total = 1
    for i in differences:
        total = total * i
    
    print(total)