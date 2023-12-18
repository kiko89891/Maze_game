#  Author: Kiril Hristov
#  Date: 30 January 2019
#  Email: kirilyavorovhristov@gmail.com
#  Version: 5.0


class Goblin:
    def __init__(self, x, y, typeofgoblin, ability1, ability2):
        """set the coordinate of the goblin in the maze"""
        self._coordX = x
        self._coordY = y
        """1 = wealth ; 2 = health ; 3 = gamer"""
        self._type = typeofgoblin
        self._ability1 = ability1
        self._ability2 = ability2

    def __str__(self):
        return "Goblin"

    def getcoords(self):
        return [self._coordX, self._coordY]

    def gettype(self):
        return self._type

    def getabilities(self):
        return [self._ability1, self._ability2]

