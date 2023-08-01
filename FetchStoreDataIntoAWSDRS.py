import json
import requests
import psycopg2

def lambda_handler(event, context):
    response = requests.get('http://api.open-notify.org/iss-now.json')
    response_data = response.json()
    latitude = response_data['iss_position']['latitude']
    longitude = response_data['iss_position']['longitude']
    timestamp = response_data['timestamp']
    message = response_data['message']

    connection = psycopg2.connect(
        host='vinoth-postgres-db.czurf89rwzej.us-east-1.rds.amazonaws.com',
        port=5432,
        user='',
        password='admin123',
        database='vinoth_db'
    )
    cursor = connection.cursor()
    try:
        cursor.execute("""CREATE TABLE space_station( latitude float, longitude float, longitude integer, message text)""")
        print("table creation is successful..")
    except:
        print("table already exists..")
    connection.commit()
    try:
        cursor.execute("""INSERT INTO space_station (latitude, longitude, timestamp, message) VALUES (%s, %s, %s, %s)""", (latitude, longitude, timestamp, message))
        print("data insertion is successful..")
    except:
        print("data insertion is unsuccessful..")
    cursor.close()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
