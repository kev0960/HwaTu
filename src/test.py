import unittest
from game import HwaTu, Player, Card

class HwaTuTest(unittest.TestCase):
  def setUp(self):
    self.game = HwaTu()

  def test_play_card_simple(self):
    # Case 1
    self.game.cards_on_pile = [Card(5)]
    self.game.opened_cards = [Card(1), Card(2)]

    earned_card = self.game.play_card((Card(3), Card(2)))
    self.assertEqual(set(earned_card), {Card(2), Card(3)})
    self.assertEqual(set(self.game.opened_cards), {Card(5), Card(1)})

    # Case 2
    self.game.cards_on_pile = [Card(3)]
    self.game.opened_cards = [Card(0), Card(1)]

    earned_card = self.game.play_card((Card(2), Card(0)))
    self.assertEqual(set(earned_card), {Card(0), Card(1), Card(2), Card(3)})
    self.assertEqual(set(self.game.opened_cards), set())

    # Case 3
    self.game.cards_on_pile = [Card(5)]
    self.game.opened_cards = [Card(0), Card(6)]

    earned_card = self.game.play_card((Card(1), Card(0)))
    self.assertEqual(set(earned_card), {Card(0), Card(1), Card(5), Card(6)})
    self.assertEqual(set(self.game.opened_cards), set())

    # Case 4
    self.game.cards_on_pile = [Card(5)]
    self.game.opened_cards = [Card(0), Card(6)]

    earned_card = self.game.play_card((Card(10), None))
    self.assertEqual(set(earned_card), {Card(5), Card(6)})
    self.assertEqual(set(self.game.opened_cards), {Card(0), Card(10)})

    # Case 5
    self.game.cards_on_pile = [Card(5)]
    self.game.opened_cards = [Card(0), Card(1)]

    earned_card = self.game.play_card((Card(10), None))
    self.assertEqual(set(earned_card), set())
    self.assertEqual(set(self.game.opened_cards), {Card(0), Card(1), Card(5), Card(10)})

    # Case 6 - Bbuck
    self.game.cards_on_pile = [Card(2)]
    self.game.opened_cards = [Card(0), Card(5)]

    earned_card = self.game.play_card((Card(1), None))
    self.assertEqual(set(earned_card), set())
    self.assertEqual(set(self.game.opened_cards), {Card(0), Card(1), Card(2), Card(5)})

    # Case 7
    self.game.cards_on_pile = [Card(5)]
    self.game.opened_cards = [Card(0), Card(3)]

    earned_card = self.game.play_card((Card(10), None))
    self.assertEqual(set(earned_card), set())
    self.assertEqual(set(self.game.opened_cards), {Card(0), Card(3), Card(5), Card(10)})

class PlayerTest(unittest.TestCase):
  def setUp(self):
    self.game = HwaTu()
    self.player = Player(self.game, 0)


if __name__ == '__main__':
    unittest.main()