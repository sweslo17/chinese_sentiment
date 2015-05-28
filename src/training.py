import json
import datetime
import jieba
import sqlite3

def preprocess(input_str):
	return input_str.strip()

def create_table(cnx,cur):
	cur.execute('DROP TABLE IF EXISTS sentiment_positive_word')
	cur.execute('DROP TABLE IF EXISTS sentiment_negative_word')
	cur.execute('DROP TABLE IF EXISTS sentiment_baseline')
	cur.execute('CREATE TABLE sentiment_positive_word (word,value)')
	cur.execute('CREATE TABLE sentiment_negative_word (word,value)')
	cur.execute('CREATE TABLE sentiment_baseline (positive_document_count,negative_document_count,positive_word_count,negative_word_count)')
	cnx.commit()

def read_data_file(file_name):
	doc_list = file(file_name).readlines()
	output = []
	for doc in doc_list:
		output.append(preprocess(doc))
	return output

def training(positive_file_name,negative_file_name,model_path,user_dic_name=''):
	if user_dic_name != '':
		jieba.load_userdict(user_dic_name)
	pos_data_list = []
	cnx = sqlite3.connect(model_path+'model.db')
	cur = cnx.cursor()
	create_table(cnx,cur)
	pos_data_list = read_data_file(positive_file_name)
	neg_data_list = read_data_file(negative_file_name)

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
		sql = "INSERT INTO sentiment_positive_word (word,value) VALUES (?,?)"
		value = float(pos_word_count_dic[word]+1)/pos_word_count
		cur.execute(sql,(word,value))

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
		sql = "INSERT INTO sentiment_negative_word (word,value) VALUES (?,?)"
		value = float(neg_word_count_dic[word]+1)/neg_word_count
		cur.execute(sql,(word,value))

	sql = "INSERT INTO sentiment_baseline (positive_document_count,negative_document_count,positive_word_count,negative_word_count) VALUES (?,?,?,?)"
	cur.execute(sql,(len(pos_data_list),len(neg_data_list),pos_word_count,neg_word_count))
	cnx.commit()
#pass

if __name__ == '__main__':
	#jieba.load_userdict('dict/user_dic.dic')
	training('data/positive.txt','data/negative.txt','model/')
