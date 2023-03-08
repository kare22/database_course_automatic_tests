class Checker:

    def __init__(self, schema, cur):
        self.schema = schema
        self.cur = cur

    def _responseWrapper(self, result, attributes):
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
                    response += 'eeldasin et ei ole kuid on olemas'
            else:
                if result:
                    response += 'on olemas'
                else:
                    response += 'ei ole olemas'

        return result, response

    def checkConstraint(self, tableName, constraintName, constraintType=None, shouldNotExist=False):
        def check():
            try:
                query = f"SELECT * FROM information_schema.table_constraints WHERE table_name = '{tableName}' AND table_schema = '{self.schema}' AND constraint_name = '{constraintName}'"

                if constraintType != None:
                    query += f"AND constraint_type = '{constraintType}'"

                self.cur.execute(query)

                return len(self.cur.fetchall()) == 1
            except:
                return False

        return self._responseWrapper(check(), {
            'tableName': tableName,
            'constraintName': constraintName,
            'constraintType': constraintType,
            'shouldExist': not shouldNotExist
        })
    
    def checkDefault(self, tableName, columnName, expectedValue, shouldNotExist=False):
        def check():
            try:
                query = f"SELECT * FROM information_schema.columns WHERE table_name  = '{tableName}' AND column_name = '{columnName}'"

                if expectedValue == None:
                    query += "AND column_default IS NULL"
                else:
                    query += f"AND column_default LIKE '%{expectedValue}%'"

                self.cur.execute(query)

                return len(self.cur.fetchall()) == (0 if expectedValue == None else 1)
            except:
                return False

        return self._responseWrapper(check(), {
            'tableName': tableName,
            'expectedValue': expectedValue,
            'shouldExist': expectedValue != None,
            'columnName': columnName,
            'funcName': 'checkDefault',
        })
    
    def checkColumn(self, tableName, columnName, attributeName='*', expectedValue=None):
        def check():
            try:
                query = f"SELECT {attributeName} FROM information_schema.columns WHERE table_name = '{tableName}' AND column_name = '{columnName}'"

                self.cur.execute(query)

                if expectedValue == None:
                    return len(self.cur.fetchall()) > 0, None

                response = self.cur.fetchall()[0][0]
                return (str(response)) == str(expectedValue), response
            except:
                return False, 'VIGA'

        result, receivedValue = check()

        return self._responseWrapper(result, {
            'tableName': tableName,
            'columnName': columnName,
            'attributeName': attributeName,
            'expectedValue': expectedValue,
            'receivedValue': receivedValue,
            'shouldExist': expectedValue is None
        })



        # return self._responseWrapper(check(), {
        #     'funcName': 'checkConstraint',
        #     'tableName': tableName,
        #     'columnName': columnName,
        #     'constraintName': constraintName,
        #     'constraintType': constraintType,
        #     'attributeName': attributeName,
        #     'expectedValue': expectedValue,
        # })