lines = open('user_dic.dic').readlines()
output = open('sentiment_dic.dic','w')
for line in lines:
	output.write(line.rstrip() + ' 50 n\n')
