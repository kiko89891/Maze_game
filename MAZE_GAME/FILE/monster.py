#  Author: Kiril Hristov
#  Date: 30 January 2019
#  Email: kirilyavorovhristov@gmail.com
#  Version: 5.0

class Monster:
    def __init__(self, x_monster, y_monster, type_of_monster):
        """set the coordinate of the monster in the maze"""
        self._coordX = x_monster
        self._coordY = y_monster
        """1 = thief ; 2 = fighter ; 3 = gamer"""
        self._type = type_of_monster

    def __str__(self):
        return "Monster"

    def getcoords(self):
        return [self._coordX, self._coordY]

    def gettype(self):
        return self._type

    def getabilities(self):
        return [self._ability1, self._ability2]
