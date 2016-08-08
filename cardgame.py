# coding=utf8
import copy
import random

unique_cards = "3 4 5 6 7 8 9 10 J Q K A 2".split()
# card54 = copy.deepcopy(unique_cards) * 4
card54 = unique_cards * 4 + ['x', 'X']

# print card54, len(card54)

card_num = {
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
    '2': 15,
    'x': 16,
    'X': 17,
}

def sort_cards(cards):
    return sorted(cards, key=lambda card: card_num[card])

def deal(count):
    random.shuffle(card54)
    n = len(card54) / count
    i = 0
    while i < len(card54):
        yield card54[i:i+n]
        i += n

# for l in deal(3):
    # print sort_cards(l)


class CardsComb:
    TP_SINGLE = 1
    TP_DOUBLE = 2
    TP_TRIPLE = 3
    TP_STRAIGHT = 4
    TP_BOMB = 5
    comb_type = None
    cards = []
    start_by_player = None


class Context:
    pass


class Dealer:
    ST_NO_CARD = 1
    ST_NORMAL = 2

    def __init__(self, n):
        self.n = n
        self.players = []
        self.cards = copy.copy(card54)
        self.lord = None

        self.current_player = None
        self.player_status = []
        self.current_cards_comb = None

    def next_player(self):
        return (self.current_player + 1) % n

    def deal(self):
        assert(self.lord)
        random.shuffle(self.cards)
        i = 0
        for player in self.players:
            player.set_cards(self.cards[i:i+17])
            i += 17
        self.lord.append_cards(self.cards[-3:])

        for player in self.players:
            player.reset_cards()

    def register_player(self, player, is_lord=False):
        self.players.append(player)
        if is_lord:
            self.lord = player
            player.set_lord()
            self.current_player = len(self.players) - 1
        self.player_status.append(self.ST_NORMAL)

    def end(self):
        return any(player.over() for player in self.players)

    def check(self, cards):
        # TODO
        return True

    def init_players(self):
        for player in self.players:
            player.set_others([p for p in self.players if p != player])

        self.deal()
        # for player in self.players:
        #     player.arrange_cards()

    def start(self):
        assert(self.lord)
        assert(len(self.players) == 3)

        self.init_players()

        while not self.end():
            response = self.current_player.lead(self.current_cards_comb, self.check)
            if response:
                self.current_cards_comb = response

            self.current_player = self.next_player()

class Player:
    def __init__(self, name, is_robot=True):
        self.name = name
        self.cards = []
        self.is_robot = is_robot
        self.is_lord = False
        self.others = []

    def set_cards(self, cards):
        self.cards = cards

    def append_cards(self, cards):
        self.cards.extend(cards)

    def reset_cards(self):
        # 整理牌面
        self.cards = sort_cards(self.cards)

        self.singles, self.doubles, self.triples, self.bombs = [], [], [], []
        a = self.cards
        i, buf = 1, [self.cards[0]]
        while i < len(a):
            while i < len(a) and a[i] == a[i-1]:
                buf.append(a[i])
                i += 1

            l = len(buf)
            if l == 1:
                self.singles.append(buf)
            elif l == 2:
                self.doubles.append(buf)
            elif l == 3:
                self.triples.append(buf)
            elif l == 4:
                self.bombs.append(buf)

            if i < len(a):
                buf = [a[i]]
                i += 1
            else:
                break

        if buf:
            self.singles.append(buf)

    def over(self):
        return not self.cards

    def left_cards_num(self):
        return len(self.cards)

    def set_lord(self):
        self.is_lord = True

    def set_others(self, others):
        self.others = others

    def lead(self, current_cards_comb, check_func):
        if not current_cards_comb or current_cards_comb.start_by_player == self:
            # first lead or no one follow you at last round
            comb = CardsComb()
            # comb.comb_type = CardsComb.TP_SINGLE
            comb.start_by_player = self
            return comb
        else:
            # follow
            pass


def main():
    jack = Player('Jack')
    tom = Player('Tom')
    bill = Player('Bill')
    dealer = Dealer(3)
    dealer.register_player(jack)
    dealer.register_player(tom)
    dealer.register_player(bill, True)
    dealer.init_players()

    for player in (jack, tom, bill):
        print player.cards, player.singles, player.doubles, player.triples, player.bombs


if __name__ == '__main__':
    main()