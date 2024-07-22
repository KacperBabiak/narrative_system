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


def make_action(df,world_state, action_name ):
	#stan swiata jest opisany w kolumnie cecha_entity row postac/world
	#moze sie zmienic wartość lub numerycznie 
	#format: cecha_entity;postac;+;x,
	line = df[df.action_name == action_name].effects_on_world


	changes = line.split(',')
	for change in changes:
		entities = change.split(';')
		if '='  == entities[2]:
			world_state.iloc[entities[0],entities[1]] = entities[3]
		elif '+'  == entities[2]:
			world_state.iloc[entities[0],entities[1]] = world_state.iloc[entities[0],entities[1]] + entities[3]
		elif '-'  == entities[2]:
			world_state.iloc[entities[0],entities[1]] = world_state.iloc[entities[0],entities[1]] - entities[3]

text = load_action('lib\\test1.txt')
print(text)