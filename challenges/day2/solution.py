
ColorInfo = tuple[int, str]

class BagInfo():
    red: int
    green: int
    blue: int

    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0

    def add(self, color_info: ColorInfo):
        if color_info[1] == "red" and color_info[0] > self.red:
            self.red = color_info[0]
        elif color_info[1] == "blue" and color_info[0] > self.blue:
            self.blue = color_info[0]
        elif color_info[1] == "green" and color_info[0] > self.green:
            self.green = color_info[0]
    
    def add_all(self, color_info: list[ColorInfo]):
        data = {}
        for info in color_info:
            if info[1] in data:
                data[info[1]] = data[info[1]] + info[0]
            else:
                data[info[1]] = info[0]

        for key, val in data.items():
            self.add((val, key))

    def power(self) -> int:
        return self.red * self.green * self.blue

class Game():
    id: int
    bag: BagInfo

    def __init__(self, id: int, bag: BagInfo):
        self.id = id
        self.bag = bag
    
    def is_possible(self, red: int, green: int, blue: int):
        return red >= self.bag.red and green >= self.bag.green and blue >= self.bag.blue

    
def parse_info(showing: str) -> list[ColorInfo]:
    results: list[ColorInfo] = []
    colors = showing.strip().split(",")
    for color in colors:
        parts = color.strip().split(" ")
        results.append((int(parts[0]), parts[1]))
    return results


if __name__ == "__main__":

    games: list[Game] = []

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            game_id_with_data = line.split(":")
            game_id = int(game_id_with_data[0].split(" ")[1])
            
            showings = game_id_with_data[1].split(";")
            showing_infos = []
            for showing in showings:
                showing_info = parse_info(showing)
                showing_infos.append(showing_info)

            bag_info = BagInfo()
            for showing_info in showing_infos:
                bag_info.add_all(showing_info)

            game = Game(game_id, bag_info)
            games.append(game)
    
    possible_total = 0
    power_total = 0
    for game in games:
        if game.is_possible(12, 13, 14):
            possible_total = possible_total + game.id

        power_total = power_total + game.bag.power()
    
    print(possible_total)
    print(power_total)


