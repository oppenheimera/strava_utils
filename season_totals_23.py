
import requests
import urllib3
from dateutil import parser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Strava API endpoints and parameters
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"
year_beginning = 1672560000 # epoch timestamp
year_end = 1704095999

# Data accumulation variables
bike_vert = 0
ebike_vert = 0
bike_miles = 0
foot_vert = 0
foot_miles = 0
my_dataset = [] # Dataset to accumulate all pages of responses

# Payload for authentication
payload = {
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'refresh_token': 'YOUR_REFRESH_TOKEN',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

print("Access Token = {}\n".format(access_token))
header = {'Authorization': 'Bearer ' + access_token}

# Helper function to get responses page by page
def get_by_page(n):
  param = {'per_page': 200, 'page': n, 'after': year_beginning}
  data = requests.get(activites_url, headers=header, params=param).json()
  return data

# Helper function to get all the activity pages
def get_all_pages() -> None:
  global my_dataset
  curr_page = 1
  data = ["placeholder starter value"] # placeholder used for 0 case
  while len(data) != 0:
    print("Retrieving data for page {}".format(curr_page))
    data = get_by_page(curr_page)
    my_dataset += data
    curr_page += 1
  return

def meters_to_feet(x):
    return x * 3.281

def meters_to_miles(x):
    return x / 1609

def iter_through_dataset(sport_type):
    vals = filter(lambda x: x["sport_type"] == sport_type, my_dataset)
    for i in vals:
        print(i["name"])

def get_activity_data_by_type(response, activity_type):
    count = 0
    distance = 0
    gain = 0
    for activity in response:
        if activity["sport_type"] == activity_type:
            count += 1
            distance += activity["distance"]
            gain += activity["total_elevation_gain"]
    return (count, meters_to_miles(distance), meters_to_feet(gain))

def get_bike_days(response):
    dateset = set()
    for activity in response:
        if activity["sport_type"] in ["MountainBikeRide", "EMountainBikeRide"]:
            date = parser.parse(activity["start_date"]).date()
            dateset.add(date)
    return len(dateset)

# Get data and add it to my_dataset
get_all_pages()

emtb_tup = get_activity_data_by_type(my_dataset, "EMountainBikeRide")
mtb_tup = get_activity_data_by_type(my_dataset, "MountainBikeRide")
run_tup = get_activity_data_by_type(my_dataset, "Run")
trail_tup = get_activity_data_by_type(my_dataset, "TrailRun")
hike_tup = get_activity_data_by_type(my_dataset, "Hike")

bike_vert += mtb_tup[2]
ebike_vert += emtb_tup[2]
bike_miles += mtb_tup[1]
foot_vert += sum([run_tup[2], trail_tup[2], hike_tup[2]])
foot_miles += sum([run_tup[1], trail_tup[1], hike_tup[1]])

print("MTB Rides", mtb_tup)
print("EMTB Rides", emtb_tup)
print("Runs", run_tup)
print("Trail Runs", trail_tup)
print("Hikes", hike_tup)

print()

print("Bike vert", bike_vert)
print("EBike vert", ebike_vert)
print("Bike miles", bike_miles)
print("Foot vert ", foot_vert)
print("Foot miles", foot_miles)

print()

print("Total bike days", get_bike_days(my_dataset))
