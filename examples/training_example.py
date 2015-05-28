import sys
sys.path.append('../src')
from training import training
training('../data/positive.txt','../data/negative.txt','../model/','../dict/user_dic.dic')
