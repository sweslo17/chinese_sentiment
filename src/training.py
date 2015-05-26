import json
import subprocess
import mysql.connector
import config
import datetime
import jieba

def get_article_list(date_from,date_to,keyword_id):
	data = json.loads(subprocess.check_output(["php", "adaptor.php",config.db_host,config.db_user,config.db_password,config.db_database,"SELECT key_no FROM ptt_data WHERE load_time>='"+date_from+"' AND load_time<'"+date_to+"' AND term_id='"+keyword_id+"'"]))
	key_no_list = []
	for result in data:
		key_no_list.append(result['key_no'])
	return key_no_list

def preprocess(input_str):
	return input_str.strip()

def training(keyword_id,date_from,date_to):
	board_list = ['Gossiping','HatePolitics']
	jieba.load_userdict('user_dic.dic')
	if keyword_id != -1:
		id_list_str = "'" + "','".join(get_article_list(str(date_from),str(date_to),str(keyword_id))) + "'"
		sql = "SELECT content FROM all_in_one WHERE likes='1' AND isreply='1' AND datatype='1' AND key_no IN ("+id_list_str+")"
	else:
		sql = "SELECT content FROM all_in_one WHERE likes='1' AND isreply='1' AND time>='"+str(date_from)+"' AND time<'"+str(date_to)+"' AND datatype='1' AND sitename IN ('"+"','".join(board_list)+"')"
	#print sql
	pos_data = json.loads(subprocess.check_output(["php", "adaptor.php",config.db_host,config.db_user,config.db_password,'social_data',sql]))
	pos_data_list = []
	cnx = mysql.connector.connect(host=config.db_host,user=config.db_user,passwd=config.db_password,database=config.db_database,charset='utf8')
	cur = cnx.cursor()
	cur.execute('TRUNCATE TABLE sentiment_positive_word')
	cur.execute('TRUNCATE TABLE sentiment_negative_word')
	cnx.commit()
	for data in pos_data:
		pos_data_list.append(preprocess(data['content']))
	if keyword_id != -1:
		sql = "SELECT content FROM all_in_one WHERE likes='-1' AND isreply='1' AND datatype='1' AND key_no IN ("+id_list_str+")"
	else:
		sql = "SELECT content FROM all_in_one WHERE likes='-1' AND isreply='1' AND time>='"+str(date_from)+"' AND time<'"+str(date_to)+"' AND datatype='1' AND sitename IN ('"+"','".join(board_list)+"')"
	neg_data = json.loads(subprocess.check_output(["php", "adaptor.php",config.db_host,config.db_user,config.db_password,'social_data',sql]))
	neg_data_list = []
	for data in neg_data:
		neg_data_list.append(preprocess(data['content']))
#		print data['content'].strip().encode('utf-8')
	#print len(neg_data)
	#print len(pos_data)

#positive
	pos_word_count_dic = {}
	pos_word_count = 0
	for data in pos_data_list:
		word_list = jieba.cut(data)
		for word in word_list:
			word = word.strip()
			if len(word) > 0:
				if word not in pos_word_count_dic:
					pos_word_count_dic[word] = 0
				pos_word_count_dic[word] += 1
				pos_word_count += 1
	for word in pos_word_count_dic.keys():
		sql = "REPLACE INTO sentiment_positive_word (word,probability,keyword_id) VALUES (%s,%s,%s)"
		probability = float(pos_word_count_dic[word]+1)/pos_word_count
		cur.execute(sql,(word,probability,keyword_id))

#negative
	neg_word_count_dic = {}
	neg_word_count = 0
	for data in neg_data_list:
		word_list = jieba.cut(data)
		for word in word_list:
			word = word.strip()
			if len(word) > 0:
				if word not in neg_word_count_dic:
					neg_word_count_dic[word] = 0
				neg_word_count_dic[word] += 1
				neg_word_count += 1
	for word in neg_word_count_dic.keys():
		sql = "REPLACE INTO sentiment_negative_word (word,probability,keyword_id) VALUES (%s,%s,%s)"
		probability = float(neg_word_count_dic[word]+1)/neg_word_count
		cur.execute(sql,(word,probability,keyword_id))

	sql = "REPLACE INTO sentiment_baseline (positive_article_count,negative_article_count,positive_word_count,negative_word_count,keyword_id,update_time) VALUES (%s,%s,%s,%s,%s,%s)"
	cur.execute(sql,(len(pos_data),len(neg_data),pos_word_count,neg_word_count,keyword_id,datetime.date.today()))
	cnx.commit()
#pass

if __name__ == '__main__':
	#print ','.join(get_article_list('2015-05-05','2015-05-06','709'))
	date_from = datetime.date.today()-datetime.timedelta(days=7)
	date_to = datetime.date.today()
	training(-1,date_from,date_to)
