
class Character:
    

    def __init__(self,gl, name,altruism,ambition) -> None:
            self.name = name
            self.points = 3
            self.lighted_candle = 0
            self.health = 10

            self.happiness = 0
            self.altruism = altruism
            self.ambition = ambition

            self.gameLogic = gl

            self.likes = {}
            self.trusts = {} 

            self.items = {}
     
    

    def add_char(self,character, like, trust) -> None :
         self.likes[character] = like
         self.trusts[character] = trust

    def add_item(self,item):
         self.items[item] += 1  

    def light_first_candle(self):
        self.lighted_candle = True
        self.points +=1

        if self.ambition > 10:
             self.ambition += 5
             self.happiness += 5
        elif self.ambition < -10:
             self.ambition -= 5
             self.happiness -= 5

        self.gameLogic.candles += 1
        self.gameLogic.first_candle_char = self

    def light_another_candle(self, char):
        self.lighted_candle = True
        self.points +=1
        char.points +=1

        self.ambition += 3

        if self.altruism >= 0:
            self.happiness += 2
        elif self.altruism < -10:
             self.happiness -= 1

        if self.likes[char] > 5:
            self.happiness += 3
        elif self.likes[char] < -5:
            self.happiness -= 2

        char.likes[self] += 2
        char.trusts[self] += 2
        char.altruism += 1

        self.gameLogic.candles += 1


    def put_out_candle(self, char):
        
        self.points += self.gameLogic.candles
        char.points -= self.gameLogic.candles

        self.ambition += 2
        self.altruism -= 4

        if self.altruism > 10:
            self.happiness -= 5
        elif self.altruism < -10:
             self.happiness += 4

        if self.ambition > 10:
            self.happiness += 2
        elif self.ambition < -10:
             self.happiness -= 4

        if self.likes[char] > 10:
            self.happiness -= 4
        elif self.likes[char] < -10:
            self.happiness += 4

        char.likes[self] -= 5
        char.trusts[self] -= 5
        char.altruism -= 2

        self.gameLogic.candles = 0
        self.gameLogic.first_candle_char = None

        for char in self.gameLogic.characters.values() :
             char.lighted_candle = False


    def put_out_first_candle(self):
        

        if self.ambition > 10:
             self.happiness -= 3
        elif self.ambition < -10:
             self.happiness += 3

        self.gameLogic.candles = 0
        self.gameLogic.first_candle_char = None

        for char in self.gameLogic.characters :
             char.lighted_candle = False
            