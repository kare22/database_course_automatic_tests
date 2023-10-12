import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("DB_NAME"))
print(os.getenv("DB_USER"))
print(os.getenv("DB_PASSWORD"))
print(os.getenv("DB_HOST"))
print(os.getenv("DB_PORT"))

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        print("Connected to the database.")
        return conn
    except psycopg2.OperationalError as e:
        print("Unable to connect to the database.")
        print(e)
        return None


def create_new_table(conn):
    try:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE new_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INTEGER,
                address TEXT,
                salary REAL
            );
        ''')
        conn.commit()
        print("Table 'new_table' created successfully.")
    except psycopg2.Error as e:
        print("Error creating table 'new_table'.")
        print(e)


def execute_custom_query(conn, query):
    try:
        cur = conn.cursor()
        cur.execute(query)

        # Fetch and print the result if it's a SELECT query
        if query.strip().upper().startswith("SELECT"):
            rows = cur.fetchall()
            for row in rows:
                print(row)
        else:
            conn.commit()
            print("Query executed successfully.")
    except psycopg2.Error as e:
        print("Error executing query.")
        print(e)


def cli():
    conn = connect_to_db()
    if conn is None:
        print("No database connection. Exiting.")
        return

    create_new_table(conn)

    conn.close()


if __name__ == "__main__":
    cli()
