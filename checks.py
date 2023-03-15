### STATIC METHODS ###
import os


def _responseWrapper(result, points, attributes):
    response = ""

    if 'tableName' in attributes:
        response += f"Tabel {attributes['tableName']} "
    if 'columnName' in attributes:
        response += f"Veerg {attributes['columnName']} "
    if 'constraintName' in attributes:
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

    if ('shouldExist' in attributes) and ('expectedValue' not in attributes or attributes['expectedValue'] is None):
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

    return result, response, points


def getCheckColumnQuery(tableName, columnName, attributeName='*', expectedValue=None, points=0):
    query = f"SELECT {attributeName} FROM information_schema.columns WHERE table_name = '{tableName}' AND column_name = '{columnName}'"

    return {
        'query': query,
        'tableName': tableName,
        'columnName': columnName,
        'attributeName': attributeName,
        'expectedValue': expectedValue,
        'points': points,
        'shouldExist': expectedValue is None,
        'funcName': 'checkColumn',
    }

    # return self._responseWrapper(check(), {
    #     'funcName': 'checkConstraint',
    #     'tableName': tableName,
    #     'columnName': columnName,
    #     'constraintName': constraintName,
    #     'constraintType': constraintType,
    #     'attributeName': attributeName,
    #     'expectedValue': expectedValue,
    # })


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


def getCheckConstraintQuery(tableName, constraintName, constraintType=None, shouldNotExist=False, points=0, schema='public'):
    query = f"SELECT * FROM information_schema.table_constraints WHERE table_name = '{tableName}' AND table_schema = '{schema}' AND constraint_name = '{constraintName}'"

    if constraintType != None:
        query += f" AND constraint_type = '{constraintType}'"

    return {
        'tableName': tableName,
        'constraintName': constraintName,
        'constraintType': constraintType,
        'shouldExist': not shouldNotExist,
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
                print(params['query'])
                self.cur.execute(params['query'])

                return len(self.cur.fetchall()) == (0 if params['shouldNotExist'] else 1)
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

                if params['expectedValue'] == None:
                    return len(self.cur.fetchall()) > 0, None

                response = self.cur.fetchall()[0][0]
                return (str(response)) == str(params['expectedValue']), response
            except:
                return False, 'VIGA'

        result, receivedValue = check()

        return _responseWrapper(result, params['points'], params)

    def runTestQuery(self, test):
        # Should be more dynamic, but python does not have a good solution for calling class methods dynamically
        if test['funcName'] == 'checkColumn':
            return self.checkColumn(test)
        elif test['funcName'] == 'checkDefault':
            return self.checkDefault(test)
        elif test['funcName'] == 'checkConstraint':
            return self.checkConstraint(test)
        else:
            raise Exception('No such test found!')
