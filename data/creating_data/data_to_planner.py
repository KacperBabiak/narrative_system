from subprocess import Popen, PIPE, STDOUT
import pandas as pd
import time

def load_action(file):

		
		p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0","-h","h+",'-c','n',"-tl","5000"], stdout=PIPE, stderr=STDOUT)
		#p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0",'-g',"","-tl","1000"], stdout=PIPE, stderr=STDOUT)

		lines=[]
		for line in p.stdout:
			lines.append(str(line, encoding='utf-8'))

		#print(lines)
		return lines 



def create_file(characters,items,row):
		with open("lib/test2.txt", 'w') as f:
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
			&char == char_acting
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
			&char == char_acting
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
			&char == char_acting
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
			&char == char_acting
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
			&char == char_acting
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
			&char == char_acting
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
			&char == char_acting
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
			 &char == char_acting
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
			&char == char_acting
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
			
			&char == char_acting
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
			&char == char_acting
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
			&char == char_acting
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
			&char == char_acting
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
			&char == char_acting
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
		   &char == char_acting
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
			&char == char_acting
			;
		effect:
			ship_status(world) = ship_status(world) + 1
			;
		consenting: char;
	};


	action support(char:character,char2:character, char3:character) {
		precondition:
	
			 state(char) != blocked
			 &char == char_acting
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
			 &char == char_acting
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
			 &char == char_acting
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
			 &char == char_acting
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
			 &char == char_acting
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
			 &char == char_acting
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


			""")

			
			
			f.write("utility(): \n ")
			f.write("satisfaction({}) ;\n".format("char_acting"))

			
		


			for char in characters:
				f.write("utility({}): \n ".format(char))
				f.write("satisfaction({}); \n ".format(char))
			
			
			f.close()

characters = ['char_acting', 'char1', 'char2']
items = ['food']
file = 'lib/test2.txt'

df = pd.read_csv('data\\creating_data\\random_states.csv')

for index in range(0,len(df)):
	print(index)
	
	start = time.time()

	row=df.loc[index]
	create_file(characters, items, row)
	action = load_action(file)
	

	end = time.time()
	
	
	df.loc[index,['results']] = action
	df.loc[index,['time']] = (end-start)

	print(action)
	print(end-start)

	df.to_csv('data/random_states_results.csv')

	
	

#print(df)