# cassandra
## Data Modeling with Cassandra
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

They want to create an Apache Cassandra database that can create queries on song play data to answer the questions. The script is to create a database for this analysis. 

## Project Overview
In this project, we'll complete an ETL pipeline using Python. 
To complete the project, we will model the data by creating tables in Apache Cassandra to run queries.

## Queries
Query 1:  Give me the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4
Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
Query 3: Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
