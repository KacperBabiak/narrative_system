import numpy as np
import pygame
import pandas as pd
import random
from subprocess import Popen, PIPE, STDOUT
import gymnasium as gym
from gymnasium import spaces
import time

class TestEnv(gym.Env):
	#metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

	def __init__(self, render_mode=None ):
		#self.size = size  # The size of the square grid
		
		
		#self._nb_features = 39
		self.characters = [ 'char1', 'char2','char3','char4']
		self.acting_character = self.characters[0]
		self.additional_utility = None
		self.df_effects = pd.read_csv('data\effects_nn.csv')
		self.randomize_df()
		self._nb_features = len(self.df.columns)
		# Observations are dictionaries with the agent's and the target's location.
		# Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
		self.observation_space = spaces.Box(
			-3,
			3,
			shape = [self._nb_features]
		)

		self.target_feature = 'ship_status'
		self.target_value = '-1'

		# We have 4 actions, corresponding to choosing character
		self.action_space = spaces.Discrete(10)

		"""
		The following dictionary maps abstract actions from `self.action_space` to
		the direction we will walk in if that action is taken.
		
		"""
		self._action_to_direction = {
			0: 'char1',
			1: 'char2',
			2: 'char3',
			3: 'char4',
			4: 'ship_status(world) > 0',
			5: 'ship_magic(world) > 0',
			6: 'ship_defense(world) > 0',
			7: 'ship_status(world) < 0',
			8: 'ship_magic(world) < 0',
			9: 'ship_defense(world) < 0',
		}

		assert render_mode is None or render_mode in self.metadata["render_modes"]
		self.render_mode = render_mode

		"""
		If human-rendering is used, `self.window` will be a reference
		to the window that we draw to. `self.clock` will be a clock that is used
		to ensure that the environment is rendered at the correct framerate in
		human-mode. They will remain `None` until human-mode is used for the
		first time.
		"""
		self.window = None
		self.clock = None



	def randomize_df(self):
		

		lists = []
		columns = []
		for c in self.characters:
			columns.append(c+"_health")
			lists.append([i for i in range(0,3)])

			columns.append(c+"_knowledge")
			lists.append([i for i in range(0,3)])

		

			columns.append(c+"_altruism")
			lists.append([i for i in range(-2,3)])
			columns.append(c+"_ambition")
			lists.append([i for i in range(0,5)])
			
			columns.append(c+"_support")
			lists.append([i for i in range(0,2)])

			columns.append(c+"_money")
			lists.append([i for i in range(0,2)])
			
			columns.append(c+"_satisfaction")
			lists.append([0])

			columns.append(c+"_state")
			lists.append(['?','blocked','hidden'])

			char_without_c = self.characters.copy()
			char_without_c.remove(c)
			for c2 in char_without_c:
				columns.append(c+"_relation_"+c2)
				lists.append([i for i in range(-2,3)])
				columns.append(c+"_supports_"+c2)
				lists.append([0,1])

			


		columns.append("ship_defense")
		lists.append([-1,0,1])

		columns.append("ship_status")
		lists.append([-1,0,1])

		columns.append("ship_magic")
		lists.append([-1,0,1])
		self.df = pd.DataFrame( columns=columns )

		d = []
		for l in lists:
			d.append(random.choice(l))
		self.df.loc[0] = d
		
	def create_file(self,characters,row):
		with open("lib/rl_planner.txt", 'w') as f:
			f.write("""//### Types:
type item;
type world;
type state;

//### Properties:
property health(char: character) : number; 
property knowledge(char: character) : number; 
property authority(char: character) : number; 


property satisfaction(char: character) : number; // Satisfaction level of each character
property altruism(char: character) : number; // Altruism level of each character (-3 to 3)
property ambition(char: character) : number; // Ambition level of each character (-3 to 3)
property max_ambition(char: character) : number; // Ambition level of each character (-3 to 3)
property relation(char: character, other: character) : number; // Relationship liking level between characters (-3 to 3)
property support(char: character) : number; 
property supports(char: character, other: character) : boolean;
property money(char: character) : number; 
property state(char: character) : state; 

property ship_defense(world:world) : number; 
property ship_magic(world:world) : number; 
property ship_status(world:world) : number;

property later(world:world) : boolean; 
entity world:world;

entity hidden :state;
entity blocked :state;
		   """
			)
			

				#warrtosci postaci
			for char in self.characters:
			
				f.write("entity "+ char + ": character;  \n")
				f.write("health(" + char  +") = " + str(row[char+"_health"]) + " ;\n")
				f.write("altruism(" + char  +") = " + str(row[char+"_altruism"]) + " ;\n")
				f.write("ambition(" + char  +") = " + str(row[char+"_ambition"]) + " ;\n")
				f.write("knowledge(" + char  +") = " + str(row[char+"_knowledge"]) + " ;\n")
				f.write("support(" + char  +") = " + str(row[char+"_support"]) + " ;\n")
				f.write("money(" + char  +") = " + str(row[char+"_money"]) + " ;\n")
				f.write("state(" + char  +") = " + str(row[char+"_state"]) + " ;\n")
				
				char_without_c = characters.copy()
				char_without_c.remove(char)
				for c2 in char_without_c:
					f.write("relation(" + char  +", "+ c2 +") = " + str(row[char+"_relation_"+c2]) + " ;\n")
					if str(row[char+"_relation_"+c2]) == 1:
						f.write("supports(" + char  +", "+ c2 +")   ;\n")
				   
				f.write("ship_defense(world) =" +str(row['ship_defense']) + ";  \n")
				f.write("ship_status(world) =" +str(row['ship_status']) + " ; \n")
				f.write("ship_magic(world) =" +str(row['ship_magic']) + ";  \n")
			

				
				

			f.write("""//key akcje
	action key_action1(char:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&ship_defense(world) > 0
			&ship_status(world) < 0
			;
		effect:
			if(altruism(char) > 2 & ambition(char) > 2 )
				satisfaction(char) = satisfaction(char) + 1
			;
		consenting: char;
	};


	action key_action2(char:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			//&ship_status(world) < 0
			&authority(char) > 1
			&relation(char2,char1) < 0
			;
		effect:
			if(altruism(char) <= 2 & ambition(char) > 2 )
				satisfaction(char) = satisfaction(char) + 1
			
			;
		consenting: char;
	};

	action key_action3(char:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&ship_magic(world) > 0
			&ship_status(world) > 0
			;
		effect:
			if(ambition(char) <= 2 )
			 satisfaction(char) = satisfaction(char) + 1
			;
		consenting: char;
	};


//akcje

	action change_health_down(char:character,char2:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {}
			;
		effect:
			health(char2) = health(char2) - 1
			& later(world) 
			;
		consenting: char;
	};

	action change_health_up(char:character,char2:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {}
			;
		effect:
			health(char2) = health(char2) + 1 
			& later(world)
			;
		consenting: char;
	};


	 action change_knowledge_down(char:character,char2:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&knowledge(char) > 1
			&char == {}
			;
		effect:
			knowledge(char2) = knowledge(char2) - 1
			& later(world) 
			;
		consenting: char;
	};

	action change_knowledge_up(char:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {}
			&state(char) == hidden
			;
		effect:
			knowledge(char) = knowledge(char) + 1
			& later(world)
			;
		consenting: char;
	};

	action change_relation_down(char:character,char2:character,char3:character) {
		precondition:
	
			health(char) > 0
			&state(char)!= blocked 
			&char == {}
			;
		effect:
			relation(char2,char3) = relation(char2,char3) - 1 
			& health(char) = health(char) - 1 
			& later(world)
			;
		consenting: char;
	};

	action change_relation_up(char:character,char2:character,char3:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {}
			;
		effect:
			relation(char2,char3) = relation(char2,char3) + 1 
			& later(world)
			;
		consenting: char;
	};


	action hide(char:character) {
		precondition:
	
			health(char) > 0 
			& state(char) != hidden
			&state(char)!= blocked
			;
		effect:
			state(char) = hidden
			& later(world)
			;
		consenting: char;
	};

	action find(char:character,char2:character) {
		precondition:
	
			health(char) > 0 
			& state(char2) == hidden
			&state(char)!= blocked
			&char == {}
			;
		effect:
			state(char2) = ?
			& later(world)
			;
		consenting: char;
	};

	action block(char:character,char2:character) {
		precondition:
	
			 state(char2) != blocked
			 &char == {}
			;
		effect:
			state(char2) = blocked
			& later(world)
			;
		consenting: char;
	};

	action unblock(char:character,char2:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			& state(char2) == blocked
			&char == {}
			;
		effect:
			state(char2) = ?
			& later(world)
			;
		consenting: char;
	};
		   
		   action unblock_yourself(char:character) {
		precondition:
	
			health(char) > 0 
			&state(char)== blocked
			
			&char == {}
			;
		effect:
			state(char) = ?
			& later(world)
			;
		consenting: char;
	};

	action change_ship_defense_down(char:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {}
			;
		effect:
			ship_defense(world) = ship_defense(world) - 1
			& later(world)
			;
		consenting: char;
	};

	action change_ship_defense_up(char:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {}
			;
		effect:
			ship_defense(world) = ship_defense(world) + 1
			& later(world)
			
			;
		consenting: char;
	};


	action change_ship_magic_down(char:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {}
			;
		effect:
			ship_magic(world) = ship_magic(world) - 1
			& later(world)
			;
		consenting: char;
	};

	action change_ship_magic_up(char:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {}
			;
		effect:
			ship_magic(world) = ship_magic(world) + 1
			& later(world)
			;
		consenting: char;
	};


	action change_ship_status_down(char:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
		   &char == {}
			;
		effect:
			ship_status(world) = ship_status(world) - 1
			& later(world)
			;
		consenting: char;
	};

	action change_ship_status_up(char:character) {
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {}
			;
		effect:
			ship_status(world) = ship_status(world) + 1
			;
		consenting: char;
	};


	action support(char:character,char2:character, char3:character) {
		precondition:
	
			 state(char) != blocked
			 &char == {}
			 &char != char2
			 &!supports(char,char2)
			;
		effect:
			supports(char,char2)
			& support(char2) = support(char2) + 1
			& later(world)
			;
		consenting: char;
	};

action lose_support(char:character,char2:character) {
		precondition:
	
			 state(char) != blocked
			 &char == {}
			 &char != char2
			 &supports(char,char2)
			;
		effect:
			!supports(char,char2)
			& support(char2) = support(char2) - 1
			& later(world)
			;
		consenting: char;
	};

action support_money(char:character,char2:character, char3:character) {
		precondition:
	
			 state(char) != blocked
			 &char != char3
			 &char != char2
			 &char == {}
			 &!supports(char2,char3)
			 &money(char) > 0
			;
		effect:
			supports(char2,char3)
			& support(char3) = support(char3) + 1
			& later(world)
			&money(char) = money(char) - 1
			&money(char2) = money(char2) + 1
			;
		consenting: char;
	};

action lose_support_money(char:character,char2:character, char3:character) {
		precondition:
	
			 state(char2) != blocked
			 &char == {}
			 &char != char3
			 &char != char2
			 &supports(char2,char3)
			  &money(char) > 0
			;
		effect:
			!supports(char2,char3)
			& support(char3) = support(char3) - 1
			& later(world)
			&money(char) = money(char) - 1
			&money(char2) = money(char2) + 1
			;
		consenting: char;
	};

action support_authority(char:character,char2:character, char3:character) {
		precondition:
	
			 state(char2) != blocked
			 &char != char3
			 &char != char2
			 &char == {}
			 &!supports(char2,char3)
			 &authority(char) > 2
			;
		effect:
			supports(char2,char3)
			& support(char3) = support(char3) + 1
			& later(world)
		   
			;
		consenting: char;
	};

action lose_support_authority(char:character,char2:character, char3:character) {
		precondition:
	
			 state(char2) != blocked
			 &char == {}
			 &char != char3
			 &char != char2
			 &supports(char2,char3)
			 &authority(char) > 2
			;
		effect:
			!supports(char2,char3)
			& support(char3) = support(char3) - 1
			& later(world)
			
			;
		consenting: char;
	};


trigger authority_calc(char:character) {
	precondition:
		authority(char) != (if (health(char)>2)  1 else 0 )+  knowledge(char) + support(char)  ;
	effect:
		authority(char) == (if (health(char)>2)  1 else 0 ) +  knowledge(char)   + support(char)   ;
};


			""".format(self.acting_character))

			
			
			f.write("utility(): \n ")
			if self.additional_utility == None:
				f.write("satisfaction({}) > 0 & {};\n".format(self.acting_character,self.additional_utility))
			else:
				f.write("satisfaction({}) > 0;\n".format(self.acting_character))
			
		


			for char in characters:
				f.write("utility({}): \n ".format(char))
				if (char == self.acting_character) and (self.additional_utility != None):
					f.write("satisfaction({}) > 0 & {};\n".format(self.acting_character,self.additional_utility))
				else:
					
					f.write("satisfaction({}) > 0 ; \n ".format(char))
			
			
			f.close()


	def _get_obs(self):
		return self.df.head(0)
	
	def _get_info(self):
		return 0

	def reset(self, seed=None, options=None):
		# We need the following line to seed self.np_random
		#super().reset(seed=seed)

		#randomize row
		self.randomize_df()
		

		observation = self._get_obs() #turn row into observation
		info = self._get_info() #turn row into info

		if self.render_mode == "human":
			self._render_frame()

		return observation, info
	

	def reset(self, seed=None):
		
		return super().reset(seed)
	
	def load_action(file):

		
		p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0","-h","h+",'-c','n',"-tl","5000"], stdout=PIPE, stderr=STDOUT)
		#p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0",'-g',"","-tl","1000"], stdout=PIPE, stderr=STDOUT)

		lines=[]
		for line in p.stdout:
			lines.append(str(line, encoding='utf-8'))

		#print(lines)
		return lines 

	def do_action(self,args):
		if len(args) > 0 and len(self.df_effects[self.df_effects.action == args[0] ]['effect_function'].values) > 0:
			functions = self.df_effects[self.df_effects.action == args[0] ]['effect_function'].values[0].split(';')
			for function in functions:
				parts = function.split(':')

				#choosing feature
				feature = parts[0]
				for count,arg in enumerate(args,0):
					feature = feature.replace('arg'+str(count),arg)

				#choosing how feature is changed
				change = parts[1].split("_")

				print(feature)
				print(change)

				if change[0] == "=":
					self.df[feature] = change[1]
				elif change[0] == "+":
					self.df[feature] = int(self.df[self.df.character == 'world'][feature]) + int(change[1])
				elif change[0] == "-":
					self.df[feature] = int(self.df[self.df.character == 'world'][feature]) - int(change[1])
				
			

	def change_state(self,actions):
		
		
		
		
		if 'No solution' not in actions:
			actions = actions.split(') ')
			
			if len(actions) > 0:
				args = actions[0].replace("("," ").replace(")","").replace(",","")
				print(args)
				if ('key_action' not in args) :
					self.do_action(args.split(" "))
				
				return True
		
		return False

	def make_action(self,action):
		if 'char' in action:
			self.acting_character = action
		else:
			self.additional_utility = action

		self.create_file(self.characters,self._get_obs())
		start = time.time()

		
		file = 'lib/rl_planner.txt'
		self.results = self.load_action(file)
		

		end = time.time()
		
		index = 0
		self.df.loc[index,['results']] = self.results
		self.df.loc[index,['time']] = (end-start)

		print(self.results)
		self.change_state(self.results)
		
	def get_reward(self):
		#stworzenie targetu na poczatku
		reward = 0
		#czy osiagnelismy target jesli tak to 1
		if self.df.at[0,self.target_feature] == self.target_value:
			reward = 1
		elif 'No solution' in self.results or 'exceeded' in self.results:
			reward = -1
		#jesli nie to 0
		#jesli nie działa to minus
		#jesli to działa, to ustawienie samemu targetu, też w tabeli
		
		return reward

	def step(self, action):
		# Map the action (element of {0,1,2,3}) to the direction we walk in
		direction = self._action_to_direction[action]
		
		self.make_action(direction)

		
		terminated = False
		reward = self.get_reward()
		if reward == 1:
			terminated = True

		observation = self._get_obs()
		info = self._get_info()

		#if self.render_mode == "human":
			

		return observation, reward, terminated, False, info

TestEnv()