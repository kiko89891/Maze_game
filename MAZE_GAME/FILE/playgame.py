#  Author: Kiril Hristov
#  Date: 30 January 2019
#  Email: kirilyavorovhristov@gmail.com
#  Version: 5.0
from hero import Hero
from maze_gen_recursive import make_maze_recursion
from copy import deepcopy
from goblin import Goblin
from monster import Monster
import random

WALL_CHAR = "#"
SPACE_CHAR = "-"
HERO_CHAR = "H"
GOBLIN_CHAR = "G"
MONSTER_CHAR = "M"

class _Environment:
    """Environment includes Maze+Monster+Goblin"""
    def __init__(self, maze):
        self._environment = deepcopy(maze)
        self._goblins = []
        self._monsters = []
        self._monsters_y_coordinates=[]
        self._monster_x_coordinates=[]

    def getgoblins(self):
        return self._goblins

    def removegoblin(self, goblin):
        self._goblins.remove(goblin)

    def getmonsters(self):
        return self._monsters

    def get_number_monsters(self):
        return len(self._monsters)

    def monster_x(self):
        return self._monster_x_coordinates

    def monster_y(self):
        return self._monsters_y_coordinates

    def initgoblins(self):
        x = random.randint(1, 15)
        y = random.randint(1, 15)
        if self.get_coord(x, y) == 0:
            if len(self._goblins) < 3:
                t = len(self._goblins) + 1
            else:
                t = random.randint(1, 3)
            self._goblins.append(Goblin(x, y, t, random.randrange(10, 51, 10), random.randrange(20, 71, 10)))
            self.set_coord(x, y, 3)
        else:
            self.initgoblins()

    def initmonsters(self):
        x = random.randint(1, 15)
        y = random.randint(1, 15)
        if self.get_coord(x, y) == 0:
            if len(self._monsters) < 3:
                t = len(self._monsters) + 1
            else:
                t = random.randint(1, 3)
            self._monsters.append(Monster(x, y, t))
            self.set_coord(x, y, 4)
            self._monsters_y_coordinates.append(x)                 # adds the y coords of the monster
            self._monster_x_coordinates.append(y)
        else:
            self.initmonsters()

    def set_coord(self, x, y, val):
        self._environment[x][y] = val

    def get_coord(self, x, y):
        return self._environment[x][y]

    def print_environment(self):
        """print out the environment in the terminal"""
        for row in self._environment:
            row_str = str(row)
            row_str = row_str.replace("1", WALL_CHAR)  # replace the wall character
            row_str = row_str.replace("0", SPACE_CHAR)  # replace the space character
            row_str = row_str.replace("2", HERO_CHAR)  # replace the hero character
            row_str = row_str.replace("3", GOBLIN_CHAR)  # replace the goblin character
            row_str = row_str.replace("4", MONSTER_CHAR)  # replace the monster character


            print("".join(row_str))



class Game:

    _count = 0

    def __init__(self):
        self.maze = make_maze_recursion(17, 17)
        self.MyEnvironment = _Environment(self.maze)  # initial environment is the maze itself
        """Init goblins and monsters"""
        for i in range(0, 5):
            self.MyEnvironment.initgoblins()
            self.MyEnvironment.initmonsters()
        """"Init hero"""
        while True:
            x = random.randint(1, 15)
            y = random.randint(1, 15)
            if self.MyEnvironment.get_coord(x, y) == 0:
                self.myHero = Hero(x, y)
                self.MyEnvironment.set_coord(x, y, 2)
                break

        self._count = 0
        self._leaguetable = [["Empty"], [0], ["Empty"], [0], ["Empty"], [0], ["Empty"], [0], ["Empty"], [0], ["Empty"], [0], ["Empty"], [0], ["Empty"], [0], ["Empty"], [0], ["Empty"], [0]]

    def play(self):
        while True:
            self.myHero.move_debug(self.MyEnvironment)  #this works in debug mode
            x = self.myHero.move(self.MyEnvironment)
            self.MyEnvironment.print_environment()
            if x[0] == 0:
                print("The hero died and lost the game!")
                break
            elif x[0] == 1:
                print("YOU HAVE WON THE GAME CONGRATULATIONS ")
                inp = input("INPUT YOUR NAME : ")
                # Update the league table
                for z in range(0, 10):
                        if self._leaguetable[9 - z][1] <= self.myHero.getcoins():
                            if z == 9:
                                self._leaguetable.insert(0, [inp, self.myHero.getcoins()])
                                self._leaguetable.pop()
                        else:
                            self._leaguetable.insert(9 - z + 1, [inp, self.myHero.getcoins()])
                            self._leaguetable.pop()
                        if self._leaguetable[9 - z][1] <= self.myHero.getcoins():
                            print("YOU ARE NOT PART OF TOP 10 ")
                        break
                # print out league table
                for t in range(1, 11):
                    print(str(t) + ". " + self._leaguetable[t-1][0] + " with a score of " + str(self._leaguetable[t-1][1]))
                break
            self.MyEnvironment = x[1]
            self._count += 1
            print("NUMBER OF MOVES MADE ", self._count)


if __name__ == "__main__":

    myGame = Game()
    myGame.MyEnvironment.print_environment()
    goblins = myGame.MyEnvironment.getgoblins()
    monsters = myGame.MyEnvironment.getmonsters()


    myGame.play()
