from random import shuffle

class Card:
    card_string_to_type = {
        'SongHak': 1,
        'MaeJo': 2,
        'Sakura': 3,
        'BlackSsari': 4,
        'ChangPo': 5,
        'Moran': 6,
        'HongSsari': 7,
        'Gongsan': 8,
        'Gookjin': 9,
        'Danpoong': 10,
        'Odong': 11,
        'Bi': 12,
        'Gwang': 13,
        'Hongdan': 14,
        'Pi': 15,
        'Yeolggut': 16,
        'Bird': 17,
        'Chodan': 18,
        'SsangPi': 19,
        'Chungdan': 20,
        'Deer': 21,
        'Pig': 22,
        'YyeolggutandSsangPi': 23
    }

    card_type_to_string = [
        'ERROR',
        'SongHak',
        'MaeJo',
        'Sakura',
        'BlackSsari',
        'ChangPo',
        'Moran',
        'HongSsari',
        'Gongsan',
        'Gookjin',
        'Danpoong',
        'Odong',
        'Bi',
        'Gwang',
        'Hongdan',
        'Pi',
        'Yeolggut',
        'Bird',
        'Chodan',
        'SsangPi',
        'Chungdan',
        'Deer',
        'Pig',
        'YyeolggutandSsangPi'
    ]

    card_index_to_type = [(1, [1, 13]),
                          (1, [14, 1]),
                          (1, [15, 1]),
                          (1, [15, 1]),
                          (2, [2, 17, 16]),
                          (2, [2, 14]),
                          (2, [2, 15]),
                          (2, [2, 15]),
                          (3, [3, 13]),
                          (3, [14, 3]),
                          (3, [3, 15]),
                          (3, [3, 15]),
                          (4, [4, 17, 16]),
                          (4, [18, 4]),
                          (4, [4, 15]),
                          (4, [4, 15]),
                          (5, [5, 16]),
                          (5, [18, 5]),
                          (5, [5, 15]),
                          (5, [5, 15]),
                          (6, [6, 16]),
                          (6, [20, 6]),
                          (6, [15, 6]),
                          (6, [15, 6]),
                          (7, [7, 22, 16]),
                          (7, [14, 7]),
                          (7, [15, 7]),
                          (7, [15, 7]),
                          (8, [13, 8]),
                          (8, [16, 17, 8]),
                          (8, [15, 8]),
                          (8, [15, 8]),
                          (9, [23]),
                          (9, [20, 9]),
                          (9, [15, 9]),
                          (9, [15, 9]),
                          (10, [10, 21, 16]),
                          (10, [20, 10]),
                          (10, [15, 10]),
                          (10, [15, 10]),
                          (11, [11, 13]),
                          (11, [11, 19]),
                          (11, [11, 15]),
                          (11, [11, 15]),
                          (12, [12, 13]),
                          (12, [12, 17, 16]),
                          (12, [14, 12]),
                          (12, [12, 19])]

    def __init__(self, index):
        self.index = index

    def __cmp__(self, other):
        return self.index == other.index

    def __repr__(self):
        month, property = Card.card_index_to_type[self.index]
        properties = ", ".join([Card.card_type_to_string[p] for p in property])
        return "(Month : " + str(month) + " : " + properties + ")"

    def get_card_info(self):
        return Card.card_index_to_type[self.index]

    def get_month(self):
        return Card.card_index_to_type[self.index][0]

class Player:
    def __init__(self, game, player_id):
        self.game = game
        self.player_id = player_id

        self.cards_in_hand = []
        self.cards_taken = []

        # Check whether Googijn's Yeolggut is used as Yeolggut or Ssangpi.
        # (True if Yeolggut)
        self.yeolggut_or_ssangpi = None

    def compute_score(self):
        has_bigwang = False
        num_gwang = 0

        num_pi = 0
        num_yeolggut = 0

        # Number of cards per Chodan, Hongdan, Chungdan
        ddi = [0, 0, 0]
        godori_bird = 0

        for card in self.cards_taken:
            _, card_types = card.get_card_info()
            if card.index == 44:
                has_bigwang = True
            if card.index == 4 or card.index == 16 or card.index == 29:
                godori_bird += 1
            for card_type in card_types:
                if card_type == 15:
                    num_pi += 1
                elif card_type == 19:
                    num_pi += 2
                elif card_type == 16:
                    num_yeolggut += 1
                elif card_type == 18:
                    ddi[0] += 1
                elif card_type == 14:
                    ddi[1] += 1
                elif card_type == 20:
                    ddi[2] += 1
                elif card_type == 13:
                    num_gwang += 1
                elif card_type == 23:
                    if self.yeolggut_or_ssangpi:
                        num_yeolggut += 1
                    else:
                        num_pi += 2

        # 3 gwang without bigwang : +3
        # 3 gwang with bigwang : +2
        # 4 gwang : +4
        # 5 gwang : +5
        # Godori (2, 4, 8 birds) : +5
        # Ddi : (5 : 1, +1 after)
        # Chodan, Hongdan, Chungdan : +3
        # Yeolggut : (5 : 1, +1 after), >= 7 --> x 2 score.
        # Pi : 10 : 1, +1 after.

        total_score = 0
        if num_gwang == 5:
            total_score += 15
        elif num_gwang == 4:
            total_score += 4
        elif num_gwang == 3:
            if has_bigwang:
                total_score += 2
            else:
                total_score += 3

        if godori_bird == 3:
            total_score += 5

        if sum(ddi) >= 5:
            total_score += (sum(ddi) - 4)

        for num_per_ddi in ddi:
            if num_per_ddi >= 3:
                total_score += 3

        if num_yeolggut >= 5:
            total_score += (num_yeolggut - 4)

        if num_pi >= 10:
            total_score += (num_pi - 9)

        if num_yeolggut >= 7:
            total_score *= 2

        return total_score

    # Given the board, determine what actions are valid by looking at cards in hand
    # A valid action is the tuple of (card from hand, target open card/None if no match)
    def get_actions(self, opened_cards):
      actions = []
      for card_h in cards_in_hand:
        has_match = False
        for card_o in opened_cards:
          if card_h.get_month() == card_o.get_month():
            actions.append((card_h, card_o))
            has_match = True
        if not has_match:
          actions.append((card_h, None))
      return actions

class HwaTu:
    def __init__(self):
        self.players = [Player(self, 0), Player(self, 1)]

        self.cards = [Card(i) for i in range(48)]
        shuffle(self.cards)

        self.players[0].cards_in_hand = self.cards[:10]
        self.players[1].cards_in_hand = self.cards[10:20]

        self.opened_cards = self.cards[20:28]
        self.cards_on_pile = self.cards[28:]

    # Returns whatever earned card.
    def play_card(self, played_card):
        played_card_month = played_card.get_month()
        top_card = self.cards_on_pile[0]
        top_card_month = top_card.get_month()

        # Remove the top card on the pile
        self.cards_on_pile = self.cards_on_pile[1:]

        month_to_cnt = {}
        for card in self.opened_cards:
            month_to_cnt[card.get_month()] += 1

        if played_card_month == top_card_month:
            if month_to_cnt[played_card_month] == 0:
                return [played_card, top_card]
            elif month_to_cnt[played_card_month] == 1: # bbuck
                self.opened_cards += [played_card, top_card]
            else:
                cards = []
                for card in self.opened_cards:
                    if card.get_month() == played_card_month:
                        cards.append(card)
                return cards + [played_card, top_card]

        else:
            cards = []
            for card in [played_card, top_card]:
                if month_to_cnt[card] == 0:
                    self.opened_cards.append(card)
                elif month_to_cnt[card] <= 2:
                    for c in self.opened_cards:
                        if c.get_month() == card.get_month():
                            cards.append(c)
                            break
                    cards.append(card)
                else:
                    for c in self.opened_cards:
                        if c.get_month() == card.get_month():
                            cards.append(c)
                    cards.append(card)

            return cards

if __name__ == '__main__':
    game = HwaTu()

    print('', game.opened_cards)
    print('', game.cards_on_pile)