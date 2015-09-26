#!/usr/bin/python

'''All credits go to NylonCalculus (http://nyloncalculus.com/2015/09/07/nylon-calculus-101-data-scraping-with-python/)
   I simply followed the above tutorial and created this program.
'''

from urllib2 import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.basketball-reference.com/draft/NBA_2014.html" #url we are scraping
html = urlopen(url) #html from the url above
soup = BeautifulSoup(html, "html.parser")
#print(type(soup))

#Getting the column headers from the table
column_headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
#print(column_headers) #Our column headers

#filling the DataFrame object with all of our data
data_rows = soup.findAll('tr')[2:] #skips the first 2 header rows
#print(type(data_rows))

#obtaining player data in a 2by2 matrix
player_data = [[td.getText() for td in data_rows[i].findAll('td')]
				for i in range(len(data_rows))]

#print(player_data)
#Storing data in pandas DataFrame
df = pd.DataFrame(player_data, columns = column_headers)
#print(df.head())

#Now, we clean up the data
#Getting rid of rows with empty values
df[df['Pk'].isnull()]

#Now we get rid of these empty rows by reassigning df to itself
df = df[df.Player.notnull()]
df[df['Pk'].isnull()]
#print(df[df['Pk'].isnull()])

#Python doesn't like identifiers beginning with % and / so we need to rename them
df.rename(columns = {'WS/48':'WS_per_48'}, inplace = True)

#Multiple columns start with %, so lets replace all of them
df.columns = df.columns.str.replace('%', '_Perc')

#Two columns begin with MP (minuted played) - career total and per game avg
#Get the columns we want by slicing the list of column names
#and replace them with the appended names
df.columns.values[14:18] = [df.columns.values[14:18][col]+
							"_per_G" for col in range(4)]
#print(df.columns)

#Changing data to the proper data types
#print(df.dtypes) #All the data is of type object
#We want them to be numeric values so we convert them

df = df.convert_objects(convert_numeric=True)
#print(df.dtypes)

#The next step is to deal with all of the NaN's 
#NaN in this case indicates the player has not played in the NBA
#We convert the NaN's to 0s:
df = df[:].fillna(0) #index all the columns and fill in the 0s

#Now we convert the Yrs, G, MP, PTS, TRB, and AST columns to integers
#Using astype()
df.loc[:,'Yrs':'AST'] = df.loc[:,'Yrs':'AST'].astype(int)
#print(df.head()) #All NaNs are replaced with 0s
#print(df.dtypes)

#Adding and deleting columns
#Adding a Draft year column
df.insert(0,'Draft_Yr', 2014)
df.drop('Rk', axis = 'columns', inplace = True)
#print(df.columns)

#Now, we want to scrape data from 1966 to 2014 - similar to above process

#Create a URL template to access each webpage
url_template = "http://www.basketball-reference.com/draft/NBA_{year}.html"
#Create an empty data frame
draft_df = pd.DataFrame()
#Create a for loop to scrape and append our data to DataFrame
for year in range(1966, 2015):  # for each year
    url = url_template.format(year=year)  # get the url
    
    html = urlopen(url)  # get the html
    soup = BeautifulSoup(html, 'html5lib') # create our BS object
    

    # get our player data
    data_rows = soup.findAll('tr')[2:] 
    player_data = [[td.getText() for td in data_rows[i].findAll('td')]
                for i in range(len(data_rows))]
    
    # Turn yearly data into a DatFrame
    year_df = pd.DataFrame(player_data, columns=column_headers)
    # create and insert the Draft_Yr column
    year_df.insert(0, 'Draft_Yr', year)
    
    # Append to the big dataframe
    draft_df = draft_df.append(year_df, ignore_index=True)

#print(draft_df.tail())
#print(draft_df.head())

# Cleaning the data

# Convert data to proper data types
draft_df = draft_df.convert_objects(convert_numeric=True)

# Get rid of the rows full of null values
draft_df = draft_df[draft_df.Player.notnull()]

# Replace NaNs with 0s
draft_df = draft_df.fillna(0)

# Rename Columns
draft_df.rename(columns={'WS/48':'WS_per_48'}, inplace=True)
# Change % symbol
draft_df.columns = draft_df.columns.str.replace('%', '_Perc')
# Add per_G to per game stats
draft_df.columns.values[15:19] = [draft_df.columns.values[15:19][col] + 
                                  "_per_G" for col in range(4)]

# Changing the Data Types to int
draft_df.loc[:,'Yrs':'AST'] = draft_df.loc[:,'Yrs':'AST'].astype(int)

# Delete the 'Rk' column
draft_df.drop('Rk', axis='columns', inplace=True)

#print(draft_df.dtypes)
draft_df['Pk'] = draft_df['Pk'].astype(int) # change Pk to int

draft_df.isnull().sum() # No missing values in our DataFrame

#Writing the data to a CSV file
draft_df.to_csv("draft_data_1966_to_2014.csv")

# sys allows us to get the info for the version of Python we use
#import sys
#import urllib.request
#import bs4

#print('Python version:', sys.version_info)
#print('Urllib.request version:', urllib.request.__version__)
#print('BeautifulSoup version:', bs4.__version__)
#print('Pandas version:', pd.__version__)