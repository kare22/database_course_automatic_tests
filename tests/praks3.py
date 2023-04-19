from checks import *
import os

#TODO schem is deprecated
def tests():
    return [
        getCheckColumnQuery('turniirid', 'asukoht', points=2),
        getCheckConstraintQuery('partiid', 'vastavus', schema=os.getenv('DB_SCHEMA'), points=1),
        getCheckConstraintQuery('isikud', 'un_isikukood', 'UNIQUE', schema=os.getenv('DB_SCHEMA'), points=0.5),
        getCheckConstraintQuery('isikud', 'nimi_unique', 'UNIQUE', shouldNotExist=True, schema=os.getenv('DB_SCHEMA'), points=0.25),
        getCheckColumnQuery('klubid', 'asukoht', 'character_maximum_length', 100, points=0.5),
        getCheckDefaultQuery('klubid', 'asukoht', None, points=1),
    ]