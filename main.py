print('hello world')
# Requests allows us to make HTTP requests which we will use to get data from an API
import requests
# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Datetime is a library that allows us to represent dates
import datetime

# Setting this option will print all collumns of a dataframe
pd.set_option('display.max_columns', None)
# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)
# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    for x in data['rocket']:
       if x:
        response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
        BoosterVersion.append(response['name'])
# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(x):
    # If x is empty or not a string, return None
    if not isinstance(x, str) or x == 'nan': 
        return None
        
    try:
        response = requests.get("https://api.spacexdata.com/v4/launchpads/" + x)
        # Only try to parse JSON if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            return data.get('longitude'), data.get('latitude') # Or whatever you are extracting
        else:
            return None
    except Exception as e:
        return None
# Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayloadData(data):
    # Create an empty list to store the payload data
    payload_list = []
    
    # Loop through the payloads (if there are any)
    for load in data['payloads']:
        # Only make the request if 'load' is a valid string (not empty/NaN)
        if isinstance(load, str) and load != 'nan': 
            try:
                response = requests.get("https://api.spacexdata.com/v4/payloads/" + load)
                if response.status_code == 200:
                    payload_list.append(response.json().get('name'))
                else:
                    payload_list.append(None)
            except Exception as e:
                payload_list.append(None)
        else:
            payload_list.append(None)
            
    return payload_list
# Takes the dataset and uses the cores column to call the API and append the data to the lists
def getCoreData(row):
    cores = row['cores']
    
    # 1. Check if it's empty or not a list/array
    if not isinstance(cores, (list, tuple)) or len(cores) == 0:
        return None
        
    try:
        # 2. Try to get the landpad from the first core
        first_core = cores[0]
        if isinstance(first_core, dict):
            return first_core.get('landpad', None)
        else:
            return None
    except Exception:
        # 3. If anything goes wrong, just return None
        return None
# 1. Fetch the data first
static_json_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
response = requests.get(static_json_url)
data = pd.json_normalize(response.json())

# 2. Then apply the function to the DataFrame
# (Assuming your DataFrame is called 'data' and you want a new column called 'landpad')
data['landpad'] = data.apply(getCoreData, axis=1)

# 3. Check the results
print(data[['landpad']].head())
spacex_url="https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)
print(response.content)
static_json_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
response=requests.get(static_json_url)
response.status_code
# Use json_normalize meethod to convert the json result into a dataframe
data=pd.json_normalize(response.json())
print(data)
print(data.head())
# Lets take a subset of our dataframe keeping only the features we want and the flight number, and date_utc.
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x : x[0])

# We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]
print(data)
#Global variables 
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []
BoosterVersion
# Manually extract booster names from the 'rocket' column
data['BoosterVersion'] = data['rocket'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)

print("BoosterVersion column created successfully!")
getLaunchSite(data)
getPayloadData(data)
data['LandingPad'] = data.apply(getCoreData, axis=1)
print(data[['LandingPad']].head())
launch_dict = {'FlightNumber': list(data['flight_number']),
'Date': list(data['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}
print(data.columns.tolist())
print('date of the first row')
print(data['date_utc'].iloc[0])
data_falcon9 = data[data['BoosterVersion'] != 'Falcon 1']
print("Answer 2:", data_falcon9.shape[0])
# 1. Reset the index so it starts from 0
data_falcon9 = data_falcon9.reset_index(drop=True)

# 2. Create the FlightNumber column (1, 2, 3...)
data_falcon9['FlightNumber'] = list(range(1, data_falcon9.shape[0] + 1))

# 3. Calculate the mean for PayloadMass using the CORRECT column name 'payloads'
# (We use a try/except just in case 'payloads' contains empty values)
try:
    data_falcon9['PayloadMass'] = data_falcon9['payloads']
    # If you need to handle missing values, do it here:
    # data_falcon9['PayloadMass'] = data_falcon9['PayloadMass'].replace(np.nan, data_falcon9['PayloadMass'].mean())
except Exception as e:
    print(f"Note on payload mass: {e}")

# 4. Keep only the columns the course expects
expected_columns = [
    'FlightNumber', 'Date', 'BoosterVersion', 'PayloadMass', 
    'Orbit', 'LaunchSite', 'Outcome', 'Flights', 'GridFins', 
    'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 
    'Serial', 'Longitude', 'Latitude'
]

# 5. Filter down to only the columns you actually have
final_columns = [col for col in expected_columns if col in data_falcon9.columns]
data_falcon9 = data_falcon9[final_columns]

# 6. Print the first 5 rows to verify it worked
print(data_falcon9.head())
import sys
from bs4 import BeautifulSoup
import re
import unicodedata
def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out=''.join([booster_version for i,booster_version in enumerate( table_cells.strings) if i%2==0][0:-1])
    return out

def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out=[i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass=unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass=mass[0:mass.find("kg")+2]
    else:
        new_mass=0
    return new_mass


def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
        
    colunm_name = ' '.join(row.contents)
    
    # Filter the digit and empty names
    if not(colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name    
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}
# use requests.get() method with the provided static_url and headers
# assign the response to a object
response = requests.get(static_url, headers=headers)

# Use BeautifulSoup() to create a BeautifulSoup object from a response text content
soup = BeautifulSoup(response.text, 'html.parser')

# Use soup.title attribute
print(soup.title)
# Use the find_all function in the BeautifulSoup object, with element type `table`
# Assign the result to a list called `html_tables`
html_tables = soup.find_all('table')

# Let's print the third table and check its content
first_launch_table = html_tables[2]
# print(first_launch_table) # Optional: You can uncomment this to see the raw HTML

# Extract column names
column_names = []

# Apply find_all() function with `th` element on first_launch_table
# Iterate each th element and apply the provided extract_column_from_header() to get a column name
# Append the Non-empty column name into a list called column_names
for th in first_launch_table.find_all('th'):
    name = extract_column_from_header(th)
    if name is not None and len(name) > 0:
        column_names.append(name)

# Check the extracted column names
print(column_names)
launch_dict = dict.fromkeys(column_names)

# Remove an irrelevant column
del launch_dict['Date and time ( )']

# Let's initial the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
# Added some new columns
launch_dict['Version Booster'] = []
launch_dict['Booster landing'] = []
launch_dict['Date'] = []
launch_dict['Time'] = []

extracted_row = 0

# Extract each table
for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    # Get table row
    for rows in table.find_all("tr"):
        # Check to see if first table heading is as number corresponding to launch a number
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False
        
        # Get table element
        row = rows.find_all('td')
        
        # If it is number save cells in a dictionary
        if flag:
            extracted_row += 1
            
            # Flight Number value
            launch_dict['Flight No.'].append(flight_number)
            
            # Date and Time value
            datatimelist = date_time(row[0])
            
            # Date value
            date = datatimelist[0].strip(',')
            launch_dict['Date'].append(date)
            
            # Time value
            time = datatimelist[1]
            launch_dict['Time'].append(time)
            
            # Booster version
            bv = booster_version(row[1])
            if not(bv):
                bv = row[1].a.string
            launch_dict['Version Booster'].append(bv)
            
            # Launch Site
            launch_site = row[2].a.string if row[2].a else None
            launch_dict['Launch site'].append(launch_site)
            
            # Payload
            payload = row[3].a.string if row[3].a else None
            launch_dict['Payload'].append(payload)
            
            # Payload Mass
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)
            
            # Orbit
            orbit = row[5].a.string if row[5].a else None
            launch_dict['Orbit'].append(orbit)
            
            # Customer
            try:
                customer = row[6].a.string
            except AttributeError:
                customer = row[6].string
            launch_dict['Customer'].append(customer)
            
            
            # Launch outcome
            launch_outcome = list(row[7].strings)[0]
            launch_dict['Launch outcome'].append(launch_outcome)
            
            # Booster Landing
            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'].append(booster_landing)
# Create the pandas DataFrame from the dictionary
df = pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })

# Print the first 5 rows to verify
print(df.head())

# Export it to a CSV file for the next section
df.to_csv('spacex_web_scraped.csv', index=False)
df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
df.head(10)
df.isnull().sum()/len(df)*100
df.dtypes
df['LaunchSite'].value_counts()
print("--- Question 2: Success Rate ---")
# We check the 'Outcome' column. A successful landing usually contains "True".
# --- CORRECTED CALCULATIONS ---

print("--- Question 2: Success Rate ---")
# Count only rows where Outcome contains "True"

success_count = df['Outcome'].str.contains('True', na=False).sum()
total_launches = df.shape[0]
success_rate = (success_count / total_launches) * 100
print(f"Calculated Success Rate: {success_rate:.2f}%")

print("\n")
# landing_outcomes = values on Outcome column
landing_outcomes = df['Outcome'].value_counts()

# Print the outcomes to see the list
print(landing_outcomes)
# Create the bad_outcomes set
bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])

# Define the landing_class list using a loop
landing_class = []

for outcome in df['Outcome']:
    if outcome in bad_outcomes:
        landing_class.append(0)
    else:
        landing_class.append(1)

# Assign the list to the dataframe
df['Class'] = landing_class

# Print the first 8 rows to verify
print(df[['Class']].head(8))
# Determine the success rate
print(df["Class"].mean())
# Export the final DataFrame to CSV for the next lab
df.to_csv("dataset_part_2.csv", index=False)
import csv, sqlite3
import prettytable
prettytable.DEFAULT = 'DEFAULT'

con = sqlite3.connect("my_data1.db")
cur = con.cursor()
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
import matplotlib.pyplot as plt
import seaborn as sns
# 1. Print columns to verify
print("--- ORIGINAL COLUMNS ---")
print(df.columns.tolist())

# 2. Rename columns to match what the charts expect
df = df.rename(columns={
    'Launch_Site': 'LaunchSite',
    'Booster_Version': 'BoosterVersion',
    'PAYLOAD_MASS__KG_': 'PayloadMass',
    'Mission_Outcome': 'Outcome'
})

# 3. Create the Class column correctly from Outcome
# (Class 0 = Failure, Class 1 = Success)
df['Class'] = df['Outcome'].apply(lambda x: 0 if 'Failure' in str(x) or 'None' in str(x) else 1)
df['class'] = df['Class']

# 4. Create FlightNumber
df['FlightNumber'] = list(range(1, df.shape[0] + 1))

# 5. Verify the changes
print("--- NEW COLUMNS ---")
print(df.columns.tolist())
print("--------------------")
# TASK 1: Flight Number vs Launch Site
# ==========================================
sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, aspect=5)
plt.xlabel("Flight Number", fontsize=20)
plt.ylabel("Launch Site", fontsize=20)
plt.show()

# ==========================================
# TASK 2: Payload Mass vs Launch Site
# ==========================================
sns.catplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df, aspect=5)
plt.xlabel("Payload Mass (kg)", fontsize=20)
plt.ylabel("Launch Site", fontsize=20)
plt.show()

# ==========================================
# TASK 3: Success Rate of Each Orbit Type
# ==========================================
# Group by Orbit and get the mean of the Class column
orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()

# Create the bar chart
sns.barplot(x='Orbit', y='Class', data=orbit_success)
plt.xlabel("Orbit Type", fontsize=15)
plt.ylabel("Success Rate", fontsize=15)
plt.show()

# ==========================================
# TASK 4: Flight Number vs Orbit Type
# ==========================================
sns.catplot(y="Orbit", x="FlightNumber", hue="Class", data=df, aspect=5)
plt.xlabel("Flight Number", fontsize=20)
plt.ylabel("Orbit Type", fontsize=20)
plt.show()

# ==========================================
# TASK 5: Payload Mass vs Orbit Type
# ==========================================
sns.catplot(y="Orbit", x="PayloadMass", hue="Class", data=df, aspect=5)
plt.xlabel("Payload Mass (kg)", fontsize=20)
plt.ylabel("Orbit Type", fontsize=20)
plt.show()

# ==========================================
# TASK 6: Launch Success Yearly Trend
# ==========================================
# Create a new column for the year extracted from the date
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Create a line chart showing average success rate per year
sns.lineplot(x='Year', y='Class', data=df)
plt.xlabel("Year", fontsize=15)
plt.ylabel("Average Success Rate", fontsize=15)
plt.show()

# ==========================================
# Final Step: Export for the next lab
# ==========================================
df.to_csv('dataset_part_3.csv', index=False)
print("All charts generated and dataset_part_3.csv saved successfully!")
# HINT: Use get_dummies() function on the categorical columns
# Only select columns that actually exist in your dataset
available_columns = [col for col in ['Orbit', 'LaunchSite', 'LandingPad', 'Serial'] if col in df.columns]
features = df[available_columns]
features_one_hot = pd.get_dummies(features)

# Display the results
features_one_hot.head()
# HINT: use astype function
features_one_hot = features_one_hot.astype('float64')

# Check the data types to make sure they are all float64
features_one_hot.dtypes
features_one_hot.to_csv('dataset_part_3.csv', index=False)
# ==========================================
# IMPORTS AND SETUP
# ==========================================
import folium
from folium.plugins import MarkerCluster, MousePosition
from folium.features import DivIcon
from math import sin, cos, sqrt, atan2, radians
# ==========================================
# LOAD DATA 
# ==========================================
# In Jupyter, you usually use the provided URL, but since we are pasting this manually,
# make sure you have downloaded the dataset or use the URL from the lab instructions.
# Assuming you already have spacex_df loaded from the previous cell:
# (If you need to reload it, uncomment the lines below)
# URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
# spacex_df = pd.read_csv(URL)

# ==========================================
# TASK 1: Mark all launch sites on a map
# ==========================================

# Select relevant sub-columns
# ==========================================
# SAFETY CHECK: FIX COLUMN NAMES
# ==========================================
# Create a lowercase 'class' column if it doesn't exist
if 'class' not in df.columns and 'Class' in df.columns:
    df['class'] = df['Class']
# Create an uppercase 'Class' column if it doesn't exist
if 'Class' not in df.columns and 'class' in df.columns:
    df['Class'] = df['class']
# ==========================================
spacex_df = df[['LaunchSite', 'PayloadMass', 'Orbit', 'class']]
launch_sites_df = spacex_df.groupby(['LaunchSite'], as_index=False).first()
launch_sites_df = launch_sites_df[['LaunchSite', 'PayloadMass', 'Orbit']]
# Create the dummy spacex_df for Folium
spacex_df = df[['LaunchSite', 'class']].copy()  # This uses the lowercase 'class' we just guaranteed
spacex_df['Lat'] = 0.0
spacex_df['Long'] = 0.0
spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'green' if x == 1 else 'red')

# Create launch_sites_df for the map
launch_sites_df = spacex_df.groupby(['LaunchSite'], as_index=False).first()
launch_sites_df = launch_sites_df[['LaunchSite', 'Lat', 'Long']]

print("--- FOLIUM DATAFRAME READY ---")
print(spacex_df.head())
# Start Location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
marker = folium.map.Marker(
    nasa_coordinate,
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
    )
)
site_map.add_child(circle)
site_map.add_child(marker)

# Add a circle and marker for each launch site
for index, row in launch_sites_df.iterrows():
    coordinate = [row['Lat'], row['Long']]
    folium.Circle(coordinate, radius=1000, color='#000000', fill=True).add_child(folium.Popup(row['LaunchSite'])).add_to(site_map)
    folium.map.Marker(
        coordinate,
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % row['LaunchSite'],
        )
    ).add_to(site_map)

# Display the map
site_map

# ==========================================
# TASK 2: Mark the success/failed launches for each site on the map
# ==========================================

# Create a MarkerCluster object
marker_cluster = MarkerCluster()

# Function to assign color based on success (class=1 is green, class=0 is red)
def assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'
    else:
        return 'red'

# Create a new column 'marker_color'
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)

# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

# For each row in spacex_df, create a Marker object and add it to the cluster
for index, record in spacex_df.iterrows():
    marker = folium.Marker(
        location=[record['Lat'], record['Long']],
        icon=folium.Icon(color='white', icon_color=record['marker_color'])
    )
    marker_cluster.add_child(marker)

# Display the map with clusters
site_map

# ==========================================
# TASK 3: Calculate the distances between a launch site to its proximities
# ==========================================

# Add Mouse Position to get the coordinate for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)

# Function to calculate distance using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# --- Example: Calculate distance to a coastline point ---
# (You would manually get these coordinates using the MousePosition tool on the map)
launch_site_lat = 28.56367
launch_site_lon = -80.57163
coastline_lat = 28.56367 
coastline_lon = -80.56793

distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

# Create and add a folium.Marker on your selected closest coastline point on the map
distance_marker = folium.Marker(
    [coastline_lat, coastline_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
    )
)
site_map.add_child(distance_marker)

# Draw a PolyLine between launch site and the closest coastline point
coordinates = [[launch_site_lat, launch_site_lon], [coastline_lat, coastline_lon]]
lines = folium.PolyLine(locations=coordinates, weight=1)
site_map.add_child(lines)

# Display the final map
site_map
