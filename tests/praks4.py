from checks import *
import os

#TODO schem is deprecated
def tests():
    return [
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
        getCheckDataQuery('isikud', schema=os.getenv('DB_SCHEMA'), points=1),  # TODO INIMESED
        getCheckConstraintQuery('isikud', None, 'PRIMARY KEY', schema=os.getenv('DB_SCHEMA'), points=1),
        getCheckConstraintQuery('isikud', None, 'UNIQUE', schema=os.getenv('DB_SCHEMA'), points=1),
        getCheckConstraintQuery('isikud', None, 'CHECK', schema=os.getenv('DB_SCHEMA'), points=1),
        getCheckColumnQuery('klubid', 'asula', points=1),
        getCheckDataQuery('turniirid', 'asula', schema=os.getenv('DB_SCHEMA'), points=1),
        getCheckConstraintQuery('turniirid', None, 'FOREIGN KEY', schema=os.getenv('DB_SCHEMA'), points=1),
        getCheckColumnQuery('klubid', 'asukoht', shouldNotExist=True, points=1),
        getCheckColumnQuery('klubid', 'toimumiskoht', shouldNotExist=True, points=1),
    ]