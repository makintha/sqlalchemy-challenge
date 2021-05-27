# Advance Data Storage and Retrieval

## Background
In this exercise we are tasked to use SQLalchemy ORM with pandas/python to query data from precipitation and temperature data from Hawaii.
Additionally, we are task to design API to query temperature and precipitation data from the sqlite database
## Task 1
We are tasked to do climate analysis and exploration. In this exercise we are to use SQLalchemy ORM to reflect the tables into classes.
Following that we are to do precipitation and station analysis.

## Task 2
We are to design API using `Flask` based on the query that we just developed in previous Task 1.

There are few routes:
- `/`
- `/api/v1.0/precipitation`
- `/api/v1.0/stations`
- `/api/v1.0/tobs`
- `/api/v1.0/<start>`
- `/api/v1.0/<start>/<end>`

Each of the `routes` will return various output from list of data of precipitation and temperature

## Task 3
This task 3 contain further exploration of analysis of the database. Which contain the followings:
- Temperature Analysis I
- Temperature Analysis II
- Bonus Analysis
