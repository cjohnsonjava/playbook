import psycopg2.extras
from ...utils.configHelper import getConfig
import logging

logger = logging.getLogger('playbook')

class BaseDAO(object):
    """BaseDAO is a base class that encapsulates basic logic necessary to 
        connect and interact with DB"""
    
    def __init__(self, database=None, host=None, user=None, password=None):
        
        if database is None or host is None  or user is None  or password is None:
            logger.info("Invalid arguments. Using configurations" +
                         " from CONFIG file to connect to the database.")
            database = getConfig("database.name")
            host = getConfig("database.host")
            user = getConfig("database.user")
            password = getConfig("database.password")
            
        self.__conn = psycopg2.connect(database=database,
                            host=host, user=user,
                            password=password)
        
        self.__cur = None
        
    def __del__(self):
        if self.__cur is not None:
            self.__cur.close()
        self.getConnection().close()
        
    def execute(self, stmt, params):
        self.__cur = self.getConnection().cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.__cur.execute(stmt, params)
        return self.__cur
        
    def getConnection(self):
        return self.__conn
    
    def setConnection(self, connection):
        self.__conn = connection
        