import pandas as pd
import random
from subprocess import Popen, PIPE, STDOUT

class Island_Loop:

	def __init__(self) -> None:
		
		self.init_world()

	
	def init_world(self):
		self.world_state = pd.read_csv('game_files\islandState.csv').set_index("Name")
		self.characters = list(self.world_state.index.drop('World'))
		#self.characters =  list(set(random.choices(list(self.world_state.index.drop(['World','Mc'])),k=3)))
		#self.characters.append('Mc')

		
		self.items = ['Gold','Fuel','Meds','Food','Map']
		self.current_character = random.choice([x for x in self.characters if x!= "Mc"])
		
		

		self.create_goals()
		#self.character_rotation()
		
		#self.create_file()
		#self.change_state()
		
		
		#self.print_state()
			
	def print_state(self):
		text = ""
		for index in self.characters:
			text = text + (index + "\n" +  " Health: " +  str(self.world_state.at[index,'Health'] ) + "\n"
											+ " Satisfaction: " +  str(self.world_state.at[index,'Satifaction']) + "\n"
											+ " Altruism: " +  str(self.world_state.at[index,'Altruism']) + "\n"
											+ " Ambition: " +  str(self.world_state.at[index,'Ambition']) + "\n \n" )
		
		#print(text)
		return text

	def character_rotation(self):
		chars = [x for x in self.characters if x!= "Mc"]
		index = chars.index(self.current_character)
		if index == len(chars) - 1:
			self.current_character = chars[0]
		else:
			self.current_character = chars[index+1]

		print(self.current_character)

	def create_goals(self):
		self.goals_dic = {}
		for char in [x for x in self.characters if x!= "Mc"]:
			goals = []
			for item in self.items:
				
				if self.world_state.at[char,'Wants_'+item] == 1.0:

					goal1 = """if(health({name})<2) 0
								else 
 							(if (knows_location({name},{item})) 1 else 0 ) + (if (has({name},{item}) > {amount} ) 1 else 0 ) + (if(exists(c : character) (wants_to_attack({name},c) & health(c)<2)) 1  else 0)
							""".format(name = char,item = item,amount = self.world_state.at[char,item])
					
					
					goal2 = """ if(health({name})<2) 0
 								elseif
								((exists(c : character) (wants_to_attack({name},c) & health(c)>2)))
									0
									else
										(if(has({name},{item}) > {amount}  ) satisfaction({name}) else 0)
									
									  ; \n""".format(name=char,item=item,amount = self.world_state.at[char,item])
					
					goals.append(goal1)
					goals.append(goal2)
					break
			
			#print(goals)
			self.goals_dic[char] = goals
			

	def create_file(self):
		with open("lib/swimming_new.txt", 'w') as f:
			f.write("""/////////////////////////////////////types


type character;
type item ;

//////////////////////////////////property


//character

property health(char: character) : number;
property satisfaction(char: character) : number;
property has(character : character, item:item) : number;
property knows_location(character : character, item:item) : boolean;
property altruism(char: character) : number;
property ambition(char: character) : number;
property likes(char: character, char2: character) : number;
property wants_to_attack(character : character, char2: character) : boolean;
property quantity(item : item) : number;"""
			)
			
			
			for item in self.items:
				f.write("entity "+ item  + ": item;  \n")
				f.write("quantity( "+ item  + ") = " +str(self.world_state.at['World',item])  + ";  \n")
				
				#warrtosci postaci
			for char in self.characters:
				f.write("entity "+ char  + ": character;  \n")
				row = self.world_state.loc[char]

				f.write("health("+ char  +") = " + str(row.Health) + " ; \n")
				f.write("altruism(" + char  +") = " + str(row.Altruism) + " ;\n")
				f.write("ambition(" + char  +") = " + str(row.Ambition) + " ;\n")
				f.write("satisfaction(" + char  +") = " + str(row.Satifaction) + " ;\n")

				#has
				for item in self.items:
					f.write("has("+ char  + "," + item  +   ") = " + str(row[item]) + " ; \n")
	
					#knows location
					if row['Knows_'+item]== 1:
						f.write("knows_location("+ char  + "," + item  +   ") ; \n")

				#likes 
				for other in self.characters:
					if other != char:
						f.write("likes("+ char  + "," + other  +   ") = " + str(row['Likes_'+other]) + " ; \n")

						#wants_to_attack
						if row['Attacks_'+other]== 1:
							f.write("wants_to_attack("+ char  + "," + other  +   ") ; \n")



			f.write("""
											////////////////////////////////////////actions


						action search_for(char : character, item:item) {
							precondition:
							!knows_location(char,item)
							&health(char) > 0
		   					&char != Mc
							;

							effect:
							knows_location(char,item)
							&  satisfaction(char) = satisfaction(char) + 1
							& health(char) = health(char) - 1 
							
							;
							consenting: char;
							
						};

						action ask_for_location(char : character,char2 : character, item:item) {
							precondition:
							char != char2
		   					&char != Mc
							&!knows_location(char,item)
							&knows_location(char2,item)
							&quantity(item) > 0
							&health(char) > 0
							&health(char2) > 0
							;

							effect:
							knows_location(char,item)
							&  satisfaction(char) = satisfaction(char) + (altruism(char)/5) + (likes(char,char2)/5)
							&  satisfaction(char2) = satisfaction(char) +(altruism(char2)/5) + (likes(char2,char)/5)
							&altruism(char) = altruism(char) + 2
							&likes(char,char2) = likes(char,char2) + 2
							;
							consenting: char;
							
						};

						//oszukaj z lokacja
						action pay_for_location(char : character,char2 : character, item:item, ex_item:item) {
							precondition:
							char != char2
		   					&char != Mc
							&!knows_location(char,item)
							&knows_location(char2,item)
							&has(char,ex_item)>0
							&quantity(item) > 0
							&health(char) > 0
							&health(char2) > 0
							;

							effect:
							knows_location(char,item)
							& has(char,ex_item) = has(char,ex_item) - 1
							& has(char2,ex_item) = has(char2,ex_item) +1

							&  satisfaction(char) = satisfaction(char)  + 2
							&  satisfaction(char2) = satisfaction(char)  + 2

							&likes(char2,char) = likes(char2,char) + 1
							&likes(char,char2) = likes(char,char2) + 1
							;
							consenting: char,char2;
							
						};

						action attack_for_location(char : character,char2 : character, item:item) {
							precondition:
							char != char2
		   					&char != Mc
							&!knows_location(char,item)
							&knows_location(char2,item)
							&quantity(item) > 0
							&health(char) > 0
							&health(char2) > 0
							;

							effect:
							knows_location(char,item)
							& satisfaction(char) = satisfaction(char) + (altruism(char)/ -7) 
							& satisfaction(char2) = satisfaction(char)  - 5 
							&wants_to_attack(char2,char)
							&health(char) = health(char) - 0.5
							&health(char2) = health(char2) - 1
							&ambition(char2) = ambition(char2) - 1
							&likes(char2,char) = likes(char2,char) - 5
							;
							consenting: char;
							
						};


						action find(char : character,item : item) {
							precondition:
								knows_location(char,item)
								&quantity(item) > 0
								&health(char) > 0
		   						&char != Mc
								;
								

							effect:
							
							has(char,item) = has(char,item)  + 1
							&quantity(item) = quantity(item) - 1
							&  satisfaction(char) =satisfaction(char) + 1
							
							;
							consenting: char;
							
						};

						action ask_for_item(char : character, other: character, item : item) {
								precondition:
									char != other
									&has(other, item) > 0
									&health(char) > 0
									&health(other) > 0
		   							&char != Mc
									;

								effect:
									
									has(char, item) = has(char, item) + 1
									&has(other, item) = has(other, item) - 1
									& satisfaction(char) = satisfaction(char) + (altruism(char)/8) + (likes(other,char)/8) 
									&likes(char,other) = likes(char,other) + 4
									;
								consenting: char,other;
								
							};


						action take_item(char : character, other: character, item : item) {
								precondition:
									char != other
									&has(other, item) > 0
									&health(char) > 0
									&health(other) > 0
									&char != Mc
									;

								effect:
									

									has(char, item) = has(char, item)  +1
									&has(other, item) = has(other, item) - 1
									&wants_to_attack(other,char)
									&satisfaction(char) = satisfaction(char) + (  likes(char,other)/ -4) + ( altruism(char)/ -4) 
									&health(char) = health(char) - 0.5
									&health(other) = health(other) - 1
									&ambition(other) = ambition(other) - 1
									&likes(other,char) = likes(other,char) - 5
									;
								consenting: char;
								
							};
							

						action exchange_item(char : character, other: character, item1 : item, item2 :item) {
								precondition:
									char != other
									&item1 !=item2
									&has(char, item1) >0
									&has(other, item2) >0
									&health(char) > 0
									&health(other) > 0
		  							 &char != Mc
									;

								effect:
									

									has(char, item1) = has(char, item1) - 1
									&has(other, item1) = has(other, item1) + 1

									&has(char, item2) = has(char, item2) + 1
									&has(other, item2) = has(other, item2) - 1
									&satisfaction(char) = satisfaction(char) + 5
									&satisfaction(other) = satisfaction(other) + 5 
									
									;
								consenting: char,other;
								
							};


						action give_item(char : character, other: character, item : item) {
								precondition:
									char != other
									&has(char, item) > 0
									&health(char) > 0
									&health(other) > 0
		   
		   							&char != Mc
									;

								effect:
									

									has(char, item) = has(char, item)  - 1
									&has(other, item) = has(other, item) + 1
									&satisfaction(char) = satisfaction(char) + (  likes(char,other)/7) + ( altruism(char)/7) 
									&satisfaction(other) = satisfaction(other) +5
									;
								consenting: char,other;
								
							};




						action use_meds(char : character) {
							precondition:
								has(char,Meds) > 0
								& 0 < health(char) < 2
								;
								

							effect:
							health(char)  = 3
							&satisfaction(char) = satisfaction(char) +1
							&has(char,Meds) = has(char,Meds) - 1;
							consenting: char;
							
						};


						action rest(char : character) {
								precondition:
									
									health(char) > 0
									&char != Mc
									;

								effect:
									health(char) = health(char) + 1
									//&satisfaction(char) = satisfaction(char) + 0
								


									
									
									;
								consenting: char;
								
							};

						/*
						action compliment(char : character, other: character) {
								precondition:
									char != other
									&health(char) > 0
									&health(other) > 0
									&char != Mc
									;

								effect:
									
									
									

									likes(char,other) =likes(char,other) +  1
									&satisfaction(char) = 1 + (altruism(char)/7) + likes(char,other)


									
									&altruism(other) = altruism(other)+  2
									&likes(other,char) =likes(other,char) +  3
									
									
									;
								consenting: char;
								
							};
						*/

						action attack(char : character, other: character) {
								precondition:
									char != other
									//&health(char) > 0
									//&points(char) > 0
									//&altruism(char) < -13
									//&ambition(char) > 13
									&char != Mc
									&wants_to_attack(char,other)
									&health(char) > 0
									&health(other) > 0
									;

								effect:
									
									altruism(char) = altruism(char) -  4	
									&satisfaction(char) = satisfaction(char) + 1

									//&health(char) = health(char) - 0.5
									&health(other) = health(other) - 1
									&ambition(other) = ambition(other) - 1
									&altruism(other) = altruism(other) - 4
									&likes(other,char) =likes(other,char) - 4
									&wants_to_attack(other,char)
									
									;
								consenting: char;
								
							};

						action ask_for_help(char : character, other: character, attacked : character) {
								precondition:
									char != other
									&health(other) > 0
									&health(char) >0
									&char != Mc
									&wants_to_attack(char,attacked)
									;

								effect:
									
										
									satisfaction(char) = satisfaction(char) + 1 + (likes(char,other)/5)
									&satisfaction(other) = satisfaction(other) + (altruism(other)/-8) + (likes(other, char)/5) + (likes(other,attacked)/-5)

									
									&altruism(other) = altruism(other) + 1
		   							&likes(char,other) = likes(other,char) + 4
		   
									&wants_to_attack(other,attacked)
									
									
									;
								consenting: char;
								
							};

						action spend_time_together(char : character, other: character) {
								precondition:
									char != other
									&char != Mc
									&health(char) >0
									&health(other) >0
									;

								effect:
									
									
									satisfaction(char) =  satisfaction(char) + (likes(char,other)/4)
									&altruism(char) = altruism(char)+  2
									&likes(char,other) =likes(char,other) +  3
									

									&satisfaction(other) = satisfaction(char) +  (likes(other,char)/4)
									&altruism(other) = altruism(other)+  2
									&likes(other,char) = likes(other,char) +  3
									
									
									;
								consenting: char,other;
								
							};

							action intimidate(char : character, other: character) {
								precondition:
									char != other
									&health(char) > 0
									&health(other) > 0
									&char != Mc
									;

								effect:
									
									
									satisfaction(char) = (altruism(char)/7 * -1) - (likes(char,other)/7)
									&altruism(char) = altruism(char) - 2
									


									&satisfaction(other) =-2 - (likes(other,char)/7) 
								
									&altruism(other) = altruism(other) - 3
									&likes(other,char) =likes(other,char) -  4
									
									
									;
								consenting: char;

							};
		   
		   trigger health_check(char : character) {
			precondition:
				health(char) > 3;
			effect:                                   // by effect or trigger runs forever.
				health(char) = 3;  // Beliefs can be updated explicitly.
		};

			""")

			f.write("utility(): \n ")
			
			f.write(self.goals_dic[self.current_character][0])
			f.write("; \n")

			for char in [x for x in self.characters if x!= "Mc"]:
				f.write("utility({}): \n ".format(char))
				f.write(self.goals_dic[char][1])
				f.write("\n")
			
			
			f.close()

	def load_action(self,file):

		
		p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0"], stdout=PIPE, stderr=STDOUT)
		#p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0",'-g',"","-tl","1000"], stdout=PIPE, stderr=STDOUT)

		lines=[]
		for line in p.stdout:
			lines.append(str(line, encoding='utf-8'))

		print(lines)
		return lines[0] 
	
	#wykonuje akcje 
	def do_action(self,args):
		
		#print(args)
		match args[0]:
			case "search_for":
				print("search_for")
				self.world_state.at[args[1],'Knows_'+args[2]] = 1.0
				self.world_state.at[args[1],'Satifaction'] += 1
				self.world_state.at[args[1],'Health'] -= 1

			case "ask_for_location":
				print("ask_for_location")
				self.world_state.at[args[1],'Knows_'+args[3]] = 1.0
				self.world_state.at[args[1],'Satifaction'] += self.world_state.at[args[1],'Altruism']/5 + self.world_state.at[args[1],'Likes_'+args[2]]/5
				self.world_state.at[args[2],'Satifaction'] += self.world_state.at[args[2],'Altruism']/5 + self.world_state.at[args[2],'Likes_'+args[1]]/5
				self.world_state.at[args[1],'Altruism'] += 2
				self.world_state.at[args[1],'Likes_'+args[2]] += 2

			case "pay_for_location":
				print("pay_for_location")
				self.world_state.at[args[1],'Knows_'+args[3]] = 1.0
				self.world_state.at[args[1],'Satifaction'] += 2
				self.world_state.at[args[2],'Satifaction'] += 2
				
				self.world_state.at[args[1],'Likes_'+args[2]] += 1
				self.world_state.at[args[2],'Likes_'+args[1]] += 1

				self.world_state.at[args[1],args[4]] -= 1
				self.world_state.at[args[2],args[4]] += 1

			case "attack_for_location":
				print("attack_for_location")
				self.world_state.at[args[1],'Knows_'+args[3]] = 1.0
				self.world_state.at[args[1],'Satifaction'] -= self.world_state.at[args[1],'Altruism']/7
				self.world_state.at[args[2],'Satifaction'] -= 5
				
				self.world_state.at[args[2],'Attacks_'+args[1]] = 1.0

				self.world_state.at[args[1],'Health'] -= 0.5
				self.world_state.at[args[2],'Health'] -= 1

				self.world_state.at[args[2],'Ambition'] -= 1

				self.world_state.at[args[2],'Likes_'+args[1]] -= 5

			case "find":
				print("find")
				self.world_state.at[args[1],args[2]] += 1
				self.world_state.at['World',args[2]] -= 1
				self.world_state.at[args[1],'Satifaction'] += 1

			case "ask_for_item":
				print("ask_for_item")

				self.world_state.at[args[1],args[3]] += 1
				self.world_state.at[args[2],args[3]] -= 1
				
				self.world_state.at[args[1],'Satifaction'] += self.world_state.at[args[1],'Altruism']/8 + self.world_state.at[args[1],'Likes_'+args[2]]/8
				self.world_state.at[args[1],'Likes_'+args[2]] += 4

			case "take_item":
				print("take_item")

				self.world_state.at[args[1],args[3]] += 1
				self.world_state.at[args[2],args[3]] -= 1

				self.world_state.at[args[2],'Attacks_'+args[1]] = 1.0
				
				self.world_state.at[args[1],'Satifaction'] -= self.world_state.at[args[1],'Altruism']/4 + self.world_state.at[args[1],'Likes_'+args[2]]/4
				
				self.world_state.at[args[1],'Health'] -= 0.5
				self.world_state.at[args[2],'Health'] -= 1

				self.world_state.at[args[2],'Ambition'] -= 1
				
				self.world_state.at[args[2],'Likes_'+args[1]] -= 5

			case "exchange_item":
				print("exchange_item")

				self.world_state.at[args[1],args[3]] -= 1
				self.world_state.at[args[2],args[3]] += 1

				self.world_state.at[args[1],args[4]] += 1
				self.world_state.at[args[2],args[4]] -= 1

				
				
				self.world_state.at[args[1],'Satifaction'] += 5
				self.world_state.at[args[2],'Satifaction'] += 5

			case "give_item":
				print("give_item")

				self.world_state.at[args[1],args[3]] -= 1
				self.world_state.at[args[2],args[3]] += 1

			
				
				
				self.world_state.at[args[1],'Satifaction'] += self.world_state.at[args[1],'Altruism']/7 + self.world_state.at[args[1],'Likes_'+args[2]]/7
				
				self.world_state.at[args[2],'Satifaction'] += 5

			case "use_meds":
				print("use_meds")

				self.world_state.at[args[1],'Meds'] -= 1
				

				self.world_state.at[args[1],'Health'] = 4
				
				
				self.world_state.at[args[1],'Satifaction'] += 1
				
			case "rest":
				print("rest")
				

				self.world_state.at[args[1],'Health'] += 1
				
			
			case "attack":
				print("attack")

				self.world_state.at[args[1],'Altruism'] -= 4

				
				
				self.world_state.at[args[1],'Satifaction'] -= self.world_state.at[args[1],'Altruism']/7 + self.world_state.at[args[1],'Likes_'+args[2]]/7
				
				self.world_state.at[args[1],'Health'] -= 0.5
				self.world_state.at[args[2],'Health'] -= 1

				self.world_state.at[args[2],'Ambition'] -= 1
				self.world_state.at[args[2],'Altruism'] -= 1
				
				self.world_state.at[args[2],'Likes_'+args[1]] -= 4
				self.world_state.at[args[2],'Attacks_'+args[1]] = 1.0

			case "ask_for_help":
				print("ask for hep")

				
				
				self.world_state.at[args[1],'Satifaction'] += 1 + self.world_state.at[args[1],'Likes_'+args[2]]/5
				self.world_state.at[args[2],'Satifaction'] += self.world_state.at[args[2],'Altruism']/-8 + self.world_state.at[args[2],'Likes_'+args[1]]/5 + self.world_state.at[args[2],'Likes_'+args[3]]/-5



				self.world_state.at[args[2],'Altruism'] += 1
				
				self.world_state.at[args[1],'Likes_'+args[2]] += 4
				self.world_state.at[args[2],'Attacks_'+args[3]] = 1.0

			case "spend_time_together":
				print("spend_time_together")

				
				
				self.world_state.at[args[1],'Satifaction'] += self.world_state.at[args[1],'Likes_'+args[2]]/4
				self.world_state.at[args[2],'Satifaction'] +=  self.world_state.at[args[2],'Likes_'+args[1]]/4 


				self.world_state.at[args[1],'Altruism'] += 2
				self.world_state.at[args[2],'Altruism'] += 2
				
				self.world_state.at[args[1],'Likes_'+args[2]] += 3
				self.world_state.at[args[2],'Likes_'+args[1]] += 3

			case "intimidate":
				print("intimidate")

				
				
				self.world_state.at[args[1],'Satifaction'] -= self.world_state.at[args[1],'Altruism']/7 + self.world_state.at[args[1],'Likes_'+args[2]]/7
				self.world_state.at[args[2],'Satifaction'] -= 2+  self.world_state.at[args[2],'Likes_'+args[1]]/7 


				self.world_state.at[args[1],'Altruism'] -= 2
				self.world_state.at[args[2],'Altruism'] -= 3
				
				
				self.world_state.at[args[2],'Likes_'+args[1]] -= 4
				
	#checks if character should escape
	def check_escapes(self):
		
		for char in [x for x in self.characters if x!= "Mc"]:
			if self.world_state.at[char,'Health'] == 0 or self.world_state.at[char,'Ambition']== 0:
				self.world_state.drop(char,inplace=True)
				self.characters.remove(char)
				
			

				

			
			


	#aktualizuje stan swiata
	def change_state(self):
		
		
		action = self.load_action('lib\swimming_new.txt')
		
		print(action)
		
		args = action.replace("("," ").replace(")","").replace("\r\n","").replace(",","").split(' ')
		self.do_action(args)
		#print(args)
		return(action)
	

#Island_Loop()