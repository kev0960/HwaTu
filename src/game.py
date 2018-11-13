'''
    Class for defining a card.
    HwaTu cards can be identified by its index in the list of total 48 cards
'''


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
        'Pig'
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


class Player:
    def __init__(self):
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
            _, card_types = Card.card_index_to_type[card]
            if card == 44:
                has_bigwang = True
            if card == 4 or card == 16 or card == 29:
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

        # 3 gwang without bigwang : +2
        # 3 gwang with bigwang : +3
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
                total_score += 3
            else:
                total_score += 2

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


class HwaTu:
    def __init__(self):
        pass


if __name__ == '__main__':
    c = Card(3)
