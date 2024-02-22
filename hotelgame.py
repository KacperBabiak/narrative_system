from subprocess import Popen, PIPE, STDOUT
import game_files.GameLogic as logic
import game_files.character as chr
from game_files.item import Item
import random

class Game:


	def __init__(self) -> None:
		self.init_state()
		#self.game_loop()

	#wprowadza stan swiata pierwszy
	def init_state(self):
		characters = {}
		items = {}
		self.gl = logic.GameLogic(characters,items)

		food = Item("food")
		money = Item("money")
		book = Item("book")

		items["food"] = food
		items["money"] = money
		items["book"] = book

		mc = chr.Character(self.gl, "mc", 0, 0 )
		characters["mc"]=mc
		

		agent = chr.Character(self.gl, "agent", -17, 3 )
		characters["agent"]=agent
		agent.add_item(book)

		doctor = chr.Character(self.gl, "doctor", 17, 15 )
		doctor.add_item(food)
		characters["doctor"]=doctor
		

		science = chr.Character(self.gl, "science", 8, -17 )
		characters["science"]=science
		science.add_item(food)

		actor = chr.Character(self.gl, "actor", -3, 17 )
		actor.add_item(money)
		actor.add_item(money)
		characters["actor"]=actor

		tumblr = chr.Character(self.gl, "tumblr", 0, 0 )
		characters["tumblr"]=tumblr
		tumblr.add_item(money)

		mc.add_char(doctor,0,0)
		mc.add_char(science,0,0)
		mc.add_char(agent,0,0)
		mc.add_char(actor,0,0)
		mc.add_char(tumblr,0,0)

		agent.add_char(doctor,15,0)
		agent.add_char(science,0,0)
		agent.add_char(actor,0,0)
		agent.add_char(tumblr,0,0)
		agent.add_char(mc,0,0)
		
		doctor.add_char(agent,0,0)
		doctor.add_char(science,0,0)
		doctor.add_char(actor,0,0)
		doctor.add_char(tumblr,0,0)
		doctor.add_char(mc,0,0)

		science.add_char(doctor,0,0)
		science.add_char(agent,0,0)
		science.add_char(actor,0,0) 
		science.add_char(tumblr,0,0)
		science.add_char(mc,0,0)

		actor.add_char(doctor,0,0)
		actor.add_char(science,0,0)
		actor.add_char(agent,0,0)
		actor.add_char(tumblr,0,0)
		actor.add_char(mc,0,0)


		tumblr.add_char(doctor,0,0)
		tumblr.add_char(science,0,0)
		tumblr.add_char(agent,0,0)
		tumblr.add_char(actor,0,0)
		tumblr.add_char(mc,0,0)

		self.gl.characters = characters
		self.gl.items = items

		#nadaj odgórnie
		doctor.add_goals()
		science.add_goals()
		agent.add_goals()
		actor.add_goals()
		tumblr.add_goals()

		self.current_character = tumblr
		self.print_state()

		

	def print_state(self):
		text= ""
		for char in self.gl.characters.values():
			text = text + char.name + "\n" +  " health: " + str(char.health) + "\n" + " happiness: " + str(char.happiness) + "\n"+  " altruism: " + str(char.altruism)+ "\n" + " ambition: " + str(char.ambition) + "\n"
			text = text + "\n".join([(item.name + str(char.items[item])) for item in char.items])  + "\n "
			text = text + "\n".join(char.goals)  + "\n \n"
		
		#print(text)
		
		return text
			

		

	#odpala plan i przejmuje akcje
	def load_action(self,file):

		
		p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0",'-g',"3","-tl","500"], stdout=PIPE, stderr=STDOUT)
		
		for line in p.stdout:
			return (str(line, encoding='utf-8'))

	#wykonuje akcje 
	def do_action(self,args):
		
		print(args)
		match args[0]:
			case "give":
				print("give")
				self.gl.characters[args[1]].give(self.gl.characters[args[2]],self.gl.items[args[3]])
			case "take":
				print("take")
				self.gl.characters[args[1]].take(self.gl.characters[args[2]],self.gl.items[args[3]])
			case "exchange":
				print("exchange")
				self.gl.characters[args[1]].exchange(self.gl.characters[args[2]],self.gl.items[args[3]],self.gl.items[args[4]])
			case "talk_altruism":
				print("talk_altruism")
				self.gl.characters[args[1]].talk_altruism(self.gl.characters[args[2]])
			case "talk_ambition":
				print("talk_ambition")
				self.gl.characters[args[1]].talk_ambition(self.gl.characters[args[2]])
			case "compliment":
				print("compliment")
				self.gl.characters[args[1]].compliment(self.gl.characters[args[2]])
			case "intimidate":
				print("intimidate")
				self.gl.characters[args[1]].intimidate(self.gl.characters[args[2]])
			case "gossip_about":
				print("gossip_about")
				self.gl.characters[args[1]].gossip_about(self.gl.characters[args[2]],self.gl.characters[args[3]])
			case "praise_someone":
				print("praise_someone")
				self.gl.characters[args[1]].praise_someone(self.gl.characters[args[2]],self.gl.characters[args[3]])
			case "attack":
				print("attack")
				self.gl.characters[args[1]].attack(self.gl.characters[args[2]])
			case "rest":
				print("rest")
				self.gl.characters[args[1]].rest()
			case "take_care_of":
				print("take_care_of")
				self.gl.characters[args[1]].take_care_of(self.gl.characters[args[2]])
			case "work":
				print("work")
				self.gl.characters[args[1]].work()
			case "eat":
				print("eat")
				self.gl.characters[args[1]].eat()
			case "read":
				print("read")
				self.gl.characters[args[1]].read()
			case "spend_time_together":
				print("spend_time_together")
				self.gl.characters[args[1]].spend_time_together(self.gl.characters[args[2]])
		
		
	#aktualizuje stan swiata
	def change_state(self):
		
		
		action = self.load_action('lib\hotel_new.txt')
		
		print(action)
		
		args = action.replace("("," ").replace(")","").replace("\r\n","").replace(",","").split(' ')
		self.do_action(args)
		print(args)
		return(action)
		
	def character_rotation(self):
		characters = list(self.gl.characters.values())
		index = characters.index(self.current_character)
		if index == len(characters) - 1:
			self.current_character = characters[1]
		else:
			self.current_character = characters[index+1]
		
	def check_all_goals(self):
		for char in self.gl.characters.values():
				char.check_goals()

	def game_loop(self):
		#jeszcze sprawdzenie wszystkich goali
		while True:
			self.check_all_goals()
			self.character_rotation()
			self.create_file()
			self.change_state()
			self.print_state()
			break
			

	#tworzy nowy plik
	def create_file(self):
		with open("lib/hotel_new.txt", 'w') as f:
			f.write("""///////////////////////////////////entity
				type object;
				type character : object;
				type item : object;

				entity actor : character;
				entity science : character;
				entity doctor : character;
				entity agent : character;
				entity mc : character;
				entity tumblr : character;

				entity game : entity;

				//////////////////////////////////property


				//properties
				property health(character : character) : number;
				property points(character : character) : number;
				property has(character : character, item : item) : number;
				property did_something(char: character) : number;
				property happiness(character : character) : number;
				property altruism(character : character) : number;
				property ambition(character : character) : number;

				//emotions towards other characters
				property likes(character1: character, character2 : character) : number;
				property trusts(character1: character, character2 : character) : number;"""
			)
			for item in self.gl.items.keys():
				f.write("entity "+ item  + ": item;  \n")
				
				#warrtosci postaci
			for char in self.gl.characters.values():
				f.write("health("+ char.name  +") = " + str(char.health) + " ; \n")
				f.write("points(" + char.name  +") = " + str(char.points) + " ; \n")
				f.write("happiness(" + char.name  +") = " + str(char.happiness) + " ;\n")
				f.write("altruism(" + char.name  +") = " + str(char.altruism) + " ;\n")
				f.write("ambition(" + char.name  +") = " + str(char.ambition) + " ;\n")

			

				for k,v in char.likes.items():
						f.write("likes("+ char.name + ", " + k.name + ") = "+str(v) + " ;\n")

				for k,v in char.trusts.items():
						f.write("trusts("+ char.name + ", " + k.name + ") = "+str(v) + " ;\n")

				for k,v in char.items.items():
						f.write("has("+ char.name + ", " + k.name + ") = "+str(v) + " ;\n")

				

			f.write("""////////////////////////////////////////actions

	//items

	action give(char : character, other: character, item : item) {
		precondition:
			char != other
			&char != mc
			&has(char, item) > 0

			&health(char) > 0
			&health(other) > 0
			
		
			;

		effect:
			did_something(char) = did_something(char) + 1
			//&did_something(other) = did_something(other) + 1
			&has(char, item) = has(char, item) - 1
			&has(other, item) = has(other, item) + 1
			
			&happiness(char) =happiness(char) + (likes(char,other)/6)
			&altruism(char) = (altruism(char) +  2 )
			&likes(char,other) =(likes(char,other) +  1 )
			
			&happiness(other) =happiness(other) + 3
			&altruism(other) = altruism(other) +  3

			&likes(other,char) = likes(other,char) +  2
			&trusts(other,char) = trusts(other,char) + 2
			
			;
		consenting: char;
		
	};



	action take(char : character, other: character, item : item) {
		precondition:
			char != other
			&has(other, item) > 0
			&char != mc
			&health(char) > 0
			&health(other) > 0
			
			;

		effect:
			did_something(char) = did_something(char) + 1

			&has(char, item) = has(char, item)  +1
			&has(other, item) = has(other, item) - 1
			
			
			&happiness(char) =happiness(char) - (altruism(char)/2) - (likes(char,other)/5) 
			&altruism(char) = altruism(char) - 3
			&ambition(char) = ambition(char) + 2
			&trusts(char,other) = trusts(char,other) - 3
			&health(char) = health(char) - 2


			&happiness(other) =happiness(other)  - 4
			&altruism(other) = altruism(other) - 3
			&ambition(other) = ambition(other) + 1
			&likes(other,char) =likes(other,char) -  4
			&trusts(other,char) = trusts(other,char) - 4
			&health(other) = health(other) - 3
			
			;
		consenting: char;
		
	};


	//dodaj value, maja rozne ceny 
	action exchange(char : character, other: character, item1 : item, item2 :item) {
		precondition:
			char != other
			&item1 !=item2
			&has(char, item1) >0
			&has(other, item2) >0
			&char != mc

			&health(char) > 0
			&health(other) > 0
			;

		effect:
			did_something(char) = did_something(char) + 1
			//&did_something(other) = did_something(other) + 1


			&has(char, item1) = has(char, item1) - 1
			&has(other, item1) = has(other, item1) + 1

			&has(char, item2) = has(char, item2) + 1
			&has(other, item2) = has(other, item2) - 1
			
			&happiness(char) =happiness(char) +3 
			&altruism(char) = altruism(char)+  1
			&ambition(char) = ambition(char) + 1
			&likes(char,other) =likes(char,other) +  1
			&trusts(char,other) = trusts(char,other) + 2


			&happiness(other) =happiness(other) +3 
			&altruism(other) = altruism(other)+  1
			&ambition(other) = ambition(other) + 1
			&likes(other,char) =likes(other,char) +  1
			&trusts(other,char) = trusts(other,char) + 2
			
			;
		consenting: char,other;
		
	};

	action compliment(char : character, other: character) {
		precondition:
			char != other
			&health(char) > 0
			&health(other) > 0
		    &char != mc
			;

		effect:
			did_something(char) = did_something(char) + 1
			
			
			&happiness(char) =happiness(char) +  (altruism(char)/7) + (likes(char,other)/7)
			&altruism(char) = altruism(char)+  2
			&likes(char,other) =likes(char,other) +  1
			&trusts(char,other) = trusts(char,other) + 1


			&happiness(other) =happiness(other) +  (altruism(other)/7) + (likes(other,char)/7) + 3
			&altruism(other) = altruism(other)+  2
			&likes(other,char) =likes(other,char) +  3
			&trusts(other,char) = trusts(other,char) + 1
			
			;
		consenting: char;
		
	};
	action work(char : character) {
		precondition:
			health(char) > 0
			&char != mc
			;

		effect:
			did_something(char) = did_something(char) + 1

			&has(char, money) = has(char, money)  +1
			
			
			&happiness(char) =happiness(char) + (ambition(char)/4) 
			&ambition(char) = ambition(char) + 1
			&health(char) = health(char) - 3
			
			;
		consenting: char;
		
	};


	action eat(char : character) {
		precondition:
			health(char) > 0
			&has(char,food) > 0
		    &char != mc
			;

		effect:
			did_something(char) = did_something(char) + 1

			&has(char,food) = has(char,food)  - 1
			
			
			&happiness(char) =happiness(char) + 2

			&health(char) = health(char) + 5
			
			;
		consenting: char;
		
	};


	action rest(char : character) {
		precondition:
			
			health(char) > 0
			&char != mc
			;

		effect:
			did_something(char) = did_something(char) + 1
			
			&health(char) = health(char) + 5
			&happiness(char) =happiness(char) + 4
			


			
			
			;
		consenting: char;
		
	};

	action take_care_of(char : character, other: character) {
		precondition:
			char != other
			&char != mc
			&health(other) < 5
			
			;

		effect:
			did_something(char) = did_something(char) + 1
			
			
			&happiness(char) =happiness(char) + (altruism(char)/7) + (likes(char,other)/7)
			&altruism(char) = altruism(char)+  2
			&likes(char,other) =likes(char,other) +  2
			&trusts(char,other) = trusts(char,other) + 1


			&health(other) = health(other) + 10
			&happiness(other) =happiness(other) + 5
			&altruism(other) = altruism(other)+  4
			&likes(other,char) =likes(other,char) +  5
			&trusts(other,char) = trusts(other,char) + 2
			
			;
		consenting: char;
		
	};

	action attack(char : character, other: character) {
		precondition:
			char != other
			//&health(char) > 0
			//&points(char) > 0
			//&altruism(char) < -13
			&ambition(char) > 13
			&char != mc
			;

		effect:
			did_something(char) = did_something(char) + 1
			
			&happiness(char) = happiness(char) - 5 - (altruism(char)/5) - (likes(char,other)/5)
			&altruism(char) = altruism(char) -  4
			&ambition(char) = ambition(char) + 3
			&trusts(char,other) = trusts(char,other) - 2

			&health(other) = health(other) - 10
			&happiness(other) = happiness(other) - (altruism(other)/5) - 3
			&altruism(other) = altruism(other) - 4
			&ambition(other) = ambition(other) - 2
			&likes(other,char) =likes(other,char) - 4
			&trusts(other,char) = (trusts(other,char) - 4)
			
			;
		consenting: char;
		
	};

	action read(char : character) {
		precondition:
			health(char) > 0
			&has(char,book) > 0
		   &char != mc
			;

		effect:
			did_something(char) = did_something(char) + 1

			
			
			&happiness(char) =happiness(char) + 3

			
			
			;
		consenting: char;
		
	};

	action spend_time_together(char : character, other: character) {
		precondition:
			char != other
			&char != mc
			;

		effect:
			did_something(char) = did_something(char) + 1
			
			
			&happiness(char) =happiness(char) +  (likes(char,other)/4)
			&altruism(char) = altruism(char)+  2
			&likes(char,other) =likes(char,other) +  3
			&trusts(char,other) = trusts(char,other) + 2

			&happiness(other) =happiness(other) + (likes(other,char)/4)
			&altruism(other) = altruism(other)+  2
			&likes(other,char) =likes(other,char) +  3
			&trusts(other,char) = trusts(other,char) + 2
			
			;
		consenting: char,other;
		
	};

	action intimidate(char : character, other: character) {
		precondition:
			char != other
			&health(char) > 0
			&health(other) > 0
		   &char != mc
			;

		effect:
			did_something(char) = did_something(char) + 1
			
			&happiness(char) =happiness(char) -  (altruism(char)/7) - (likes(char,other)/7)
			&altruism(char) = altruism(char) - 2
			&trusts(char,other) = trusts(char,other) - 1


			&happiness(other) =happiness(other) -  (altruism(other)/7) - (likes(other,char)/7) - 2
			&ambition(other) = ambition(other) - 3
			&altruism(other) = altruism(other) - 3
			&likes(other,char) =likes(other,char) -  4
			&trusts(other,char) = trusts(other,char) - 1
			
			;
		consenting: char;

	};

	action gossip_about (char : character, other: character, about : character) {
		precondition:
			char != other
			&other != about
			&char !=about
			&health(char) > 0
			&health(other) > 0
		   &char != mc
			;

		effect:
			did_something(char) = did_something(char) + 1

			&happiness(char) = happiness(char) - (altruism(char)/8)
			&altruism(char) = altruism(char) - 1


			&happiness(other) = happiness(other) - (altruism(other)/8)
			&altruism(other) = altruism(other) - 1
			&likes(other,char) =likes(other,char) +  1
			&trusts(other,char) = trusts(other,char) - 1

			&likes(other,about) =likes(other,about) - 2 - (trusts(other,char)/6)
			&trusts(other,about) = trusts(other,about) - 2 - (trusts(other,char)/6)
			
			;
		consenting: char;
		
	};

	action praise_someone(char : character, other: character, about :character) {
		precondition:
			char != other
			&other != about
			&char !=about
			&health(char) > 0
			&health(other) > 0
		   &char != mc
			;

		effect:
			did_something(char) = did_something(char) + 1
			
			
			&happiness(char) = happiness(char) + (altruism(char)/8)
			&altruism(char) = altruism(char) + 1


			&happiness(other) = happiness(other) + (altruism(other)/8)
			&altruism(other) = altruism(other) + 1
			&likes(other,char) =likes(other,char) +  1
			&trusts(other,char) = trusts(other,char) + 1

			&likes(other,about) =likes(other,about) + 2 + (trusts(other,char)/6)
			&trusts(other,about) = trusts(other,about) + 2 + (trusts(other,char)/6)
			
			;
		consenting: char;
		
	};
	
	//////////////////utility

	
			""")

			f.write("utility(): \n ".format(char.name))
			f.write("if (did_something({}) ==1) \n".format(self.current_character.name))

			for count, goal in enumerate(self.current_character.goals):
					f.write("(if{} 1 else 0 )".format(goal))
					if count == len(self.current_character.goals)-1:
						f.write( "\n")
					else: f.write(" + ")

			f.write("else 0; \n ")
		


			for char in self.gl.characters.values():
				f.write("utility({}): \n ".format(char.name))
				for count, goal in enumerate(char.goals):
					f.write("(if {} 1 else 0 )".format(goal))
					if count == len(char.goals)-1:
						f.write( ";\n")
					else: f.write(" + ")
			
			
			f.close()

gm = Game()
