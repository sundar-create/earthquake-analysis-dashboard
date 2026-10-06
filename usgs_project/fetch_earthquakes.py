#Create separate repositories for each of the projects and add the code to the respective repositories.
import requests

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

parameters = {
    "format": "geojson",
    "starttime": "2025-01-01",
    "endtime": "2025-02-01"
}

response = requests.get(url, params=parameters)

#print("Status:", response.status_code)

data = response.json()

#print(type(data))
#print(data.keys())

#step2
features = data["features"]

#print(type(features))
#print(len(features))

#step3
#print(features[0])

#step4
#earthquake = features[0]

#properties = earthquake["properties"]
#coordinates = earthquake["geometry"]["coordinates"]

#print("Magnitude:", properties["mag"])
#print("Place:", properties["place"])
#print("Time:", properties["time"])
#print("Magnitude Type:", properties["magType"])
#print("Longitude:", coordinates[0])
#print("Latitude:", coordinates[1])
#print("Depth:", coordinates[2])

#option1
records = []

for earthquake in features:
    properties = earthquake["properties"]
    coordinates = earthquake["geometry"]["coordinates"]

    record = {
        "mag": properties["mag"],
        "place": properties["place"],
        "time": properties["time"],
        "magType": properties["magType"],
        "longitude": coordinates[0],
        "latitude": coordinates[1],
        "depth": coordinates[2]
    }

    records.append(record)
#print(len(records))
#print(records[0]) 

#step into dataframe
import pandas as pd
df = pd.DataFrame(records)

#print(df.head()) 
#print(df.shape)
#print(df.columns) 
#print(df.info()) 

#Datetime in actual values from millisecs
df["time"] = pd.to_datetime(df["time"], unit="ms")
#print(df[["time", "place"]].head()) 

#Null values detection
#print(df.isnull().sum()) 

#print(f"Shape: {df.shape}")

#print(f"Columns: {df.columns}")

#print(f"Dtypes:\n{df.dtypes}")

#print(f"Null Values:\n{df.isnull().sum()}") 

#print(f"Descriptive Statistics for Magnitude:\n{df['mag'].describe()}\n\n")

#print(f"Value Counts for Magnitude Type:\n{df['magType'].value_counts()}") 

#step into mysql database 
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1234"
)

cursor = conn.cursor() 

cursor.execute("CREATE DATABASE IF NOT EXISTS earthquake") 

conn.commit() 

conn.close() 


conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="earthquake"
)

cursor = conn.cursor()

create_table = """
CREATE TABLE IF NOT EXISTS earthquakes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mag FLOAT,
    place VARCHAR(255),
    time DATETIME,
    magType VARCHAR(50),
    longitude FLOAT,
    latitude FLOAT,
    depth FLOAT
)
"""

cursor.execute(create_table)
conn.commit()  

cursor.execute("SHOW TABLES")
print(cursor.fetchall()) 

#NOW empty table in sql will get the required data from the dataframe
row = df.iloc[0]

sql = """
INSERT ignore INTO earthquakes
(mag, place, time, magType, longitude, latitude, depth)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

values = (
    row["mag"],
    row["place"],
    row["time"],
    row["magType"],
    row["longitude"],
    row["latitude"],
    row["depth"]
)

cursor.execute(sql, values)
conn.commit()  

cursor.execute("SELECT * FROM earthquakes")
result = cursor.fetchall()

#print(result) 

cursor.execute("TRUNCATE TABLE earthquakes")
conn.commit() 

cursor.execute("SELECT COUNT(*) FROM earthquakes")
print(cursor.fetchone()) 

#Important STEP: Insert all records from the DataFrame into the MySQL table 
rows = [
    (
        row.mag,
        row.place,
        row.time.to_pydatetime(),
        row.magType,
        row.longitude,
        row.latitude,
        row.depth
    )
    for row in df.itertuples(index=False)
]
#itertuples() method is used to iterate over the rows of a DataFrame as namedtuples.
print(df.itertuples(index=False))  
print(len(rows)) 

sql = """
INSERT INTO earthquakes
(mag, place, time, magType, longitude, latitude, depth)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(sql, rows)
conn.commit() 

cursor.execute("SELECT COUNT(*) FROM earthquakes")
#print(cursor.fetchone())  

#Query parts
cursor.execute("SELECT * FROM earthquakes LIMIT 5")

result = cursor.fetchall()
#view 
#for row in result:
 #   print(row) 

#sql reverse back to dataframe 
import pandas as pd

query = "SELECT * FROM earthquakes"

df_mysql = pd.read_sql(query, conn)

print(df_mysql.head()) 
print(df_mysql.shape) 

query = """
SELECT *
FROM earthquakes
ORDER BY mag DESC
LIMIT 10
"""

cursor.execute(query)

result = cursor.fetchall()

#for row in result:
 #   print(row) 

#One more query to get the average magnitude of earthquakes grouped by magnitude type 
query = """
SELECT magType, COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY magType
ORDER BY earthquake_count DESC
"""

cursor.execute(query)

result = cursor.fetchall()

#for row in result:
 #   print(row) 
cursor.execute("TRUNCATE TABLE earthquakes")
conn.commit()

cursor.execute("SELECT COUNT(*) FROM earthquakes")
print(cursor.fetchone())  
