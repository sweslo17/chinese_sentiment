import mysql.connector
import json
import subprocess

def run(user_dictionary,stopword):
	dic = {}
	'''data = json.loads(subprocess.check_output(["php", "adaptor.php","172.16.78.171","youtube","youtube123!","media_term","SELECT DISTINCT(keyword) as keyword FROM google_trend WHERE category='p12'"]))
	for result in data:
		if result['keyword'].find(" ") == -1:
			dic[result['keyword']] = 1'''
	data = json.loads(subprocess.check_output(["php", "adaptor.php","118.163.94.26","rogerlo","roge2@iii","keyword_topic","SELECT word FROM user_dictionary"]))
	for result in data:
		if result['word'].find(" ") == -1:
			dic[result['word']] = 1
	file = open(user_dictionary,'w')
	for result in dic.keys():
		file.write(result.encode('utf-8')+' 50 n\n')
	file.close()

	dic = {}
	data = json.loads(subprocess.check_output(["php", "adaptor.php","118.163.94.26","rogerlo","roge2@iii","keyword_topic","SELECT word FROM stopword"]))
	for result in data:
		if result['word'].find(" ") == -1:
			dic[result['word']] = 1
	file = open(stopword,'w')
	for result in dic.keys():
		file.write(result.encode('utf-8')+'\n')
	file.close()

if __name__ == '__main__':
	run('user_dic.dic','stopword.dic')
