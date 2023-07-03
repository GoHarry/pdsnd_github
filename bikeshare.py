import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    month = ''
    day = ''
    ans = ''
    
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("Would you like to see data for chicago, new york city, or washington? :").lower() 

    while ans not in ['month', 'day', 'both', 'none']:
        ans = input("Would you like to filter data by month, day, both or not at all?. Type 'none' for no filter :").lower()

    # get user input for month (all, january, february, ... , june)
    if ans in ['month','both']:
        while month not in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
            month = input("Which month? January, February, March, April, May, June, All :").title()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if ans in ['day','both']:
        while day not in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']:
            day = input("Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, All :").title()
            
    if ans == 'none':
        month = 'All'
        day = 'All'
        
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

    df_temp=pd.read_csv(CITY_DATA[city])
    
    df_temp[['Start Time','End Time']] = df_temp[['Start Time','End Time']].apply(pd.to_datetime)
    
    if month == 'All' and day == 'All':
        df = df_temp
    elif month == 'All':
        df = df_temp[df_temp['Start Time'].dt.day_name()==day]
    elif day == 'All':
        df = df_temp[df_temp['Start Time'].dt.month_name()==month]
    else:
        df = df_temp[(df_temp['Start Time'].dt.month_name()==month) & (df_temp['Start Time'].dt.day_name()==day)]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most Common Month:', df['Start Time'].dt.month_name().mode()[0])

    # display the most common day of week
    print('Most Common Day of Week:', df['Start Time'].dt.day_name().mode()[0])

    # display the most common start hour
    print('Most Popular Start Hour:', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Commonly used Start Station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most Commonly used End Station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    ## extract values from the Start Station column and End Station column to create a new combination column
    df['Start and End Station'] = df['Start Station'] + ' and ' + df['End Station']
    print('Most frequent combination of start station and end station trip:', df['Start and End Station'].mode()[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ', df['Trip Duration'].sum())

    # display mean travel time
    print('Total average time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of User Types: ', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Count of Gender: ', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest, Most recent, Most Common Year of Birth are: ', df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_data(df):
    start_pos = 0
    end_pos = 5
    res = 'yes'
    while res.lower() == 'yes':
        if start_pos == 0:
            res = input("Do you want to see the first 5 rows of data? Yes or No?")
        else:
            res = input("Do you want to see the next 5 rows of data? Yes or No?")
        if res.lower() != 'yes':
            break
        print(df.iloc[start_pos:end_pos, :])
        start_pos += 5
        end_pos += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
