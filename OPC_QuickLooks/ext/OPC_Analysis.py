import numpy as np
import pandas as pd
from datetime import datetime
import xlrd

import time

data0_5 = pd.read_csv(r"C:\Users\makom\OneDrive\Desktop\Madras_2021\OPC-N3\madras_2021_0_5m_911_0.csv",skiprows=13)
#data1_5 = pd.read_csv(r"C:\Users\makom\OneDrive\Desktop\Madras_2021\OPC-N3\madras_2021_1_5m_903_0.csv",skiprows=13)
#data3 = pd.read_csv(r"C:\Users\makom\OneDrive\Desktop\Madras_2021\OPC-N3\madras_2021_03m_902_0.csv",skiprows=13)
#data5 = pd.read_csv(r"C:\Users\makom\OneDrive\Desktop\Madras_2021\OPC-N3\madras_2021_05m_901_0.csv",skiprows=13)
#data10 = pd.read_csv(r"C:\Users\makom\OneDrive\Desktop\Madras_2021\OPC-N3\madras_2021_10m_906_0.csv",skiprows=13)

print(data0_5)
#print(data0_5.iloc[0])
#print(data0_5.iloc[0][1])

excel_date = data0_5["OADateTime"][0]

python_date = datetime(*xlrd.xldate_as_tuple(excel_date, 0))
print(str(python_date))
print(type(python_date))

t1 = time.time()

data_sec = []

for i in range(len(data0_5["OADateTime"])):

    excel_date = data0_5["OADateTime"][i]
    excel_date = datetime(*xlrd.xldate_as_tuple(excel_date, 0))
    excel_date = str(excel_date)
    #print(excel_date)
    ed = excel_date[17:]
    data_sec.append(ed)
    #print(ed)
t2 = time.time()
print(t2-t1)

data_1min = []

t1 = time.time()
for i in range(1,len(data_sec)):
    min = []
    if data_sec[i-1] < data_sec[1]:
        min.append(data0_5.iloc[i])
    data_1min.append(min)

print(np.shape(data_1min))

t2 = time.time()
print(t2-t1)