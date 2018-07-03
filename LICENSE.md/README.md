# twitterAndStock
During a project at HTW Berlin my team Kristina Spiegel and Alexander Röll created a projekt to see if tweets could impact the stock market. 
Have tweets impacted the share price of a company?

USWS HTW Berlin SoSe 2018 
Group:  Kristina Spiegel, s0553423@htw-berlin.de
	      Alexander Röll, s0554705@htw-berlin.de
	      Kalina Sperber, s0554634@htw-berlin.de 


-------- All files are in Folder "scripts"------
How to
    run a python script add the path for python: /home/sperber/anaconda3/bin/python3

SetUp
    Create Database and Basic Data (e.g. Sectors & Companies) with "create.py" and "fill.py"

---------Historical Analysis--------------------

Get Historical Daily Data 
    Stock Data:  /home/sperber/anaconda3/bin/python3 getHistStock.py HOG


---------Automatize Scripts  --------------------
1. In DB Table with followed people "people"
2. Crontab sync new tweets every....
with Script ...
3. if a company is found the minutely  based syncing of Brand and refering Sector Data  based on Stocksymbol is started
    	getSectorData.py
    	getStockData.py
	
