
from flask import Flask, render_template, json
import requests
import mysql.connector

app = Flask(__name__)

# Connect to the MySQL database
mydb = mysql.connector.connect(
    # host="awseb-e-pt4frxidgt-stack-awsebrdsdatabase-vojt32kir8c7.cngube3qxh6b.eu-west-1.rds.amazonaws.com",
    host = "database-1.cngube3qxh6b.eu-west-1.rds.amazonaws.com",
    user="admin",
    password="Password",
    database="statistics_table"
)

# Create a cursor for executing database queries
cursor = mydb.cursor()

# Define a route to call the API, insert its data into the database, and return a response
@app.route('/call_api')
def call_api_and_insert():
    url = "https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%22TLIST(A1)%22,%22C02352V02829%22,%22C02677V03567%22%5D,%22dimension%22:%7B%22TLIST(A1)%22:%7B%22category%22:%7B%22index%22:%5B%222020%22%5D%7D%7D,%22C02352V02829%22:%7B%22category%22:%7B%22index%22:%5B%22103%22%5D%7D%7D,%22C02677V03567%22:%7B%22category%22:%7B%22index%22:%5B%22AT%22,%22BE%22,%22BG%22,%22HR%22,%22CY%22,%22CZ%22,%22DK%22,%22EE%22,%22E272020%22,%22FI%22,%22FR%22,%22DE%22,%22GR%22,%22HU%22,%22IS%22,%22IE%22,%22IT%22,%22LV%22,%22LI%22,%22LT%22,%22LU%22,%22MK%22,%22MT%22,%22ME%22%5D%7D%7D%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:false,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22JSON-stat%22,%22version%22:%222.0%22%7D,%22matrix%22:%22MIP08%22%7D,%22version%22:%222.0%22%7D%7D"
    response = requests.get(url)
    json_data = response.json()

    # Check if the request was successful
    if response.status_code == 200:
        try:
            

            # Extract relevant information
            year = json_data["result"]["dimension"]["TLIST(A1)"]["category"]["index"][0]
            country_data = json_data["result"]["dimension"]["C02677V03567"]["category"]["label"]
            statistic = json_data["result"]["extension"]["subject"]["value"]
            values = json_data["result"]["value"]
            teachers_data = json_data["result"]["dimension"]["C02352V02829"]["category"]["label"]

        

            # Insert data into the database
            for i in range(len(country_data)):
                country = list(country_data.values())[i]

                # Check if 'values' has enough elements before accessing an index
                if i < len(values):
                    value = values[i] if values[i] is not None else None
                else:
                    value = None

                

                # Define the SQL query to insert data
                query = "INSERT INTO statistics_table (Countries, Statistic, Teachers, Year, Unit, Value) VALUES (%s, %s, %s, %s, %s, %s)"
                insert_values = (country, statistic, "Primary", year, "Ratio ", value)  # Set Unit to None for now

                cursor.execute(query, insert_values)

            # Commit the changes to the database
            mydb.commit()

            
            return "Data inserted into the database successfully!", 200
        
        
        
        
        except KeyError as e:
            # Handle missing keys or other issues in the JSON structure
            error_message = {"error": "JSON data structure is not as expected"}
            return json.dumps(error_message), 500
    else:
        # If the request was not successful, return an error message
        error_message = {"error": "Failed to fetch data from the API"}
        return json.dumps(error_message), 500
    
    

# Created a route to retrieve data from the database
@app.route('/')
def fetch_data_from_database():
    # Define the SQL query to retrieve data
    query = "SELECT Statistic, Year, Teachers, Countries, Unit, Value FROM statistics_table"

    cursor.execute(query)

    # Fetch all rows from the database
    rows = cursor.fetchall()

    # Convert the rows to a list of dictionaries for HTML rendering
    data = []
    for row in rows:
        data.append({
            "Statistic": row[0],
            "Year": row[1],
            "Teachers": row[2],
            "Countries": row[3],
            "Unit": row[4],
            "Value": float(row[5]) if row[5] is not None else None
        })

    # Render the HTML template with the data
    return render_template('database.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
