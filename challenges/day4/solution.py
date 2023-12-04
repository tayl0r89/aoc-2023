import math

class Card():

    winning: list[str]
    numbers: list[str]
    copies: int

    def __init__(self, winning: list[str], numbers: list[str]) -> None:
        self.winning = winning
        self.numbers = numbers
        self.copies = 1
    
    def get_matches(self):
        matches = len(list(filter(lambda x: x in self.winning, self.numbers)))
        return matches
    
    def get_points(self):
        matches = self.get_matches()
        if matches == 0:
            return 0
    
        return math.pow(2, matches - 1)
    
    def inc_copies(self, by: int) -> None:
        self.copies = self.copies + by

def str_to_list(numbers: str) -> list[str]:
    return list(filter(lambda x: x.strip() != "", numbers.strip().split(" ")))

def parse_card(line: str) -> Card:
    game_id_with_numbers = line.strip().split(":")
    game_parts = game_id_with_numbers[1].split("|")
    return Card(str_to_list(game_parts[0]), str_to_list(game_parts[1]))

if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as file:
        cards = [parse_card(line) for line in file.readlines()]
    

    card_counter = {}
    total_points = 0
    total_copies = 0
    for ind, card in enumerate(cards):
        matches = card.get_matches()

        for i in range(0, matches):
            if ind + i + 1 < len(cards):
                cards[ind + i + 1].inc_copies(card.copies)

        points = card.get_points()
        if points in card_counter:
            card_counter[points] = card_counter[points] + 1
        else:
            card_counter[points] = 1

        total_points = total_points + points
        total_copies = total_copies + card.copies
    
    print(f"Total points {total_points}")
    print(f"Total copies {total_copies}")