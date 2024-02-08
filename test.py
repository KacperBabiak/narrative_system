
action = "put_out_candle(agent, actor)"
args = action.replace("("," ").replace(")","").replace("\r\n","").replace(",","").split(' ')

print(args)