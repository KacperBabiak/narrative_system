from subprocess import Popen, PIPE, STDOUT
import pandas as pd
import time

def load_action(file):

		
		p = Popen(['java', '-jar', 'ship\\planners\\sabre.jar', '-p', file,'-el',"0","-h","h+",'-c','n',"-tl","5000"], stdout=PIPE, stderr=STDOUT)
		#p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0",'-g',"","-tl","1000"], stdout=PIPE, stderr=STDOUT)

		lines=[]
		for line in p.stdout:
			lines.append(str(line, encoding='utf-8'))

		#print(lines)
		return lines 



def create_file(characters,places,utilities,row,file):
		
		
		with open(file, 'w') as f:
			f.write("""type place;
type pirate;
type world;

property power(character : character) : number;
property injured(character : character) : number;
property satisfaction(character : character) : number;
property state(character : character) : number; //0 - nic 1- odwrócenie uwagi 2 -ogłuszenie
property at(character : character) : place;
property treasure(character : character) : number;
property altruism(character : character) : number;
property ambition(character : character) : number;
property knows_location_treasure(character : character) : number;
property has_access_pirates(character : character) : number;

property world_state(world : world) : number; //dzień, noc, słaba pogoda 
property later(world : world) : boolean;
property pirates_knows_location_treasure(pirate : pirate) : number;
property pirates_relation(pirate : pirate) : number; //słaba, neutralna, dobra
property pirates_power(pirate : pirate) : number; 
property pirates_treasure(pirate : pirate) : number; 

property distraction(place:place) :number;

entity char1 : character;
entity char2 : character;
entity char3 : character;

entity world:world;
entity pirates:pirate;

entity  ship : place;
entity  pirate_base : place;
entity  treasure_place : place;


		   """
			)
			

			f.write("world_state(world) = "  + str(row["world_state"]) + " ;\n")
			f.write("pirates_relation(pirates) = "  + str(row["pirates_relation"]) + " ;\n")
			f.write("pirates_power(pirates) = "  + str(row["pirates_power"]) + " ;\n")
			f.write("pirates_treasure(pirates) = "  + str(row["pirates_treasure"]) + " ;\n")
			f.write("pirates_knows_location_treasure(pirates) = "  + str(row["pirates_knows_location_treasure"]) + " ;\n")
			
			for char in characters:
				
				f.write("power(" + char  +") = " + str(row[char+"_power"]) + " ;\n")
				f.write("injured(" + char  +") = " + str(row[char+"_injured"]) + " ;\n")
				f.write("state(" + char  +") = " + str(row[char+"_state"]) + " ;\n")
				f.write("at(" + char  +") = " + str(row[char+"_at"]) + " ;\n")
				f.write("treasure(" + char  +") = " + str(row[char+"_treasure"]) + " ;\n")
				f.write("altruism(" + char  +") = " + str(row[char+"_altruism"]) + " ;\n")
				f.write("ambition(" + char  +") = " + str(row[char+"_ambition"]) + " ;\n")
				f.write("knows_location_treasure(" + char  +") = " + str(row[char+"_knows_location_treasure"]) + " ;\n")
				f.write("has_access_pirates(" + char  +") = " + str(row[char+"_has_access_pirates"]) + " ;\n")
			
				
			for p in places:
				f.write("distraction(" + p  +") = " + str(row[p+"_distraction"]) + " ;\n")
				

			
			
				
				

			f.write("""
action travel(character : character,  to : place){
	precondition:
		(
		(to==pirate_base & has_access_pirates(character)==1)
		|
		(to==treasure_place & knows_location_treasure(character) ==1)
		|
		(to==ship)
		)
		& character == char1
		;
	effect:
		later(world)&
		at(character) = to;
	consenting: character; 
	
};

action distraction(character : character,  place : place){
	precondition:
		at(character) == place & character == char1;
		
	effect:
		distraction(place) =1 & later(world);
	consenting: character; 
	
};

action stun(character : character,character2 : character, place : place){
	precondition:
		at(character) == place &
		at(character2) == place &
		distraction(place)==1 &
		character != character2 
		
		& character == char1;
		
	effect:
		if (altruism(character) > 0)
			satisfaction(character) = satisfaction(character) - 1 
		&state(character2) = 2
		& later(world);
	consenting: character; 
	
};


action escape(character : character){
	precondition:
		at(character) == ship &
		distraction(ship) == 1
		
		
		& character == char1;
		
	effect:
		if (ambition(character) == 0 | injured(character) == 1) 
			satisfaction(character) = satisfaction(character) + 1
		& later(world);
	consenting: character; 
	
};

action escape_pirates_help(character : character){
	precondition:
		at(character) == ship &
		(distraction(ship) == 1 & pirates_relation(pirates) == 1) |
		pirates_power(pirates) == 0 |
		world_state(world) > 0 
		
		& character == char1;
		
	effect:
		if (ambition(character) == 0 | injured(character) == 1) 
			satisfaction(character) = satisfaction(character) + 1
		& later(world);
	consenting: character; 
	
};

action take_treasure_char(character : character,character2 : character, place : place){
	precondition:
		at(character) == place &
		at(character2) == place &
		state(character2) == 2 &
		character != character2 &
		treasure(character2) > 0
		& character == char1;
		
	effect:
		if (altruism(character) > 0)
			satisfaction(character) = satisfaction(character) - 1 
		&
		if (ambition(character) > 0)
			satisfaction(character) = satisfaction(character) + 1 
		&
		treasure(character2) = treasure(character2) - 1 &
		treasure(character) = treasure(character) + 1
		& later(world);
	consenting: character; 
	
};

action take_treasure_location_char(character : character,character2 : character, place : place){
	precondition:
		at(character) == place &
		at(character2) == place &
		state(character2) == 2 &
		character != character2 &
		knows_location_treasure(character2)==1
		& character == char1;
		
	effect:
		if (altruism(character) > 0)
			satisfaction(character) = satisfaction(character) - 1 
		&
		
		knows_location_treasure(character)=1
		& later(world);
	consenting: character; 
	
};

action get_access_pirates(character : character){
	precondition:
		pirates_relation(pirates) == 1 |
		pirates_power(pirates) == 0 |
		world_state(world) > 0 
		& character == char1
		;
	effect:
		later(world)&
		has_access_pirates(character) = 1;
	consenting: character; 
	
};

action tell_treasure_location(character : character,character2 : character){
	precondition:
		
		knows_location_treasure(character)==1
		& character == char1
		;
	effect:
		later(world)&
		knows_location_treasure(character2)=1;
	consenting: character; 
	
};


action get_treasure(character : character){
	precondition:
		
		knows_location_treasure(character)==1
		&treasure(character) < 2
		& character == char1
		;
	effect:
	
		if (ambition(character) > 0)
			satisfaction(character) = satisfaction(character) + 1 
		&
		later(world)&
		treasure(character) = treasure(character) + 1;
	consenting: character; 
	
};

action give_pirates_treasure_location(character : character){
	precondition:
		pirates_knows_location_treasure(pirates)==0 &
		knows_location_treasure(character)==1
		& character == char1
		& at(character) == pirate_base
		;
	effect:
		later(world)&
		pirates_knows_location_treasure(pirates)==1 &
		pirates_relation(pirates) = pirates_relation(pirates) + 1;
	consenting: character; 
	
};


action give_pirates_treasure(character : character){
	precondition:
		treasure(character) > 0
		& character == char1
		& at(character) == pirate_base
		;
	effect:
		if (ambition(character) > 0)
			satisfaction(character) = satisfaction(character) - 1 
		&
		later(world)&
		treasure(character) = treasure(character) - 1 &
		pirates_treasure(pirates) = pirates_treasure(pirates) + 1 &
		pirates_relation(pirates) = pirates_relation(pirates) + 1;
	consenting: character; 
	
};

action take_pirates_treasure(character : character){
	precondition:
		has_access_pirates(character) == 1
		& pirates_treasure(pirates) > 0
		& character == char1
		;
	effect:
		if (ambition(character) > 0)
			satisfaction(character) = satisfaction(character) + 1 
		&
		later(world)&
		treasure(character) = treasure(character) + 1 &
		pirates_treasure(pirates) = pirates_treasure(pirates) - 1 &
		pirates_relation(pirates) = pirates_relation(pirates) - 1;
	consenting: character; 
	
};

action wait_for_night(character : character){
	precondition:
		world_state(world) == 0 
		& character == char1
		;
	effect:
		later(world)&
		world_state(world) =  1 ; 
	consenting: character; 
	
};

action attack_pirate_base(character : character){
	precondition:
		power(character) > 0
		& character == char1
		;
	effect:
		later(world)&
		pirates_power(pirates) = pirates_power(pirates) - 1
		 ; 
	consenting: character; 
	
};

action train(character : character){
	precondition:
		 character == char1
		;
	effect:
		later(world)&
		power(character) = power(character) + 1
		 ; 
	consenting: character; 
	
};


action take_treasure_pirates(character : character){
	precondition:
		((pirates_power(pirates) == 0 ) | distraction(pirate_base) == 1 )
		& at(character) == pirate_base
		& character == char1
		& pirates_treasure(pirates) > 0
		;
	effect:
	
		if (ambition(character) > 0)
			satisfaction(character) = satisfaction(character) + 1 
		&
		later(world)&
		pirates_treasure(pirates) = pirates_treasure(pirates) - 1
		&treasure(character) = treasure(character) + 1

		 ; 
	consenting: character; 
	
};


			""")

			
			
			f.write("utility(): \n ")
			f.write('satisfaction(char1);')

			
		


			for char in characters:
				f.write("utility({}): \n ".format(char))
				f.write(utilities[char])
			
			
			f.close()

characters = ['char1', 'char2', 'char3']
places= ['ship','pirate_base','treasure_place']
utilities = {
	'char1':'satisfaction(char1);\n',
	'char2':'satisfaction(char2);\n',
	'char3':'satisfaction(char3);\n',
	
}
file = "ship\\planners\\create_table.txt"

df = pd.read_csv('ship\\rules\\table_training.csv')

for index in range(0,2000):
	print(index)
	
	start = time.time()

	row=df.loc[index]
	create_file(characters, places,utilities, row,file)
	action = load_action(file)
	

	end = time.time()
	
	
	df.loc[index,['results']] = action
	df.loc[index,['time']] = (end-start)

	print(action)
	print(end-start)

	df.to_csv('ship\\rules\\dataset_results.csv',index=False)
	
	
	

#print(df)