import csv
import os
import subprocess

import psycopg2
from uuid import uuid4
from datetime import datetime
from dotenv import load_dotenv

#TODO imporve these imports
import tests.praks3
import tests.praks4
import tests.praks7
import tests.praks10
import tests.kodu4
import tests.kodu5
import tests.kodu6

from checks import *

# Load environment variables from .env file
load_dotenv()

#TODO move all imports to checks.py
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

            writer.writerow([getNameFromPath(testFileName), '', '', id])
            result = 0
            maxResult = 0
            index = 0
            for i, test in enumerate(tests):

                if test.get('type', '') == 'title':
                    writer.writerow(['', '', '', test['text'], '',])
                    continue
                index += 1

                testResult = checker.runTestQuery(test)

                if test.get('type', '') == 'ignore':
                    continue

                maxResult += test.get('points', 0)

                #TODO add color to ÕIGE-VALE
                rowResult = (testResult[2] if testResult[0] else 0)
                writer.writerow(['', index, ('ÕIGE' if testResult[0] else 'VALE'), testResult[1], rowResult])
                result += rowResult

            writer.writerow(['', '', '', '', f"{result}/{maxResult}"])


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
    print('p3 --> Praks3')
    print('p4 --> Praks4/Kodu3')
    print('k4 --> Kodu4')
    print('k5 --> Kodu5')
    print('p7 --> Praks7')
    print('p10 --> Praks10')
    print('k6 --> Kodu6')

    answer = input('Millist praksi soovid jooksutada?: ')

    if answer == 'p3':
        subprocess.call(['sh', './convert.sh', 'praks3'])
        run('praks3', 'praks3', tests.praks3.tests())
    elif answer == 'p4':
        subprocess.call(['sh', './convert.sh', 'praks4'])
        run('praks4', 'praks4', tests.praks4.tests())
    elif answer == 'k4':
        name = 'kodu4'
        subprocess.call(['sh', './convert.sh', name])
        run(name, name, tests.kodu4.tests())
    elif answer == 'k5':
        name = 'kodu5'
        subprocess.call(['sh', './convert.sh', name])
        run(name, name, tests.kodu5.tests())
    elif answer == 'k6':
        name = 'kodu6'
        # subprocess.call(['sh', './convert.sh', name])
        run(name, name, tests.kodu6.tests())
    elif answer == 'p7':
        name = 'praks7'
        subprocess.call(['sh', './convert.sh', name])
        run(name, name, tests.praks7.tests())
    elif answer == 'p10':
        name = 'praks10'
        subprocess.call(['sh', './convert.sh', name])
        run(name, name, tests.praks10.tests())
    else:
        print('Ebalubatud sisend, palun proovi uuesti!')
        continue

    print('Töö tehtud!')
    break