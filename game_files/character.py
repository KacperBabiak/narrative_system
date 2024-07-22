from game_files.item import Item
import random

class Character:
    

    def __init__(self,gl, name, altruism,ambition, max_ambition,money = 0, support = 0, sat = 0,health = 2, state = '?') -> None:
            self.name = name
            self.health = health

            self.satisfaction = sat
            self.altruism = altruism
            self.ambition = ambition
            self.max_ambition = max_ambition
            self.relation = {}
            self.support = support
            self.supports = {}
            self.money = money
            self.state = state


            self.gameLogic = gl

            

           
     
            
    

    