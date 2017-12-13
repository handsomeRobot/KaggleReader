
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from sys import argv
from optparse import OptionParser

def agree_terms(url):
    username, password = payload['UserName'], payload['Password']
    fail_count = 0
    while fail_count < 5:
        try:
            driver = webdriver.Firefox()
            driver.set_window_size(1000, 1000)
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='button button--small']/span")))
            element.click()
            element = wait.until(EC.presence_of_element_located((By.ID, "username-input-text")))
            element.send_keys(username)
            element = wait.until(EC.presence_of_element_located((By.ID, "password-input-text")))
            element.send_keys(password)
            element = wait.until(EC.presence_of_element_located((By.ID, "submit-sign-in-button")))
            element.click()
            try:
                element = driver.find_elements_by_class_name("competition-rules__accepted-text")
                if len(element) > 0:
                    driver.quit()
                    return
            except Exception as e:
                continue
            time.sleep(3)
            try:
                element = driver.find_elements_by_id("PhoneNumber")
                if len(element) > 0:
                    driver.quit()
                    return
            except Exception as e:
                continue
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='competition-rules__acceptance-actions']//a[@class='button-auto-width competition-rules__accept']")))
            element.click() 
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "competition-rules__accepted-text")))
            #print 'Agreed rules.'
            driver.quit()
            driver.quit()
        except Exception as e:
            print e
            fail_count += 1
            driver.quit()


#convert .tsv file into .csv file
def convert(f):
    if os.path.splitext(f)[1] == '.tsv':
        csv.writer(open(os.path.splitext(f)[0] + '.csv', 'w+')).writerows(csv.reader(open(f), delimiter="\t"))
        os.remove(f)
        return os.path.splitext(f)[0] + '.csv'
    else:
        return f


#to validate the column names
def isAllNum(ls):
    try:
        map(lambda x: float(x), ls)
    except ValueError:
        return False
    return True


import pandas as pd
def cstm_concat(df1, df2):
    df1_var = list(df1.columns.values)
    df2_var = list(df2.columns.values)
    id_var = [var for var in df1_var if var in df2_var]
    for var in id_var:
        intersect = [row for row in list(df1[var]) if row in list(df2[var])]
        if len(intersect) == 0:
            id_var.remove(var)
    if len(id_var) > 0:
        df = pd.merge(df1, df2, on = id_var, how = 'outer')
        return df
    df = pd.concat([df1, df2], axis = 1, join = 'outer')
    return df




#initialize
parser = OptionParser()
parser.add_option("-f", "--folder", dest = "wkdir", default = './kaggleData', help = "create folder for parse result, default is './kaggleData'")
parser.add_option("-c", "--clear", dest = "clear", default = 'N', help = "whether delete original downloaded data or not, choices are 'Y' or 'N', default is 'N'")
(options, args) = parser.parse_args()
wkdir = options.wkdir
clear = options.clear
#script, url = argv
base_url = str(args[0])
username = str(args[1])
password = str(args[2])
cmp_file = ['.zip', '.gz', '.7z']
print 'Competition address: ', base_url
print 'Logging...'
payload = {'UserName': username, 'Password': password}
disturbs = ['the', 'a', 'on', 'should', 'of', 'in', 'is', 'to', 'it', 'id']
rule_url = base_url + '/rules'
agree_terms(rule_url)
data_url = base_url + '/data'
r = requests.get(data_url)
r = requests.post(r.url, data = payload, headers={'Connection':'close'})
htmlpage = r.text
print 'Login success. Terms aggreed.'


#download the files
if not os.path.exists(wkdir):
    os.mkdir(wkdir)
os.chdir(wkdir)
print 'Downloading data...'
info = re.findall(r"\"files\":\[(.*?)\]", htmlpage)[0] #file-chuck
files = re.findall(r"\"name\":\"(.*?)\",", info)
for file in files:
    if os.path.splitext(file)[1] in cmp_file:
        if os.path.splitext(file)[0] in files:
            files.remove(file)
for n, file in enumerate(files):
    print str(n + 1) + '/' + str(len(files))
    file_url = base_url + '/download/' + file
    r = requests.get(file_url)
    r = requests.post(r.url, data = payload)
    f = open(file, 'w')
    for chunk in r.iter_content(chunk_size = 512 * 1024): # Reads 512KB at a time into memory
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()
print 'Download success.'
print 'Unzipping data...'
for file in [file for file in files if os.path.splitext(file)[1] in cmp_file]:
    try:
        os.system('dtrx ' + file)
        os.remove(file)
    except OSError:
        pass
#Extract files from folders
print 'Moving data...'
files = [file for file in os.listdir('.') if os.path.isdir(file)]
for file in files:
    try:
        os.system('mv ' + file + ' DELETETHIS')
        os.system('cp ' + 'DELETETHIS/* ' + './')
        os.system('rm -r ' + 'DELETETHIS')
    except Exception as e:
        print e
#convert tsv to csv
files = os.listdir('.')
files = map(lambda x: convert(x), files)


#locate the test file and train file and (if there is) train_label_file
files = [file for file in os.listdir('.') if os.path.splitext(file)[1] == '.csv']
print '>>>Files: ', files
train_files = [file for file in files if 'train' in file.lower() and 'unlabeled' not in file.lower()]
test_files = [file for file in files if 'test' in file.lower()]
submission_files = [file for file in files if 'submission' in file.lower()]
supply_files = [file for file in files if file not in test_files and file not in submission_files and file not in train_files and os.path.splitext(file)[1] != '.log' and os.path.splitext(file)[1] != '' and os.path.splitext(file)[1] != '.ipynb' and os.path.splitext(file)[1] != '.py' and 'description'.lower()not in file.lower() and 'check' not in file.lower() and 'dictionary' not in file.lower() and 'unlabeledtrain' not in file.lower() and 'documentation' not in file.lower()]
print '>>>Train Files: ', train_files
print '>>>Test Files: ', test_files
print '>>>Submission Files: ', submission_files
print '>>>Supply Files: ', supply_files


#retrieve the target variables
target_lines = [line for line in htmlpage.split('.') if ('target' in line.lower()or 'predict' in line.lower() or 'prediction' in line.lower() or 'classify' in line.lower() or 'classified' in line.lower()
                                                        or 'forcast' in line.lower() or 'expect' in line.lower() or 'label' in line.lower()) and '=' not in line]
target_lines = map(lambda x: x.split(), target_lines)
target_words = [word for line in target_lines for word in line if word.lower() not in disturbs]
target_words = map(lambda x: x.replace('*', ''), target_words)
target_words2 = []
for w in target_words:
    inner = re.findall(r"\u.{4}(\w*)\\", w) + re.findall(r"\u.{4}(\w*)\W", w)
    if len(inner) > 0:
        target_words2 += inner
    elif len(inner) == 0:
        target_words2.append(w.replace('`','').replace('`',''))
target_words = {}
for w in target_words2:
    if w in target_words.keys():
        target_words[w] += 1
    else:
        target_words[w] = 1
#extract the column names in the test file and train file and train_label_file, respectively
train_var = []
for file in train_files:
    with open(file) as f:
        train_var += f.readline().strip().split(',')
train_var = list(set(map(lambda x: x.replace('"', '').strip(), train_var)))
test_var = []
for file in test_files:
    with open(file) as f:
        test_var += f.readline().strip().split(',')
test_var = list(set(map(lambda x: x.replace('"', '').strip(), test_var)))
supply_var = []
for file in supply_files:
    with open(file) as f:
        supply_var += f.readline().strip().split(',')
#print 'FOR DEBUG, target_words: ', target_words
#findout the target_variables
if not isAllNum(train_var):
    target_var = []
    for var in [var for var in train_var if var not in test_var]:
        for w in target_words.keys():
            if w == '':
                continue
            if w.lower() in map(lambda x: x.lower(), re.findall(r"_([A-Za-z]+)", var) + re.findall(r"([A-Za-z]+)_", var) + re.findall(r"[a-z]*([A-Z][a-z]*)", var) + [var]):
                target_var.append(var)
                break
    target_var = map(lambda x: x.replace('"', ''), target_var)
    target = target_var[0]
    var_cnt = []
    target_cnt = []
    for w in [w for w in target_words.keys() if w.lower() in target.lower()]:
        target_cnt.append(target_words[w])
    for var in target_var:
        for w in [w for w in target_words.keys() if w.lower() in var.lower()]:
            var_cnt.append(target_words[w])
        if max(var_cnt) < max(target_cnt):
            continue
        else:
            target = var
            for w in [w for w in target_words.keys() if w.lower() in target.lower()]:
                target_cnt.append(target_words[w])
    print '>>>Target variable: ', target
    target_var = [target]



#merge train_data and test_data, respectively
print 'Processing data...'
outfile_train = open('parse_train.csv', 'w')
outfile_test = open('parse_test.csv', 'w')
if not isAllNum(train_var): #if there are column names
    for n, file in enumerate(train_files):
        if n == 0:
            train_data = pd.read_csv(file)
        elif n > 0:
            data = pd.read_csv(file)
            if list(set(list(data.columns.values))) == list(set(list(train_data.columns.values))):
                train_data = pd.concat([train_data, data], join = 'outer')
            else:
                train_data = cstm_concat(train_data, data)
    for n, file in enumerate(test_files):
        if n == 0:
            test_data = pd.read_csv(file)
        elif n > 0:
            data = pd.read_csv(file)
            if list(set(list(data.columns.values))) == list(set(list(test_data.columns.values))):
                test_data = pd.concat([test_data, data], join = 'outer')
            else:
                test_data = cstm_concat(test_data, data)
    for n, file in enumerate(supply_files):
        data = pd.read_csv(file)
        train_data = cstm_concat(train_data, data)
        test_data = cstm_concat(test_data, data)
    train_data = train_data[target_var + [var for var in train_data if var not in target_var]]
    try:
        test_data = test_data[target_var + [var for var in train_data if var not in target_var]]
        test_data.insert(len(target_var), column = 'NA', value = [None]*test_data.shape[0])
        train_data.insert(len(target_var), column = 'NA', value = [None]*train_data.shape[0])
    except KeyError as e:
        emp_cols = re.findall(r"\[(.*)\] not in index", e.message.replace("'\n", "'"))[0].split()
        emp_cols = map(lambda x: x.strip(), emp_cols)
        emp_cols = map(lambda x: x.replace("'", ''), emp_cols)
        for col in emp_cols:
            test_data[col] = [None] * test_data.shape[0]
        blank_col = [None]*train_data.shape[0]
        test_data = test_data[target_var + [var for var in train_data if var not in target_var]]
        test_data.insert(len(target_var), column = 'NA', value = [None]*test_data.shape[0])
        train_data.insert(len(target_var), column = 'NA', value = [None]*train_data.shape[0])
    print '>>>parse_train.csv: ', train_data.describe(include = 'all')
    print '>>>parse_test.csv: ', test_data.describe(include = 'all')
    print 'Saving data into files...'
    train_data.to_csv(outfile_train, index = False)
    test_data.to_csv(outfile_test, index = False)
    if clear == 'Y':
        print 'Deleting original downloaded files...'
        for file in files:
            os.remove(file)

    

elif isAllNum(train_var): #if there are not column names:
    print 'Processing data...'
    if len(train_files) == 2 and ('label' in train_files[0].lower() or 'label' in train_files[1].lower()) and len(test_files) == 1 and len(supply_files) == 0:
        train_data = pd.read_csv([file for file in train_files if 'label' not in file.lower()][0], header = None)
        label_data = pd.read_csv([file for file in train_files if 'label' in file.lower()][0], header = None)
        label_data['NA'] = ''
        train_data = pd.concat([label_data, train_data], axis = 1)
        train_data.columns = list(range(len(train_data.columns)))
        test_data = pd.read_csv(test_files[0], header = None)
        test_data = pd.concat([label_data, test_data], axis = 1)
        test_data.columns = list(range(len(test_data.columns)))
        test_data[0] = ''
        print '>>>parse_train.csv: ', train_data.describe(include = 'all')
        print '>>>parse_test.csv: ', test_data.describe(include = 'all')
        print 'Saving data into files...'
        train_data.to_csv(outfile_train, index = False)
        test_data.to_csv(outfile_test, index = False)
        if clear == 'Y':
            print 'Deleting original downloaded files...'
            for file in files:
                os.remove(file)
        
        
outfile_train.close()
outfile_test.close()
