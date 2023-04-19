import sys


### STATIC METHODS ###

def titleLayer(text):
    return {'type': 'title', 'text': text,}

def _convertValue(value, dataType=None):
    try:
        if dataType == 'float':
            return float(value)
        elif dataType == 'int':
            return int(value)
    except:
        return str(value)

    return str(value)

def _responseWrapper(result, points, attributes):
    response = ""

    def has(param):
        return param in attributes and attributes[param] is not None

    hasExpectedValue = has('expectedValue')
    hasColumnName = has('columnName')
    hasConstraintName = has('constraintName')
    hasTableName = has('tableName')
    hasConstraintType = has('constraintType')
    hasFuncName = has('functionName')
    hasReceivedValue = has('receivedValue')
    shouldNotExist = 'shouldNotExist' in attributes and attributes['shouldNotExist']

    if hasTableName:
        response += f"Tabel {attributes['tableName']} "
    if hasColumnName:
        response += f"Veerg {attributes['columnName']} "
    if 'where' in attributes and attributes['where'] is not None and attributes['where'] != '':
        response += f"WHERE {attributes['where']} "
    if hasConstraintName:
        response += f"Kitsendus {attributes['constraintName']} "
    if hasConstraintType:
        response += f"Kitsendustüüp {attributes['constraintType']} "
    if hasFuncName and attributes['funcName'] == 'checkDefault':
        response += 'Vaikevaartus '

    if hasReceivedValue and hasExpectedValue:
        if result:
            response += f"Väärtus {attributes['receivedValue']} on olemas "
        else:
            response += f"Oodati väärtust {attributes['expectedValue']} kuid saadi {attributes['receivedValue']}"

    if shouldNotExist:
        if result:
            response += 'on eemaldatud'
        else:
            response += 'eeldati et ei ole kuid on olemas '
    elif ('shouldExist' in attributes) and not hasExpectedValue:
        if attributes['shouldExist'] == False:
            if result:
                response += 'on eemaldatud'
            else:
                response += 'eeldati et ei ole kuid on olemas '
        else:
            if result:
                response += 'on olemas '
            else:
                response += 'ei ole olemas '

    elif 'funcName' in attributes and attributes['funcName'] == 'checkTable':
        if result:
            response += 'on olemas '
        else:
            response += 'ei ole olemas '
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


def getCheckDataQuery(tableName, columnName=None, expectedValue=None, where='', runPreQuery=False, schema='public', dataType='str', points=0):
    preQuery = None
    #TODO is this necessary
    if runPreQuery:
        preQuery = f"SELECT table_name FROM information_schema.tables WHERE table_name='{tableName}'"

    schemaString = f"{schema}." if schema != '' and schema != None else ''
    query = f"SELECT {'*' if columnName is None else columnName} FROM {schemaString}{tableName}"

    if where != '':
        query += f" WHERE {where}"

    #TODO WHY WAS THIS HERE?
    # if columnName is not None:
    #     query += f" WHERE {columnName} IS NOT NULL"

    return {
        'query': query,
        'where': where,
        'preQuery': preQuery,
        'tableName': tableName,
        'columnName': columnName,
        'expectedValue': expectedValue,
        'points': points,
        'funcName': 'checkTableData',
        'dataType': dataType,
    }


def getCheckColumnQuery(tableName, columnName, attributeName='*', expectedValue=None, shouldNotExist=False, where=None, points=0):
    query = f"SELECT {attributeName} FROM information_schema.columns WHERE table_name = '{tableName}' AND column_name = '{columnName}'"

    if where != '' and where != None:
        query += f" AND ({where})"

    return {
        'query': query,
        'where': where,
        'tableName': tableName,
        'columnName': columnName,
        'attributeName': attributeName,
        'expectedValue': expectedValue,
        'points': points,
        'shouldExist': expectedValue is None,  # TODO shouldn't it be not None?? :D
        'shouldNotExist': shouldNotExist,  # TODO needs a better understanding
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


def getCheckConstraintQuery(tableName, constraintName=None, constraintType=None, shouldNotExist=False, points=0,
                            schema='public'):
    query = f"SELECT * FROM information_schema.table_constraints WHERE table_name = '{tableName}' AND table_schema = '{schema}'"

    if constraintName is not None:
        query += f" AND constraint_name = '{constraintName}'"
    if constraintType is not None:
        query += f" AND constraint_type = '{constraintType}'"

    return {
        'tableName': tableName,
        'constraintName': constraintName,
        'constraintType': constraintType,
        'shouldExist': not shouldNotExist,  # TODO why the double negative??
        'query': query,
        'points': points,
        'funcName': 'checkConstraint',
    }

def getCheckViewExistsQuery(tableName, points=0):
    query = f"SELECT * FROM information_schema.views WHERE table_name = '{tableName}'"

    return {
        'tableName': tableName,
        'query': query,
        'points': points,
        'funcName': 'checkViewExists',
    }

def getExecuteQuery(query, hasFeedback=False, points=0):
    return {
        'type': 'ignore' if not hasFeedback else '',
        'query': query,
        'points': points,
        'funcName': 'executeQuery',
    }

def getCheckFunction(functionName, functionParams, expectedValue=None, where='', checkCount=None, dataType='str', points=0):
    query = f"SELECT * FROM {functionName}({functionParams})"

    if where != '':
        query += f" WHERE {where}"

    return {
        'query': query,
        'where': where,
        'points': points,
        'expectedValue': expectedValue,
        'dataType': dataType,
        'sqlFunctionName': functionName,
        'sqlFunctionParams': functionParams,
        'checkCount': checkCount,
        'funcName': 'checkFunction',
    }

def getCheckProcedure(procedureName, procedureParams, preQuery=None, resultQuery=None, numberOfCols=None, points=0):
    query = f"CALL {procedureName}({procedureParams})"

    return {
        'query': query,
        'points': points,
        'numberOfCols': numberOfCols,
        'procedureName': procedureName,
        'procedureParams': procedureParams,
        'preQuery': preQuery,
        'resultQuery': resultQuery,
        'funcName': 'checkProcedure',
    }


class Checker:

    def __init__(self, schema, cur):
        self.schema = schema
        self.cur = cur

        self.cur.execute(f"SET search_path TO public")

    def handleDBException(self, error):
        print(error)
        self.cur.execute("ROLLBACK")

    def checkConstraint(self, params):
        def check():
            try:
                self.cur.execute(params['query'])
                if params.get('shouldNotExist', False):
                    return len(self.cur.fetchall()) == 0
                else:
                    return len(self.cur.fetchall()) > 0
            except:
                self.handleDBException(sys.exc_info())
                return False, '', 0

        return _responseWrapper(check(), params['points'], params)

    def checkDefault(self, params):
        def check():
            try:
                self.cur.execute(params['query'])

                return len(self.cur.fetchall()) == 1
            except:
                self.handleDBException(sys.exc_info())
                return False, '', 0

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
                self.handleDBException(sys.exc_info())
                return False, '', 0

        result, receivedValue = check()

        params['receivedValue'] = receivedValue

        return _responseWrapper(result, params['points'], params)

    def checkTable(self, params):
        def check():
            try:
                self.cur.execute(params['query'])

                return len(self.cur.fetchall()) == 1
            except:
                self.handleDBException(sys.exc_info())
                return False, '', 0

        return _responseWrapper(check(), params['points'], params)

    def checkTableData(self, params):
        def check():
            if 'preQuery' in params and params['preQuery'] is not None:
                try:
                    self.cur.execute(params['preQuery'])
                    if len(self.cur.fetchall()) <= 0:
                        return False, None
                except:
                    self.handleDBException(sys.exc_info())
                    return False, '', 0
            try:
                self.cur.execute(params['query'])

                if params['expectedValue'] is None:
                    return len(self.cur.fetchall()) > 0, None

                response = self.cur.fetchall()[0][0]
                return (_convertValue(response, params['dataType'])) == _convertValue(params['expectedValue'], params['dataType']), response
            except:
                self.handleDBException(sys.exc_info())
                return False, '', 0

        result, receivedValue = check()

        params['receivedValue'] = receivedValue

        return _responseWrapper(result, params['points'], params)

    def checkViewExists(self, params):
        def check():
            try:
                self.cur.execute(params['query'])
                return len(self.cur.fetchall()) > 0, None
            except:
                self.handleDBException(sys.exc_info())
                return False, '', 0

        return _responseWrapper(check(), params['points'], params)

    def executeQuery(self, query):
        try:
            self.cur.execute(query)
        except:
            self.handleDBException(sys.exc_info())
            return False, '', 0

        return None, None, None

    def checkFunction(self, params):
        #TODO better response text

        # Check that function name exists
        try:
            self.cur.execute(f"SELECT * FROM pg_catalog.pg_proc WHERE proname='{params['sqlFunctionName']}'")

            if not len(self.cur.fetchall()) > 0:
                return False, f"Funktsiooni nimega {params['sqlFunctionName']} ei leitud", 0
        except:
            self.handleDBException(sys.exc_info())
            return False, None, None

        # Check that type is correct
        try:
            self.cur.execute(f"SELECT routine_name FROM information_schema.routines WHERE routine_type = 'FUNCTION' AND routine_name='{params['sqlFunctionName']}'")

            if not len(self.cur.fetchall()) > 0:
                return False, f"Funktsiooni nimega {params['sqlFunctionName']} ei ole tüüpi funktsioon", 0
        except:
            self.handleDBException(sys.exc_info())
            return False, None, None

        try:
            self.cur.execute(params['query'])

            if params['expectedValue'] is None:
                response = self.cur.fetchall()

                if params['checkCount'] is not None:
                    result = len(response) == params['checkCount']
                else:
                    result = len(response) > 0
            else:
                response = self.cur.fetchall()[0][0]
                result = _convertValue(response, params['dataType']) == _convertValue(params['expectedValue'], params['dataType'])

            # return _responseWrapper(result, params['points'], params)
            #TODO improve if-else
            feedback = f"Funktsiooni{' päringu tulemus' if params['expectedValue'] is None else ''} {params['sqlFunctionName']}({params['sqlFunctionParams']}){' WHERE ' + params['where'] + '' if params['where'] != '' else ''} "
            if params['checkCount'] is not None:
                feedback += f"oodati {params['checkCount']} olemit, saadi {len(response)}"
            elif params['expectedValue'] is None:
                feedback += 'on olemas' if result else 'ei ole olemas'
            else:
                feedback += f"tulemuseks {'saadi' if result else 'ei saadud'} {_convertValue(params['expectedValue'], params['dataType'])}"

                if not result:
                    feedback += f" tagastati {_convertValue(response, params['dataType'])}"

            return result, feedback, params['points'] if result else 0
        except:
            self.handleDBException(sys.exc_info())

            if params['where'] != '' and params['where'] is not None:
                return False, f"{params['sqlFunctionName']}({params['sqlFunctionParams']}){' WHERE ' + params['where'] + '' if params['where'] != '' else ''} ei saanud käivitada", 0

            return False, f"Viga funktsiooni {params['sqlFunctionName']} käivitamisel", 0

    def checkProcedure(self, params):
        try:
            if params['numberOfCols'] is not None:
                self.cur.execute(f"SELECT pronargs FROM pg_catalog.pg_proc WHERE proname = '{params['procedureName']}'")
                if not self.cur.fetchall()[0][0] == params['numberOfCols']:
                    return False, f"Protseduuri {params['procedureName']} parameetrite arv on vale või protseduuri ei letiud", 0
        except:
            self.handleDBException(sys.exc_info())

        try:
            if params['preQuery'] != '' and params['preQuery'] is not None:
                self.cur.execute(params['preQuery'])
        except:
            self.handleDBException(sys.exc_info())

        try:
            self.cur.execute(params['query'])
        except:
            self.handleDBException(sys.exc_info())
            return False, 'Viga protseduuri käivitamisel', 0

        try:
            self.cur.execute(params['resultQuery'])

            response = self.cur.fetchall()
            print(response)
            if not len(response) > 0:
                return True, 'ok', params['points']

            return False, 'Viga, protseduuri tulemus ei ole vastav', 0
        except:
            self.handleDBException(sys.exc_info())

        return False, 'Viga', 0

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
        elif test['funcName'] == 'checkViewExists':
            return self.checkViewExists(test)
        elif test['funcName'] == 'executeQuery':
            return self.executeQuery(test)
        elif test['funcName'] == 'checkFunction':
            return self.checkFunction(test)
        elif test['funcName'] == 'checkProcedure':
            return self.checkProcedure(test)
        else:
            raise Exception('No such test found!')
