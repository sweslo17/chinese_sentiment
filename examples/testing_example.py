#coding=utf-8
import sys
sys.path.append('../src')
import testing

testing.load_training_data('../model/','../dict/user_dic.dic')
result = testing.test_sentance('沒做功課就來討罵')
if result['pos'] > result['neg']:
	print 'positive'
elif result['neg'] > result['pos']:
	print 'negative'
else:
	print 'neutral'
result = testing.test_sentance('這個消息我聽說了!!很正確!!')
if result['pos'] > result['neg']:
	print 'positive'
elif result['neg'] > result['pos']:
	print 'negative'
else:
	print 'neutral'
