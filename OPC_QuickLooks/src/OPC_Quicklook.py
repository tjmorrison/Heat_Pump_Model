

'''----------------------------------- IMPORT PACKAGES ----------------------------------------------------'''
import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['text.usetex'] = True
'''----------------------------------- PATHS ----------------------------------------------------'''
Figure_Name = "SWOPC_IOP1_08_04_2021"
Data_file = "SWOPC_08_03_2021_1716UTC.csv"
Data_path = "C:/Users/tjmor/OneDrive/Research/Projects/Oregon_Carrot/Data/IOP1/SWOPC/"
'''----------------------------------- Load Data ----------------------------------------------------'''
df = pd.read_csv(Data_path + Data_file,skiprows=13)
'''----------------------------------- Convert Excel Time ----------------------------------------------------'''

def read_date(date):
    return xlrd.xldate.xldate_as_datetime(date, 0)

df['Time'] = pd.to_datetime(df['OADateTime'].apply(read_date), errors='coerce')
df = df.set_index('Time')
df_subtime = df.loc['2020-08-03T23:30:00.00':'2021-08-04T00:10:00.00']
'''----------------------------------- Take average of data ----------------------------------------------------'''
df_1min = df.resample(rule = '1Min').mean() #Note that rolling values look the same~ so we will use these for now
df_subtime = df_1min.loc['2020-08-03 23:30:00':'2021-08-04 00:10:00']
print(df_1min.index[-1]) #Print last time so we can name the figure
'''----------------------------------------------PLOT SETTINGS ------------------------------------------------------'''
plt.style.use('seaborn-colorblind') # Color Scheme for plots
plt.rcParams["font.family"] = "Times New Roman" # Font style
plt.rcParams.update({'font.size': 16}) #Set font size
'''---------------------------------------------- FIGURE 1 ------------------------------------------------------'''
#Figure 1 ~ PM1, PM2.5, and PM10
fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(15, 10))

ax1.plot(df.index, df['RollMean_PM1'])
ax1.set(ylabel = r'PM1 [$\mu$g/m$^3$]')
ax1.grid(b=bool, which='major', axis='both')
ax1.autoscale(enable=True, axis='x', tight=True)

ax2.plot(df.index, df['RollMean_PM2.5'])
ax2.set(ylabel = r'PM2.5 [$\mu$g/m$^3$]')
ax2.grid(b=bool, which='major', axis='both')
ax2.autoscale(enable=True, axis='x', tight=True)

ax3.plot(df.index, df['RollMean_PM10'])
ax3.set(ylabel = r'PM10 [$\mu$g/m$^3$]')
ax3.grid(b=bool, which='major', axis='both')
ax3.autoscale(enable=True, axis='x', tight=True)
#plt.ylim(0, 200)

plt.minorticks_on()
#save figure
plt.savefig('../gen/' + Figure_Name +'.png', bbox_inches='tight')