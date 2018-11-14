import unittest
from game import HwaTu, Player, Card

class HwaTuTest(unittest.TestCase):
  def setUp(self):
    self.game = HwaTu()

  def test_play_card(self):
    self.game.cards_on_pile = [Card(5)]
    self.game.opened_cards = [Card(1), Card(2)]

    earned_card = self.game.play_card((Card(3), Card(2)))
    self.assertEqual(earned_card, [Card(2), Card(3)])

class PlayerTest(unittest.TestCase):
  def setUp(self):
    self.game = HwaTu()
    self.player = Player(self.game, 0)


if __name__ == '__main__':
    unittest.main()