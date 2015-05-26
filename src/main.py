import training
import test_fb
import datetime
import sys

if __name__ == '__main__':
	date_from = datetime.date.today()-datetime.timedelta(days=7)
	date_to = datetime.date.today()
	keyword_id = -1
	print str(date_from) + ',' + str(date_to)
	if len(sys.argv) > 1 and sys.argv[1] == 'training':
		print 'training'
		training.training(keyword_id,date_from,date_to)
	print 'testing fb'
	test_fb.run(keyword_id,date_to-datetime.timedelta(days=1))
