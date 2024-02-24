import mysql.connector as mc

class DBConnection:

    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.name = 'perpustakaan'
        self.user = 'root'
        self.password = ''
        self.conn = None
        self.cursor = None
        self.result = None
        self.connected = False
        self.affected = 0
        self.connect()

    @property
    def connection_status(self):
        return self.connected

    def connect(self):
        try:
            self.conn = mc.connect(host=self.host, port=self.port, database=self.name, user=self.user, password=self.password)
            self.connected = True
            self.cursor = self.conn.cursor()
        except mc.Error as e:
            print(f"Error during connection: {e}")
            self.connected = False
        return self.conn

    def disconnect(self):
        if self.connected:
            self.conn.close()
            print("Disconnected from the database.")
        else:
            print("Not connected to the database.")
        self.connected = False
        self.conn = None

    def execute_query(self, sql, params=None):
        self.connect()
        try:
            self.cursor.execute(sql, params) if params else self.cursor.execute(sql)
            self.conn.commit()
            self.affected = self.cursor.rowcount
            return True
        except mc.Error as e:
            print(f"Error during query execution: {e}")
            return False
        finally:
            self.disconnect()

    def findone(self, sql, params=None):
        self.connect()
        try:
            self.cursor.execute(sql, params) if params else self.cursor.execute(sql)
            self.result = self.cursor.fetchone()
            return self.result
        except mc.Error as e:
            print(f"Error during findone query execution: {e}")
            return None
        finally:
            self.disconnect()

    def findAll(self, sql, params=None):
        self.connect()
        try:
            self.cursor.execute(sql, params) if params else self.cursor.execute(sql)
            self.result = self.cursor.fetchall()
            return self.result
        except mc.Error as e:
            print(f"Error during findAll query execution: {e}")
            return None
        finally:
            self.disconnect()

    def show(self, sql, params=None):
        self.connect()
        try:
            self.cursor.execute(sql, params) if params else self.cursor.execute(sql)
            self.result = self.cursor.fetchone()
            return self.result
        except mc.Error as e:
            print(f"Error during show query execution: {e}")
            return None
        finally:
            self.disconnect()

    def insert(self, sql, params=None):
        self.connect()
        try:
            self.cursor.execute(sql, params) if params else self.cursor.execute(sql)
            self.conn.commit()
            self.affected = self.cursor.rowcount
            return True
        except mc.Error as e:
            print(f"Error during insert operation: {e}")
            return False
        finally:
            self.disconnect()

    @property
    def info(self):
        if self.connected:
            return f"Server is running on {self.host} using port {self.port}"
        else:
            return "Server is offline."
