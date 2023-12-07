from functools import cmp_to_key

INCLUDE_JOKERS = True

def parse_card(card: str):
    if card.isdigit():
        return int(card)
    
    match card:
        case "T": return 10
        case "J": return 0 if INCLUDE_JOKERS else 11
        case "Q": return 12
        case "K": return 13
        case "A": return 14

    raise ValueError(f"Bad card value: {card}")

def parse_hand(hand: str):
    return list(map(parse_card, [*hand]))


def count_hand_cards(hand:list[int]) -> dict[int, int]:
    results = {}
    for val in hand:
        if val in results:
            results[val] = results[val] + 1
        else:
            results[val] = 1
    return results


def rank_groups(counts: dict[int, int]) -> int:
    groups = sorted(list(counts.values()), reverse=True)
    match groups[0]:
        case 5: return 7 
        case 4: return 6 
        case 3: return 5 if groups[1] == 2 else 4 
        case 2: return 3 if groups[1] == 2 else 2
        case 1: return 1
    
    raise ValueError(f"Hand {counts} got grouped as {groups}")


def get_hand_rank_with_jokers(hand: list[int]) -> int:
    counts = count_hand_cards(hand)
    jokers = counts.get(0, 0)
    
    if jokers == 5:
        return 7
    
    if jokers == 0:
        return rank_groups(counts)

    counts[0] = 0
    groups = sorted(list(counts.values()), reverse=True)

    # hand must have jokers, rank doesnt include jokers
    match groups[0]:
        case 4: return 7 # 4 of a kind becomes 5
        case 3: return 5 + jokers
        case 2:
            if jokers > 1:
                return 4 + jokers
            return 5 if groups[1] == 2 else 4
        case 1:
            if jokers > 2:
                return 3 + jokers
            elif jokers == 2:
                return 4
            return 2

    raise ValueError("Reached end of joker ranking")


def get_hand_rank(hand: list[int]) -> int:
    counts = count_hand_cards(hand)
    return rank_groups(counts)


def hand_comparator(a_bid: tuple[list[int], int], b_bid: tuple[list[int], int]):
    a = a_bid[0]
    b = b_bid[0]
    a_rank = get_hand_rank_with_jokers(a) if INCLUDE_JOKERS else get_hand_rank(a)
    b_rank = get_hand_rank_with_jokers(b) if INCLUDE_JOKERS else get_hand_rank(b)

    if a_rank > b_rank:
        return -1
    elif b_rank > a_rank:
        return 1
    
    for i, val in enumerate(a):
        if val > b[i]:
            return -1
        if val < b[i]:
            return 1
    
    return 0


if __name__ == "__main__":
    data = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for l in file.readlines():
            hand, bid = l.strip().split(" ")
            data.append((parse_hand(hand), int(bid)))

    results = sorted(data, key=cmp_to_key(hand_comparator), reverse=True)
    bid_total = 0
    for i, hand in enumerate(results):
        print(f"Rank {i+1} is {hand}")
        hand_score = hand[1] * (i+1)
        bid_total = bid_total + hand_score
    
    print(bid_total)