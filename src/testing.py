#coding=utf-8
import json
import subprocess
import mysql.connector
import config
import datetime
import jieba
import math
from decimal import *

pos_sentiment_dic = {}
neg_sentiment_dic = {}
pos_word_count = 0
neg_word_count = 0
pos_prior = 0
neg_prior = 0

def load_training_data(keyword_id):
	global pos_sentiment_dic
	global neg_sentiment_dic
	global pos_word_count
	global neg_word_count
	global pos_prior
	global neg_prior
	cnx = mysql.connector.connect(host=config.db_host,user=config.db_user,passwd=config.db_password,database=config.db_database,charset='utf8')
	cur = cnx.cursor()
	cur.execute('SELECT word,probability FROM sentiment_positive_word WHERE keyword_id=%s',(keyword_id,))
	results = cur.fetchall()
	for result in results:
		pos_sentiment_dic[result[0]] = result[1]
	cur.execute('SELECT word,probability FROM sentiment_negative_word WHERE keyword_id=%s',(keyword_id,))
	results = cur.fetchall()
	for result in results:
		neg_sentiment_dic[result[0]] = result[1]
	cur.execute('SELECT positive_word_count,negative_word_count,positive_article_count/(negative_article_count+positive_article_count),negative_article_count/(negative_article_count+positive_article_count) FROM sentiment_baseline WHERE keyword_id=%s',(keyword_id,))
	result = cur.fetchone()
	pos_word_count = int(result[0])
	neg_word_count = int(result[1])
	pos_prior = float(result[2])
	neg_prior = float(result[3])

def test_sentance(input_sentence):
	jieba.load_userdict('user_dic.dic')
	word_list = jieba.cut(input_sentence.strip())
	#print ','.join(word_list).encode('utf-8')
	pos_result = math.log(pos_prior)
	neg_result = math.log(neg_prior)
	temp_list = []
	for word in word_list:
		word = word.strip()
		if len(word) > 0:
			temp_list.append(word)
			if word in pos_sentiment_dic:
				pos_result += math.log(pos_sentiment_dic[word])
			else:
				pos_result += math.log(float(1)/pos_word_count)
			if word in neg_sentiment_dic:
				neg_result += math.log(neg_sentiment_dic[word])
			else:
				neg_result += math.log(float(1)/neg_word_count)
	#print ','.join(temp_list).encode('utf-8')
	return {'pos':pos_result,'neg':neg_result}


if __name__ == '__main__':
	#print ','.join(get_article_list('2015-05-05','2015-05-06','709'))
	load_training_data(-1)
	#result = test_sentance('她是誰 他承認關我屁事 幹她娘的')
	result = test_sentance('民進黨的政治學者，想去大陸出賣台灣，結果被拒絕了，悲哀~')
	if result['pos'] > result['neg']:
		print 'positive'
	elif result['neg'] > result['pos']:
		print 'negative'
	else:
		print 'neutral'
	result = test_sentance('這個消息我聽說了!!很正確!!')
	if result['pos'] > result['neg']:
		print 'positive'
	elif result['neg'] > result['pos']:
		print 'negative'
	else:
		print 'neutral'
