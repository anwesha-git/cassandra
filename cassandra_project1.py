# Import Python packages 
import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv
# checking your current working directory
print(os.getcwd())

# Get your current folder and subfolder event data
filepath = os.getcwd() + '/event_data'

# Create a for loop to create a list of files and collect each filepath
for root, dirs, files in os.walk(filepath):
    
# join the file path and roots with the subdirectories using glob
    file_path_list = glob.glob(os.path.join(root,'*'))
    #print(file_path_list)

# initiating an empty list of rows that will be generated from each file
full_data_rows_list = [] 
    
# for every filepath in the file path list 
for f in file_path_list:

# reading csv file 
    with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
        # creating a csv reader object 
        csvreader = csv.reader(csvfile) 
        next(csvreader)
        
 # extracting each data row one by one and append it        
        for line in csvreader:
            #print(line)
            full_data_rows_list.append(line) 
            
# creating a smaller event data csv file called event_datafile_full csv that will be used to insert data into the \
# Apache Cassandra tables
csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
    writer = csv.writer(f, dialect='myDialect')
    writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',\
                'level','location','sessionId','song','userId'])
    for row in full_data_rows_list:
        if (row[0] == ''):
            continue
        writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))
# check the number of rows in your csv file
with open('event_datafile_new.csv', 'r', encoding = 'utf8') as f:
    print(sum(1 for line in f))

# This should make a connection to a Cassandra instance your local machine 
# (127.0.0.1)

from cassandra.cluster import Cluster
cluster = Cluster()

# To establish connection and begin executing queries, need a session
session = cluster.connect()

try:
    session.execute ("CREATE KEYSPACE IF NOT EXISTS udacity_p1 WITH REPLICATION = {'class': 'SimpleStrategy' , 'replication_factor':1}")
except Exception as e:
    print (e)
#Set KEYSPACE to the keyspace specified above
session.set_keyspace ('udacity_p1')

##Query 1:  Give me the artist, song title and song's length in the music app history that was heard during \
## sessionId = 338, and itemInSession = 4

query = "CREATE TABLE IF NOT EXISTS songs_per_session (sessionId text, itemInSession text, artist text, song_title text, length text, PRIMARY KEY (sessionId, itemInSession))"
try:
    session.execute(query)
except Exception as e:
    print (e)                    

file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
##Assign the INSERT statements into the `query` variable
        query = "INSERT INTO songs_per_session (sessionId,itemInSession, artist, song_title, length)"
        query = query + "VALUES (%s, %s, %s, %s, %s)"
        ##Assign which column element should be assigned for each column in the INSERT statement.
        ## For e.g., to INSERT artist_name and user first_name, you would change the code below to `line[0], line[1]`
        session.execute(query, (line[8], line[3], line[0], line[9],line[5]))
## SELECT statement to verify the data was entered into the table
query = "select artist,song_title,length from songs_per_session WHERE sessionId = '338' and itemInSession = '4'"
try:
    rows = session.execute(query)
except Exception as e:
    print(e)
for row in rows:
    print (row.artist, row.song_title, row.length)
	
## Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name)\
## for userid = 10, sessionid = 182

query = "CREATE TABLE IF NOT EXISTS songs_per_user_session (userid text, sessionId text, itemInSession text, artist text, song_title text, firstName text, lastName text, PRIMARY KEY ((userid, sessionId), itemInSession))"
try:
    session.execute(query)
except Exception as e:
    print (e)
file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
## Assign the INSERT statements into the `query` variable
        query = "INSERT INTO songs_per_user_session (userid,sessionId, itemInSession, artist, song_title, firstName, lastName)"
        query = query + "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        ##Assign which column element should be assigned for each column in the INSERT statement.
        ## For e.g., to INSERT artist_name and user first_name, you would change the code below to `line[0], line[1]`
        session.execute(query, (line[10], line[8], line[3], line[0], line[9],  line[1], line[4]))

query = "select artist,song_title,firstName,lastName from songs_per_user_session WHERE userid = '10' and sessionId = '182'"
try:
    rows = session.execute(query)
except Exception as e:
    print(e)
for row in rows:
    print (row.artist, row.song_title, row.firstname,row.lastname)
	
## Query 3: Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
query = "CREATE TABLE IF NOT EXISTS songs_userdetail (song_title text, firstName text, lastName text, PRIMARY KEY (song_title))"

try:
    session.execute(query)
except Exception as e:
    print (e) 

file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
## Assign the INSERT statements into the `query` variable
        query = "INSERT INTO songs_userdetail (song_title,firstname, lastname)"
        query = query + "VALUES (%s, %s, %s)"
        ## Assign which column element should be assigned for each column in the INSERT statement.
        ## For e.g., to INSERT artist_name and user first_name, you would change the code below to `line[0], line[1]`
        session.execute(query, (line[9], line[1], line[4]))

query = "select firstName,lastName from songs_userdetail WHERE song_title = 'All Hands Against His Own'"
try:
    rows = session.execute(query)
except Exception as e:
    print(e)
for row in rows:
    print (row.firstname,row.lastname)

##Drop the table before closing out the sessions
query = "drop table songs_per_session"
try:
    rows = session.execute(query)
except Exception as e:
    print(e)
query = "drop table songs_per_user_session"
try:
    rows = session.execute(query)
except Exception as e:
    print(e)
query = "drop table songs_userdetail"
try:
    rows = session.execute(query)
except Exception as e:
    print(e)

##Shutting down the session
session.shutdown()
cluster.shutdown()                   