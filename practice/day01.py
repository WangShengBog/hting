import collections
from random import choice
from math import hypot

__author__ = 'bog'
__doc__ = """smooth python"""

Card = collections.namedtuple('Card', ['rank', 'suit'])
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


class FrenchDeck:
    ranks = [str(i) for i in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


class Vector:
    """ 二维向量 """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector(%r, %r)" % (self.x, self.y)

    # def __str__(self):
    """此方法会优先于repr"""
    #     return "Str"

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


City = collections.namedtuple('City', 'name country population coordinates')


def test_kwargs(a, b, **kwargs):
    print(a)
    print("========")
    print(kwargs.get("a"))
    print("========")
    print(kwargs)


if __name__ == '__main__':
    # deck = FrenchDeck()
    # print(spades_high(choice(deck)))
    # for i in sorted(deck, key=spades_high):
    #     print(i)
    # print(Vector(1, 2))
    # print(str(Vector(1, 2)))
    # tokyo = City('Tokyo', 'JP', 36.933, (35, 139))
    # print(tokyo)
    # print(tokyo._asdict())
    # print(tokyo._fields, '==', type(tokyo._fields))

    data = {"a": 1, "b3": 3}
    test_kwargs(**data)


