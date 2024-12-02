import sqlite3

# Path to your .db file
db_file = '/home/rish/data/PROJECTS/innertune/data.db'

# Connect to the database
conn = sqlite3.connect(db_file)

# Create a cursor object
cursor = conn.cursor()

# SQL query to select all columns from the songs table
query = "SELECT * FROM song"

# Execute the query
cursor.execute(query)

# Fetch the column names from the cursor description
columns = [column[0] for column in cursor.description]

# Print the column names
# print("Attributes:", columns)

# Fetch all results from the executed query
rows = cursor.fetchall()


liked=[]
for row in rows:
    current_id=0
    for column, value in zip(columns, row):
        if column=="id":
            current_id=value
        
        if column=="likedAt":
            if value!=None:
                liked.append(current_id)
            break
        
for i in liked:
    print(i)



# Iterate over the rows and print each row along with its corresponding attribute names
# for row in rows:
#     for column, value in zip(columns, row):
#         print(f"{column}: {value}")
#     print()  # Print a newline between rows

# Close the cursor and the connection
cursor.close()
conn.close()