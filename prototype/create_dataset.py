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



def create_file(characters,items,places,utilities,row):
		
		acting_character = str(row["acting_char"])
		with open("prototype\\basketball_prototype.txt", 'w') as f:
			f.write("""type item;
type place;
type basketballPlace : place;
type arrestPlace : place;
type crime; 
type citizen : character;
type police : character;
type detective : police;
type inspector : police;

property alive(character : character) : boolean;
property underArrest(character : character) : number;
property angry(character : character) : number;
property searched(place : place) : number;
property suspect(character : character, c : crime) : boolean;
property clue(crime : crime, item : item, place : place) : boolean;
property at(character : character) : place;
property has(item : item) : character;

entity Alice : citizen;
entity Bob : citizen;
entity Charlie : citizen;
entity Sherlock : detective;
entity HomeB : place;
entity BasketballCourt : basketballPlace;
entity Downtown : arrestPlace;
entity Basketball : item;
entity Bat : item;
entity Theft : crime;
entity Murder : crime;

		   """
			)
			
			for char in characters:
				if str(row[char+"_alive"]) == '1':
					f.write("alive(" + char  +")  ;\n")
				else:
					f.write("!alive(" + char  +")  ;\n")
				f.write("underArrest(" + char  +") = " + str(row[char+"_underArrest"]) + " ;\n")
				f.write("angry(" + char  +") = " + str(row[char+"_angry"]) + " ;\n")
				if str(row[char+"_suspect"]) != '2' and str(row[char+"_suspect"]) != '?':
					f.write("suspect(" + char + ', '+ str(row[char+"_suspect"]) +")   ;\n")
				f.write("at(" + char  +") = " + str(row[char+"_at"]) + " ;\n")

			
				
			for p in places:
				f.write("searched(" + p  +") = " + str(row[p+"_searched"]) + " ;\n")
				

			
			for i in items:
				f.write("has(" + i  +") = " + str(row[i+"_has"]) + " ;\n")
				
			clues = [x for x in row.index if 'clues' in x]
			
			for c in clues:
				if str(row[c]) == '1':
					
					entities = c.split('_')
					f.write("clue(" + entities[0]+","+entities[1]+","+ entities[2] +")   ;\n")
				#warrtosci postaci
			

				
				

			f.write("""
action travel(character : character, from : place, to : place){{
	precondition:
		from != to & 
		at(character) == from &
		alive(character)
		&character == {0};
	effect:
		at(character) = to;
	consenting: character; 
	observing(c : character) : at(c) == from | at(c) == to; 
}};

action arrest(police : police, character : character, place : place, crime : crime){{
	precondition: 
		at(police) == place &
		at(character) == place &
		police != character &
		alive(police) &
		alive(character) &
		suspect(character, crime)&police == {0};
	effect:
		underArrest(character) = 1;
	consenting: police;
	observing(a : character) : at(a) == place;
}};

action steal(thief : citizen, victim : citizen, item : item, place : place){{
	precondition:
		at(thief) == place &
		at(victim) == place &
		has(item) == victim &
		thief != victim &
		alive(thief)&thief == {0};
	effect:
		has(item) = thief &
		angry(victim) = 1 &
		clue(Theft, item, place);
	consenting: thief;
	observing(c : character) : (c == thief | c == victim) | (at(c) == place & place != Downtown); // crimes downtown aren't observed
}};

action play_basketball(player1 : citizen, player2 : citizen, place : basketballPlace){{
	precondition:
		player1 != player2 &
		at(player1) == place &
		alive(player1) &
		at(player2) == place &
		alive(player2) &
		has(Basketball) == player1 & player1 == {0};
	effect:
		angry(player1) = 0 &
		angry(player2) = 0;
	consenting: player1;
	observing(c : character) : at(c) == place;
}};

action kill(killer : citizen, victim : citizen, item : item, place : place){{
	precondition:
		killer != victim &
		at(killer) == place &
		at(victim) == place &
		alive(killer) &
		alive(victim) &
		has(item) == killer &
		underArrest(killer) == 0 & killer == {0};
	effect:
		!alive(victim) &
		clue(Murder, item, place);
	consenting: killer;
	observing(c : character) : c == killer | (at(c) == place & place != Downtown); 
}};
	
action find_clues(police : police, crime : crime, item : item, place : place){{
	precondition:
		at(police) == place &
		alive(police)
		&clue(crime, item, place) &police == {0};
	effect:
		searched(place) = 1 &
		if(clue(crime, item, place))
			believes(police, clue(crime, item, place));
	consenting: police;
	observing(c : character) : at(c) == place;
}};

action share_clues(police1 : police, police2 : police, crime : crime, item : item, place : place){{
	precondition:
		police1 != police2 &
		at(police1) == place &
		alive(police1) &
		at(police2) == place &
		alive(police2) &
		clue(crime, item, place) &police1 == {0} ;
	effect:
		believes(police2, clue(crime, item, place));
	consenting: police1;
	observing(c : character) : at(c) == place;
}};
 
action suspect_of_crime(police : police, citizen : citizen, crime : crime, item : item, place : place){{
	precondition:
		police != citizen &
		at(police) == place &
		alive(police) &
		at(citizen) == place &
		alive(citizen) &
		has(item) == citizen
		&police == {0} &
		exists(p : place) clue(crime, item, p);
	effect:
		suspect(citizen, crime);
	consenting: police;
	observing(c : character) : at(c) == place;
}};
trigger see_has(character : character, other : character, item : item, place : place){{
	precondition:
		at(character) == place &
		at(other) == place &
		has(item) == other &
		believes(character, has(item) != other);
	effect:
		believes(character, has(item) = other);
}};

trigger see_hasnt(character : character, other : character, item : item, place : place){{
	precondition:
		at(character) == place &
		at(other) == place &
		has(item) != other & 
		believes(character, has(item) == other);
	effect:
		believes(character, has(item) = ?);
}};

trigger see_at(character : character, other : character, place : place){{
	precondition:
		at(character) == place &
		at(other) == place &
		believes(character, at(other) != place);
	effect:
		believes(character, at(other) = place);
}};

trigger see_gone(character : character, other : character, place : place){{
	precondition:
		at(character) == place &
		at(other) != place &
		believes(character, at(other) == place);
	effect:
		believes(character, at(other) = ?);
}};

			""".format(str(acting_character)))

			
			
			f.write("utility(): \n ")
			f.write(utilities[acting_character])

			
		


			for char in characters:
				f.write("utility({}): \n ".format(char))
				f.write(utilities[char])
			
			
			f.close()

characters = ['Alice', 'Bob', 'Charlie','Sherlock']
items = ['Basketball','Bat']
places= ['HomeB','BasketballCourt','Downtown']
crimes = ['Theft','Murder']
utilities = {
	'Alice':'1 - angry(Alice);\n',
	'Bob':'3 - (sum(c : citizen) angry(c));\n',
	'Charlie':'if(!alive(Alice)) 1 else 0;\n',
	'Sherlock':'(sum(c : citizen) underArrest(c)) + (sum(p : place) searched(p)); \n',
}
file = 'prototype\\basketball_prototype.txt'

df = pd.read_csv('prototype\\table_training_simple.csv')

for index in range(0,len(df)):
	print(index)
	
	start = time.time()

	row=df.loc[index]
	create_file(characters, items, places,utilities, row)
	action = load_action(file)
	

	end = time.time()
	
	
	df.loc[index,['results']] = action
	df.loc[index,['time']] = (end-start)

	print(action)
	print(end-start)

	df.to_csv('prototype\dataset_results.csv',index=False)

	
	

#print(df)