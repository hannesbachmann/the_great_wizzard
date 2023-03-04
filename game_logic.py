import random


def play_card(top_card, hand, play_stack=None, first_played_trump=None):
    # predicted strikes and total predicted strikes will be added soon
    possible_choices = get_possible_choices(top_card, hand, play_stack=play_stack, first_played_trump=first_played_trump)

    # firstly select and play random hand card from possible ones
    played_card = possible_choices[random.randint(0, len(possible_choices) - 1)]
    return played_card


def get_possible_choices(top_card, hand, play_stack=None, first_played_trump=None):
    # apply rules
    if first_played_trump:
        round_color = first_played_trump[0]
        possible_choices = []
        no_col = True
        for card in hand:
            if card[0] == round_color:
                possible_choices.append(card)
                no_col = False
            elif card[0] == 'z':
                possible_choices.append(card)
            elif card[0] == 'n':
                possible_choices.append(card)
        if no_col:
            return hand
        return possible_choices
    else:
        return hand


def predict_strikes(hand, top_card):
    """get from how much trump card, high value cards and mages"""
    count = 0
    for card in hand:
        if top_card[0] == card[0] and card[1] > 8:
            count += 1
        elif card[0] == 'z':
            count += 1
        elif card[1] > 11:
            count += 1
    return count


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

        self.players_turn = 0
        self.current_color = None
        self.play_stack = []
        self.players_round_scores = {f'player{i}': {'predicted': [], 'done': []} for i in range(players)}

        self.highest_value = {'card': ('', 0), 'player': 1}

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
        """every player perform one turn

        :return:
        """
        current_stack = self.shuffle_card_set(self.cards)
        self.hands = [[] for p in range(self.players)]
        # give cards
        for j in range(self.players):
            for i in range(self.round):
                self.hands[j].append(current_stack.pop(0))
        if len(current_stack) > 0:
            self.top_card = current_stack.pop(0)
        for p in range(self.players):
            self.players_round_scores[f'player{p}']['predicted'].append(predict_strikes(self.hands[p], self.top_card))

    def play_round(self):
        self.play_stack = []
        strike_counts = [0 for i in range(self.players)]
        for r in range(self.round):
            for t in range(self.players):
                self.play_turn(t)
            strike_counts[self.highest_value["player"]] += 1
        for p in range(self.players):
            self.players_round_scores[f'player{p}']['done'].append(strike_counts[p])
        self.round += 1

    def play_turn(self, t):
        """one players turn
        a player select and play one (possible) hand card

        :return:
        """
        trump = self.top_card
        hand = self.hands[self.players_turn].copy()
        first_played_trump = self.current_color
        play_stack = self.play_stack
        if t == 0:
            # player[players_turn] start with the first turn
            # playes a tuple ('color', number) # add to play_stack, delete from hand .remove(self.play_stack[-1])
            c = play_card(trump, hand, play_stack=None, first_played_trump=None)
            self.play_stack.append(c)
            self.hands[self.players_turn].remove(c)
            self.current_color = c
            self.highest_value['card'] = c
            self.highest_value['player'] = self.players_turn
        else:
            c = play_card(trump, hand, play_stack=play_stack, first_played_trump=play_stack[0])
            self.play_stack.append(c)
            self.hands[self.players_turn].remove(c)
            self.calc_card_value(c)
        print(f'turn: {t}\t|\tround: {self.round}\t|\tplayer: {self.players_turn}')
        print(f'hand: {hand}')
        print(f'trump: {self.top_card}\t|\tground color: {self.play_stack[0]}\t|\tplayed card: {c}\t|\thighest: {self.highest_value}')
        print('-------------------------------------------------')
        self.players_turn += 1
        if self.players_turn == self.players:
            self.players_turn = 0

    def calc_card_value(self, c):
        h_value = self.highest_value.copy()
        # handle trump == n and trump == z
        if self.highest_value['card'][0] == 'z':
            return
        if self.top_card[0] == 'z' or self.top_card[0] == 'n':
            if c[1] > self.highest_value['card'][1]:
                self.highest_value['card'] = c
                self.highest_value['player'] = self.players_turn
                return
            elif c[0] == 'z' and h_value['card'][0] != 'z':
                self.highest_value['card'] = c
                self.highest_value['player'] = self.players_turn
                return
        if c[0] == 'z' and h_value['card'][0] != 'z':
            self.highest_value['card'] = c
            self.highest_value['player'] = self.players_turn
        elif c[0] == h_value['card'][0] and c[1] > h_value['card'][1]:
            self.highest_value['card'] = c
            self.highest_value['player'] = self.players_turn
        elif c[0] == self.top_card[0]:
            if self.highest_value['card'][0] == self.top_card[0] and c[1] > h_value['card'][1]:
                self.highest_value['card'] = c
                self.highest_value['player'] = self.players_turn
            elif self.highest_value['card'][0] != self.top_card[0]:
                self.highest_value['card'] = c
                self.highest_value['player'] = self.players_turn

    def ground_rules(self):
        pass


if __name__ == '__main__':
    g = Game(2)
    for n in range(30):
        g.start_round()
        g.play_round()
    pass
