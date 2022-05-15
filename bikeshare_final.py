import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
        #HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("What city would you like to explore?"
            "(Chicago, New York City, or Washington)").title())
        if city not in ['Chicago', 'New York City', 'Washington']:
            print("That is not a valid entry!")
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("What month(s) would you like to view?"
            "(All, January, February, March, April, May, June)").title())
        if month not in ['All', 'January', 'February',
            'March', 'April', 'May', 'June']:
            print("That is not a valid entry!")
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("What day would you like to view?"
            "(All, Monday, Tuesday, Wednesday, Thursday, Friday)").title())
        if day not in ['All', 'Monday', 'Tuesday',
            'Wednesday', 'Thursday', 'Friday']:
            print("That is not a valid entry!")
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # allows user to view more data
    view_data = str(input('\nWould you like to view 5 rows of individual '
    'trip data? Enter yes or no\n'))
    start_loc = 0
    while True:
        if view_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_data = str(input("Do you wish to continue?: ").lower())

        else:
            break

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day'] = df['Start Time'].dt.day
    popular_day = df['day'].mode()[0]
    print('Most Popular Day:', popular_day)
    # display the most common start hour

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', end_station)

    # display most frequent combination of start station and end station trip
    start_end = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most Popular Trip', start_end)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total Travel Time", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean Travel Duration", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Display counts of gender
    if city != 'Washington':
        gender = df['Gender'].value_counts()
        print('Gender Count: ', gender)


    # Display earliest, most recent, and most common year of birth
    earliest_birth = df['Birth Year'].min()
    print('Earliest Birth Year: ', earliest_birth)
    most_recent_birth = df['Birth Year'].max()
    print('Most Recent Birth Year: ', most_recent_birth)
    most_common_birth = df['Birth Year'].mode()[0]
    print('Most Common Birth Year: ', most_common_birth)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
    # allows user to restart or end program    
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
