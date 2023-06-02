import pandas as pd
import numpy as np
import calendar
import time

# CSV Data Load
chicago = pd.read_csv('chicago.csv')
new_york_city = pd.read_csv('new_york_city.csv')
washington = pd.read_csv('washington.csv')

# Functions
def check_data_entry(prompt, valid_entries):
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()
        while user_input not in valid_entries :
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()
        print('Great! the chosen entry is: {}\n'.format(user_input))
        return user_input
    except:
        print('Seems like there is an issue with your input')

def get_filters():
    """
    Asks user to specify a city, month or day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
    """
    print('Hi there! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    valid_cities = ['chicago', 'new york', 'washington']
    prompt_cities = 'Please choose one of the 3 cities (chicago, new york, washington): '
    city = check_data_entry(prompt_cities, valid_cities)

    # get user input for period type (month, day or none).
    valid_period_type = ['month', 'day', 'none']
    prompt_period_type = 'Would you like to filter the data by month, day, or none? '
    period_type = check_data_entry(prompt_period_type, valid_period_type)

    if period_type == 'month':
        # get user input for month (all, january, february, ... , june)
        valid_months = ['january', 'february', 'march', 'april', 'may', 'june']
        prompt_month = 'Please choose a month (january, february, march, april, may or june): '
        period = check_data_entry(prompt_month, valid_months)

    elif period_type == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        prompt_day = 'Please choose a day (monday, tuesday, wednesday, thursday, friday, saturday or sunday): '
        period = check_data_entry(prompt_day, valid_days)
    elif period_type == 'none':
        period = "*"

    print('-' * 40)
    return city, period_type, period.title()

# User Input Data (City and Period) by functions
city, period_type, period = get_filters()

#Changing input city to correct city name
if city == 'chicago':
    city = chicago
elif city == 'new york':
    city = new_york_city
elif city == 'washington':
    city = washington

#Converting fields
city['Start Time'] = pd.to_datetime(city['Start Time'])
try:
    city['Birth Year'].fillna(0, inplace=True)
    city['Birth Year'] = city['Birth Year'].astype(int)
except:
    a = 'a'
city['hour'] = city['Start Time'].dt.hour

# Filters
if period_type == 'month':
    filter = (city['Start Time'].apply(lambda x: time.strftime('%B', time.strptime(str(x), '%Y-%m-%d %H:%M:%S')) == period))
elif period_type == 'day':
    filter = (city['Start Time'].apply(lambda x: time.strftime('%A', time.strptime(str(x), '%Y-%m-%d %H:%M:%S')) == period))
elif period_type == 'none':
    filter = (city['Start Time'] == city['Start Time'])
city_filter = city[filter]


# Calculations
#1
# Most common month
most_common_month = city_filter['Start Time'].dt.month.value_counts().idxmax()
most_common_month_name = calendar.month_name[most_common_month]
# Most common day of the week
most_common_day = city_filter['Start Time'].dt.dayofweek.value_counts().idxmax()
most_common_day_name = calendar.day_name[most_common_day]
# Most common hour
most_common_hour = city_filter['hour'].mode().values[0]

#2
#Most common start station
most_common_start_station = city_filter['Start Station'].value_counts().idxmax()
#Most common end station
most_common_end_station = city_filter['End Station'].value_counts().idxmax()
#Most common start/end station
combined_stations = city_filter['Start Station'] + ' - ' + city_filter['End Station']
most_common_stations = combined_stations.value_counts().idxmax()

#3
tot_time_travel = city_filter['Trip Duration'].sum()
avg_time_travel = city_filter['Trip Duration'].mean()

#4
user_type_counts = city_filter['User Type'].value_counts()
try:
    user_gender_counts = city_filter['Gender'].value_counts()
    most_recent_birth_year = city_filter['Birth Year'].max()
    oldest_birth_year = city_filter[city_filter['Birth Year'] != 0]['Birth Year'].min()
    most_common_birth_year = city_filter[city_filter['Birth Year'] != 0]['Birth Year'].value_counts().idxmax()
except:
    user_gender_counts = 'There is no data for Gender'
    most_recent_birth_year = 'There is no data for Birth Year'
    oldest_birth_year = 'There is no data for Birth Year'
    most_common_birth_year = 'There is no data for Birth Year'

# 1 Popular times of travel
print()
print('#1 Popular times of travel:')
print('Most common month:', most_common_month_name)
print('Most common day of week:', most_common_day_name)
print('Most common hour of day:', most_common_hour)

# 2 Popular stations and trip
print()
print('#2 Popular stations and trip:')
print('Most common start station:', most_common_start_station)
print('Most common end station:', most_common_end_station)
print('Most common trip from start to end:', most_common_stations)

# 3 Trip duration
print()
print('#3 Trip duration:')
print('Total travel time:', tot_time_travel)
print('Average travel time:', avg_time_travel)

# 4 User info
print()
print('#4 User Info:')
print('Counts of each user type:', user_type_counts)
print()
print('Counts of each gender:', user_gender_counts)
print()
print('Most recent birth year:', most_recent_birth_year)
print('Oldest birth year:', oldest_birth_year)
print('Most common birth year:', most_common_birth_year)
print()

# Raw data
show_raw_data = input('Would you like to see the raw data? (y/n) ').lower()

if show_raw_data == 'y':
    row_count = 0
    while row_count < len(city_filter):
        print(city_filter.iloc[row_count:row_count+5])
        row_count += 5
        show_more = input('Would you like to see 5 more rows of data? (y/n) ').lower()
        if show_more != 'y':
            break
    else:
        print('There is no more raw data to display')