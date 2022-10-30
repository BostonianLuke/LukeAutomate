import pyodbc
import pandas as pd
import math
import os

class DatabaseConnect:
    
    def __init__(self, connectionDict):
        
        driver = "SQL Server" if os.name == 'nt' else r"ODBC Driver 17 for SQL Server"

        self.connectionString = f'DRIVER={driver};SERVER={connectionDict["server"]};DATABASE={connectionDict["database"]};UID={connectionDict["username"]};PWD={connectionDict["password"]};Trusted_Connection=no;'
        self.__maxInsertRows = 1000
        
    def processQuery(self, query, cursor):
        if ".sql" in query:
            with open(query) as file:
                query = file.read()
        
        if "SELECT" in query.strip().upper()[0:6]:
            columns = query.split("SELECT")[-1].split("FROM")[0].strip().split(",")
            if "*" in columns:
                table = query.split("FROM")[-1].split(";")[0].strip()
                findColumnsQuery = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';"
                columns = self.processQuery(findColumnsQuery, cursor).T.values[0]
                
            cursor.execute(query)
            resultSet = []
            row = cursor.fetchone()
                
            while row:
                resultSet.append([value for value in row])
                row = cursor.fetchone()                      # Does Row Exist? Lets check brovfe
            
            
            return pd.DataFrame(resultSet, columns = columns)
            
        else:
            cursor.execute(query)    
        
    def executeQuery(self, query):
        with pyodbc.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                return self.processQuery(query, cursor)
            
            
    """
    UPDATE table_name
    SET column1 = value1, column2 = value2, ...
    WHERE condition;
    """
    def updateData(self, df, table, primaryKey):
        primaryKeyValue = df[primaryKey].values.tolist()[0]
        df = df[[col for col in df.columns if col not in [primaryKey]]]
        setClause = ", ".join(
            [
                f"{col} = '{val}'" 
                for col, val 
                in zip(
                    df.columns, df.values.tolist()[0]
                )
            ]
        )
        
        query = f"UPDATE {table} SET {setClause} WHERE {primaryKey} = '{primaryKeyValue}'" 
        self.executeQuery(query)
        
    
    def insertData(self, df, table):
        columns = df.columns

        

        for insertOperarion in range(math.ceil(len(df) / self.__maxInsertRows)):
            values = df.loc[
                (
                    insertOperarion * self.__maxInsertRows
                ) : (
                    (self.__maxInsertRows - 1) + (insertOperarion * self.__maxInsertRows)
                )
            ].values

            rows = ','.join(
                [
                    f"({','.join([str(val) for val in row])})" 
                    for row 
                    in values
                    ])

            if rows:
                query = f'INSERT INTO {table} ({",".join([str(col) for col in columns])}) VALUES {rows};'
                self.executeQuery(query)