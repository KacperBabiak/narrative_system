from game_files.item import Item
import random

class Character:
    

    def __init__(self,gl, name, altruism,ambition,points = 0,health = 15) -> None:
            self.name = name
            self.points = points
            self.health = health

            self.happiness = 10
            self.altruism = altruism
            self.ambition = ambition

            self.gameLogic = gl

            self.likes = {}
            self.trusts = {} 

            self.goals = []
            self.start_goals = []
             
            self.items = {}
     
            
    

    def add_char(self,character, like, trust) -> None :
         self.likes[character] = like
         self.trusts[character] = trust

    def add_item(self,item):
        if item in self.items.keys():
            self.items[item] += 1
        else: self.items[item] = 0 
    
    def check_goals(self):

        goals = []

        goals.append("(happiness({})> {})".format(self.name,self.happiness))

        if self.health < 5 : 
            goals.append("(health({})> {})".format(self.name,self.health))
            number = 0
            if self.gameLogic.items['food'] in self.items:
                number = self.items[self.gameLogic.items['food']]
            goals.append("(has({},food)> {})".format(self.name,number))
        
        #zrób wzory
        if self.ambition > 13:
            number = 0
            if self.gameLogic.items['money'] in self.items:
                number = self.items[self.gameLogic.items['money']]
            goals.append("(has({},money)> {})".format(self.name,number))
        elif self.ambition > -7:
            if self.altruism > 20:
                for char in self.likes.keys():
                    goals.append("(happiness({})> {})".format(char.name,char.happiness))
                    
            elif self.altruism > 10:
                for char in self.likes.keys():
                    if self.likes[char] > -7:
                       goals.append("(happiness({})> {})".format(char.name,char.happiness))
                    elif self.likes[char] < -7:
                       goals.append("(happiness({})< {})".format(char.name,char.happiness))   

            elif self.altruism < -10:
                for char in self.likes.keys():
                    if self.likes[char] > 15:
                       goals.append("(happiness({})> {})".format(char.name,char.happiness))
                    else:
                       goals.append("(happiness({})< {})".format(char.name,char.happiness)) 

            elif self.altruism < -20:
                for char in self.likes.keys():
                    goals.append("(happiness({})< {})".format(char.name,char.happiness)) 
            
        
        print(goals)
        self.goals = goals
        self.goals.extend(self.start_goals)
        print(self.goals)

    def add_goals(self):
        
        goals_nbs = random.sample(range(1, 10), 1)
        
        
        for goal in goals_nbs:
            g= ""
            
            match goal:
                
                case 1:
                    char = random.choice(list(self.likes.keys()))
                    g="(health({})>{})".format(char.name,char.health)
                
                case 2:
                    item = random.choice( list(self.gameLogic.items.values()) )
                    number = 0
                    if item in self.items:
                        number = self.items[item]
                    g="(has({},{})>{})".format(self.name,item.name,number)
                
                case 3:
                    g="(altruism({}) > {})".format(self.name,self.altruism)
                case 4:
                    g="(altruism({}) < {})".format(self.name,self.altruism)
                
                case 5:
                    g="(ambition({}) > {})".format(self.name,self.ambition)
                case 6:
                    g="(ambition({}) > {})".format(self.name,self.ambition)
                case 7:
                    item = random.choice( list(self.gameLogic.items.values()) )
                    number = 0
                    if item in self.items:
                        number = self.items[item]
                    g="(has({},{})>{})".format(self.name,item.name,number)
                case 8:
                    item = random.choice( list(self.gameLogic.items.values()) )
                    number = 0
                    if item in self.items:
                        number = self.items[item]
                    g="(has({},{})>{})".format(self.name,item.name,number)
                case 9:
                    item = random.choice( list(self.gameLogic.items.values()) )
                    number = 0
                    if item in self.items:
                        number = self.items[item]
                    g="(has({},{})>{})".format(self.name,item.name,number)
    
            """
                case 2:
                    char = random.choice(list(self.likes.keys()))
                    g="(happiness({})>{})".format(char.name,char.happiness)
                case 3:
                    char = random.choice(list(self.likes.keys()))
                    g="(happiness({})<{})".format(char.name,char.happiness)
                """ 
            self.start_goals.append(g)
            self.goals.append(g)
            
            return g    
             

            
        
    def give(self, other, item):
        self.items[item ] -= 1
        other.add_item(item) 

        
        self.happiness += round(self.likes[other]/6,3)
        self.altruism +=  2
        self.likes[other] +=  1

        
        other.happiness +=  3
        other.altruism +=  3
        other.likes[self] +=  2
        other.trusts[self] += 2

    def take(self, other, item):
        self.add_item(item) 
        other.items[item] -= 1

        
        self.happiness -= round(self.likes[other]/5 + self.altruism/2,3)
        self.altruism -=  3
        self.ambition += 2
        self.trusts[other] -=  3
        self.health -=2
        
        other.happiness -=  4
        other.altruism -=  3
        other.ambition += 1
        other.likes[self] -=  4
        other.trusts[self] -= 4
        self.health -=3

    def exchange(self, other, item1, item2):
        self.items[item1 ] -= 1
        other.add_item(item1) 
        
        self.add_item(item2) 
        other.items[item2] -= 1

        
        
        self.happiness += 3
        self.altruism +=  1
        self.ambition += 1
        self.likes[other] +=  1
        self.trusts[other] += 2

        
        other.happiness += 3
        other.altruism +=  1
        other.ambition += 1
        other.likes[self] +=  1
        other.trusts[self] += 2

    

    def compliment(self, other):
        
        self.happiness += round(self.altruism/7 + self.likes[other]/7,3)
        self.altruism +=  2
        self.likes[other] +=  1
        self.trusts[other] += 1

        other.happiness += round(other.altruism/7 + other.likes[self]/7,3)
        other.altruism +=  2
        other.likes[self] +=  3
        other.trusts[self] += 1

    def intimidate(self, other):
        
        self.happiness -= round(self.altruism/7 + self.likes[other]/3,3)
        self.altruism -=  2
        self.trusts[other] -= 1

        other.happiness -= round(other.altruism/7 + other.likes[self]/7,3)
        other.altruism -=  3
        other.ambition -=  3
        other.likes[self] -=  4
        other.trusts[self] -= 1

    def gossip_about(self, other,about):
        self.happiness -= round(self.altruism/8,3 )
        self.altruism -=  1
        

        other.happiness -= round(other.altruism/8,3)
        other.altruism -=  1
        other.likes[self] +=  1
        other.trusts[self] -= 1
		
        other.likes[about] -=  round(2 + other.trusts[self]/6,3)
        other.trusts[about] -= round(2 + other.trusts[self]/6,3)

    def praise_someone(self, other,about):
        self.happiness += round(self.altruism/8 ,3)
        self.altruism +=  1
        

        other.happiness += round(other.altruism/8,3)
        other.altruism +=  1
        other.likes[self] +=  1
        other.trusts[self] += 1
		
        other.likes[about] +=  round(2 + other.trusts[self]/6,3)
        other.trusts[about] += round(2 + other.trusts[self]/6,3)

    def attack(self, other):
        
        self.happiness -= round(self.altruism/5 + self.likes[other]/5 + 5,3)
        self.altruism -=  4
        self.ambition += 3
        self.trusts[other] -= 2

        other.health -= 10
        other.happiness -= round(other.altruism/5 + 3,3)
        other.altruism -=  4
        other.ambition -= 2
        other.likes[self] -=  4
        other.trusts[self] -= 4

    def rest(self):
        self.health += 5
        self.happiness += 4

    def take_care_of(self, other):
        
        self.happiness += round(self.altruism/7 + self.likes[other]/7,3)
        self.altruism +=  2
        self.likes[other] +=  2
        self.trusts[other] += 1

        other.health += 10
        other.happiness += 5
        other.altruism +=  4
        other.likes[self] +=  5
        other.trusts[self] += 2

    def work(self):
        self.add_item(self.gameLogic.items['money'])  
        self.health -= 3
        self.happiness += round(self.ambition/7 ,3)
        self.ambition += 1
    
    def eat(self):
        self.items[self.gameLogic.items['food']] -=1
        self.health += 5
        self.happiness += 2

    def read(self):
        self.happiness += 3

    def spend_time_together(self, other):
        
        self.happiness += round( self.likes[other]/4,3)
        self.altruism +=  2
        self.likes[other] +=  3
        self.trusts[other] += 2

        
        other.happiness += round( other.likes[self]/4,3)
        other.altruism +=  2
        other.likes[self] +=  3
        other.trusts[self] += 2
        