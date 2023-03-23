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
            index = 0
            for i, test in enumerate(tests):
                if test.get('type', '') == 'title':
                    writer.writerow(['', '', '', '', test['text']])
                    continue
                index += 1

                testResult = checker.runTestQuery(test)
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
    print('3 --> Praks3')
    print('4 --> Praks4/Kodu3')
    print('k4 --> Kodu4')
    print('5 --> Kodu5')
    print('6 --> Kodu6')

    answer = input('Millist praksi soovid jooksutada?: ')

    if answer == '3':
        subprocess.call(['sh', './convert.sh', 'praks3'])
        run('praks3', 'praks3', [
            getCheckColumnQuery('turniirid', 'asukoht', points=2),
            getCheckConstraintQuery('partiid', 'vastavus', schema=os.getenv('DB_SCHEMA'), points=1),
            getCheckConstraintQuery('isikud', 'un_isikukood', 'UNIQUE', schema=os.getenv('DB_SCHEMA'), points=0.5),
            getCheckConstraintQuery('isikud', 'nimi_unique', 'UNIQUE', shouldNotExist=True, schema=os.getenv('DB_SCHEMA'), points=0.25),
            getCheckColumnQuery('klubid', 'asukoht', 'character_maximum_length', 100, points=0.5),
            getCheckDefaultQuery('klubid', 'asukoht', None, points=1),
        ])
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
    elif answer == 'k4':
        name = 'kodu4'
        subprocess.call(['sh', './convert.sh', name])
        run(name, name, [
            titleLayer('Kodutöö 4'),

            titleLayer('Vaade v_turniiripartiid'),
            getCheckViewExistsQuery('v_turniiripartiid', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'turniir_nimi', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'toimumiskoht', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'partii_id', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'partii_algus', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'partii_lopp', points=1),
            getCheckColumnQuery('v_turniiripartiid', 'kes_voitis', points=1),
            getCheckDataQuery('v_turniiripartiid', 'COUNT(*)', expectedValue=299, points=1),
            getCheckDataQuery('v_turniiripartiid', 'LOWER(kes_voitis)', where='partii_id = 270', expectedValue='valge', points=1),
            getCheckDataQuery('v_turniiripartiid', 'LOWER(kes_voitis)', where='partii_id = 241', expectedValue='must', points=1),
            getCheckDataQuery('v_turniiripartiid', 'LOWER(kes_voitis)', where='partii_id = 193', expectedValue='viik', points=1),

            titleLayer('Vaade v_klubipartiikogused'),
            getCheckViewExistsQuery('v_klubipartiikogused', points=1),
            getCheckColumnQuery('v_klubipartiikogused', 'klubi_nimi', points=1),
            getCheckColumnQuery('v_klubipartiikogused', 'partiisid', points=1),
            getCheckDataQuery('v_klubipartiikogused', 'COUNT(*)', expectedValue=12, points=1),
            getCheckDataQuery('v_klubipartiikogused', 'SUM(partiisid)', expectedValue=571, points=1),

            titleLayer('Vaade v_keskminepartii'),
            getCheckViewExistsQuery('v_keskminepartii', points=1),
            getCheckColumnQuery('v_keskminepartii', 'turniiri_nimi', points=1),
            getCheckColumnQuery('v_keskminepartii', 'keskmine_partii', points=1),
            getCheckDataQuery('v_keskminepartii', 'COUNT(*)', expectedValue=5, points=1),
            getCheckDataQuery('v_keskminepartii', "EXTRACT ('epoch' FROM keskmine_partii)", where="turniiri_nimi = 'Plekkkarikas 2010'", expectedValue='1456.000000', points=1),
            getCheckDataQuery('v_keskminepartii', "EXTRACT ('epoch' FROM keskmine_partii)", where="turniiri_nimi = 'Kolme klubi kohtumine'", expectedValue='1416.040000', points=1),

            titleLayer('Materialseeritud vaade mv_vaate_kontroll'),
            #select * from pg_matviews where matviewname = 'mv_partiide_arv_valgetega'
            getCheckDataQuery('mv_partiide_arv_valgetega', 'COUNT(*)', expectedValue=85, points=1),
            getCheckDataQuery('mv_partiide_arv_valgetega', '*', where="eesnimi = 'Tarmo' AND perenimi = 'Kooser'", points=1),
            getCheckDataQuery('mv_partiide_arv_valgetega', 'MIN(partiisid_valgetega)', expectedValue=0, points=1),
            getCheckDataQuery('mv_partiide_arv_valgetega', 'MAX(partiisid_valgetega)', expectedValue=14, points=1),
        ])
    elif answer == '5':
        print('Pole implementeeritud')
        continue
    elif answer == '6':
        print('Pole implementeeritud')
        continue
    else:
        print('Ebalubatud sisend, palun proovi uuesti!')
        continue

    print('Töö tehtud!')
    break