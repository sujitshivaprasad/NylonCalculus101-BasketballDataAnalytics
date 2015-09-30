#!/usr/bin/python
''' 
All credits go to NylonCalculus
The purpose of this program is to use the previously scraped data
	to create a variety of visualizations using matplotlib and seaborn 
	Python libraries
'''
import pandas as pd
import numpy as np

# we need this 'magic' function to plot within the ipython notebook
#%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns

#Extracting the data from the .csv file (from the previous post)
draft_df = pd.read_csv("draft_data_1966_to_2014.csv", index_col=0)
#print(draft_df.head())
#print(draft_df.info())
#print(draft_df.describe())
draft_df[draft_df['Draft_Yr'] == 1996]['WS_per_48'].mean()
# draft_df.Draft_Yr.unique() contains all the years in our DataFrame
WS48_yrly_avg = [draft_df[draft_df['Draft_Yr']==yr]['WS_per_48'].mean()
				for yr in draft_df.Draft_Yr.unique()]
#print(type(WS48_yrly_avg))
WS48_yrly_avg = draft_df.groupby('Draft_Yr').WS_per_48.mean()
#print(WS48_yrly_avg)

#Now we plot the data
#Plot WS/48 by year

#Use seaborn to set our graphing style
#style 'white' creates a white background for the graph
sns.set_style("whitegrid")

#Set the size - width = 12 inches, height = 9 inches
plt.figure(figsize=(12,9))
#Obtain the x and y values
x_values = draft_df.Draft_Yr.unique()
y_values = WS48_yrly_avg

#Add a title
title = ('Average Career Win Shares Per 48 minutes\nby Draft Year (1966-2014)')
plt.title(title, fontsize=20)

#Label the y-axis
#We don't need to label the year values
plt.ylabel('Win Shares Per 48 minutes', fontsize=18)

#Limit the range of axis labels to show only our data -> no unnecessary whitespace
plt.xlim(1966, 2014.5)
plt.ylim(0,0.08)

#Create a series of grey dashed lines across each labeled y-value
plt.grid(axis='y', color='grey', linestyle='--', lw=0.5, alpha=0.5)

#Change the size of tick labels for both axis to a more readable size
plt.tick_params(axis = 'both', labelsize = 14)

#Get rid of borders for our graph using seaborn's despine function
sns.despine(left = True, bottom = True)

#plot the line for our graph
plt.plot(x_values, y_values)

# Provide a reference to data source and credit yourself
# by adding text to the bottom of the graph.
# The first 2 arguments are the x and y axis coordinates of where
# we want to place the text.
# The coordinates given below should place the text below
# the xlabel and aligned left against the y-axis
plt.text(1966, -0.012,
         'Primary Data Source: http://www.basketball-reference.com/draft/'
         '\nAuthor: Sujit Shivaprasad',
          fontsize=12)

# Display our graph
#plt.show()
#The huge jump in year 1989 is when the draft format changed to a 2 round draft format
#Now, we will analyze the number of players drafted per year
#Then replace the y_value variable

players_drafted = draft_df.groupby('Draft_Yr').Pk.count()
sns.set_style("white")  
plt.figure(figsize=(12,9))

# set the x and y values
x_values = draft_df.Draft_Yr.unique()  
y_values = players_drafted

# set our title
title = ('The Number of players Drafted in each Draft (1966-2014)')
plt.title(title, fontsize=20)

# set y label
plt.ylabel('Number of Players Drafted', fontsize=18)

# set the value limits for x and y axis
plt.xlim(1966, 2014.5)
plt.ylim(0, 250)

# Create a series of grey dashed lines across the each
# labled y-value of the graph
plt.grid(axis='y',color='grey', linestyle='--', lw=0.5, alpha=0.5)


plt.tick_params(axis='both', labelsize=14) 
sns.despine(left=True, bottom=True) 
plt.plot(x_values, y_values)
plt.text(1966, -35,
         'Primary Data Source: http://www.basketball-reference.com/draft/'
         '\nAuthor: Sujit Shivaprasad',
          fontsize=12)
#plt.show()

#Now we can plot both on the same graph:

sns.set_style("white")  

# change the mapping of default matplotlib color shorthands (like 'b' 
# or 'r') to default seaborn palette 
sns.set_color_codes()

# the x values for the plot
x_values = draft_df.Draft_Yr.unique() 

# plt.subplots returns a tuple containing a Figure and an Axes
# fig is a Figure object and ax1 is an Axes object
# we can also set the size of our plot
fig, ax1 = plt.subplots(figsize=(12,9))  

title = ('The Number of Players Drafted and Average Career WS/48'
         '\nfor each Draft (1966-2014)')
plt.title(title, fontsize=20)

# Create a series of grey dashed lines across the each
# labeled y-value of the graph
plt.grid(axis='y',color='grey', linestyle='--', lw=0.5, alpha=0.5)

# Change the size of tick labels for x-axis and left y-axis
# to a more readable font size for
plt.tick_params(axis='both', labelsize=14)

# Plot our first line representing number of players drafted
# We assign it to plot1 to reference later for our legend
# We also give it a label, in order to use in the legend
plot1 = ax1.plot(x_values, players_drafted, 'b', label='No. of Players Drafted')
# Create the ylabel for our WS/48 line
ax1.set_ylabel('Number of Players Drafted', fontsize=18)
# Set limits for 1st y-axis
ax1.set_ylim(0, 240)
# Have tick color match corresponding line color
for tl in ax1.get_yticklabels():
    tl.set_color('b')

# Now we create the our 2nd Axes object that will share the same x-axis
# To do this we call the twinx() method from our first Axes object
ax2 = ax1.twinx()
# Create our second line for avg WS/48
plot2 = ax2.plot(x_values, WS48_yrly_avg, 'r', label='Avg WS/48')
# Create our label for the 2nd y-axis
ax2.set_ylabel('Win Shares Per 48 minutes', fontsize=18)
# Set the limit for 2nd y-axis
ax2.set_ylim(0, 0.08)
# Set tick size for second y-axis
ax2.tick_params(axis='y', labelsize=14)
# Have tick color match corresponding line color
for tl in ax2.get_yticklabels():
    tl.set_color('r')


# Limit our x-axis values to minimize white space
ax2.set_xlim(1966, 2014.15)

# create our legend 
# First add our lines together
lines = plot1 + plot2
# Then create legend by calling legend and getting the label for each line
ax1.legend(lines, [l.get_label() for l in lines])

# Create evenly aligned up tick marks for both y-axes.
# np.linspace allows us to get evenly spaced numbers over
# the specified interval given by first 2 arguments.
# Those 2 arguments are the the outer bounds of the y-axis values
# the third argument is the number of values we want to create.
# ax1 - create 9 tick values from 0 to 240
ax1.set_yticks(np.linspace(ax1.get_ybound()[0], ax1.get_ybound()[1], 9))
# ax2 - create 9 tick values from 0.00 to 0.08
ax2.set_yticks(np.linspace(ax2.get_ybound()[0], ax2.get_ybound()[1], 9))

# need to get rid of spines for each Axes object
for ax in [ax1, ax2]:
    ax.spines["top"].set_visible(False)  
    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)  
    
# Create text by calling the text() method from our figure object    
fig.text(0.1, 0.02,
         'Data source: http://www.basketball-reference.com/draft/'
        '\nAuthor: Sujit Shivaprasad',
          fontsize=10)

#plt.show()

#Create a DataFrame of only the top 60 picks, and acquire the data
#Note: Drafts from 1989-2004 have fewer than 60 picks

#Get the top 60 picks for each year
top60 = draft_df[(draft_df['Pk'] < 61)]
#Get the average WS/48 for each year
top60_yrly_WS48 = top60.groupby('Draft_Yr').WS_per_48.mean()
# Create a line graph for avg WS/48 for top 60 picks
sns.set_style("white")  

plt.figure(figsize=(12,9))
x_values = draft_df.Draft_Yr.unique() 
y_values = top60_yrly_WS48
title = ('Average Career Win Shares Per 48 minutes for'
         '\nTop 60 Picks by Draft Year (1966-2014)')
plt.title(title, fontsize=20)
plt.ylabel('Win Shares Per 48 minutes', fontsize=18)
plt.xlim(1966, 2014.5)
plt.ylim(0, 0.08)
plt.grid(axis='y',color='grey', linestyle='--', lw=0.5, alpha=0.5)
plt.tick_params(axis='both', labelsize=14)
sns.despine(left=True, bottom=True) 
plt.plot(x_values, y_values)
plt.text(1966, -0.012,
         'Primary Data Source: http://www.basketball-reference.com/draft/'
         '\nAuthor: Sujit Shivaprasad'
         '\nNote: Drafts from 1989 to 2004 have less than 60 draft picks',
          fontsize=12)
#plt.show()

#Now lets create some bar plots for the average WS/48 of each pick
#in the top 60

top60_mean_WS48 = top60.groupby('Pk').WS_per_48.mean()
sns.set_style("white")  

# Set the x and y values
x_values = top60.Pk.unique()
y_values = top60_mean_WS48

# Get our Figure and Axes objects
fig, ax = plt.subplots(figsize=(15,10))  
# Create a title
title = ('Average Win Shares per 48 Minutes for each' 
         '\nNBA Draft Pick in the Top 60 (1966-2014)')
# Set the title font size to 18
ax.set_title(title, fontsize=18)

# Set x and y axis labels
ax.set_xlabel('Draft Pick', fontsize=16)
ax.set_ylabel('Win Shares Per 48 minutes', fontsize=16)

# Set the tick label font size to 12
ax.tick_params(axis='both', labelsize=12)

# Set the x-axis limits
ax.set_xlim(0,61)

# Set the tick lables for picks 1 to 60
ax.set_xticks(np.arange(1,61)) 

# Create white y-axis grid lines to 
ax.yaxis.grid(color='white')

# overlay the white grid line on top of the bars
ax.set_axisbelow(False)

# Now add the bars to our plot
# this is equivalent to plt.bar(x_values, y_values)
ax.bar(x_values, y_values)

# Get rid chart borders
sns.despine(left=True, bottom=True)

plt.text(0, -.05, 
         'Primary Data Source: http://www.basketball-reference.com/draft/'
         '\nAuthor: Sujit Shivaprasad'
         '\nNote: Drafts from 1989 to 2004 have less than 60 draft picks',
          fontsize=12)
#plt.show()

#Or horizontally so the axes are better labeled:

sns.set_style("white")  

# Note we flipped the value variable names
y_values = top60.Pk.unique()
x_values = top60_mean_WS48

fig, ax = plt.subplots(figsize=(10,15))  
title = ('Average Win Shares per 48 Minutes for each' 
         '\nNBA Draft Pick in the Top 60 (1966-2014)')
# Add title with space below for x-axix ticks and label
ax.set_title(title, fontsize=18, y=1.06)
# We can rotate an axis label via the rotation argument.
# Here we set roation to 0 to so ylabel is read horizontally
ax.set_ylabel('Draft \nPick', fontsize=16, rotation=0)
ax.set_xlabel('Win Shares Per 48 minutes', fontsize=16)
ax.tick_params(axis='both', labelsize=12)

# Set a limit for our y-axis so that pick 1 is at the top
ax.set_ylim(61,0)
# Show all values for draft picks
ax.set_yticks(np.arange(1,61))
# pad the y-axis label so it doesn't overlap tick labels
ax.yaxis.labelpad = 25

# Move x-axis ticks and label to the top
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')

# create white x-axis grid lines to 
ax.xaxis.grid(color='white')

# overlay the white grid line on top of the bars
ax.set_axisbelow(False)

# Now add the horizontal bars to our plot, 
# and align them centerd with ticks
ax.barh(y_values, x_values, align='center')

# get rid of borders for our graph
# Not using sns.despine as I get an issue with displaying
# the x-axis at the top of the graph
ax.spines["top"].set_visible(False)  
ax.spines["bottom"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.spines["left"].set_visible(False)

plt.text(-0.02, 65, 
         'Primary Data Source: http://www.basketball-reference.com/draft/'
         '\nAuthor: Sujit Shivaprasad'
         '\nNote: Drafts from 1989 to 2004 have less than 60 draft picks',
          fontsize=12)

#plt.show()

#Or with plots/point plots:

sns.set_style("white")  

plt.figure(figsize=(10,15))

# Create Axes object with pointplot drawn onto it.
# This pointplot by default returns the mean along with a confidence
# intervals drawn, default returns 95% CI.
# The join parameter when set to True, draws a line connecting the points.
ax = sns.pointplot(x='WS_per_48', y='Pk', join=False, data=top60, 
                   orient='h')

title = ('Average Win Shares per 48 Minutes (with 95% CI)' 
         '\nfor each NBA Draft Pick in the Top 60 (1966-2014)')
# Add title with space below for x-axix ticks and label
ax.set_title(title, fontsize=18, y=1.06)

ax.set_ylabel('Draft \nPick', fontsize=16, rotation=0)
ax.set_xlabel('Win Shares Per 48 minutes', fontsize=16)
ax.tick_params(axis='both', labelsize=12)
# pad the y-axis label to not overlap tick labels
ax.yaxis.labelpad = 25
# limit x-axis
ax.set_xlim(-0.1, 0.15)
# Move x-axis ticks and label to the top
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')

# add horizontal lines for each draft pick
for y in range(len(y_values)):
    ax.hlines(y, -0.1, 0.15, color='grey', linestyle='-', lw=0.5)
    
# Add a vertical line at 0.00 WS/48
ax.vlines(0.00, -1, 60, color='grey', linestyle='-', lw=0.5)

# get rid of borders for our graph
# Not using sns.despine as I get an issue with displaying
# the x-axis at the top of the graph
ax.spines["top"].set_visible(False)  
ax.spines["bottom"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.spines["left"].set_visible(False)

plt.text(-0.1, 63, 
         'Primary Data Source: http://www.basketball-reference.com/draft/'
         '\nAuthor: Sujit Shivaprasad'
         '\nNote: Drafts from 1989 to 2004 have less than 60 draft picks',
          fontsize=12)

#plt.show()

#Or with boxplots:

top30 = top60[top60['Pk'] < 31]
sns.set_style("whitegrid")

plt.figure(figsize=(15,12))

# create our Axes that contains our boxplot
bplot = sns.boxplot(x='Pk', y='WS_per_48', data=top30, whis=[5,95], color='salmon')

title = ('Distribution of Win Shares per 48 Minutes for each' 
         '\nNBA Draft Pick in the Top 30 (1966-2014)')

# set title, axis labels, and change tick label size
bplot.set_title(title, fontsize=20)
bplot.set_xlabel('Draft Pick', fontsize=16)
bplot.set_ylabel('Win Shares Per 48 minutes', fontsize=16)
bplot.tick_params(axis='both', labelsize=12)

# get rid of chart borders
sns.despine(left=True) 

plt.text(-1, -.5, 
         'Data source: http://www.basketball-reference.com/draft/'
        '\nAuthor: Sujit Shivaprasad'
         '\nNote: Whiskers represent the 5th and 95th percentiles',
          fontsize=12)
#plt.show()

#Or violin plots:
sns.set(style="whitegrid")

plt.figure(figsize=(15,10))

# create an Axes object that contains our violin plot
vplot = sns.violinplot(x='Pk', y='WS_per_48', data=top10)

title = ('Distribution of Win Shares per 48 Minutes for each' 
         '\nNBA Draft Pick in the Top 10 (1966-2014)')

# set title, axis labels, and change tick label size
vplot.set_title(title, fontsize=20)
vplot.set_xlabel('Draft Pick', fontsize=16)
vplot.set_ylabel('Win Shares Per 48 minutes', fontsize=16)
vplot.tick_params(axis='both', labelsize=12)

plt.text(-1, -.55, 
         'Data source: http://www.basketball-reference.com/draft/'
        '\nAuthor: Sujit Shivaprasad',         
          fontsize=12)

sns.despine(left=True) 
           
plt.show()