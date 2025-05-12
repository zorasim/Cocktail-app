import requests
import json
import psycopg2
from psycopg2 import sql
import datetime
import string
import os
from dotenv import load_dotenv

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
) #Connecting to the database

cur = conn.cursor()


current_date = datetime.datetime.now() #to get the date of the screaping session


for letter in string.ascii_lowercase: #to get the aplabetical order of the drinks
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() 

       # print(f"Fetching data for letter {letter}...")
        
   
        if data.get('drinks'):
                    for drink in data['drinks']:
                        drink_name = drink.get('strDrink') #Drink name
                        print(f"Processing drink: {drink_name}")

                        
                        for i in range(1, 16):
                            ingredient = drink.get(f'strIngredient{i}') #drink ingredients
                            measurement = drink.get(f'strMeasure{i}') #drink measurement

                            
                            if ingredient and measurement:
                                #print(f"I'M IN.")
                                #print(f"Processing ingredient: {ingredient} with measurement: {measurement}")
                                try:
                                    #print(f"I'm in the try block")
                                    # Insert data into the temp table
                                    cur.execute("""
                                        INSERT INTO temp ( drink_name, drink_ingredient, ingredient_measurment, date_scraped)
                                        VALUES ( %s, %s, %s, %s)
                                        
                                    """, (
                                            drink_name,
                                            ingredient,
                                            measurement,
                                            current_date
                                    ))
                                    conn.commit()

                                    print(f"SAVED data for letter {letter}...")

                                    
                                 
                                except Exception as e:
                                    conn.rollback()  
                                    print(f"Error inserting data for ingredient {ingredient}: {e}")
                                    continue  #skips if error
            

        else:
            print(f"No drinks found for letter {letter}")
    else:
        print(f"Error fetching data for letter {letter}: {response.status_code}")



cur.execute("SELECT * FROM temp LIMIT 5")
for row in cur.fetchall():
    print(row)


cur.close()
conn.close()
