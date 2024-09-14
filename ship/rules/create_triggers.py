import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
import operator
from scipy.stats import chi2_contingency 
import numpy as np
import itertools

df = pd.read_csv('ship\\rules\dataset_results.csv')
df_effects = pd.read_csv('ship\\rules\\ship_effects_nn.csv')

df = df[df.results.notna()]
df = df.drop(df[df.results == 'Time limit reached.\r\n'].index)
df = df.drop(df[df.results == 'No solution exists.\r\n'].index)
df.reset_index(inplace=True,drop=True)

def removern(row):
    if 'results' in row.index:
        row.results = row.results.replace('\r','')
        row.results = row.results.replace('\n','')
        row.results = row.results.replace('\t','')
    if 'effect' in row.index:
        row.effect = row.effect.replace('\r','')
        row.effect = row.effect.replace('\n','')
        row.effect = row.effect.replace('\t','')
    return row


df = df.apply(removern,axis=1)
df_effects = df_effects.apply(removern,axis=1)


def replace_effect(effect,args):
	for count,arg in enumerate(args,0):			
		effect = effect.replace('arg'+str(count+1),arg)
	
	return effect	

def create_result(df ,row):

    new_row = row
    if (('Time limit reached' in row.results) ):
        new_row.results = 'Time limit reached'
        df.loc[len(df)] = new_row
        return 'Time limit reached'
    if ( ('No solution exists' in row.results)):
        new_row.results = 'No solution exists'
        df.loc[len(df)] = new_row
        return 'No solution exists'
    
    
    
    actions = row.results.split(') ')

    action = actions[0]
    
    action = action.split('(')
    only_action = action[0]
    
    variables = action[1].replace(')','').split(', ')
    
    if df_effects[df_effects.action == action[0]].empty:
        return 'No solution exists' 
    effects= df_effects[df_effects.action == action[0]].effect_function
    
    effects2 = df_effects[df_effects.action == action[0]].effect_args.values[0].split(';')
    
        
    if len(effects) > 0:
        effects_results = ""
        for i,effect in enumerate(str(effects.values[0]).split(';')):
            new_row.results = str(str(replace_effect(effect,variables) )   + "&" + str(df_effects[df_effects.action == action[0]].action.values[0])+ "&" + str(replace_effect(effects2[i],variables) ))
            df.loc[len(df)] = new_row
            
            break


        #df.drop(index)
    return only_action
        


df2 = pd.DataFrame(columns = df.columns)
for index, row in df.iterrows():
    create_result(df2,row)
df = df2
df.rename({'results':'result'},axis=1,inplace=True)
df.drop(['time'],axis=1,inplace=True)


results_all = []

df3 = df.copy()

#print(df3)
df3.reset_index(inplace=True,drop=True)



chi = {}
features = [x for x in df3.columns if x != 'result' and x!= 'index']
#print('chi',features)
for feature in features:
    chisqt = pd.crosstab(df3[feature], df3.result, margins=True)
    if len(chisqt) > 0:
        #print(chisqt)
        #print(chisqt.iloc[0][0:5].values)
        #print(chisqt.iloc[1][0:5].values)
        value = np.array([chisqt.iloc[0][0:5].values,
                    chisqt.iloc[1][0:5].values])
        
        try:
            c = chi2_contingency(value)[0:3]
            chi[str(feature)] = c
        except:
            print("An exception occurred")
        

features = [k for k,v in chi.items() if v[1] < 0.05] 
if len(features) > 4:
    features = features[:4]   
#print('corr',features)

feature_values = {}
for feat in features:
    feature_values[feat] = list(df3[feat].value_counts().index)


combination_often = {}

total_combinations = []
for i in range(1,len(features)):
    combinations = list(itertools.combinations(feature_values.keys(), i))
    total_combinations.extend(combinations)


#print('total_combinations',total_combinations)

for combination in total_combinations:
    #print(combination)
    #znalezienie wszystkich możliwych wartości każdej z wybranych cech
    values_list = [value for key,value in feature_values.items() if key in combination]
    #print(values_list)
    #znalezienie każdej możliwej kombinacji wartości tych cech
    combination_values = list(itertools.product(*values_list))
    #print((combination_values))
    
    for comb in combination_values:
        #print(comb)
        #stworzenie pomocniczego df w której cechy mają wybrane wartości
        df_new = df3.copy()
        name=''
        for i,c in enumerate(comb,0):
            #stworzenie nazwy dla kombinacji
            name = name+combination[i]+"="+str(c)+';'
            #print(combination[i],c)
            df_new = df_new[df_new[str(combination[i])]==c]
        
        #print(name)
        
            d = dict(df_new.result.value_counts())
            all = sum(d.values())
            d['sum']=all
            #print(d)
            combination_often[name] = d

    l = list(df3.result.value_counts().keys())
    if len(l)>0:
        for t in l:
            target = t
            print(target)
            combination_counts = {}
            for comb in combination_often:
                counts = combination_often[comb]
                if target in counts:
                    combination_counts[comb] = counts[target]/counts['sum']

            better_comb_often = {k:v for k,v in combination_counts.items() if v == 1.0}
            
            for key,value in better_comb_often.items():
                if value == 1.0:
                #if value > 0.8:
                    better_comb_often = {k:v for k,v in better_comb_often.items() if ((key not in k) or (k == key)) and (v==1.0)}


            sorted_better_comb_often = dict( sorted(better_comb_often.items(), key=operator.itemgetter(1), reverse=True))

            if len(sorted_better_comb_often) > 0:
                results ={}
                
                results['target'] = target
                results['results'] = sorted_better_comb_often
                
                results_all.append(results) 

#print(results_all)
df_all = pd.DataFrame.from_records(results_all)
df_all.to_csv('triggers.csv',index=False)
df_all = pd.read_csv('triggers.csv')

def results_to_list(x):
    x = x.replace('{','')
   
    x = x.replace('}','')
    x = x.replace("'",'')
    
    x = x.replace(': 1.0','')
    split = (x.split(','))
    
    list_lists = []
    for value in split:
        list_lists.append(value.split(';')[:-1])
    return list_lists
    
df_all['results'] = df_all.results.apply(results_to_list)

def simplify_results(df_old):
    df_new = pd.DataFrame(columns = df_old.columns)
    for index,row in df_old.copy().iterrows():
        new_row = row
        
        
        
        list_lists = row.results
        
        
        
        
        new_new_list=[]
        i=0
        
        while i <  len(list_lists)-1:
            
            
            list1 = list_lists[i]
            list2 = list_lists[i+1]
            differences = 0
            new_list=[]
            for j in range(0,len(list1)):
                if list1[j].replace(' ','') != list2[j].replace(' ',''):
                    
                    differences += 1

            
            if differences == 1:
                for k in range(0,len(list1)):
                    if list1[k].replace(' ','') == list2[k].replace(' ',''):
                        new_list.append(list1[k])
                    else:
                        new_list.append(str(list1[k]) + "|" + str(list2[k]))
                i = i + 2
            else:
                new_list = list1
                i = i + 1

            if len(new_list) > 0:
                new_new_list.append(new_list)
        
        if len(new_new_list) > 0:
                
                new_row.results=(new_new_list)

        df_new.loc[len(df_new)] = new_row
    return df_new

df_all = simplify_results(df_all)
#df_all = simplify_results(df_all)

#print(df_all.to_string())

def pred_to_planner(pred):
    parts = pred.split('_')
    value = pred.split('=')[1]
    if '_alive' in pred:
        
        char = parts[0]
        if str(value) == 1:
            return str('alive({})'.format(char))
        else: 
            return str('!alive({})'.format(char))
    elif '_at' in pred:
        
        char = parts[0]
        return str('at({0})=={1}'.format(char,value))
    elif '_underArrest' in pred:
        char = parts[0]
        return str('underArrest({0})=={1}'.format(char,value))
    elif '_angry' in pred:
        char = parts[0]
        return str('angry({0})=={1}'.format(char,value))
    elif '_suspect' in pred:
        char = parts[0]
        return str('suspect({0},{1})'.format(char,value))
    elif '_searched' in pred:
        place = parts[0]
        return str('searched({0})=={1}'.format(place,value))
    elif '_has' in pred:
        item = parts[0]
        return str('has({0})=={1}'.format(item,value))
    elif '_clues' in pred:
        if str(value) == 1:
            return str('clue({0},{1},{2})'.format(parts[0],parts[1],parts[2]))
        else:
            return str('!clue({0},{1},{2})'.format(parts[0],parts[1],parts[2]))
        
actions_dict = {}
i=0
for index, row in df_all.iterrows():
    action_name = row.target.split('&')[1]
    effect = row.target.split('&')[2]
    for action in row.results:
        i+=1
        text = 'action '
        text += 'predictaction_' + str(i) + "_" + action_name   +"(char : character){ \n"
        text += "precondition: \n"
        text += "later(world) & \n"
        
        for pred in action:
            parts = pred.split("|")
            if len(parts) == 1:
                text += '( '+ pred_to_planner(pred) + ') & \n'
            else:
                text += '( '
                for part in parts:
                    text += '( '+ pred_to_planner(pred) + ') |\n'  
                
                text = text[:-3]
                text += ') & \n'     
            
        text = text[:-3]

        text += "; \n effect: \n"
        text += effect + ' \n'
        text += "}; \n"
        actions_dict[text] = 'char1'
        #print(text)


df_actions = pd.DataFrame(data=actions_dict.items(),columns=['actions','char'])
df_actions.to_csv('ship\\rules\df_actions.csv',index=False)