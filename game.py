from subprocess import Popen, PIPE, STDOUT
import GameLogic as logic
import entities.character as chr

class Game:

    
    def __init__(self) -> None:
        self.init_state()
        self.change_state('first')
        self.game_loop()

    #wprowadza stan swiata pierwszy
    def init_state(self):
        characters = {}
        self.gl = logic.GameLogic(characters)

        agent = chr.Character(self.gl, "agent", -17, 3 )
        characters["agent"]=agent

        doctor = chr.Character(self.gl, "doctor", 17, 10 )
        characters["doctor"]=doctor

        science = chr.Character(self.gl, "science", 0, -17 )
        characters["science"]=science

        actor = chr.Character(self.gl, "actor", -3, 17 )
        characters["actor"]=actor


        agent.add_char(doctor,0,0)
        agent.add_char(science,0,0)
        agent.add_char(actor,0,0)
        
        doctor.add_char(agent,0,0)
        doctor.add_char(science,0,0)
        doctor.add_char(actor,0,0)

        science.add_char(doctor,0,0)
        science.add_char(agent,0,0)
        science.add_char(actor,0,0)

        actor.add_char(doctor,0,0)
        actor.add_char(science,0,0)
        actor.add_char(agent,0,0)


        self.gl.characters = characters
        self.print_state()

        

    def print_state(self):
        print("candles: " + str(self.gl.candles) + "\n")
        for char in self.gl.characters.values():
            print(char.name + " | points: " + str(char.points) + " altruism: " + str(char.altruism) + " ambition: " + str(char.ambition) )

        

    #odpala plan i przejmuje akcje
    def load_action(self,file):

        
        p = Popen(['java', '-jar', 'lib\sabre.jar', '-p', file,'-el',"0"], stdout=PIPE, stderr=STDOUT)
        
        for line in p.stdout:
            return (str(line, encoding='utf-8'))

    #wykonuje akcje 
    def do_action(self,args):

        match args[0]:
            case "light_first_candle":
                print("lighted first candle")
                self.gl.characters[args[1]].light_first_candle()
            case "light_another_candle":
                print("lighted another candle")
                self.gl.characters[args[1]].light_another_candle(self.gl.characters[args[2]])
            case "put_out_candle":
                print("putted out candle")
                self.gl.characters[args[1]].put_out_candle(self.gl.characters[args[2]])
            case "put_out_first_candle":
                print("putted out first candle")
                self.gl.characters[args[1]].put_out_first_candle()


    #aktualizuje stan swiata
    def change_state(self,mode):
        action=''
        if mode == 'first':
            action = self.load_action('lib\hotel4.txt')
        else:
            action = self.load_action('lib\hotel_new.txt')
        
        print(action)
        
        args = action.replace("("," ").replace(")","").replace("\r\n","").replace(",","").split(' ')
        self.do_action(args)
        #self.print_state()
        


    def game_loop(self):
        while True:
            self.create_file()
            self.change_state('new')
            

    #tworzy nowy plik
    def create_file(self):
        with open("lib/hotel_new.txt", 'w') as f:
            f.write("""///////////////////////////////////entity


entity actor : character;
entity science : character;
entity doctor : character;
entity agent : character;
entity mc : character;
entity tumblr : character;

entity game : entity;

//////////////////////////////////property


//character
property health(character : character) : number;
property points(character : character) : number;
property did_something(char: character) : number;
property imprisoned(char: character) : boolean;

//game
property lighted_candle(char: character) : boolean;
property lighted_first_candle(char: character) : boolean;
property number_of_candles(entity:entity) : number;

//emotions
property happiness(character : character) : number;
property altruism(character : character) : number;
property ambition(character : character) : number;

//emotions towards other characters
property likes(character1: character, character2 : character) : number;
property trusts(character1: character, character2 : character) : number;""")

            #warrtosci postaci
            for char in self.gl.characters.values():
                f.write("health("+ char.name  +") = " + str(char.health) + " ; \n")
                f.write("points(" + char.name  +") = " + str(char.points) + " ; \n")
                f.write("happiness(" + char.name  +") = " + str(char.happiness) + " ;\n")
                f.write("altruism(" + char.name  +") = " + str(char.altruism) + " ;\n")
                f.write("ambition(" + char.name  +") = " + str(char.ambition) + " ;\n")

                if char.lighted_candle:
                    f.write("lighted_candle(" + char.name  +") ;\n")

                for k,v in char.likes.items():
                    f.write("likes("+ char.name + ", " + k.name + ") = "+str(v) + " ;\n")

                for l in char.trusts:
                    f.write("trusts("+ char.name + ", " + k.name + ") = "+str(v) + " ;\n")

            #wartości fry
            f.write("number_of_candles(game)= " + str(self.gl.candles) + " ; \n")

            if self.gl.first_candle_char != None:
                f.write("lighted_first_candle(" + self.gl.first_candle_char.name +  ") ; \n")

            f.write("""action light_first_candle(char : character) {
	precondition:
		number_of_candles(game) == 0
		;

	effect:
		did_something(char) = did_something(char) + 1 &
		lighted_first_candle(char)
		& number_of_candles(game) =  number_of_candles(game) + 1

        & points(char) =  points(char) + 1

        & if(ambition(char) > 10) (
                                    ambition(char) = ambition(char) + 2
								    & happiness(char) = happiness(char) + 2)
                                 
								  
        & if(ambition(char) < -10)   (ambition(char) = ambition(char) + 3
								  & happiness(char) = happiness(char) - 3
								  )

		;
		 
	consenting: char;
	
};


//char
//altruizm - + szczeszcie jesli wysoko, minus jesli nisko
//ambicja -,zwieksza sie + troche szczescie jesli wysoko
//lubienie - jesli bardzo lubi to plus szczescie, minus jesli nie lubi
//ufanie  -  brak

//other
//altruizm - lekki plus
//ambicja - brak
//lubienie - plus lubienie
//ufanie  - plus ufanie

action light_another_candle(char : character, other : character ) {
	precondition:
        char != other 
		& number_of_candles(game) > 0
		& lighted_first_candle(other)
		& ! lighted_candle(char)
		;

	effect:
		did_something(char) = did_something(char) + 1 
		& number_of_candles(game) =  number_of_candles(game) + 1
		& lighted_candle(char)
        & points(char) =  points(char) + 1
		& points(other) =  points(other) + 1

		& ambition(char) = ambition(char) + 1
		& altruism(char) = altruism(char) + 1

        & if(altruism(char) >= 0) ( 
                            
								   happiness(char) = happiness(char) + 2
                                 ) 
								  
        & if(altruism(char) < -10)   (happiness(char) = happiness(char) - 1
								  )


		 & if(likes(char,other) > 5) ( 
								   happiness(char) = happiness(char) + 3
                                 ) 
								  
        & if(likes(char,other) < -5)   (happiness(char) = happiness(char) - 2
								  )
		
		&likes(other,char) =  likes(other,char) + 2
		& trusts(other,char) = trusts(other,char)  + 2
		& altruism(other) = altruism(other)  + 1
		;
		 
	consenting: char;
	
};

//char
//altruizm - zmmniejsza sie, szczeszcie jesli wysoko, plus jesli nisko
//ambicja zwieksza sie + troche szczescie jesli wysoko, traci szczescie jesli nisko
//lubienie - jesli bardzo lubi to minus szczescie, plus jesli nie lubi
//ufanie  -  brak

//other
//altruizm - lekki minus
//ambicja - brak
//lubienie - minus lubienie
//ufanie  - minus ufanie

action put_out_candle(char : character, other : character ) {
	precondition:
        char != other 
		& number_of_candles(game) > 0
		& lighted_first_candle(other)
		
		;

	effect:
		did_something(char) = did_something(char) + 1 
		
        & points(char) =  points(char) + number_of_candles(game)
		& points(other) =  points(other) - number_of_candles(game)

		& ambition(char) = ambition(char) + 2
		& altruism(char) = altruism(char) - 4

        & if(altruism(char) > 10) ( 
                            
								   happiness(char) = happiness(char) - 5
                                 ) 
								  
        & if(altruism(char) < -10)   (happiness(char) = happiness(char) + 4
								  )

		& if(ambition(char) > 10) ( 
                            
								   happiness(char) = happiness(char) + 2
                                 ) 
		& if(ambition(char) < -10) ( 
                            
								   happiness(char) = happiness(char) - 4
                                 ) 

		 & if(likes(char,other) > 10) ( 
								   happiness(char) = happiness(char) - 4
                                 ) 
								  
        & if(likes(char,other) < -10)   (happiness(char) = happiness(char) + 3
								  )
		
		&likes(other,char) =  likes(other,char) - 5
		& trusts(other,char) = trusts(other,char)  - 5
		& altruism(other) = altruism(other)  - 2


		& number_of_candles(game) = 0
		& !lighted_first_candle(other)
		& forall(c : character) 
			if(lighted_candle(c)) !lighted_candle(c)
		;
		 
	consenting: char;
	
};


action put_out_first_candle(char : character ) {
	precondition:
         number_of_candles(game) > 0
		& lighted_first_candle(char)
		
		;

	effect:
		did_something(char) = did_something(char) + 1 
		

		& if(ambition(char) > 10) ( 
                            
								   happiness(char) = happiness(char) - 3
                                 ) 
		& if(ambition(char) < -10) ( 
                            
								   happiness(char) = happiness(char)  + 3
                                 ) 

		


		& number_of_candles(game) = 0
		& !lighted_first_candle(char)
		& forall(c : character) 
			if(lighted_candle(c)) !lighted_candle(c)
		;
		 
	consenting: char;
	
};


utility(): ((sum(c : character) did_something(c)) == 1 ) 
        //&did_something(science) > 0
		//&did_something(actor) > 0
            ;

//(if(0 < (sum(c : character) did_something(c)) < 3) 1 else 0) ;



utility(doctor):
	 (points(doctor)  + happiness(doctor) );

utility(agent):
	 (points(agent)   + happiness(agent));

utility(actor):
	 (points(actor)  + happiness(actor));

utility(science):
	 (points(science)  + happiness(science));""")
        f.close()

gm = Game()
