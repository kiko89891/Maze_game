#  Author: Kiril Hristov
#  Date: 30 January 2019
#  Email: kirilyavorovhristov@gmail.com
#  Version: 5.0

from getch1 import *
import sys
import random


class Hero:
    """this is the hero class, further define it please"""
    def __init__(self, x, y):
        """set the coordinate of the hero in the maze"""
        self._coordX = x
        self._coordY = y
        self._health = 100
        self._coins = 1000 # gold coins the hero have.
        self._gem = 3
        self._monstersmeat = []
        self._heromeatsomeone = [0, 0, 0, 0]
        self._list_x=[]

    def getcoins(self):
        return self._coins


    def move(self, environment):
        """move in the maze, it is noted this function may not work in the debug mode"""

        ch2 = getch()
        f = environment.monster_y()  # GETS THE Y COORD
        k = environment.monster_x()  # GETS THE X COORD
        answer = zip(k, f)
        for u in answer:
            print("NUMBER OF MONSTERS",environment.get_number_monsters(),u)


        if ch2 == b'H' or ch2 == "A":
            # the up arrow key was pressed
            print("up key pressed")
            environment = self.action(self._coordX - 1, self._coordY, environment)



        elif ch2 == b'P' or ch2 == "B":
            # the down arrow key was pressed
            print("down key pressed")
            environment = self.action(self._coordX + 1, self._coordY, environment)


        elif ch2 == b'K' or ch2 == "D":
            # the left arrow key was pressed
            print("left key pressed")
            environment = self.action(self._coordX, self._coordY - 1, environment)




        elif ch2 == b'M' or ch2 == "C":
            # the right arrow key was pressed
            print("right key pressed")
            environment = self.action(self._coordX, self._coordY + 1, environment)



        elif ch2 == b'Z' or ch2 == "F":
            print("PRINT MAP KEY")
            environment.print(environment)                # PRINTS THE MAP


        elif ch2 == b'U' or ch2 == "J":
            print("H IS PRESSET")





        """Return if the player won, lost, or the game continues"""
        if self._health <= 0:
            return [0, environment]
        elif len(self._monstersmeat) == 5:
            return [1, environment]
        else:
            return [2, environment]


    def health_movement_reduction(self,enviorment):
        self._health = self._health - 1
        return enviorment


    def action(self, x, y, environment):

        result = environment.get_coord(x, y)
        self._coordX = x
        self._coordY = y
        environment.set_coord(x, y, 2)
        self.health_movement_reduction(environment)
        if environment.get_coord(x + 1, y) == environment.get_coord(x, y):  # if the coord behind me is me
            environment.set_coord(x + 1, y, 0)                                 # DELETE IT to 0
        elif environment.get_coord(x, y - 1) == environment.get_coord(x, y):
            environment.set_coord(x, y - 1, 0)
        elif environment.get_coord(x, y + 1) == environment.get_coord(x, y):
            environment.set_coord(x, y + 1, 0)
        elif environment.get_coord(x - 1, y) == environment.get_coord(x, y):
            environment.set_coord(x - 1, y, 0)



        # User goes into wall
        if result == 1:
            print("You can't walk through walls!")
        # User goes to an empty field
        elif result == 0:
            self._coordX = x
            self._coordY = y
            environment.set_coord(x, y, 2)
            self.health_movement_reduction(environment)
            if environment.get_coord(x+1, y)==environment.get_coord(x,y): # if the coord behind me is me
                environment.set_coord(x+1,y,0)
            elif environment.get_coord(x, y-1)==environment.get_coord(x,y):
                environment.set_coord(x , y-1, 0)
            elif  environment.get_coord(x, y+1)==environment.get_coord(x,y):
                environment.set_coord(x , y+1, 0)
            elif environment.get_coord(x-1, y)==environment.get_coord(x,y):
                environment.set_coord(x - 1, y, 0)







            print("1 health point consumed for moving.")
            print("The hero is now at x: " + str(x) + " y: " + str(y))


            # User meets a goblin
            #User goes to goblin
        elif result == 3:
            self.health_movement_reduction(environment)
            print("1 health point consumed for moving.")
            for i in environment.getgoblins():
                goblin = i.getcoords()
                if goblin[0] == x and goblin[1] == y:
                    goblin = i
                    break               #######################

            if goblin.gettype() == 1:
                result=random.randrange(1,100)
                if result<=50:
                    self._coins=self._coins+100
                    print("You have met a wealth goblin and you gained 100 coins","total coins ", self._coins)


                elif result > 50:
                    print("You have met a goblin but it doesn't like you and will not give you anything")
            elif goblin.gettype() == 2:
                if result <= 70:
                    self._health=self._health + 50
                    print("You have met a wealth goblin and you gained 50 health", "total health ", self._health)
                elif result > 70:
                    print("You have met a goblin but it doesn't like you and will not give you anything")

            elif goblin.gettype() == 3:
                print("The hero met a gamer goblin and wants you to play rock,paper scisiors")
                self.gamer_goblin(environment)
            self._coordX = x
            self._coordY = y
            environment.set_coord(x, y, 2)

        # User meets a monster
        elif result == 4:
            self.health_movement_reduction(environment)
            print("1 health point consumed for moving.")

            for i in environment.getmonsters():          #################################
                monster = i.getcoords()
                if monster[0] == x and monster[1] == y:
                    monster = i
                    if monster in self._monstersmeat:
                        print("The hero already meat this monster once.")
                    else:
                        self._monstersmeat.append(monster)
                        print("The hero and this monster meat for the first time.",)

                    break
            if monster.gettype() == 1:
                print("THIS IS A THIEF MONSTER")
                result = random.randrange(1, 100)
                if result >90:
                    self._coins = self._coins - 10
                    print("THE MONSTER COULDN'T ROB YOU")
                elif result <= 90:
                    print("YOU HAVE BEEN ROBED BY THE MONSTER FOR 10 COINS", "total coins ", self._coins)

            elif monster.gettype() == 2:
                print("THIS IS A FIGHTER MONSTER")
                result=random.randrange(1,100)
                if result <= 40:
                    self._health=self._health - 30
                    print("THE FIGHER TAKES 30 OF YOUR HEALTH ", "total health ", self._health)
                elif result > 40:
                    print("THE FIGHER TAKE NO DAMAGE ","total health ", self._health)

            elif monster.gettype() == 3:
                print("THE HERO MET A GAMER MONSTER AND WANTS TO PLAY ROCK , PAPER AND SCISIORS")
                self.gamer_monster(environment)
            self._coordX = x
            self._coordY = y
            environment.set_coord(x, y, 4)

            """Save position of monster"""
        return environment


    def move_debug(self, environment):

        """move in the maze, you need to press the enter key after keying in
        direction, and this works in the debug mode"""

        ch2 = sys.stdin.read(1)

        if ch2 == "w":
            # the up arrow key was pressed
            print("up key pressed")



        elif ch2 == "s":
            # the down arrow key was pressed
            print("down key pressed")

        elif ch2 == "a":
            # the left arrow key was pressed
            print("left key pressed")

        elif ch2 == "d":
            # the right arrow key was pressed
            print("right key pressed")

        elif ch2 == "M":
            print("PRINT MAP KEY")

        elif ch2 == "H":           # GAME DESCRIPTION
            print("""YOU ARE PLAYING A MAZE GAME WHERE YOU LOCATION ON THE MAP IS H AND YOU MOVE WITH THE KEYS: W,S,A,D (up,down,left,right) respectivly
                     THERE ARE 3 TYPES OF MONSTERS WITH LOCATION M-  1 = thief ; 2 = fighter ; 3 = gamer
                     THERE ARE ALSO 3 TYPES OF GOBLINS ON THE MAP WITH LOCATION G: 1 = thief ; 2 = fighter ; 3 = gamer 
                     YOUR GOAL IS TO MEET ALL THE MONSTERS ATLEAST ONCE AND GET AS MANY COINS AS POSSIBLE
                     YOUR HEALTH IS DECREASED BY 1 FOR EVERY MOVE SO RETHINK YOU MOVES WISELY""")


    def gamer_goblin(self,enviorment):
        user_input=input("TYPE YOUR ANSWER ")
        goblin_answer=random.randint(1,3)
        print(goblin_answer)
        if user_input =="P" and goblin_answer==1:  # starts comparing human and goblin answer
            self._health=self._health+50
            self._coins=self._coins+100
            print("YOUR HEALTH IS ",self._health)

        elif user_input =="P" and goblin_answer==2:
            print("YOU LOSE CONTINUE ON YOUR WAY")

        elif user_input =="P" and goblin_answer==3:
            print("YOU HAVE THE SAME ANSWERS TYPE AGAIN")
            self.gamer_goblin(enviorment)  # if the answers match then repeat the procedure

        if user_input =="R" and goblin_answer ==1:
            self._health = self._health + 50
            self._coins = self._coins + 100
            print("YOUR HEALTH IS ", self._health)

        elif user_input =="R" and goblin_answer ==2:
            print("YOU LOSE CONTINUE ON YOUR WAY")

        elif user_input =="R" and goblin_answer ==3:
            print("YOU HAVE THE SAME ANSWERS TYPE AGAIN")
            self.gamer_goblin(enviorment)

        if user_input =="I" and goblin_answer ==1:
            self._health = self._health + 50
            self._coins = self._coins + 100
            print("YOUR HEALTH and coins are  ", self._health,self._coins)

        elif user_input =="I" and goblin_answer ==2:
            print("YOU LOSE CONTINUE ON YOUR WAY")

        elif user_input =="I" and goblin_answer ==3:
            print("YOU HAVE THE SAME ANSWERS TYPE AGAIN")
            self.gamer_goblin(enviorment)  # if the answers match then repeat the procedure
        return enviorment

    def gamer_monster(self,enviorment):
        user_input=input("TYPE YOUR ANSWER ")
        monster_answer=random.randint(1,3)
        print(monster_answer)
        if user_input =="P" and monster_answer==1:  # starts comparing human and goblin answer
            self._health=self._health-50
            self._coins=self._coins-100
            print("YOU LOSE AND YOUR HEALTH IS ",self._health,"YOUR COINS ARE",self._coins)

        elif user_input =="P" and monster_answer==2:
            print("YOU WIN CONTINUE ON YOUR WAY")

        elif user_input =="P" and monster_answer==3:
            print("YOU HAVE THE SAME ANSWERS TYPE AGAIN")
            self.gamer_monster(enviorment)  # if the answers match then repeat the procedure

        if user_input =="R" and goblin_answer==1:
            self._health = self._health - 50
            self._coins = self._coins -100
            print("YOU LOSE AND YOUR HEALTH IS ", self._health, "YOUR COINS ARE", self._coins)

        elif user_input =="R" and monster_answer ==2:
            print("YOU WIN CONTINUE ON YOUR WAY")

        elif user_input =="R" and monster_answer ==3:
            print("YOU HAVE THE SAME ANSWERS TYPE AGAIN")
            self.gamer_monster(enviorment)

        if user_input =="I" and monster_answer ==1:
            self._health = self._health - 50
            self._coins = self._coins - 100
            print("YOU LOSE AND YOUR HEALTH IS ", self._health, "YOUR COINS ARE", self._coins)

        elif user_input =="I" and monster_answer ==2:
            print("YOU WIN CONTINUE ON YOUR WAY")

        elif user_input =="I" and monster_answer ==3:
            print("YOU HAVE THE SAME ANSWERS TYPE AGAIN")
            self.gamer_monster(enviorment)  # if the answers match then repeat the procedure
        return enviorment



