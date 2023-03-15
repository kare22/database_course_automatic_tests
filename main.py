import csv
import os

import psycopg2
from uuid import uuid4
from datetime import datetime
from dotenv import load_dotenv

from checks import Checker

# Load environment variables from .env file
load_dotenv()

def getNameFromPath(path):
    finalPath = ''
    try:
        finalPath = path.split('/')[len(path.split('/')) - 1]
    except:
        finalPath = path

    return finalPath.split('.')[0]

def checkIfDumpUsesCopy(fileName):
    with open(fileName, 'r') as f:
        for line in f:
            if line.startswith("COPY"):
                return True

    return False

def connect(dbName=os.getenv('DB_NAME'), autoCommit=False):
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=dbName,
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

    if(autoCommit):
        connection.autocommit = True

    return connection

def testStudent(testFileName):
    id = f"temp_{str(uuid4()).replace('-', '_')}"

    # Create substitute database for testing
    try:
        connection = connect(autoCommit=True)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE {id}")

        cursor.close()
        connection.close()
    except:
        True

    connection = connect(id)

    # Migrate created database with data (to be tested)
    with open(testFileName, 'r') as f:
        with connection.cursor() as cur:
            cur.execute(f.read().replace('public', os.getenv('DB_SCHEMA')).replace('OWNER TO postgres', f"OWNER TO {os.getenv('DB_USER')}"))
    connection.commit()



    with connection.cursor() as cur:
        checker = Checker(os.getenv('DB_SCHEMA'), cur)

        tests = [
            checker.checkColumn('turniirid', 'asukoht', points=2),
            checker.checkConstraint('partiid', 'vastavus', points=1),
            checker.checkConstraint('isikud', 'un_isikukood', 'UNIQUE', points=0.5),
            checker.checkConstraint('isikud', 'nimi_unique', 'UNIQUE', shouldNotExist=True, points=0.25),
            checker.checkColumn('klubid', 'asukoht', 'character_maximum_length', 100, points=0.5),
            checker.checkDefault('klubid', 'asukoht', None, points=1),
        ]

        with open('tulemused.csv', 'a', newline='', encoding='UTF8') as file:
            writer = csv.writer(file)

            writer.writerow([getNameFromPath(testFileName)])
            result = 0
            for i, test in enumerate(tests):
                #TODO add color to ÕIGE-VALE
                rowResult = (test[2] if test[0] else 0)
                writer.writerow(['', i+1, ('ÕIGE' if test[0] else 'VALE'), test[1], rowResult])
                result += rowResult

            writer.writerow(['', '', '', '', result])


    #TODO cur.execute(f"DROP DATABASE {id}")
    connection.close()

#TODO change w -> a
with open('tulemused.csv', 'w', newline='', encoding='UTF8') as file:
    writer = csv.writer(file)
    writer.writerow(['', '', '', '', ''])
    writer.writerow(['Praktikum3', datetime.today().strftime('%Y-%m-%d %H:%M:%S')])

# Get the current directory
directory = os.getcwd()

# Loop through all files in the current directory that end with ".sql"
for filename in os.listdir(f"{directory}/praks3"):
    if filename.endswith('.sql'):
        if checkIfDumpUsesCopy(f"{directory}/praks3/{filename}"):
            print('Siin on COPY, väga halb: ' + filename)
        else:
            testStudent(f"{directory}/praks3/{filename}")