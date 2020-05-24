# Import related lib
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#***************************Importing Data and cleaning the raw data********************************************
# Import sensor data and set date as index
sensor = pd.read_csv('D:/Mitsubishi-MERCE-UK/Data/sensor_data.csv',
                     index_col="Date", parse_dates=True)
sensor.head()
# pivot table to look at data
pd.pivot_table(sensor, index=["Sensor", "Date"])
sensor.head()
# Change the numbering of sensor as per the layout
sensor['Sensor'].replace({"a200000014": "1", 
                            "a200000016": "2",
                            "a200000017": "3", 
                            "a200000018": "4", 
                            "a200000019": "5", 
                            "a200000024": "6", 
                            "a300000007": "7",
                            "a300000004": "8",
                            "b100000004": "9",
                            "a200000015": "10",
                            "b100000003": "11",
                            "a200000020": "12",
                            "a300000006": "13",
                            "a200000021": "14",
                            "a200000023": "15",
                            "a300000008": "16",
                            "a200000022": "17",
                            "a200000025": "18",
                            "a300000005": "19", }, inplace=True)
sensor.head()
sensor_new = sensor.sort_values(by=['Sensor', 'Date'])
sensor_new.head()
#**********************Data visualisation*************************************************
#Plot bar graph with temperature vs sensor
plt.rcParams["font.family"] = "Times New Roman"
fig, ax = plt.subplots()
fig.set_size_inches(10, 6)
a = sns.boxplot(x="Sensor", y="temperature", data=sensor_new, order=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'])
a.set_xlabel("Sensor Label",fontsize=15)
a.set_ylabel("Air temperature($^\circ$C)",fontsize=15)
a.tick_params(labelsize=15)
plt.show()

#*****************************************Visualisation of temperature and humidity - mean and standard deviation*********************************
#Seperate Time and date
sensor_new['Time'] = sensor_new.index.map(lambda t: t.time())
sensor_new['Date'] = sensor_new.index.map(lambda t: t.date())
sensor_new.head()

#Make a copy of data with temperature and humidity
sensor_temp_humid = sensor_new[['Sensor', 'temperature', 'humidity', 'Time', 'Date']].copy()
sensor_temp_humid.head()
#resample hourly by mean temp
sensor_temp_humid_hourly = sensor_temp_humid.resample('H').mean()
sensor_temp_humid_hourly.info()
#resample hourly by std
sensor_temp_humid_std = sensor_temp_humid.resample('H').std()
sensor_temp_humid_std.head()

#import weather data
weather = pd.read_excel('D:/Mitsubishi-MERCE-UK/Data/weather.xlsx', index_col ="Time_Stamp", parse_dates=True)
weather.head()
weather.sort_index()

#Select specific date
weather_sep = weather.sort_index().truncate(before = '2019-09-19 00:00:00', after= '2019-09-19 23:00:00')
weather_sep.head()
weather_sep.tail()

#Select specific date
x = sensor_temp_humid_hourly.truncate(before = '2019-09-19 00:00:00', after= '2019-09-19 23:00:00')
y = sensor_temp_humid_std.truncate(before = '2019-09-19 00:00:00', after= '2019-09-19 23:00:00')

#Adding Std of temperature to the mean values
x['temp_pos_std'] = x['temperature'] + y['temperature']
x.head()
x['temp_neg_std'] = x['temperature'] - y['temperature']
x.head()
#Roundin the values
x_r = x.round(2)
x_r.head()

#Seperate Time and date
x_r['Time'] = x_r.index.map(lambda t: t.time().strftime('%H:%M'))
x_r['Date'] = x_r.index.map(lambda t: t.date())
x_r.head()
x_r.tail()

x_r.info()

#Testing fill through with one axis
import datetime

plt.figure(figsize=(20,10))
plt.plot(x_r['Time'], x_r['temperature'], label='Average Indoor temperature')
plt.plot(x_r['Time'], x_r['temp_pos_std'], linewidth=0.01)
plt.plot(x_r['Time'], x_r['temp_neg_std'], linewidth=0.01)
plt.fill_between(x_r['Time'], x_r['temp_pos_std'], x_r['temp_neg_std'], alpha=0.25)
plt.legend(fontsize=20)
plt.xlabel('Time (hours)', fontsize =20)
plt.ylabel('Air temperature($^\circ$C)', fontsize =20)
plt.xticks(rotation=90)
plt.tick_params(labelsize=20)
plt.rcParams.update({'font.size': 20})
plt.show()

#Adding std to the values and rounding values
x_r['humid_pos_std'] = x_r['humidity'] + y['humidity']
x_r.head()
x_r['humid_neg_std'] = x_r['humidity'] - y['humidity']
x_r.head()
x_r = x_r.round(2)
x_r.head()

#Plot Two y-axis
fig, ax1 = plt.subplots(figsize=(20,10))
plt.xticks(rotation=90)

ax2 = ax1.twinx()
ax1.plot(x_r['Time'], x_r['temperature'], 'b-o', label='Average Indoor temperature')
ax1.plot(x_r['Time'], x_r['temp_pos_std'], linewidth=0.01)
ax1.plot(x_r['Time'], x_r['temp_neg_std'], linewidth=0.01)
ax1.plot(x_r['Time'], weather_sep['Temp'], 'g-o',label='Outdoor temperature')
ax1.fill_between(x_r['Time'], x_r['temp_pos_std'], x_r['temp_neg_std'], alpha=0.25)

ax2.plot(x_r['Time'], x_r['humidity'], 'r-o', label='Average Relative humidity')
ax2.plot(x_r['Time'], x_r['humid_pos_std'], linewidth=0.01)
ax2.plot(x_r['Time'], x_r['humid_neg_std'], linewidth=0.01)
ax2.plot(x_r['Time'], weather_sep['RH'], 'm-o', label='Outdoor Relative humidity')
ax2.fill_between(x_r['Time'], x_r['humid_pos_std'], x_r['humid_neg_std'], color ='red', alpha=0.25)

ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('Air temperature($^\circ$C)', color='b')
ax2.set_ylabel('Relative humidity(%)', color='r')

ax1.legend(fontsize=20,loc=0)
ax2.legend(fontsize=20,loc='upper center')
plt.show()
#***************************************************Ignore Below section**************************************************
#Calculating pmv and ppd for the office
# sensor_new.head()
# sensor_pmv = sensor_temp_humid_hourly[['temperature', 'humidity']].copy()
# #Replacing the empty values with NAN
# sensor_pmv['temperature'].replace('', np.nan, inplace=True)
# sensor_pmv['humidity'].replace('', np.nan, inplace=True)
# sensor_pmv.tail()
# #Droping NAN columns
# sensor_pmv.dropna(inplace = True)
# sensor_pmv.info()
# #Adding air velocity, met and clo values
# sensor_pmv['vr'] = 0.1
# sensor_pmv['met'] = 1.0
# sensor_pmv['clo'] = 0.8
# sensor_pmv.describe()

# sensor_pmv.isnull()
# print(sensor_pmv['temperature']<10)

# import pythermalcomfort
# from pythermalcomfort.models import pmv_ppd

# sensor_pmv['pmv'] = None
# sensor_pmv['ppd'] = None

# for index, row in sensor_pmv.iterrows():
#     results = pmv_ppd(tdb=sensor_pmv['temperature'], tr=sensor_pmv['temperature'], vr=sensor_pmv['vr'], rh=sensor_pmv['humidity'], met=sensor_pmv['met'], clo=sensor_pmv['clo'], standard="ASHRAE")
#     sensor_pmv.loc[index, 'pmv'] = results['pmv']
#     sensor_pmv.loc[index, 'ppd'] = results['ppd']
# print(sensor_pmv)
#***************************************************Ignore above Section**************************************************

#*********************************************Visualisation of IAQ data***************************************************
#Plotting CO2, PM2.5 and TVOC
sensor_new.head()
sensor_new1 = sensor_new[['Sensor', 'co2']].copy()
sensor_new1.head()
sensor_new1.reset_index(inplace = True)
sensor_new1.head()
sensor_new2 = sensor_new1.set_index('Sensor')
sensor_new2.head()
sensor_new2 = sensor_new2.truncate(before='8', after = '8')
sensor_new2.head()

sensor_new2 = sensor_new2.set_index('Date')
sensor_new2.head()

sensor_new2 = sensor_new2.asfreq('30 min')
sensor_new2.head()

sensor_new3 = sensor_new2.truncate( before = '2019-08-16 00:00:00', after ='2019-08-16 23:00:00')
sensor_new3

#PM 2.5 and TVOC
sensor_new.head()
sensor_pm = sensor_new[['Sensor', 'pm', 'tvoc']].copy()
sensor_pm.head()
sensor_pm.reset_index(inplace = True)
sensor_pm.head()
sensor_pm1 = sensor_pm.set_index('Sensor')
sensor_pm1.head()
sensor_pm2 = sensor_pm1.truncate(before='9', after = '9')
sensor_pm2.head()
sensor_pm2 = sensor_pm2.set_index('Date')
sensor_pm2.head()

sensor_pm2 = sensor_pm2.asfreq('30 min')
sensor_pm2.head()

sensor_pm3 = sensor_pm2.truncate( before = '2019-08-16 00:00:00', after ='2019-08-16 23:00:00')
sensor_pm3

#Combine Co2, pm2.5 and tvoc

sensor_new3['pm'] = sensor_pm3['pm']
sensor_new3['tvoc'] = sensor_pm3['tvoc']
sensor_new3
#Seperate Time and date
sensor_new3['Time'] = sensor_new3.index.map(lambda t: t.time().strftime('%H:%M'))
sensor_new3['Date'] = sensor_new3.index.map(lambda t: t.date())
sensor_new3.head()


#Plotting graph for IAQ

#Plot Two y-axis
fig, ax1 = plt.subplots(figsize=(20,10))
plt.xticks(rotation=90)

ax2 = ax1.twinx()
ax1.plot(sensor_new3['Time'], sensor_new3['co2'], 'b-o', label='CO2 level')

ax2.plot(sensor_new3['Time'], sensor_new3['tvoc'], 'r-o', label='TVOC level')

ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('CO2 (ppm)', color='b')
ax2.set_ylabel('TVOC (ppm)', color='r')

ax1.legend(fontsize=20,loc=0)
ax2.legend(fontsize=20,loc='upper left')
plt.show()

#Plotting co2 levels in full office
sensor_new4 = sensor_new1.set_index('Sensor')
sensor_new4.head()
sensor_7 = sensor_new4.loc['7']
sensor_8 = sensor_new4.loc['8']
sensor_13 = sensor_new4.loc['13']
sensor_16 = sensor_new4.loc['16']
sensor_19 = sensor_new4.loc['19']
sensor_co2_level = pd.concat([sensor_7, sensor_8, sensor_13, sensor_16, sensor_19])
sensor_co2_level
sensor_co2_level.reset_index(inplace = True)
sensor_co2_level


plt.rcParams["font.family"] = "Times New Roman"
fig, ax = plt.subplots()
fig.set_size_inches(10, 6)
b = sns.boxplot(x="Sensor", y="co2", data=sensor_co2_level, order=[ '7', '8', '13', '16', '19'])
b.set_xlabel("Sensor Label",fontsize=15)
b.set_ylabel("CO2 (ppm)",fontsize=15)
b.tick_params(labelsize=15)
plt.show()

#*******************CALCULATING MIN MEAN AND MAX*****************

#Taking the variable which has the initial data
sensor_new.head()
#Setting index as Sensor so that its easy to extract sensors using their numbers
sensor_split = sensor
sensor_split.reset_index(inplace = True)
sensor_split.head()

sensor_split = sensor_split.set_index('Sensor')
sensor_split

office_room_1_sensor = sensor_split.loc[['1', '2', '3', '4', '5', '6', '7']]
office_room_1_sensor

meeting_room_sensor = sensor_split.loc[['8','9','19']]
meeting_room_sensor

admin_office_sensor = sensor_split.loc[['10','11','12']]
admin_office_sensor

gm_office_sensor = sensor_split.loc[['13']]
gm_office_sensor

office_room_2_sensor = sensor_split.loc[['16','17','18']]
office_room_2_sensor


#Calculating min, mean and max in office room 1 sensor
office_room_1_sensor = office_room_1_sensor.set_index('Date')
office_room_1_sensor['Weekday'] = office_room_1_sensor.index.map(lambda t: t.date().weekday())
#Weekday
office_room_1_sensor_weekday = office_room_1_sensor[(office_room_1_sensor.Weekday <6)]
office_room_1_sensor_weekday_wh = office_room_1_sensor_weekday.resample('BH').mean()
office_room_1_sensor_weekday_wh

#Weekday statistics of office room 1 sensor
print("office_room_1 Min temperature:", office_room_1_sensor_weekday_wh['temperature'].min())
print("office_room_1 Max temperature:", office_room_1_sensor_weekday['temperature'].max())
print("office_room_1 Mean temperature:", office_room_1_sensor_weekday_wh['temperature'].mean())

print("office_room_1 Min humidity:", office_room_1_sensor_weekday_wh['humidity'].min())
print("office_room_1 Max humidity:", office_room_1_sensor_weekday['humidity'].max())
print("office_room_1 Mean humidity:", office_room_1_sensor_weekday_wh['humidity'].mean())

print("office_room_1 Min co2:", office_room_1_sensor_weekday_wh['co2'].min())
print("office_room_1 Max co2:", office_room_1_sensor_weekday['co2'].max())
print("office_room_1 Mean co2:", office_room_1_sensor_weekday_wh['co2'].mean())

#Weekend statistics of office room 1 sensor
office_room_1_sensor_weekend = office_room_1_sensor[(office_room_1_sensor.Weekday >5)]
office_room_1_sensor_weekend

print("office_room_1 Min temperature weekend:", office_room_1_sensor_weekend['temperature'].min())
print("office_room_1 Max temperature weekend:", office_room_1_sensor_weekend['temperature'].max())
print("office_room_1 Mean temperature weekend:", office_room_1_sensor_weekend['temperature'].mean())

print("office_room_1 Min humidity weekend:", office_room_1_sensor_weekend['humidity'].min())
print("office_room_1 Max humidity weekend:", office_room_1_sensor_weekend['humidity'].max())
print("office_room_1 Mean humidity weekend:", office_room_1_sensor_weekend['humidity'].mean())

print("office_room_1 Min co2 weekend:", office_room_1_sensor_weekend['co2'].min())
print("office_room_1 Max co2 weekend:", office_room_1_sensor_weekend['co2'].max())
print("office_room_1 Mean weekend:", office_room_1_sensor_weekend['co2'].mean())





#Calculating min, mean and max in office room 2 sensor
office_room_2_sensor = office_room_2_sensor.set_index('Date')
office_room_2_sensor['Weekday'] = office_room_2_sensor.index.map(lambda t: t.date().weekday())
#Weekday
office_room_2_sensor_weekday = office_room_2_sensor[(office_room_2_sensor.Weekday <6)]
office_room_2_sensor_weekday_wh = office_room_2_sensor_weekday.resample('BH').mean()
office_room_2_sensor_weekday_wh

#Weekday statistics of office room 2 sensor
print("office_room_2 Min temperature:", office_room_2_sensor_weekday_wh['temperature'].min())
print("office_room_2 Max temperature:", office_room_2_sensor_weekday['temperature'].max())
print("office_room_2 Mean temperature:", office_room_2_sensor_weekday_wh['temperature'].mean())

print("office_room_2 Min humidity:", office_room_2_sensor_weekday_wh['humidity'].min())
print("office_room_2 Max humidity:", office_room_2_sensor_weekday['humidity'].max())
print("office_room_2 Mean humidity:", office_room_2_sensor_weekday_wh['humidity'].mean())

print("office_room_2 Min co2:", office_room_2_sensor_weekday_wh['co2'].min())
print("office_room_2 Max co2:", office_room_2_sensor_weekday['co2'].max())
print("office_room_2 Mean co2:", office_room_2_sensor_weekday_wh['co2'].mean())

#Weekend statistics of office room 2 sensor
office_room_2_sensor_weekend = office_room_2_sensor[(office_room_2_sensor.Weekday >5)]
office_room_2_sensor_weekend

print("office_room_2 Min temperature weekend:", office_room_2_sensor_weekend['temperature'].min())
print("office_room_2 Max temperature weekend:", office_room_2_sensor_weekend['temperature'].max())
print("office_room_2 Mean temperature weekend:", office_room_2_sensor_weekend['temperature'].mean())

print("office_room_2 Min humidity weekend:", office_room_2_sensor_weekend['humidity'].min())
print("office_room_2 Max humidity weekend:", office_room_2_sensor_weekend['humidity'].max())
print("office_room_2 Mean humidity weekend:", office_room_2_sensor_weekend['humidity'].mean())

print("office_room_2 Min co2 weekend:", office_room_2_sensor_weekend['co2'].min())
print("office_room_2 Max co2 weekend:", office_room_2_sensor_weekend['co2'].max())
print("office_room_2 Mean weekend:", office_room_2_sensor_weekend['co2'].mean())




#Calculating min, mean and max in admin office sensor
admin_office_sensor = admin_office_sensor.set_index('Date')
admin_office_sensor['Weekday'] = admin_office_sensor.index.map(lambda t: t.date().weekday())
#Weekday
admin_office_sensor_weekday = admin_office_sensor[(admin_office_sensor.Weekday <6)]
admin_office_sensor_weekday_wh = admin_office_sensor_weekday.resample('BH').mean()
admin_office_sensor_weekday_wh

#Weekday statistics of admin office sensor
print("admin_office Min temperature:", admin_office_sensor_weekday_wh['temperature'].min())
print("admin_office Max temperature:", admin_office_sensor_weekday['temperature'].max())
print("admin_office Mean temperature:", admin_office_sensor_weekday_wh['temperature'].mean())

print("admin_office Min humidity:", admin_office_sensor_weekday_wh['humidity'].min())
print("admin_office Max humidity:", admin_office_sensor_weekday['humidity'].max())
print("admin_office Mean humidity:", admin_office_sensor_weekday_wh['humidity'].mean())

print("admin_office Min pm2.5:", admin_office_sensor_weekday_wh['pm'].min())
print("admin_office Max pm2.5:", admin_office_sensor_weekday['pm'].max())
print("admin_office Mean pm2.5:", admin_office_sensor_weekday_wh['pm'].mean())

print("admin_office Min tvoc:", admin_office_sensor_weekday_wh['tvoc'].min())
print("admin_office Max tvoc:", admin_office_sensor_weekday['tvoc'].max())
print("admin_office Mean tvoc:", admin_office_sensor_weekday_wh['tvoc'].mean())

#Weekend statistics of admin office sensor
admin_office_sensor_weekend = admin_office_sensor[(admin_office_sensor.Weekday >5)]
admin_office_sensor_weekend

print("admin_office Min temperature weekend:", admin_office_sensor_weekend['temperature'].min())
print("admin_office Max temperature weekend:", admin_office_sensor_weekend['temperature'].max())
print("admin_office Mean temperature weekend:", admin_office_sensor_weekend['temperature'].mean())

print("admin_office Min humidity weekend:", admin_office_sensor_weekend['humidity'].min())
print("admin_office Max humidity weekend:", admin_office_sensor_weekend['humidity'].max())
print("admin_office Mean humidity weekend:", admin_office_sensor_weekend['humidity'].mean())

print("admin_office Min pm2.5 weekend:", admin_office_sensor_weekend['pm'].min())
print("admin_office Max pm2.5 weekend:", admin_office_sensor_weekend['pm'].max())
print("admin_office Mean pm2.5 weekend:", admin_office_sensor_weekend['pm'].mean())

print("admin_office Min tvoc weekend:", admin_office_sensor_weekend['tvoc'].min())
print("admin_office Max tvoc weekend:", admin_office_sensor_weekend['tvoc'].max())
print("admin_office Mean tvoc weekend:", admin_office_sensor_weekend['tvoc'].mean())






#Calculating min, mean and max in GM room sensor
gm_office_sensor = gm_office_sensor.set_index('Date')
gm_office_sensor['Weekday'] = gm_office_sensor.index.map(lambda t: t.date().weekday())
#Weekday
gm_office_sensor_weekday = gm_office_sensor[(gm_office_sensor.Weekday <6)]
gm_office_sensor_weekday_wh = gm_office_sensor_weekday.resample('BH').mean()
gm_office_sensor_weekday_wh

#Weekday statistics of gm_room sensor
print("gm_room Min temperature:", gm_office_sensor_weekday_wh['temperature'].min())
print("gm_room Max temperature:", gm_office_sensor_weekday['temperature'].max())
print("gm_room Mean temperature:", gm_office_sensor_weekday_wh['temperature'].mean())

print("gm_room Min humidity:", gm_office_sensor_weekday_wh['humidity'].min())
print("gm_room Max humidity:", gm_office_sensor_weekday['humidity'].max())
print("gm_room Mean humidity:", gm_office_sensor_weekday_wh['humidity'].mean())

print("gm_room Min co2:", gm_office_sensor_weekday_wh['co2'].min())
print("gm_room Max co2:", gm_office_sensor_weekday['co2'].max())
print("gm_room Mean co2:", gm_office_sensor_weekday_wh['co2'].mean())

#Weekend statistics of GM office sensor
gm_office_sensor_weekend = gm_office_sensor[(gm_office_sensor.Weekday >5)]
gm_office_sensor_weekend

print("gm_room Min temperature weekend:", gm_office_sensor_weekend['temperature'].min())
print("gm_room Max temperature weekend:", gm_office_sensor_weekend['temperature'].max())
print("gm_room Mean temperature weekend:", gm_office_sensor_weekend['temperature'].mean())

print("gm_room Min humidity weekend:", gm_office_sensor_weekend['humidity'].min())
print("gm_room Max humidity weekend:", gm_office_sensor_weekend['humidity'].max())
print("gm_room Mean humidity weekend:", gm_office_sensor_weekend['humidity'].mean())

print("gm_room Min co2 weekend:", gm_office_sensor_weekend['co2'].min())
print("gm_room Max co2 weekend:", gm_office_sensor_weekend['co2'].max())
print("gm_room Mean weekend:", gm_office_sensor_weekend['co2'].mean())






#Calculating min, mean and max in meeting room sensor
meeting_room_sensor = meeting_room_sensor.set_index('Date')
meeting_room_sensor['Weekday'] = meeting_room_sensor.index.map(lambda t: t.date().weekday())
#Weekday
meeting_room_sensor_weekday = meeting_room_sensor[(meeting_room_sensor.Weekday <6)]
meeting_room_sensor_weekday_wh = meeting_room_sensor_weekday.resample('BH').mean()
meeting_room_sensor_weekday_wh

#Weekday statistics of meeting_room sensor
print("meeting_room Min temperature:", meeting_room_sensor_weekday_wh['temperature'].min())
print("meeting_room Max temperature:", meeting_room_sensor_weekday['temperature'].max())
print("meeting_room Mean temperature:", meeting_room_sensor_weekday_wh['temperature'].mean())

print("meeting_room Min humidity:", meeting_room_sensor_weekday_wh['humidity'].min())
print("meeting_room Max humidity:", meeting_room_sensor_weekday['humidity'].max())
print("meeting_room Mean humidity:", meeting_room_sensor_weekday_wh['humidity'].mean())

print("meeting_room Min co2:", meeting_room_sensor_weekday_wh['co2'].min())
print("meeting_room Max co2:", meeting_room_sensor_weekday['co2'].max())
print("meeting_room Mean co2:", meeting_room_sensor_weekday_wh['co2'].mean())

print("meeting_room Min pm2.5:", meeting_room_sensor_weekday_wh['pm'].min())
print("meeting_room Max pm2.5:", meeting_room_sensor_weekday['pm'].max())
print("meeting_room Mean pm2.5:", meeting_room_sensor_weekday_wh['pm'].mean())

print("meeting_room Min tvoc:", meeting_room_sensor_weekday_wh['tvoc'].min())
print("meeting_room Max tvoc:", meeting_room_sensor_weekday['tvoc'].max())
print("meeting_room Mean tvoc:", meeting_room_sensor_weekday_wh['tvoc'].mean())


#Weekend statistics of meeting_room sensor
meeting_room_sensor_weekend = meeting_room_sensor[(meeting_room_sensor.Weekday >5)]
meeting_room_sensor_weekend

print("meeting_room Min temperature weekend:", meeting_room_sensor_weekend['temperature'].min())
print("meeting_room Max temperature weekend:", meeting_room_sensor_weekend['temperature'].max())
print("meeting_room Mean temperature weekend:", meeting_room_sensor_weekend['temperature'].mean())

print("meeting_room Min humidity weekend:", meeting_room_sensor_weekend['humidity'].min())
print("meeting_room Max humidity weekend:", meeting_room_sensor_weekend['humidity'].max())
print("meeting_room Mean humidity weekend:", meeting_room_sensor_weekend['humidity'].mean())

print("meeting_room Min co2 weekend:", meeting_room_sensor_weekend['co2'].min())
print("meeting_room Max co2 weekend:", meeting_room_sensor_weekend['co2'].max())
print("meeting_room Mean weekend:", meeting_room_sensor_weekend['co2'].mean())

print("meeting_room Min pm2.5 weekend:", meeting_room_sensor_weekend['pm'].min())
print("meeting_room Max pm2.5 weekend:", meeting_room_sensor_weekend['pm'].max())
print("meeting_room Mean pm2.5 weekend:", meeting_room_sensor_weekend['pm'].mean())

print("meeting_room Min tvoc weekend:", meeting_room_sensor_weekend['tvoc'].min())
print("meeting_room Max tvoc weekend:", meeting_room_sensor_weekend['tvoc'].max())
print("meeting_room Mean tvoc weekend:", meeting_room_sensor_weekend['tvoc'].mean())
