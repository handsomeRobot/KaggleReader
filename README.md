# KaggleReader
Feed in Kaggle competition url, output normalized train file and test file.  

The basci usage is to call the below commands:  
$ python kaggleReader.py URL(REPLACE THIS WITH THE ACTUAL URL POINTINTG TO A COMPETITION WEBPAGE) KAGGLE-USERNAME(REPLACE THIS WITH YOUR KAGGLE ACCOUNT USERNAME) KAGGLE-PASSWORD(REPLACE THIS WITH YOUR KAGGLE ACCOUNT PASSWORD)  
for example:  
$ python kaggleReader.py https://www.kaggle.com/c/titanic myKaggleUsername my KagglePassword  

KaggleReader.py browses the competition url, login in, agree the competition rules, parse the descriptions, download the competition data, unzip and format-convert the downloaded data, merge the datasheets, findout the label column and align the colums so that the final output files share the same columns. There are two final output files, the parse_train.csv file and parse_test.csv file.  
The output files have the formats like below:  

label, NA, Feature1, Feature2, Feature3...  
....., NA, ........, ........, ...........  

There are two options attached to the command.  
(a) -f
    This flag nominates the path to be created for stroing the downloaded and parsed data. By default, KaggleReader.py creates a folder named 'KaggleData' under the current directory. A example to use this flag:  
    $ python kaggleReader.py -f './data' https://www.kaggle.com/c/titanic myKaggleUsername my KagglePassword  
(b) -c

