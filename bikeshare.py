import time
import pandas as pd
import numpy as np

#_______________________________________________________________________________________#

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['January', 'February', 'March', 'April', 'May', 'June'] # data is available only until june

dow = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#_______________________________________________________________________________________#
# Functions:

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze, already lower case and stripped of whitespaces to match the dict keys
        (str) month - name of the month to filter by, or "all" to apply no month filter, already w/ first chr upper case and stripped of whitespaces to match the dict keys
        (str) day - name of the day of week to filter by, or "all" to apply no day filter, already w/ first chr upper case and stripped of whitespaces to match the dict keys
    """
    print('''
==================================================================
                                   $"   *.      ****
              d$$$$$$$P"                  $    J
                  ^$.                     4r  "
                  d"b                    .db
                 P   $                  e" $
        ..ec.. ."     *.              zP   $.zec..
    .^        3*b.     *.           .P" .@"4F      "4
  ."         d"  ^b.    *c        .$"  d"   $         %
 /          P      $.    "c      d"   @     3r         3
4        .eE........$r===e$$$$eeP    J       *..        b
$       $$$$$       $   4$$$$$$$     F       d$$$.      4
$       $$$$$       $   4$$$$$$$     L       *$$$"      4
4         "      ""3P ===$$$$$$"     3                  P
 *                 $       """        b                J
  ".             .P                    %.             @
    %.         z*"                      ^%.        .r"
       "*==*""                             ^"*==*""
==================================================================
    ''')
    #source for ASCII art above: https://www.asciiart.eu/sports-and-outdoors/cycling
    print('Hello! Let\'s explore some US bikeshare data!')
    
    print('\nChoose one of the following cities:')
    print('\n • Chicago\n • New York City\n • Washington\n')
    
    # Checking whether a valid city was entered:
    while True:
        city = input('>').lower().strip() # adjusting to accomodate either upper / lower case and whitespaces
        if city in CITY_DATA:
            print('\nYou selected {}.'.format(city.title()))
            break
        print('That is not one of the cities available. Choose again or ctrl + c / ctr + z to exit\n')

    # Ensuring user types correctly
    while True:
        selection = input('\nDo you wish to filter by month? Yes / No:\n').lower().strip()
        if selection in ('yes', 'no'):
            break
            
        print('That is not an option. Choose again or ctrl + c / ctr + z to exit')
        
    if selection.lower()== 'yes':
        # Ensuring user types month correctly
        while True:
            month = input('\nWhich month (there is data available until June)?\n').title().strip()
            if month in months:                
                print('\nYou selected {}.'.format(month.title()))
                break
                
            print('That is not an option. Did you type it correctly (remember data is available only until June)? Choose again or ctrl + c / ctr + z to exit\n')
    
    else:
        month = 'all' # for 'no'
    
    # Ensuring user types correctly
    while True:
        selection = input('\nDo you wish to filter by day? Yes / No:\n').lower().strip()
        if selection in ('yes', 'no'):
            break
        
        print('That is not an option. Choose again or ctrl + c / ctr + z to exit')
        
    if selection.lower()== 'yes':
        # Ensuring user types day of the week correctly
        while True:
            day = input('\nWhich day?\n').title().strip()
            if day in dow:
                print('\nYou selected {}.'.format(day.title()))
                break
            
            print('That is not a day. Did you type it correctly? Choose again or ctrl + c / ctr + z to exit\n')
    
    else:
        day ='all' # for when the user opted not to filter by week day
        
    print('-'*100)
    # Below is a summary of all selected criteria for filtering
    print('\n\nYOUR QUERY CRITERIA: \n • city = {} \n • month(s) = {} \n • day(s) = {}\n\n'.format( city.title(), month.title(), day.title()))
    print('-'*100)
    
    return city, month, day # returns variables to be used by other functions


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Besides, an extra column with (start and end stations) concatenated is created, to aid further down the road.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city]) # loading csv file listed in the cities dictionary
    df['Start Time'] = pd.to_datetime(df['Start Time']) # converting colum to datetime
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour
    df['startend']= df['Start Station'] + ' - ' + df['End Station']
    
    # filtering the DataFrame according to previous specifications inputed by user:
    month = months.index(month) + 1 if month != 'all' else 'all' # to get numerical value for later
    if month != 'all': df = df[df['month'] == month] # if there is a filter, the df is subsetted
    
    day = dow.index(day) if day != 'all' else 'all' # as weekday function is also zero based monday == 0
    if day != 'all': df = df[df['day'] == day] # if there is a filter, the df is subsetted
        
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    
    # prints most common month, referring to months list to get the word instead of number
    
    if month == 'all':
        print('\n • Most common MONTH: {}'.format(months[df['month'].mode()[0]-1])) # [0] because mode always returns series | -1 because
        # list indexing starts at 0 and months at 1
    else:
        print(' • Only {} selected.'.format(month))
              
    # prints most common day, referring to dow list to get the word instead of number
    if day == 'all':
        print(' • Most common DAY: {}'.format(dow[df['day'].mode()[0]]))
    else:
        print(' • Only {} selected.'.format(day))
        
    # prints most common start hour
    
    print(' • Most common start HOUR: {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""
    
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # prints most popular start
    print('\n • Most common START STATION: {}'.format(df['Start Station'].mode()[0]))

    # prints most popular end
    print(' • Most common END STATION: {}'.format(df['End Station'].mode()[0]))

    # prints most start - end
    print(' • Most common START-END STATIONS : {}'.format(df['startend'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    
    print('\n Trip stats:')
    # displays sum of all trip duration column
    print(' • Total time traveled: {}'.format(df['Trip Duration'].sum()))

    # displays avg of trip duration column
    print(' • Average time traveled: {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating Clients Data...\n')
    start_time = time.time()

    # Display user type as a DF table
    print('\n User stats:')
    ut = df['User Type'].value_counts().to_frame()
    ut['| percentage (%)'] = round(ut['User Type']/ut['User Type'].sum()*100,2) # % value rounded to 2 decimals
    print('____________________________________________')
    print(ut)
    print('____________________________________________')
    
    # Display gender as a DF table (if available)
    
    print('\nGender stats:')
    try:
        gt = df['Gender'].value_counts().to_frame()
        gt['| percentage (%)'] = round(gt['Gender']/gt['Gender'].sum()*100,2) # % value rounded to 2 decimals
        print('____________________________________________')
        print(gt)
        print('____________________________________________')
    
    except:
        print('\nThere is no available gender data for this city.') 
    
    # Display year of Birth data (when available)
    print('\nYear of Birth data:')
    try:
        print(' • Earliest year:{}'.format(int(df['Birth Year'].min())))
        print(' • Most recent year:{}'.format(int(df['Birth Year'].max())))
        print(' • Most common year:{}'.format(int(df['Birth Year'].mode()[0])))

    except:
        print('\nThere is no available birth data for this city.') 
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)

def line_loader(df):
    """ This function takes in the loaded dataframe and asks whether the user wants
    to load 5 rows (starting from the top). It only stops displaying rows when the
    user chooses to.
    """
    i=0
    while True:
        choice = input('\nDo you wish to load 5 rows of the data filtered for selected criteria?\n').lower().strip()
        if choice != 'yes':
            break
        print(df.iloc[i:i+5,:]) # as DFs are zero based!
        i += 5
        
def main():
    """ This function takes all the above defined and inserts
    into a loop that only ends should the user decide to quit.
    Else, it runs queries on the data indefinitely.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        line_loader(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower().strip() != 'yes':
            print('\nExiting program...')
            break
#_______________________________________________________________________________________#
# User interface loop:
# will only run if current file is the main opened file
# will not work if imported as a module.
if __name__ == "__main__":
	main()
