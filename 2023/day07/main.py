from collections import Counter, defaultdict
from typing import List, Tuple

class Card:
    """
    Class representing a card
    """

    def __init__(self, value, part) -> None:
        self.part = part
        self.value = value

    def __translate_value(self, value): 
        translation_table={'T': 10, 'J': 11 if self.part == 1 else 0, 'Q': 12, 'K': 13, 'A': 14}
        if value.isdigit():
            return int(value)
        return translation_table[value]

    def __lt__(self, other):
        return self.__translate_value(self.value) < self.__translate_value(other.value)  
    
    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f'Card({self.value})'

class Hand:
    """
    Class representing a hand of cards.
    """

    def __init__(self, cards: List[str], strength: int, part: int) -> None:
        self.cards = [Card(card, part) for card in cards]
        self.strength = int(strength)
        self.type, self.type_idx = self.__find_type(cards, part)

    def __find_type(self, cards: List[str], part: int) -> Tuple[str, int]:
        cards_freq = Counter(cards)
        joker_count = 0 if part == 1 else cards_freq.pop('J', 0)
        instances = list(cards_freq.values())

        if joker_count == 5 or 5 - joker_count in instances:
            return "five of a kind", 6
        elif 4 - joker_count in instances:
            return "four of a kind", 5
        elif (joker_count == 1 and instances.count(2) == 2) or (3 in instances and 2 in instances):
            return "full house", 4
        elif 3 - joker_count in instances:
            return "three of a kind", 3
        elif instances.count(2) == 2:
            return "two pairs", 2
        elif joker_count == 1 or 2 in instances:
            return "one pair", 1
        else:
            return "high card", 0

    def __lt__(self, other: 'Hand') -> bool:
        for card_1, card_2 in zip(self.cards, other.cards):
            if card_1 != card_2:
                return card_1 < card_2
        return False  # Return False instead of printing error

    def __repr__(self) -> str:
        return f'Hand({self.cards}, Type: {self.type})'

def group_hands(hands):
    """Group hands of the same type together"""
    grouped_hands = defaultdict(list)
    for hand in hands:
        grouped_hands[hand.type_idx].append(hand)
    return grouped_hands

def sort_hands(hands):
    """Sort hands by type and then by card value"""
    grouped_hands = group_hands(hands) 
    return [hand for hand_type_idx, hands in sorted(grouped_hands.items(), key=lambda x: x[0]) for hand in sorted(hands)]

def parse_input(input_path, part):
    hands = []
    for line in open(input_path).readlines():
        cards, strength = line.strip().split()
        hands.append(Hand(cards, strength, part=part))
    return hands

def part_1(hands):
    """Calculates the total winnings"""
    sorted_hands = sort_hands(hands)
    return sum(hand.strength*(i+1) for i, hand in enumerate(sorted_hands))

def part_2(hands):
    """Calculates the total winnings considering joker cards"""
    sorted_hands = sort_hands(hands)
    return sum([hand.strength*(i+1) for i, hand in enumerate(sorted_hands)])

def main():
    hands = parse_input('input.txt', part=1)
    print("Part 1:", part_1(hands)) # 256448566
    hands = parse_input('input.txt', part=2)
    print("Part 2:", part_2(hands)) # 254412181


if __name__ == '__main__':
    main()