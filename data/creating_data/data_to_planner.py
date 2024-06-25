from subprocess import Popen, PIPE, STDOUT
import pandas as pd

def load_action(file):

		
		p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"1","-tl","5000"], stdout=PIPE, stderr=STDOUT)
		#p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0",'-g',"","-tl","1000"], stdout=PIPE, stderr=STDOUT)

		lines=[]
		for line in p.stdout:
			lines.append(str(line, encoding='utf-8'))

		#print(lines)
		return lines 



def create_file(characters,items,row):
		with open("lib/boat_new.txt", 'w') as f:
			f.write("""//### Types:
type character;
type ship;

//### Properties:
property satisfaction(char: character) : number; // Satisfaction level of each character
property altruism(char: character) : number; // Altruism level of each character (-3 to 3)
property ambition(char: character) : number; // Ambition level of each character (-3 to 3)
property likes(char: character, other: character) : number; // Relationship liking level between characters (-3 to 3)
property food(char: character) : number; // Food resource of each character
property safety(char: character) : number; // Safety level of each character
property fighting_ability(char: character) : number; // Fighting ability level of each character (-3 to 3)

property ghost_relations(s :ship) : number; // Relationship level with ghosts (-3 to 3)
property overall_food(s :ship) : number; // Overall food resource available
property overall_coins(s :ship) : number; // Overall coins available

property wants_to_survive(char: character) : boolean; 
property wants_to_help_everyone(char: character) : boolean; 
property wants_to_help_themself(char: character) : boolean; 


entity mc : character;
		   entity ship:ship;
		   """
			)
			

				#warrtosci postaci
			for char in characters:
			
				f.write("entity "+ char + ": character;  \n")
				f.write("altruism(" + char  +") = " + str(row[char+"_altruism"]) + " ;\n")
				f.write("ambition(" + char  +") = " + str(row[char+"_ambition"]) + " ;\n")
				f.write("fighting_ability(" + char  +") = " + str(row[char+"_fighting_ability"]) + " ;\n")
				f.write("safety(" + char  +") = " + str(row[char+"_safety"]) + " ;\n")
				f.write("food(" + char  +") = " + str(row[char+"_food"]) + " ;\n")
				
				char_without_c = characters.copy()
				char_without_c.remove(char)
				for c2 in char_without_c:
					f.write("likes(" + char  +", "+ c2 +") = " + str(row[char+"_likes_"+c2]) + " ;\n")
				   
				f.write("ghost_relations(ship) =" +str(row['ghost_relations']) + ";  \n")
				f.write("overall_food(ship) =" +str(row['overall_food']) + " ; \n")
				f.write("overall_coins(ship) =" +str(row['overall_coins']) + ";  \n")
			

				

				

			f.write("""//# Action: survive
action survive(char: character) {
    precondition:
        food(char) >= 0 // Character has no food
        &safety(char) > 0
        &char != mc; // Character's safety level is adequate
    effect:
        if (ambition(char)<=0)
            satisfaction(char) = satisfaction(char) + 1; // Character gains satisfaction
    consenting: char;
};

//# Action: help_everyone
action help_everyone(char: character) {
    precondition:
        overall_food(ship) > 0 // Character has food
       // &safety(char) < 0
        &char != mc; // Character's safety level is low
    effect:
    if (ambition(char)>0 & altruism(char)>= 0)
         satisfaction(char) = satisfaction(char) + 1; // Character gains satisfaction
    consenting: char;
};

//# Action: help_themself
action help_themself(char: character) {
    precondition:
        food(char) > 0 // Character has food
        //&safety(char) < 0
        &char != mc; // Character's safety level is low
    effect:
    if (ambition(char)>0 & altruism(char) < 0)
         satisfaction(char) = satisfaction(char) + 1;// Character gains satisfaction
    consenting: char;
};

//# Action: ghost_deal
action ghost_deal(char: character) {
    precondition:
        ghost_relations(ship) > 0
        &char != mc; // Character has good relations with ghosts
    effect:
        overall_food(ship) = overall_food(ship) + 1 // Character gains overall food
        &safety(char) =  safety(char) - 1 // Character's safety level decreases
        &ghost_relations(ship) = ghost_relations(ship) - 1; // Character's relations with ghosts decrease
    consenting: char;
};

//# Action: fight_monster
action fight_monster(char: character) {
    precondition:
        fighting_ability(char) > 0
        &char != mc; // Character has high fighting ability
    effect:
        
        overall_food(ship) = overall_food(ship) + 1
        &fighting_ability(char) = fighting_ability(char) - 1 // Character's fighting ability decreases
        &safety(char) = safety(char) - 1; // Character's safety level decreases
    consenting: char;
};

//# Action: sacrifice_food
action sacrifice_food(char: character) {
    precondition:
        food(char) > 0
        &char != mc; // Character has food
    effect:
       
        food(char) = food(char) -  1 // Character sacrifices food
        &ghost_relations(ship) = ghost_relations(ship) + 1;// Character's relations with ghosts improve
    consenting: char;
};

//# Action: sacrifice_money
action sacrifice_money(char: character) {
    precondition:
        overall_coins(ship) > 0
        &char != mc; // There are overall coins available
    effect:
        overall_coins(ship) = overall_coins(ship)- 1 // Overall coins decrease
        &ghost_relations(ship) = ghost_relations(ship) + 1;  // Character's relations with ghosts improve
    consenting: char;
};

//# Action: pray
action pray(char: character, char2: character) {
    precondition:
        wants_to_survive(char2) 
        &char != char2
        &char != mc; // Character2's safety level is low
    effect:
       
        ghost_relations(ship) = ghost_relations(ship) + 1; 
    consenting: char;
};

//# Action: train_together
action train_together(char: character, char2: character) {
    precondition:
        (likes(char2, char) > 1 | 
        wants_to_help_everyone(char2))
        &char != char2
        &char != mc;
    effect:
        
        fighting_ability(char) = fighting_ability(char) + 1 // Character's fighting ability increases
        &fighting_ability(char2) =  fighting_ability(char) + 1 // Char2's fighting ability increases
        &safety(char) = safety(char) + 1 // Character's safety level increases
        &safety(char2) = safety(char2) + 1; // Char2's safety level increases
    consenting: char;
};



//# Action: take_food
action take_food(char: character, char2: character) {
    precondition:
        fighting_ability(char) > fighting_ability(char2) // Character has higher fighting ability than char2
        &food(char2) > 0
        &char != char2
         &char != mc; // Char2 has food
    effect:
        
        food(char) = food(char) + 1 // Character gains food
        &food(char2) = food(char2) - 1 // Char2 loses food
        &likes(char2, char) = likes(char2, char) -  1 // Relationship liking decreases between char and char2
        &safety(char) = safety(char) -  1 
        &safety(char2) = safety(char2) - 1; // Character's safety level decreases
    consenting: char;
};

//# Action: threaten
action threaten(char: character, char2: character) {
    precondition:
        wants_to_survive(char2) 
        &char != char2
        &char != mc; 
    effect:
        
        fighting_ability(char2) = fighting_ability(char2) - 1 // Character's fighting ability increases
        &likes(char2, char) = likes(char2, char) - 1; // Relationship liking decreases between char and char2
    consenting: char;
};

//# Action: weaken
action weaken(char: character, char2: character) {
    precondition:
    char != char2
    &char != mc;
    effect:
         fighting_ability(char2) = fighting_ability(char2) - 1 // Character's fighting ability increases
        &likes(char2, char) = likes(char2, char) - 1; // Relationship liking decreases between char and char2
    consenting: char;
};

//# Action: safe_alone
action safe_alone(char: character) {
    precondition:
    char != mc;
    effect:
        safety(char) = safety(char) + 1; // Character's safety level increases
    consenting: char;
};

//# Action: safe_together
action safe_together(char: character, char2: character) {
    precondition:
        wants_to_survive(char2)
        &char != char2
        &char != mc; // Char2 has no food
    effect:
        safety(char) =  safety(char) +1 // Character's safety level increases
        &safety(char2) =  safety(char2) +1; // Char2's safety level increases
    consenting: char;
};

//# Action: accuse
action accuse(char: character, char2: character) {
    precondition:
        wants_to_help_themself(char2)
        &char != char2
        &char != mc; // Character has no food
    effect:
        food(char) = 0
        &likes(char2, char) = likes(char2, char) - 1; // Relationship liking increases between char and char2
    consenting: char;
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
file = 'lib/boat_new.txt'

df = pd.read_csv('data\\creating_data\\random_states.csv')

for index in range(0,len(df)):
	row=df.loc[index]
	create_file(characters, items, row)

	action = load_action(file)
	print(index)
	df.loc[index,['results']] = action
	df.to_csv('data/random_states_results.csv')
	

print(df)