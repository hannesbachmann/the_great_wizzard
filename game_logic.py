import random

def play_card(top_card, hand, first_played_trump=None):
    pass


class Game:
    def __init__(self, players=2):
        self.colors = ['red', 'blue', 'green', 'yellow']
        self.numbers = [i+1 for i in range(13)]
        self.cards = [(c, n) for c in self.colors for n in self.numbers]
        for i in range(4):
            self.cards.append(('z', 0))
            self.cards.append(('n', 0))

        self.hands = [[] for p in range(players)]
        self.players = players
        self.round = 1
        self.top_card = (0, 0)

        self.turn = 1
        self.players_turn = 0
        self.current_color = None
        self.play_stack = []

    def shuffle_card_set(self, card_set):
        card_set = card_set.copy()
        shuffled = []
        l = len(card_set)
        for c in range(l):
            r = random.randint(0, l - 1)
            shuffled.append(card_set[r])
            card_set.remove(card_set[r])
            l = len(card_set)
        return shuffled

    def start_round(self):
        current_stack = self.shuffle_card_set(self.cards)
        self.hands = [[] for p in range(self.players)]
        # give cards
        for j in range(self.players):
            for i in range(self.round):
                self.hands[j].append(current_stack.pop(0))
        if len(current_stack) > 0:
            self.top_card = current_stack.pop(0)
        self.round += 1

    def play_turn(self):
        trump = self.top_card
        hand = self.hands[self.players_turn]
        first_played_trump = self.current_color
        if self.turn == 1:
            # player[players_turn] start with the first turn
            # playes a tuple ('color', number) # add to play_stack, delete from hand .remove(self.play_stack[-1])
            c = play_card(trump, hand, first_played_trump=None)
            self.play_stack.append(c)
            self.hands[self.players_turn].remove(c)
            self.current_color = c
        else:
            pass
        self.players_turn += 1

    def ground_rules(self):
        pass


if __name__ == '__main__':
    g = Game(2)
    for n in range(30):
        g.start_round()
    pass