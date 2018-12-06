from random import shuffle
from collections import defaultdict
import numpy as np
import util


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

  def __hash__(self):
    return self.index

  def __eq__(self, other):
    if other is None:
      return False
    return self.index == other.index

  def __repr__(self):
    month, property = Card.card_index_to_type[self.index]
    properties = ", ".join([Card.card_type_to_string[p] for p in property])
    # return "(Month : " + str(month) + " : " + properties + ")"
    return str(self.index)

  def get_card_info(self):
    return Card.card_index_to_type[self.index]

  def get_month(self):
    return Card.card_index_to_type[self.index][0]


# Convert the array of cards to numpy vector
def card_array_to_vec(cards):
  vec = np.zeros(48)
  for c in cards:
    vec[c.index] = 1

  return vec

def action_to_vec(action):
  if action[1] is None:
    card_to_hit = np.zeros(48)
  else:
    card_to_hit = np.zeros(48)
    card_to_hit[action[1].index] = 1

  card_to_play = np.zeros(48)
  card_to_play[action[0].index] = 1
  return np.concatenate((card_to_play, card_to_hit), axis=None)


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
    for card_h in self.cards_in_hand:
      has_match = False
      for card_o in opened_cards:
        if card_h.get_month() == card_o.get_month():
          actions.append((card_h, card_o))
          has_match = True
      if not has_match:
        actions.append((card_h, None))
    return actions

  def get_random_action(self):
    possible_actions = []
    for card_h in self.cards_in_hand:
      for card_o in self.game.opened_cards:
        if card_h.get_month() == card_o.get_month():
          possible_actions.append((card_h, card_o))

    if len(possible_actions) == 0:
      possible_actions = [(card, None) for card in self.cards_in_hand]

    idx = np.random.choice(len(possible_actions), 1)[0]
    return possible_actions[idx]

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
  def play_card(self, played_card_and_card_to_hit):
    played_card, card_to_hit = played_card_and_card_to_hit
    played_card_month = played_card.get_month()
    top_card = self.cards_on_pile[0]
    top_card_month = top_card.get_month()

    # Remove the top card on the pile
    self.cards_on_pile = self.cards_on_pile[1:]

    month_to_cards = defaultdict(list)
    for card in self.opened_cards:
      month_to_cards[card.get_month()].append(card)

    if played_card_month == top_card_month:
      match_cnt = len(month_to_cards.get(played_card_month, []))
      if match_cnt == 0:
        return [played_card, top_card]
      elif match_cnt == 1:  # bbuck
        self.opened_cards += [played_card, top_card]
        return []
      else:
        for c in month_to_cards[played_card_month]:
          self.opened_cards.remove(c)
        return month_to_cards[played_card_month] + [played_card, top_card]
    else:
      cards = []
      for card in [played_card, top_card]:
        match_cnt = len(month_to_cards[card.get_month()])

        if match_cnt == 0:
          self.opened_cards.append(card)
        elif match_cnt == 1:
          cards += month_to_cards[card.get_month()]
          cards.append(card)
          self.opened_cards.remove(month_to_cards[card.get_month()][0])
        elif match_cnt == 2:
          if card_to_hit in month_to_cards[card.get_month()]:
            cards.append(card_to_hit)
            self.opened_cards.remove(card_to_hit)
          else:  # If top card matches 2 opened cards, pick first match in the array
            cards.append(month_to_cards[card.get_month()][0])
            self.opened_cards.remove(month_to_cards[card.get_month()][0])
          cards.append(card)
        else:
          for c in self.opened_cards:
            if c.get_month() == card.get_month():
              cards.append(c)
              self.opened_cards.remove(c)
          cards.append(card)

      return cards

  # Returns the player's state
  # State : [my cards on hand, my taken cards, cards on board, cards taken by opponent]
  def get_player_state(self, player_id):
    opponent = 0 if player_id == 1 else 1
    my_cards_on_hand = card_array_to_vec(self.players[player_id].cards_in_hand)
    my_taken_cards = card_array_to_vec(self.players[player_id].cards_taken)
    cards_on_board = card_array_to_vec(self.opened_cards)
    opponent_taken_cards = card_array_to_vec(self.players[opponent].cards_taken)

    return np.concatenate((my_cards_on_hand, my_taken_cards, cards_on_board, opponent_taken_cards), axis=None)

  def is_game_ended(self):
    return len(self.cards_on_pile) == 0

  def get_player_random_action(self, player_id):
    return self.players[player_id].get_random_action()

  def get_player_possible_action(self, player_id):
    return self.players[player_id].get_actions(self.opened_cards)

  def player_do_action(self, player_id, action):
    earned_card = self.play_card(action)
    prev_score = self.players[player_id].compute_score()

    # Add earned cards to the player's board
    self.players[player_id].cards_taken += earned_card

    # Remove the card from the hand
    self.players[player_id].cards_in_hand.remove(action[0])
    current_score = self.players[player_id].compute_score()

    reward = (current_score - prev_score) + 0.1 * len(earned_card)
    return reward

class SARSA:
  def __init__(self):
    # size of state + size of action
    self.weights = {}
    self.exploration = 0.9
    self.learning_rate = 0.01
    self.gamma = 0.9


  def initialize_weights(self):
    W1 = np.random.randn(48 * 4 + 48 + 48, 48 * 4 + 48 + 48) * 0.01
    b1 = np.zeros(48 * 4 + 48 + 48)
    W2 = np.random.randn(48 * 4 + 48 + 48, 1) * 0.01
    b2 = np.zeros(1)
    self.weights['W1'] = W1
    self.weights['b1'] = b1
    self.weights['W2'] = W2
    self.weights['b2'] = b2

  # Get Q(s, a)
  def get_Q(self, state, action):
    vec = np.concatenate((state, action_to_vec(action)), axis=None)
    Z, linear_cache_1 = util.linear_forward(vec, self.weights['W1'], self.weights['b1'])
    A, activation_cache = util.relu(Z)
    Z, linear_cache_2 = util.linear_forward(A, self.weights['W2'], self.weights['b2'])
    caches = (linear_cache_1, activation_cache, linear_cache_2)
    return Z, caches

  def update_weights(self, delta, caches):
    linear_cache_1, activation_cache, linear_cache_2 = caches
    dA, dW2, db2 = util.linear_backward(delta, linear_cache_2)
    dZ = util.relu_backward(dA, activation_cache)
    _, dW1, db1 = util.linear_backward(dZ, linear_cache_1)
    self.weights['W1'] += self.learning_rate * dW1
    self.weights['b1'] += self.learning_rate * db1
    self.weights['W2'] += self.learning_rate * dW2
    self.weights['b2'] += self.learning_rate * db2

  def run(self):
    game = HwaTu()
    s_prev = None
    a_prev = None
    r_prev = None

    while not game.is_game_ended():
      s_curr = game.get_player_state(0)
      # Player 0 plays the card
      if np.random.rand() < self.exploration:
        # Explore the action.
        a_curr = game.get_player_random_action(0)
      else :
        # Pick the action that gives maximum Q value
        player_0_actions = game.get_player_possible_action(0)

        # Calculate Q(s,a) for each
        q_vals = [self.get_Q(s_curr, action)[0] for action in player_0_actions]

        # What gives max q val?
        max_action = np.argmax(q_vals)
        a_curr = player_0_actions[max_action]

      # Do SARSA step with s_prev, a_prev, r_prev and s_curr, a_curr
      if s_prev is not None:
        # Q(s_prev, a_prev)
        # <- Q(s_prev, a_prev) + lr * (r_prev + gamma * Q(s_curr, a_curr) - Q(s_prev, a_prev))
        q_curr = self.get_Q(s_curr, a_curr)[0]
        q_prev, caches = self.get_Q(s_prev, a_prev)
        delta = r_prev + self.gamma * q_curr - q_prev
        update_weights(delta, caches)

      # Do the max action.
      r_prev = game.player_do_action(0, a_curr)

      s_prev = s_curr
      a_prev = a_curr

      # Now let the opponent (player 1) to play.
      player_1_action = game.get_player_random_action(1)
      game.player_do_action(1, player_1_action)

sarsa = SARSA()

for _ in range(10000):
  sarsa.run()
