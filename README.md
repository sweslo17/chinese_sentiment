# chinese_sentiment
----------------------

中文情緒分析 

* 使用jieba斷詞
* 使用Naive Bayes分類器(目前)
* 支援正負情緒分類
* 支援使用者自訂字典

# 安裝說明
-----------------------
```
git clone https://github.com/sweslo17/chinese_sentiment.git
pip install -r requirements.txt
```

# 使用說明
----------------------
* Training
	* 將正/負訓練資料放置`data`資料夾下
	* 
	```
		cd examples
		python training_example.py
	```
* Testing
	* 
	```
		cd examples
		python testing_example.py
	```
	* 回傳結果為`{'pos':value,'neg':value}`之結構
