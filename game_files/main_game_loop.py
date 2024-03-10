import pandas as pd
import random

class Main_Loop:

    def __init__(self) -> None:
        
        self.world_state = pd.read_csv('game_files\gameState.csv').set_index("Name")
        #self.give_main_goal()
        #self.randomize_start()
        #print(self.world_state)
        self.start_loop()
        
        #self.print_islands()


    def give_goal(self):
        
        characters = list(self.world_state.index.drop('World'))
        items = ['Fuel', 'Gold', 'Food', 'Meds','Map']

        #zdobycie surowca

        for ind in random.sample(characters,5):
            wants = random.choice(items)

            #print(wants)
            self.world_state.at[ind, 'Wants_'+wants] = 1

        #zabicie innego gracza
        
        for ind in random.sample(characters,2):
            kill = random.choice(characters)

            if ind != kill:
                self.world_state.at[ind, 'Attacks_'+kill] = 1
            
    def create_islands(self):
        islands = ['Island1','Island2','Island3']

        characters = list(self.world_state.index.drop(['World','Mc']))
        
        number = 2
        chosen_list = ['']

        while len(characters) > 0:
    
            chosen = (random.sample(characters,number))
            characters = [x for x in characters if x not in chosen]
            chosen_list.append(chosen)
            
            number = len(characters)
            
        self.chosen_island = dict(zip(islands, chosen_list))
        #print(chosen_island)

    def print_islands(self):
        text = " "

        for key in self.chosen_island.keys():
            text = text + key + str(self.chosen_island[key]) + "\n"

        #print(text)
        return text

    def start_loop(self):
        self.give_goal()
        #randomize first event
        self.create_islands()
        #self.prepare_island('Island2')

    def prepare_island(self,isl):
        chars = list(self.chosen_island[isl])
        chars.extend(['World','Mc'])
        #losuj surowce

        isl_df = self.world_state[self.world_state.index.isin(chars)]

        isl_df.to_csv('game_files/islandState.csv')

    #aktualizuje jak wyglada świat po akcji wyspy
    def update_world(self,df):
        #aktualizacja zmian z wyspy
        self.world_state.update(df)
        #przywórcenie niektórych atrybutów
        self.world_state['Satifaction'] = 0
        self.world_state['Ambition'] += 2

#Main_Loop()