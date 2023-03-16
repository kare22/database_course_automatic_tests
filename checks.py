### STATIC METHODS ###
import os


def _responseWrapper(result, points, attributes):
    response = ""

    if 'tableName' in attributes and attributes['tableName'] is not None:
        response += f"Tabel {attributes['tableName']} "
    if 'columnName' in attributes and attributes['columnName'] is not None:
        response += f"Veerg {attributes['columnName']} "
    if 'constraintName' in attributes and attributes['constraintName'] is not None:
        response += f"Kitsendus {attributes['constraintName']} "
    if 'constraintType' in attributes and attributes['constraintType'] is not None:
        response += f"Kitsendustüüp {attributes['constraintType']} "
    if 'funcName' in attributes and attributes['funcName'] == 'checkDefault':
        response += 'Vaikevaartus '

    if 'receivedValue' in attributes and attributes['receivedValue'] is not None:
        if result:
            response += f"Väärtus {attributes['receivedValue']} on olemas"
        else:
            response += f"Oodati väärtust {attributes['expectedValue']} kuid saadi {attributes['receivedValue']}"

    if 'shouldNotExist' in attributes:
        if result:
            response += 'on eemaldatud'
        else:
            response += 'eeldati et ei ole kuid on olemas'
    elif ('shouldExist' in attributes) and ('expectedValue' not in attributes or attributes['expectedValue'] is None):
        if attributes['shouldExist'] == False:
            if result:
                response += 'on eemaldatud'
            else:
                response += 'eeldati et ei ole kuid on olemas'
        else:
            if result:
                response += 'on olemas'
            else:
                response += 'ei ole olemas'

    elif 'funcName' in attributes and attributes['funcName'] == 'checkTable':
        if result:
            response += 'on olemas'
        else:
            response += 'ei ole olemas'
    elif 'funcName' in attributes and attributes['funcName'] == 'checkTableData':
        if result:
            response += 'andmed leitud'
        else:
            response += 'ei leidnud andmeid'

    return result, response, points

def getCheckTableQuery(tableName, points=0):
    query = f"SELECT DISTINCT table_name FROM information_schema.columns WHERE table_name = '{tableName}'"

    return {
        'query': query,
        'tableName': tableName,
        'points': points,
        'funcName': 'checkTable',
    }

def getCheckDataQuery(tableName, columnName=None, schema='public', points=0):
    preQuery=f"SELECT table_name FROM information_schema.tables WHERE table_name='{tableName}'"
    query = f"SELECT {'*' if columnName is None else columnName} FROM {schema}.{tableName}"

    if columnName is not None:
        query += f" WHERE {columnName} IS NOT NULL"

    return {
        'preQuery': preQuery,
        'query': query,
        'tableName': tableName,
        'columnName': columnName,
        'points': points,
        'funcName': 'checkTableData',
    }

def getCheckColumnQuery(tableName, columnName, attributeName='*', expectedValue=None, shouldNotExist=False, points=0):
    query = f"SELECT {attributeName} FROM information_schema.columns WHERE table_name = '{tableName}' AND column_name = '{columnName}'"

    return {
        'query': query,
        'tableName': tableName,
        'columnName': columnName,
        'attributeName': attributeName,
        'expectedValue': expectedValue,
        'points': points,
        'shouldExist': expectedValue is None, #TODO shouldn't it be not None?? :D
        'shouldNotExist': shouldNotExist, #TODO needs a better understanding
        'funcName': 'checkColumn',
    }

def getCheckDefaultQuery(tableName, columnName, expectedValue, points=0):
    query = f"SELECT * FROM information_schema.columns WHERE table_name  = '{tableName}' AND column_name = '{columnName}'"

    if expectedValue is None:
        query += "AND column_default IS NULL"
    else:
        query += f"AND column_default LIKE '%{expectedValue}%'"

    return {
        'query': query,
        'tableName': tableName,
        'expectedValue': expectedValue,
        'shouldExist': expectedValue != None,
        'columnName': columnName,
        'points': points,
        'funcName': 'checkDefault',
    }


def getCheckConstraintQuery(tableName, constraintName=None, constraintType=None, shouldNotExist=False, points=0, schema='public'):
    query = f"SELECT * FROM information_schema.table_constraints WHERE table_name = '{tableName}' AND table_schema = '{schema}'"

    if constraintName is not None:
        query += f" AND constraint_name = '{constraintName}'"
    if constraintType is not None:
        query += f" AND constraint_type = '{constraintType}'"

    return {
        'tableName': tableName,
        'constraintName': constraintName,
        'constraintType': constraintType,
        'shouldExist': not shouldNotExist, #TODO why the double negative??
        'query': query,
        'points': points,
        'funcName': 'checkConstraint',
    }


class Checker:

    def __init__(self, schema, cur):
        self.schema = schema
        self.cur = cur

    def checkConstraint(self, params):
        def check():
            try:
                self.cur.execute(params['query'])
                if params.get('shouldNotExist', False):
                    return len(self.cur.fetchall()) == 0
                else:
                    return len(self.cur.fetchall()) > 0
            except:
                return False

        return _responseWrapper(check(), params['points'], params)

    def checkDefault(self, params):
        def check():
            try:
                self.cur.execute(params['query'])

                return len(self.cur.fetchall()) == 1
            except:
                return False

        return _responseWrapper(check(), params['points'], params)

    def checkColumn(self, params):
        def check():
            try:
                self.cur.execute(params['query'])

                if params['shouldNotExist']:
                    return len(self.cur.fetchall()) == 0, None
                if params['expectedValue'] is None:
                    return len(self.cur.fetchall()) > 0, None

                response = self.cur.fetchall()[0][0]
                return (str(response)) == str(params['expectedValue']), response
            except:
                return False, 'VIGA'

        result, receivedValue = check()

        params['receivedValue'] = receivedValue

        return _responseWrapper(result, params['points'], params)

    def checkTable(self, params):
        def check():
            try:
                self.cur.execute(params['query'])

                return len(self.cur.fetchall()) == 1
            except:
                return False

        return _responseWrapper(check(), params['points'], params)

    def checkTableData(self, params):
        def check():
            if 'preQuery' in params:
                try:
                    self.cur.execute(params['preQuery'])
                    if len(self.cur.fetchall()) <= 0:
                        return False
                except:
                    return False
            try:
                self.cur.execute(params['query'])
                return len(self.cur.fetchall()) > 0
            except:
                return False

        return _responseWrapper(check(), params['points'], params)

    def runTestQuery(self, test):
        # Should be more dynamic, but python does not have a good solution for calling class methods dynamically
        if test['funcName'] == 'checkColumn':
            return self.checkColumn(test)
        elif test['funcName'] == 'checkDefault':
            return self.checkDefault(test)
        elif test['funcName'] == 'checkConstraint':
            return self.checkConstraint(test)
        elif test['funcName'] == 'checkTable':
            return self.checkTable(test)
        elif test['funcName'] == 'checkTableData':
            return self.checkTableData(test)
        else:
            raise Exception('No such test found!')
