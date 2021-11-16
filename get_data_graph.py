import datetime
import requests
from enum import Enum
import matplotlib.pyplot as plt
from dateutil.tz import tzutc, gettz

API_URL = "https://api.density.io/v2/spaces"
SPACE_ID = "spc_863128347956216317"
API_TOKEN = "shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e"

class Interval(Enum):
    MINUTE = "1m"
    HOUR = "1h"
    DAY = "1d"
    WEEK = "1w"

def get_historical_data(start, end, interval):
    """ Get historical data from density.io """

    start = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end.strftime("%Y-%m-%dT%H:%M:%SZ")

    url = "{}/{}/counts?start_time={}&end_time={}&interval={}&page=1&page_size=5000".format(API_URL, SPACE_ID, start, end, interval.value)

    response = requests.get(url, headers={"Authorization": "Bearer {}".format(API_TOKEN)})

    return response.json()


data = [[] for i in range(0, 7)]

start = datetime.datetime(2021, 10, 1)
end = datetime.datetime.now()

resp = get_historical_data(start, end, Interval.HOUR)

for row in resp["results"]:
    timestamp = datetime.datetime.strptime(row["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
    timestamp = timestamp.astimezone(gettz("America/Los_Angeles"))

    day = timestamp.weekday()
    hour = timestamp.hour
    percentage_full = row["interval"]["analytics"]["utilization"]

    if len(data[day]) < hour + 1:
        data[day].append(percentage_full)
    else:
        data[day][hour] = (data[day][hour] + percentage_full) / 2

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)

plt.imshow(data, interpolation='none', cmap="plasma", aspect="auto")
plt.savefig("map.png")
