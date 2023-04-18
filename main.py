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
        print(sys.exc_info())

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
                if test.get('type', '') == 'ignore':
                    continue
                elif test.get('type', '') == 'title':
                    writer.writerow(['', '', '', test['text'], '',])
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
    print('p3 --> Praks3')
    print('p4 --> Praks4/Kodu3')
    print('k4 --> Kodu4')
    print('k5 --> Kodu5')
    print('p7 --> Praks7')
    print('k6 --> Kodu6')

    answer = input('Millist praksi soovid jooksutada?: ')

    if answer == 'p3':
        subprocess.call(['sh', './convert.sh', 'praks3'])
        run('praks3', 'praks3', [
            getCheckColumnQuery('turniirid', 'asukoht', points=2),
            getCheckConstraintQuery('partiid', 'vastavus', schema=os.getenv('DB_SCHEMA'), points=1),
            getCheckConstraintQuery('isikud', 'un_isikukood', 'UNIQUE', schema=os.getenv('DB_SCHEMA'), points=0.5),
            getCheckConstraintQuery('isikud', 'nimi_unique', 'UNIQUE', shouldNotExist=True, schema=os.getenv('DB_SCHEMA'), points=0.25),
            getCheckColumnQuery('klubid', 'asukoht', 'character_maximum_length', 100, points=0.5),
            getCheckDefaultQuery('klubid', 'asukoht', None, points=1),
        ])
    elif answer == 'p4':
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
            getCheckDataQuery('v_keskminepartii', 'ROUND(keskmine_partii, 3)', where="turniiri_nimi = 'Plekkkarikas 2010'", expectedValue='23.765', points=1),
            getCheckDataQuery('v_keskminepartii', 'ROUND(keskmine_partii, 3)', where="turniiri_nimi = 'Kolme klubi kohtumine'", expectedValue='23.040', points=1),

            titleLayer('Materialseeritud vaade mv_vaate_kontroll'),
            #select * from pg_matviews where matviewname = 'mv_partiide_arv_valgetega'
            getCheckDataQuery('mv_partiide_arv_valgetega', 'COUNT(*)', expectedValue=85, points=1),
            getCheckDataQuery('mv_partiide_arv_valgetega', '*', where="eesnimi = 'Tarmo' AND perenimi = 'Kooser'", points=1),
            getCheckDataQuery('mv_partiide_arv_valgetega', 'MIN(partiisid_valgetega)', expectedValue=0, points=1),
            getCheckDataQuery('mv_partiide_arv_valgetega', 'MAX(partiisid_valgetega)', expectedValue=14, points=1),
        ])
    elif answer == 'k5':
        print('Pole implementeeritud')
        continue
    elif answer == 'k6':
        print('Pole implementeeritud')
        continue
    elif answer == 'p7':
        name = 'praks7'
        subprocess.call(['sh', './convert.sh', name])
        run(name, name, [
            titleLayer('Vaade v_partiid'),
            getCheckColumnQuery('v_partiid', 'asula', points=1),
            getCheckColumnQuery('v_partiid', 'turniir', points=1),
            getCheckColumnQuery('v_partiid', 'algus', points=1),
            getCheckColumnQuery('v_partiid', 'valge_nimi', points=1),
            getCheckColumnQuery('v_partiid', 'valge_klubi', points=1),
            getCheckColumnQuery('v_partiid', 'valge_punkt', points=1),
            getCheckColumnQuery('v_partiid', 'must_nimi', points=1),
            getCheckColumnQuery('v_partiid', 'must_klubi', points=1),
            getCheckColumnQuery('v_partiid', 'must_punkt', points=1),
            getCheckDataQuery('v_partiid', 'COUNT(*)', expectedValue=299, points=1),

            titleLayer('Vaade v_partiidpisi'),
            getCheckColumnQuery('v_partiidpisi', 'id', points=1),
            getCheckColumnQuery('v_partiidpisi', 'valge_mangija', points=1),
            getCheckColumnQuery('v_partiidpisi', 'valge_punkt', points=1),
            getCheckColumnQuery('v_partiidpisi', 'must_mangija', points=1),
            getCheckColumnQuery('v_partiidpisi', 'must_punkt', points=1),
            getCheckDataQuery('v_partiidpisi', 'COUNT(*)', expectedValue=299, points=1),
            getCheckDataQuery('v_partiidpisi', 'valge_mangija', where='id = 10', expectedValue='Anna Raha', points=1),
            getCheckDataQuery('v_partiidpisi', 'must_mangija', where='id = 10', expectedValue='Aljona Aljas', points=1),
            getCheckDataQuery('v_partiidpisi', 'must_punkt', where='id = 10', expectedValue=0, points=1),
            getCheckDataQuery('v_partiidpisi', 'COUNT(*)', expectedValue=1, points=1),
            getCheckColumnQuery('v_partiidpisi', 'must_punkt', 'data_type', 'numeric', points=1),
            getCheckDataQuery('v_partiidpisi', 'must_punkt', where='id = 12', expectedValue=0.5, points=1),

            titleLayer('Vaade v_punktid'),
            getCheckColumnQuery('v_punktid', 'partii', points=1),
            getCheckColumnQuery('v_punktid', 'turniir', points=1),
            getCheckColumnQuery('v_punktid', 'mangija', points=1),
            getCheckColumnQuery('v_punktid', 'varv', points=1),
            getCheckColumnQuery('v_punktid', 'punkt', points=1),
            getCheckDataQuery('v_punktid', 'COUNT(*)', expectedValue=598, points=1),
            getCheckColumnQuery('v_punktid', 'partii', where="data_type LIKE 'int%'", points=1),
            getCheckColumnQuery('v_punktid', 'punkt', 'data_type', 'numeric', points=1),
            getCheckColumnQuery('v_punktid', 'varv', where="data_type LIKE 'varchar%' OR data_type LIKE 'text%'", points=1),
            getCheckColumnQuery('v_punktid', 'mangija', where="data_type LIKE 'int%'", points=1),
            getCheckDataQuery('v_punktid', 'COUNT(*)', where='partii = 299 AND mangija = 76', expectedValue=1, points=1),
            getCheckDataQuery('v_punktid', 'UPPER(varv)', where='partii = 299 AND mangija = 76', expectedValue='V', points=1),
            getCheckDataQuery('v_punktid', 'COUNT(*)', where='partii = 299 AND mangija = 85', expectedValue=1, points=1),
            getCheckDataQuery('v_punktid', 'UPPER(varv)', where='partii = 299 AND mangija = 85', expectedValue='M', points=1),
            getCheckDataQuery('v_punktid', 'COUNT(*)', where='partii = 299 AND mangija = 76',  expectedValue=1, points=1),
            getCheckDataQuery('v_punktid', 'punkt', where='partii = 299 AND mangija = 76', dataType='float', expectedValue=0.5, points=1),
            getCheckDataQuery('v_punktid', 'COUNT(*)', where='partii = 11 AND mangija = 91', expectedValue=1, points=1),
            getCheckDataQuery('v_punktid', 'punkt', where='partii = 11 AND mangija = 91', dataType='float', expectedValue=0, points=1),
            getCheckDataQuery('v_punktid', 'COUNT(*)', where='partii = 1 AND mangija = 150', expectedValue=1, points=1),
            getCheckDataQuery('v_punktid', 'punkt', where='partii = 1 AND mangija = 150', dataType='float', expectedValue=1, points=1),

            titleLayer('Vaade v_edetabelid'),
            getCheckColumnQuery('v_edetabelid', 'id', points=1),
            getCheckColumnQuery('v_edetabelid', 'mangija', points=1),
            getCheckColumnQuery('v_edetabelid', 'synniaeg', points=1),
            getCheckColumnQuery('v_edetabelid', 'ranking', points=1),
            getCheckColumnQuery('v_edetabelid', 'klubi', points=1),
            getCheckColumnQuery('v_edetabelid', 'turniir', points=1),
            getCheckColumnQuery('v_edetabelid', 'punkte', points=1),
            getCheckDataQuery('v_edetabelid', 'COUNT(*)', expectedValue=184, points=1),

            titleLayer('Vaade mv_edetabelid'),
            getCheckDataQuery('pg_matviews', 'COUNT(*)', where="matviewname = 'mv_edetabelid'", schema='', expectedValue=1, points=1),
            getExecuteQuery('REFRESH MATERIALIZED VIEW mv_edetabelid'),
            getCheckDataQuery('mv_edetabelid', 'COUNT(*)', expectedValue=184, points=1),

            titleLayer('Vaade v_klubi54'),
            getCheckColumnQuery('v_klubi54', 'eesnimi', points=1),
            getCheckColumnQuery('v_klubi54', 'perenimi', points=1),
            getCheckColumnQuery('v_klubi54', 'synniaeg', points=1),
            getCheckColumnQuery('v_klubi54', 'ranking', points=1),
            getCheckColumnQuery('v_klubi54', 'klubi_id', points=1),
            getCheckDataQuery('v_klubi54', 'COUNT(*)', expectedValue=5, points=1),
            getCheckDataQuery('v_klubi54', 'klubi_id', where="eesnimi = 'Maria' AND perenimi = 'Lihtne'", expectedValue=54, points=1),

            titleLayer('Vaade v_maletaht'),
            getCheckColumnQuery('v_maletaht', 'id', points=1),
            getCheckColumnQuery('v_maletaht', 'eesnimi', points=1),
            getCheckColumnQuery('v_maletaht', 'perenimi', points=1),
            getCheckColumnQuery('v_maletaht', 'isikukood', points=1),
            getCheckColumnQuery('v_maletaht', 'klubis', points=1),
            getCheckColumnQuery('v_maletaht', 'synniaeg', points=1),
            getCheckColumnQuery('v_maletaht', 'sugu', points=1),
            getCheckColumnQuery('v_maletaht', 'ranking', points=1),
            getCheckDataQuery('v_maletaht', 'COUNT(*)', expectedValue=9, points=1),

        ])
    else:
        print('Ebalubatud sisend, palun proovi uuesti!')
        continue

    print('Töö tehtud!')
    break