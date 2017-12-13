Function:
    Input a Kaggle competition url, output 'parse_train.csv' and 'parse_test.csv' while these two files share the same column names.
    A new folder 'kaggleData' is created in the current working directory and has all the data in it.
    
    

    
Output format:
    label, NA, Feature1, Feature2, Feature2...
    ....., NA, ........, ........, ...........




Usage:
    type the below command:
        $ python kaggleReader.py -f "FOLDER FOR STORING DATA (DEFAULT './kaggleData')" -c 'WHETHER DELETE THE ORIGINAL DOWNLOADED DATA OR NOT, COULD BE 'Y' OR 'N', (DEFAULT 'N')" "COMPETITION URL"
    for example:
        $ python kaggleReader.py -f './data' -c 'Y' https://www.kaggle.com/c/predicting-red-hat-business-value
        
        
        

Platforms:
    Python 2.7.12 + Ubuntu 16.04 LTS + latest Firefox (with geckodriver)



[issue]
delete duplicated columns or not
    
    
