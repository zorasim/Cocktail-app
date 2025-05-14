from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'logIn.env')
load_dotenv(dotenv_path=dotenv_path)



app = Flask(__name__)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD not found. Please check your .env file path and contents.")

print("DB_PASSWORD:", DB_PASSWORD)


# Connect to database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
) #Connecting to the database

ROWS_PER_PAGE = 15

@app.route('/')
@app.route('/page/<int:page>')
def show_table(page=1):
    offset = (page - 1) * ROWS_PER_PAGE

    cur = conn.cursor()
    # Get total row count for pagination
    cur.execute("SELECT COUNT(*) FROM temp")
    total_rows = cur.fetchone()[0]
    total_pages = (total_rows + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE

    # Fetch paginated data (kill me now)
    cur.execute("""
        SELECT temp_id, drink_name, drink_ingredient, ingredient_measurment, date_scraped
        FROM temp
        ORDER BY temp_id
        LIMIT %s OFFSET %s
    """, (ROWS_PER_PAGE, offset))
    rows = cur.fetchall()
    cur.close()

    return render_template('index.html', rows=rows, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
 #why am I doing this to myself