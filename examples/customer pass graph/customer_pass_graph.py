from PyKIPass import *
from datetime import datetime, timedelta
import json
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
import os

kipass = KIPass(username=os.environ.get("KI_PASS_ID"), password=os.environ.get("KI_PASS_PASSWORD"))

def get_customer_count_on_days_list(past_days):
    customer_count_on_days_list = []

    for days in range(past_days):
        try:
            date = datetime.now() - timedelta(days=days)
            customer_count_on_day_list = kipass.get_customer_count_on_day(date=date.strftime("%Y%m%d"))
            customer_count_list = []

            for customer_count_on_day in customer_count_on_day_list:
                customer_count_list.append([f"{date.strftime('%Y-%m-%d')} {customer_count_on_day.time}:00",
                                            customer_count_on_day.total_customer_count])

            customer_count_on_days_list.append(customer_count_list)

        except ResponseIsNotSuccess:
            break

    customer_count_on_days_list.reverse()

    return customer_count_on_days_list


customer_data = get_customer_count_on_days_list(100)

with open("customer_data.json", 'w') as f:
    json.dump(customer_data, f, indent=4)

with open("customer_data.json", "r") as f:
    customer_data = json.load(f)

# Graph: Customer pass by weekday

data = {
    "customer_count": [],
    "weekday": []
}

for day in customer_data:
    total_customer = 0
    for time in day:
        total_customer += time[1]

    date = datetime.strptime(day[0][0], "%Y-%m-%d %H:00")
    data["weekday"].append(date.strftime("%A"))
    data["customer_count"].append(total_customer)

df = pd.DataFrame(data)

sns.set(rc={'figure.figsize': (15, 8)})
sns.boxplot(x="weekday", y="customer_count", data=df).set(title="Customer pass by weekday")

# Graph: Customer pass by weekend

data = {
    "customer_count": [],
    "time": []
}

for day in customer_data:

    date = datetime.strptime(day[0][0], "%Y-%m-%d %H:00")
    date = date.strftime("%A")

    if not (date == "Saturday" or date == "Sunday"):
        pass

    for time in day:
        date = datetime.strptime(time[0], "%Y-%m-%d %H:00")
        date = date.strftime("%H:00")

        data["time"].append(date)
        data["customer_count"].append(time[1])

df = pd.DataFrame(data)
df = df.sort_values(by=["time"])

sns.set(rc={'figure.figsize': (15, 8)})
sns.boxplot(x="time", y="customer_count", data=df).set(title="Customer count by time on weekend")