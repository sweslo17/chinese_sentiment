#coding=utf-8
import sys
sys.path.append('../src')
import testing

testing.load_training_data('../model/')
result = testing.test_sentance('民進黨的政治學者，想去大陸出賣台灣，結果被拒絕了，悲哀~')
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
