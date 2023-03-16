import csv
import os
import subprocess

import psycopg2
from uuid import uuid4
from datetime import datetime
from dotenv import load_dotenv

from checks import *

# Load environment variables from .env file
load_dotenv()

def titleLayer(text):
    return {'type': 'title', 'text': text,}

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

def testStudent(testFileName, name, tests):
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

        with open(f"tulemused_{name}.csv", 'a', newline='', encoding='UTF8') as file:
            writer = csv.writer(file)

            writer.writerow([getNameFromPath(testFileName)])
            result = 0
            maxResult = 0
            for i, test in enumerate(tests):
                if test.get('type', '') == 'title':
                    writer.writerow(['', '', '', '', test['text']])
                    continue

                testResult = checker.runTestQuery(test)
                maxResult += test.get('points', 0)

                #TODO add color to ÕIGE-VALE
                rowResult = (testResult[2] if testResult[0] else 0)
                writer.writerow(['', i+1, ('ÕIGE' if testResult[0] else 'VALE'), testResult[1], rowResult])
                result += rowResult

            writer.writerow(['', '', result, '/', maxResult])


    #TODO cur.execute(f"DROP DATABASE {id}")
    connection.close()



def run(name, path, tests):
    # TODO change w -> a
    with open(f"tulemused_{name}.csv", 'w', newline='', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(['', '', '', '', ''])
        writer.writerow([name, datetime.today().strftime('%Y-%m-%d %H:%M:%S')])

    # Get the current directory
    directory = os.getcwd()

    # Loop through all files in the current directory that end with ".sql"
    for filename in os.listdir(f"{directory}/{path}"):
        if filename.endswith('.sql'):
            if checkIfDumpUsesCopy(f"{directory}/{path}/{filename}"):
                print('Siin on COPY, väga halb: ' + filename)
            else:
                testStudent(f"{directory}/{path}/{filename}", name, tests)

while True: #TODO Schema loading inside check
    answer = input('Millist praksi soovid jooksutada?: ')

    if answer == '?':
        print('3 --> Praks3')
    elif answer == '3':
        subprocess.call(['sh', './convert.sh', 'praks3'])
        run('praks3', 'praks3', [
            getCheckColumnQuery('turniirid', 'asukoht', points=2),
            getCheckConstraintQuery('partiid', 'vastavus', schema=os.getenv('DB_SCHEMA'), points=1),
            getCheckConstraintQuery('isikud', 'un_isikukood', 'UNIQUE', schema=os.getenv('DB_SCHEMA'), points=0.5),
            getCheckConstraintQuery('isikud', 'nimi_unique', 'UNIQUE', shouldNotExist=True, schema=os.getenv('DB_SCHEMA'), points=0.25),
            getCheckColumnQuery('klubid', 'asukoht', 'character_maximum_length', 100, points=0.5),
            getCheckDefaultQuery('klubid', 'asukoht', None, points=1),
        ])

        print('Töö tehtud!')
        break
    elif answer == '4':
        subprocess.call(['sh', './convert.sh', 'praks4'])
        run('praks4', 'praks4', [
            titleLayer('Praktikum 4'),
            getCheckTableQuery('asulad'),
            getCheckDataQuery('asulad', schema=os.getenv('DB_SCHEMA')),
            getCheckTableQuery('riigid'),
            getCheckDataQuery('riigid', schema=os.getenv('DB_SCHEMA')),
            getCheckDataQuery('klubid', columnName='asula', schema=os.getenv('DB_SCHEMA')),
            getCheckColumnQuery('klubid', 'asula'),
            getCheckConstraintQuery('klubid', None, 'FOREIGN KEY', schema=os.getenv('DB_SCHEMA')),
            getCheckColumnQuery('klubid', 'asukoht', shouldNotExist=True),

            titleLayer('Kodutöö 3'),
            getCheckDataQuery('isikud', schema=os.getenv('DB_SCHEMA'), points=1),#TODO INIMESED
            getCheckConstraintQuery('isikud', None, 'PRIMARY KEY', schema=os.getenv('DB_SCHEMA'), points=1),
            getCheckConstraintQuery('isikud', None, 'UNIQUE', schema=os.getenv('DB_SCHEMA'), points=1),
            getCheckConstraintQuery('isikud', None, 'CHECK', schema=os.getenv('DB_SCHEMA'), points=1),
            getCheckColumnQuery('klubid', 'asula', points=1),
            getCheckDataQuery('turniirid', 'asula', schema=os.getenv('DB_SCHEMA'), points=1),
            getCheckConstraintQuery('turniirid', None, 'FOREIGN KEY', schema=os.getenv('DB_SCHEMA'), points=1),
            getCheckColumnQuery('klubid', 'asukoht', shouldNotExist=True, points=1),
            getCheckColumnQuery('klubid', 'toimumiskoht', shouldNotExist=True, points=1),

        ])

        print('Töö tehtud!')
        break
    else:
        print('Ebalubatud sisend, palun proovi uuesti!')

