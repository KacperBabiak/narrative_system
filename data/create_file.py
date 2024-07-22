import pandas as pd
import random
import itertools

#opening file with key actions
df = pd.read_csv('data\\key_action.csv').drop(['priority'],axis=1)
df = df.rename({'name':'action_name'},axis=1)

#choosing main module, actions and tag that it has
modules = list(set(df.module.values))
chosen_module = random.choice(modules)
chosen_actions = [row.action_name for index,row in df[df.module == chosen_module].iterrows()]
chosen_tag = df[df.module == chosen_module].iloc[0].tags

#opening file with  actions
df_actions = pd.read_csv('data\\actions.csv').drop(['priority'],axis=1)

#choosing a second module with a missing tag
tags = list(set(df_actions.tags.values))
tags.remove(chosen_tag)
tags.remove('always')
action_modules = list(set(df_actions[df_actions.tags == tags[0]].module.values))
second_module = random.choice(action_modules)

#adding rest of actions
chosen_actions.extend([row.action_name for index,row in df_actions[df_actions.module == second_module].iterrows()])
chosen_actions.extend([row.action_name for index,row in df_actions[df_actions.module == 'basic_always'].iterrows()])
print(chosen_actions)


df_req = pd.read_csv('data\\requirements.csv',index_col='index')
print(df_req)

requirements = {}
columns = df_req.columns
for index,row in df_req.iterrows():
    for column in columns:
        name = str(index) + "_" + column
        
        requirements[name] = df_req.loc[index,column]

df_eff = pd.read_csv('data\\effects.csv',index_col='index')
df_eff

effects = {}
columns = df_eff.columns
for index,row in df_eff.iterrows():
    for column in columns:
        name = str(index) + "_" + column
        
        effects[name] = df_eff.loc[index,column]

def key_action_to_text(row):
    entities = ""
    for ent in row.entities.split(';'):
        
        if 'char' in ent:
            entities = entities + ent + ":character,"
        elif 'item' in ent:
            entities = entities + ent + ":item,"
    entities = entities.rstrip(',')

    req = ""
    items = ['food', 'weapon', 'book', 'poison', 'money' ,'item']
    for r in row.requires.split(';'):
        
        req = req +  str(requirements[r.replace(' ','')]) + " & "
        
    req = req.rstrip(' & ')

    altruism = row.altruism.split(';')
    ambition = row.ambition.split(';')

    sat = "if ("
    
    if len(altruism) > 1:
        sat = sat + altruism[0] + 'altruism(char) & (ambition(char) + desperation(char)) ' + altruism[1]
        
    else:
        sat = sat + 'altruism(char) ' + altruism[0]
    
    if len(ambition) > 1:
         sat = sat + ambition[0] + '& ambition(char) & (ambition(char) + desperation(char))  ' + ambition[1]
    else:
        sat = sat + ' & ambition(char) ' + ambition[0]
    
    sat += ") \n            satisfaction(char) = satisfaction(char) + 1 "

    text= f"""
    action {row.action_name}({entities}) {{
        precondition:
    
            {req}
            ;
        effect:
        {sat}
            ;
        consenting: {row.consents};
    }};

    """
    return text

def action_to_text(row):
    entities = ""
    for ent in row.entities.split(';'):
        
        if 'char' in ent:
            entities = entities + ent + ":character,"
        elif 'item' in ent:
            entities = entities + ent + ":item,"
    entities = entities.rstrip(',')

    req = ""
    if  'char2' in entities:
        req = req + " char != char2 & \n"
        if  'char3' in entities:
            req = req + " char2 != char3 & char != char3 & \n"

    for r in row.requires.split(';'):
        
        req = req +  str(requirements[r.replace(' ','')]) + " & "
        
    req = req.rstrip(' & ')

    eff =''
    for e in row.effects.split(';'):
        
        eff = eff +  str(effects[e.replace(' ','')]) + " & "
    eff = eff.rstrip(' & ')

    text= f"""
    action {row.action_name}({entities}) {{
        precondition:
            {req}
            ;
        effect:
        {eff}
            ;
        consenting: {row.consents};
    }};

    """
    return text

text="""
type item;
type world;
type change;

//### Properties:
property satisfaction(char: character) : number; // Satisfaction level of each character
property altruism(char: character) : number; // Altruism level of each character (-3 to 3)
property ambition(char: character) : number; // Ambition level of each character (-3 to 3)
property in_danger(char: character) : number; 
property desperation(char: character) : number; // Ambition level of each character (-3 to 3)
property max_ambition(char: character) : number; // Ambition level of each character (-3 to 3)

property health(char: character) : number; 
property knowledge(char: character) : number; 
property threat(char: character) : number; 
property authority(char: character) : number; 
property has_item(char: character) : item; 
property relation(char: character, other: character) : number; // Relationship liking level between characters (-3 to 3)

property willSupport(char: character) : character; 
property willHarm(char: character,char2 : character) : boolean; 
property willChange(ch : change, char2 : character) : number; 

property current_ship_defense(world:world) : number; 
property current_ship_magic(world:world) : number; 
property ship_defense(world:world) : number; 
property ship_magic(world:world) : number; 
property avalaible(char: item) : boolean; 

entity world:world;

entity mc : character;
entity actress : character;
entity actor : character;

entity food : item;
entity weapon : item;
entity book : item;
entity medicine : item;
entity money : item;

entity defense :change;
entity magic :change;

forall(i:item)
    (avalaible(i));
health(mc) = 5;
health(actress) = 5;
health(actor) = 5;

ambition(mc) = 5;
altruism(mc) = -2;


""".format(5,-2)


df_chosen = df[df.action_name.isin(chosen_actions) ]


for index, row in df_chosen.iterrows():
    text = text + key_action_to_text(row) + "\n"




df_chosen = df_actions[df_actions.action_name.isin(chosen_actions) ]


for index, row in df_chosen.iterrows():
    text = text + action_to_text(row) + "\n"

text= text + """

trigger max_ambition_calc(char:character) {
	precondition:
		max_ambition(char) !=  ambition(char) + desperation(char) ;
	effect:
		max_ambition(char) =  ambition(char) + desperation(char) ;
};

trigger threat_calc(char:character) {
	precondition:
		threat(char) !=  health(char) + (if (has_item(char) == weapon) 1 else 0) - sum(c:character) (if (willHarm(c,char)) 1 else 0) ;
	effect:
		threat(char) ==  health(char) + (if (has_item(char) == weapon) 1 else 0) - sum(c:character) (if (willHarm(c,char)) 1 else 0);
};


trigger authority_calc(char:character) {
	precondition:
		authority(char) !=  knowledge(char) + (if (has_item(char) == book) 1 else 0) + sum(c:character) (if (willSupport(c) == char ) 1 else 0);
	effect:
		authority(char) ==  knowledge(char) + (if (has_item(char) == book) 1 else 0) + sum(c:character) (if (willSupport(c) == char ) 1 else 0);
};

trigger ship_defense_calc() {
	precondition:
		ship_defense(world) !=   current_ship_defense(world) + sum(c:character) willChange(defense, c) ;
	effect:
		ship_defense(world) ==   current_ship_defense(world) + sum(c:character) willChange(defense, c) ;
};

trigger ship_magic_calc() {
	precondition:
		ship_magic(world) !=   current_ship_magic(world) + sum(c:character) willChange(magic, c) ;
	effect:
		ship_magic(world) ==   current_ship_magic(world) + sum(c:character) willChange(magic, c) ;
};




utility():
    satisfaction(mc);

utility(mc):
    satisfaction(mc);

utility(actress):
    satisfaction(actress);

utility(actor):
    satisfaction(actor);


"""

print(text)

file1 = open("lib\\test1.txt", "w") 
file1.write(text)


file1.close() 


