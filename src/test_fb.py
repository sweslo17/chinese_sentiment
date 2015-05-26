#coding=utf-8
import testing
import mysql.connector
import config
import subprocess
import datetime
import json

def run(keyword_id,date):
	#date = date - datetime.timedelta(days=1)
	testing.load_training_data(keyword_id)
	cnx = mysql.connector.connect(host=config.db_host,user=config.db_user,passwd=config.db_password,database=config.db_database,charset='utf8')
	cur = cnx.cursor()
	cur.execute('SELECT DISTINCT(id) FROM fb_data WHERE load_time=%s',(date,))

#data = json.loads(subprocess.check_output(["php", "adaptor.php",config.db_host,config.db_user,config.db_password,config.db_database,"SELECT id FROM fb_data WHERE load_time='"+str(date)+"' AND term_id='"+str(keyword_id)+"'"]))
	results = cur.fetchall()

	page_id_list = []
	for result in results:
		page_id_list.append(result[0])
	id_list_str = "'" + "','".join(page_id_list) + "'"

	sql = "SELECT * FROM facebook_pages_comments_%d_%02d" % (date.year,date.month)

	sql += " WHERE post_id IN ("+id_list_str+")"
	#print sql

	result = json.loads(subprocess.check_output(["php", "adaptor.php",'172.16.78.153','fb','fb123!','facebook',sql]))

	for data in result:
		test_result = testing.test_sentance(data['message'])
		cur.execute('REPLACE INTO fb_comments_sentiment (id,from_id,from_name,message,created_time,likes,comments,page_id,post_id,post_created_time,updatetime,app_id,sentiment_positive,sentiment_negative) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(data['id'],data['from_id'],data['from_name'],data['message'],data['created_time'],data['likes'],data['comments'],data['page_id'],data['post_id'],data['post_created_time'],data['updatetime'],data['app_id'],test_result['pos'],test_result['neg']))
	cnx.commit()

