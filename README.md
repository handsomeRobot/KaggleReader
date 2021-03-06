# KaggleReader
Feed in Kaggle competition url, output normalized train file and test file.   <br />

The basci usage is to call the below commands:   <br />
$ python kaggleReader.py URL(REPLACE THIS WITH THE ACTUAL URL POINTINTG TO A COMPETITION WEBPAGE) KAGGLE-USERNAME(REPLACE THIS WITH YOUR KAGGLE ACCOUNT USERNAME) KAGGLE-PASSWORD(REPLACE THIS WITH YOUR KAGGLE ACCOUNT PASSWORD)   <br />
for example:   <br />
$ python kaggleReader.py https://www.kaggle.com/c/titanic myKaggleUsername myKagglePassword   <br />

KaggleReader.py browses the competition url, login in, agree the competition rules, parse the descriptions, download the competition data, unzip and format-convert the downloaded data, merge the datasheets, findout the label column and align the colums so that the final output files share the same columns. There are two final output files, the parse_train.csv file and parse_test.csv file.  
The output files have the formats like below:   <br />

label, NA, Feature1, Feature2, Feature3...  <br />
....., NA, ........, ........, ...........   <br />

There are two options attached to the command.   <br />
(a) -f --file   <br />
    This flag nominates the path to be created for stroing the downloaded and parsed data. By default, KaggleReader.py creates a folder named 'KaggleData' under the current directory. An example to use this flag:   <br />
    $ python kaggleReader.py -f './data' https://www.kaggle.com/c/titanic myKaggleUsername myKagglePassword   <br />
(b) -c --clear   <br />
    This flag declears whether or not clear the original downloaded files after being parsed. Possible values are 'Y' for clearing and 'N' for not clearing. By default, KaggleReader.py keeps these files after run. An example to use this flag:   <br />
    $ python kaggleReader.py -c 'Y' https://www.kaggle.com/c/titanic myKaggleUsername myKagglePassword   

Running environments:  <br />
Python 2.7.12 + Ubuntu 16.04 LTS + latest Firefox (with geckodriver executable)  

Config: <br />
KaggleReader.py imports several external packages. Please run config.sh first to make sure having these packages ready. 
