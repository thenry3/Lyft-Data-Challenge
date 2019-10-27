import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from datetime import datetime
from dateutil.parser import parse

d_ids = pd.read_csv("driver_ids.csv")
r_ids = pd.read_csv("ride_ids.csv")
r_ts = pd.read_csv("ride_timestamps.csv")

r_ids_c = r_ids.loc[r_ids.ride_id.isin(r_ts.ride_id)].copy()
r_ts_c = r_ts.loc[(r_ts.ride_id.isin(r_ids.ride_id)) &
                  (r_ts.event == "dropped_off_at")].copy()

r_ids_c['price'] = round((((2+1.15*r_ids_c.ride_distance*0.00062137119+0.22 *
                            r_ids_c.ride_duration/60)*(1+r_ids_c.ride_prime_time/100.0)) + 1.75), 2)
r_ids_c['price'].clip(5, 400)

rides = pd.merge(r_ids_c, r_ts_c, on='ride_id')
earnings = []
lifetime = []
number_of_rides = []
average_earnings = []

d_ids['driver_onboard_date'] = pd.to_datetime(d_ids['driver_onboard_date'])
rides['timestamp'] = pd.to_datetime(rides['timestamp'])
r_ts['timestamp'] = pd.to_datetime(r_ts['timestamp'])
for index, row in d_ids.iterrows():
    r_list = rides.loc[rides['driver_id'] == row[0]]
    ind_earning = r_list['price'].sum()
    numRides = len(r_list.index)
    number_of_rides.append(numRides)
    average = 0
    if numRides > 0:
        average = ind_earning / numRides
    average_earnings.append(round(average, 2))
    earnings.append(round(ind_earning, 2))
    if(not r_list.empty):
        lifetime.append((max(r_list.timestamp)-row[1]).days)
    else:
        lifetime.append(0)

d_ids['earnings'] = earnings
d_ids['days_on_lyft'] = lifetime
d_ids['number_of_completed_rides'] = number_of_rides
d_ids['average_earnings'] = average_earnings
# print(round(d_ids['average_earnings'].mean() * (d_ids['number_of_completed_rides'].mean() /
#                                                 d_ids['days_on_lyft'].mean()) * d_ids['days_on_lyft'].mean(), 2))

# print(d_ids['days_on_lyft'].mean(), d_ids['days_on_lyft'].std())
d_active = d_ids.loc[d_ids.days_on_lyft != 0].copy()

morning = 0
afternoon = 0
evening = 0
late_night = 0

morningtime = datetime(2000, 1, 1, 6, 0, 0)
noontime = datetime(2000, 1, 1, 12, 0, 0)
eveningtime = datetime(2000, 1, 1, 18, 0, 0)
count = 1

r_ts_c['timestamp'] = pd.to_datetime(r_ts_c['timestamp'])
for index, row in r_ids_c.iterrows():
    completed = r_ts_c.loc[r_ts_c['ride_id'] == row[1]]
    requested = datetime.time(min(completed.timestamp))
    if requested < morningtime.time():
        late_night += 1
    elif requested < noontime.time():
        morning += 1
    elif requested < eveningtime.time():
        afternoon += 1
    else:
        evening += 1

print("done")

raw_data = {"time_of_day": ['morning', 'afternoon', 'evening', 'late_night'],
            'completed_rides': [morning, afternoon, evening, late_night]}
df = pd.DataFrame(raw_data, columns=[
                  'Time of Day', 'Number of Completed Rides'])
df.plot(kind="pie", y="Number of Completed Rides",
        labels=df["Time of Day"], fontsize=14)
plt.show()
plt.clf()


# ax = plt.axes()

# ax.xaxis.set_minor_locator(ticker.MultipleLocator(250))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))

# sns.distplot(d_active['earnings'], bins=[250*i for i in range(0, 61)], norm_hist=False, hist=True, kde=False)
# plt.title("Distribution of Driver Earnings", fontsize=21)
# ax.set_xlabel("Earnings, in $", fontsize=17)
# ax.set_ylabel("# of drivers", fontsize=17)
# plt.tick_params(labelsize=14)
# plt.show()

# plt.clf()
# ax = plt.axes()
# ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))

# sns.distplot(d_active['days_on_lyft'], bins=[
#              5*i for i in range(0, 18)], norm_hist=False, hist=True, kde=False)
# plt.title("Distribution of Total Time of Drivers Using Lyft", fontsize=21)
# ax.set_xlabel("Time (days)", fontsize=17)
# ax.set_ylabel("# of drivers", fontsize=17)
# plt.tick_params(labelsize=14)
# plt.show()

# plt.clf()
# print(d_active)
# d_active.plot.scatter(x='days_on_lyft', y='earnings')
# plt.show()
# plt.clf()

# ax = plt.axes()
# ax = d_active.plot.scatter(x="number_of_completed_rides", y="earnings")
# plt.title("Total Earnings Compared to Completed Rides", fontsize=18)
# ax.set_xlabel("Number of Completed Rides", fontsize=17)
# ax.set_ylabel("Total Earnings", fontsize=17)
# plt.show()
# plt.clf()

# ax = plt.axes()
# sns.distplot(d_active['average_earnings'], norm_hist=False)
# plt.title("Distribution of Average Earnings per Ride of Drivers", fontsize=18)
# ax.set_xlabel("Earnings per Ride", fontsize=17)
# ax.set_ylabel("Proportion of Drivers", fontsize=17)
# plt.show()
# plt.clf()


# print(d_active['days_on_lyft'].mean())
# print(d_active['days_on_lyft'].std())
#plt.title("Scatterplot of Driver Earnings for Days Spent on Lyft")
# d_active.plot(x='ride_duration', y='earnings')
# plt.show()
# plt.clf()
# d_active.plot.scatter(x='ride_distance', y='earnings')
# plt.show()
# plt.clf()
# d_active.plot.scatter(x='ride_prime_time', y='earnings')
# plt.show()
# plt.clf()
