from subprocess import Popen, PIPE, STDOUT
import game_files.GameLogic as logic
import game_files.character as chr
from game_files.item import Item
import random
import pandas as pd

class Game:


	def __init__(self) -> None:
		
		pd.set_option('display.max_columns', 999)
		self.init_state()
		self.game_loop()

	#wprowadza stan swiata pierwszy
	def init_state(self):
		self.df_effects = pd.read_csv('data\effects_nn.csv')

		self.characters = ['mc','actor','actress','soldier']
		lists = []
		columns = []
		columns.append('character')
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

		self.df_state = pd.DataFrame( columns=columns )
		self.df_state

		d = []
		d.append('world')
		for l in lists:
			d.append(random.choice(l))
		self.df_state.loc[len(self.df_state)] = d

		for entity in self.characters:
			d[0] = entity
		
			
			self.df_state.loc[len(self.df_state)] = d
    

		self.current_character = self.characters[0]
		#self.character_rotation()
		#self.print_state()
		
		

	def print_state(self):
		print(self.df_state)
			

		

	#odpala plan i przejmuje akcje
	def load_action(self,file):

		
		p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0","-h","h+",'-c','n',"-tl","5000"], stdout=PIPE, stderr=STDOUT)
		#p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0",'-g',"","-tl","1000"], stdout=PIPE, stderr=STDOUT)

		lines=[]
		for line in p.stdout:
			lines.append(str(line, encoding='utf-8'))

		#print(lines)
		return lines[0].replace("\r\n","")

	#wykonuje akcje 
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
					self.df_state[feature] = change[1]
				elif change[0] == "+":
					self.df_state[feature] = int(self.df_state[self.df_state.character == 'world'][feature]) + int(change[1])
				elif change[0] == "-":
					self.df_state[feature] = int(self.df_state[self.df_state.character == 'world'][feature]) - int(change[1])
				
			
		
		
		
		
	#aktualizuje stan swiata
	def change_state(self,actions):
		
		
		
		print(actions)
		if 'No solution' not in actions:
			actions = actions.split(') ')
			
			if len(actions) > 0:
				args = actions[0].replace("("," ").replace(")","").replace(",","")
				print(args)
				if ('key_action' not in args) :
					self.do_action(args.split(" "))
				
				return True
		
		return False
		
	def character_rotation(self):
		
		index = self.characters.index(self.current_character)
		if index == len(self.characters) - 1:
			self.current_character = self.characters[1]
		else:
			self.current_character = self.characters[index+1]
		
	

	def game_loop(self):
		#jeszcze sprawdzenie wszystkich goali
		while True:
			self.print_state()
			self.character_rotation()
			
			self.create_file(self.df_state[self.df_state.character == self.current_character])
			self.change_state(self.load_action('lib\\boat_loop.txt'))

			command = ''
			while command != 'next'  :
				command = input("write next \n")
				self.change_state(command)
				self.print_state()
			
			

	#tworzy nowy plik
	def create_file(self,row):
		characters = self.characters
		current_character = row.character.values[0]
		with open("lib/boat_loop.txt", 'w') as f:
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
			for char in characters:
			
				f.write("entity "+ char + ": character;  \n")
				f.write("health(" + char  +") = " + str(row[char+"_health"].values[0]) + " ;\n")
				f.write("altruism(" + char  +") = " + str(row[char+"_altruism"].values[0]) + " ;\n")
				f.write("ambition(" + char  +") = " + str(row[char+"_ambition"].values[0]) + " ;\n")
				f.write("knowledge(" + char  +") = " + str(row[char+"_knowledge"].values[0]) + " ;\n")
				f.write("support(" + char  +") = " + str(row[char+"_support"].values[0]) + " ;\n")
				f.write("money(" + char  +") = " + str(row[char+"_money"].values[0]) + " ;\n")
				f.write("state(" + char  +") = " + str(row[char+"_state"].values[0]) + " ;\n")
				
				char_without_c = characters.copy()
				char_without_c.remove(char)
				for c2 in char_without_c:
					f.write("relation(" + char  +", "+ c2 +") = " + str(row[char+"_relation_"+c2].values[0]) + " ;\n")
					if str(row[char+"_relation_"+c2].values[0]) == 1:
						f.write("supports(" + char  +", "+ c2 +")   ;\n")
				   
				f.write("ship_defense(world) =" +str(row['ship_defense'].values[0]) + ";  \n")
				f.write("ship_status(world) =" +str(row['ship_status'].values[0]) + " ; \n")
				f.write("ship_magic(world) =" +str(row['ship_magic'].values[0]) + ";  \n")
			

				
				

			f.write("""//key akcje
	action key_action1(char:character) {{
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
	}};


	action key_action2(char:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&ship_status(world) < 0
			&authority(char) > 1
			//&relation(char2,char1) < 0
			;
		effect:
			if(altruism(char) <= 2 & ambition(char) > 2 )
				satisfaction(char) = satisfaction(char) + 1
			
			;
		consenting: char;
	}};

	action key_action3(char:character) {{
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
	}};


//akcje

	action change_health_down(char:character,char2:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {0}
			;
		effect:
			health(char2) = health(char2) - 1
			& later(world) 
			;
		consenting: char;
	}};

	action change_health_up(char:character,char2:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {0}
			;
		effect:
			health(char2) = health(char2) + 1 
			& later(world)
			;
		consenting: char;
	}};


	 action change_knowledge_down(char:character,char2:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&knowledge(char) > 1
			&char == {0}
			;
		effect:
			knowledge(char2) = knowledge(char2) - 1
			& later(world) 
			;
		consenting: char;
	}};

	action change_knowledge_up(char:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {0}
			&state(char) == hidden
			;
		effect:
			knowledge(char) = knowledge(char) + 1
			& later(world)
			;
		consenting: char;
	}};

	action change_relation_down(char:character,char2:character,char3:character) {{
		precondition:
	
			health(char) > 0
			&state(char)!= blocked 
			&char == {0}
			;
		effect:
			relation(char2,char3) = relation(char2,char3) - 1 
			& health(char) = health(char) - 1 
			& later(world)
			;
		consenting: char;
	}};

	action change_relation_up(char:character,char2:character,char3:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {0}
			;
		effect:
			relation(char2,char3) = relation(char2,char3) + 1 
			& later(world)
			;
		consenting: char;
	}};


	action hide(char:character) {{
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
	}};

	action find(char:character,char2:character) {{
		precondition:
	
			health(char) > 0 
			& state(char2) == hidden
			&state(char)!= blocked
			&char == {0}
			;
		effect:
			state(char2) = ?
			& later(world)
			;
		consenting: char;
	}};

	action block(char:character,char2:character) {{
		precondition:
	
			 state(char2) != blocked
			 &char == {0}
			;
		effect:
			state(char2) = blocked
			& later(world)
			;
		consenting: char;
	}};

	action unblock(char:character,char2:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			& state(char2) == blocked
			&char == {0}
			;
		effect:
			state(char2) = ?
			& later(world)
			;
		consenting: char;
	}};
		   
		   action unblock_yourself(char:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)== blocked
			
			&char == {0}
			;
		effect:
			state(char) = ?
			& later(world)
			;
		consenting: char;
	}};

	action change_ship_defense_down(char:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {0}
			;
		effect:
			ship_defense(world) = ship_defense(world) - 1
			& later(world)
			;
		consenting: char;
	}};

	action change_ship_defense_up(char:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {0}
			;
		effect:
			ship_defense(world) = ship_defense(world) + 1
			& later(world)
			
			;
		consenting: char;
	}};


	action change_ship_magic_down(char:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {0}
			;
		effect:
			ship_magic(world) = ship_magic(world) - 1
			& later(world)
			;
		consenting: char;
	}};

	action change_ship_magic_up(char:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {0}
			;
		effect:
			ship_magic(world) = ship_magic(world) + 1
			& later(world)
			;
		consenting: char;
	}};


	action change_ship_status_down(char:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
		   &char == {0}
			;
		effect:
			ship_status(world) = ship_status(world) - 1
			& later(world)
			;
		consenting: char;
	}};

	action change_ship_status_up(char:character) {{
		precondition:
	
			health(char) > 0 
			&state(char)!= blocked
			&char == {0}
			;
		effect:
			ship_status(world) = ship_status(world) + 1
			;
		consenting: char;
	}};


	action support(char:character,char2:character, char3:character) {{
		precondition:
	
			 state(char) != blocked
			 &char == {0}
			 &char != char2
			 &!supports(char,char2)
			;
		effect:
			supports(char,char2)
			& support(char2) = support(char2) + 1
			& later(world)
			;
		consenting: char;
	}};

action lose_support(char:character,char2:character) {{
		precondition:
	
			 state(char) != blocked
			 &char == {0}
			 &char != char2
			 &supports(char,char2)
			;
		effect:
			!supports(char,char2)
			& support(char2) = support(char2) - 1
			& later(world)
			;
		consenting: char;
	}};

action support_money(char:character,char2:character, char3:character) {{
		precondition:
	
			 state(char) != blocked
			 &char != char3
			 &char != char2
			 &char == {0}
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
	}};

action lose_support_money(char:character,char2:character, char3:character) {{
		precondition:
	
			 state(char2) != blocked
			 &char == {0}
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
	}};

action support_authority(char:character,char2:character, char3:character) {{
		precondition:
	
			 state(char2) != blocked
			 &char != char3
			 &char != char2
			 &char == {0}
			 &!supports(char2,char3)
			 &authority(char) > 2
			;
		effect:
			supports(char2,char3)
			& support(char3) = support(char3) + 1
			& later(world)
		   
			;
		consenting: char;
	}};

action lose_support_authority(char:character,char2:character, char3:character) {{
		precondition:
	
			 state(char2) != blocked
			 &char == {0}
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
	}};


trigger authority_calc(char:character) {{
	precondition:
		authority(char) != (if (health(char)>2)  1 else 0 )+  knowledge(char) + support(char)  ;
	effect:
		authority(char) == (if (health(char)>2)  1 else 0 ) +  knowledge(char)   + support(char)   ;
}};


			""".format(current_character))

			
			
			f.write("utility(): \n ")
			f.write("satisfaction({0}) ;\n".format(current_character))

			
		


			for char in characters:
				f.write("utility({0}): \n ".format(char))
				f.write("satisfaction({0}); \n ".format(char))
			
			
			f.close()

gm = Game()
